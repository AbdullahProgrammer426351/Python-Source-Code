#!/usr/bin/env python3
"""
SVG Format Converter — Converts SVG files to a canvas-compatible format.
"""

import base64
import io
import math
import os
import re
import subprocess
import sys
import argparse
import tempfile

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

# Script root = directory containing this script
_SCRIPT_ROOT = os.path.dirname(os.path.abspath(__file__))
_DEFAULT_OUTPUT = os.path.join(_SCRIPT_ROOT, 'output_folder')


def _get_attrs(tag_str):
    """Return dict of attributes parsed from an opening tag string."""
    inner = tag_str.strip()
    inner = re.sub(r'^</?(\w+:)?\w+', '', inner)
    inner = inner.rstrip('/>').strip()
    return dict(re.findall(r'''(\S+)\s*=\s*"([^"]*)"''', inner))


def _make_svg_tag(attrs):
    """Build the <svg ...> tag with attributes in a fixed order."""
    order = [
        'version', 'xmlns', 'xmlns:xlink', 'x', 'y', 'width', 'height',
        'viewBox', 'style', 'xml:space',
    ]
    parts = []
    seen = set()
    for k in order:
        if k in attrs:
            parts.append(f'{k}="{attrs[k]}"')
            seen.add(k)
    for k, v in attrs.items():
        if k not in seen:
            parts.append(f'{k}="{v}"')
    return '<svg ' + ' '.join(parts) + '>'


def _fmt_num(value):
    """Format numbers without noisy trailing decimals."""
    try:
        f = float(value)
    except (TypeError, ValueError):
        return str(value)
    if abs(f - round(f)) < 0.0005:
        return str(int(round(f)))
    return f'{f:.3f}'.rstrip('0').rstrip('.')


def _wrap_data_uri(uri, width=76):
    """Wrap base64 payloads so Android's XML parser does not see giant lines."""
    if not uri.startswith('data:image/') or ',' not in uri:
        return uri
    header, b64data = uri.split(',', 1)
    compact = re.sub(r'\s+', '', b64data)
    wrapped = '\n'.join(compact[i:i + width] for i in range(0, len(compact), width))
    return f'{header},{wrapped}'


def _count_leading_tabs(line):
    """Count leading tab characters (or convert leading spaces to tabs)."""
    s = line
    # If line uses spaces, convert the leading spaces to a tab count
    leading_spaces = len(s) - len(s.lstrip(' '))
    if leading_spaces > 0:
        # Assume 4 spaces = 1 tab
        return leading_spaces // 4
    leading_tabs = len(s) - len(s.lstrip('\t'))
    return leading_tabs


def _reindent(text, new_base=1):
    """Normalize indentation (strip all leading whitespace), then re-indent
    each line to *new_base* + original_relative_depth tabs.
    """
    lines = text.splitlines()
    if not lines:
        return text

    # Determine the minimum indentation across non-blank lines
    min_indent = None
    for line in lines:
        if line.strip():
            tabs = _count_leading_tabs(line)
            if min_indent is None or tabs < min_indent:
                min_indent = tabs

    if min_indent is None:
        min_indent = 0

    result = []
    for line in lines:
        if line.strip():
            tabs = _count_leading_tabs(line)
            relative = tabs - min_indent
            result.append('\t' * (new_base + relative) + line.lstrip('\t '))
        else:
            result.append('')
    return '\n'.join(result)


def _flatten_transforms(body, defs_raw='', inlined_ids=None):
    """Flatten <g transform='matrix(...)'> wrappers into child attributes.
    Applies the affine matrix to child element x/y/font-size,
    converts <use> references to <image>, and removes wrapper groups.
    """
    def _parse_matrix(val):
        a = re.match(
            r'matrix\(\s*([\d.eE+-]+)\s*[, ]\s*([\d.eE+-]+)\s*[, ]\s*([\d.eE+-]+)\s*[, ]\s*'
            r'([\d.eE+-]+)\s*[, ]\s*([\d.eE+-]+)\s*[, ]\s*([\d.eE+-]+)\s*\)', val
        )
        return tuple(float(x) for x in a.groups()) if a else None

    def _is_identity(m):
        return all(abs(v) < 0.0001 for v in m[2:]) and abs(m[0] - 1) < 0.0001 and abs(m[3] - 1) < 0.0001

    def _strip_px(v):
        v = v.strip()
        return v[:-2] if v.endswith('px') else v

    def _fix_tspan(m, orig_tx, orig_ty, matrix):
        a, b, c, d, _, _ = matrix
        astr = m.group(1)
        ta = dict(re.findall(r'''(\S+)\s*=\s*"([^"]*)"''', astr))
        if 'x' in ta and 'y' in ta:
            def _transform_val(val):
                v = _strip_px(val)
                try:
                    return float(v)
                except ValueError:
                    return None
            xs = [_transform_val(x) for x in ta['x'].strip().split()]
            ys = [_transform_val(y) for y in ta['y'].strip().split()]
            if None not in xs and None not in ys and len(xs) == len(ys):
                nxs = [a * (x - orig_tx) + c * (y - orig_ty) for x, y in zip(xs, ys)]
                nys = [b * (x - orig_tx) + d * (y - orig_ty) for x, y in zip(xs, ys)]
                ta['x'] = ' '.join(f'{nx:.3f}' for nx in nxs)
                ta['y'] = ' '.join(f'{ny:.3f}' for ny in nys)
        na = ' '.join(f'{k}="{v}"' for k, v in ta.items())
        return f'<tspan {na}>'

    # Build defs image lookup
    defs_map = {}
    if defs_raw:
        for img_match in re.finditer(r'<image\s+([^>]*)>', defs_raw):
            a = dict(re.findall(r'''(\S+)\s*=\s*"([^"]*)"''', img_match.group(1)))
            if a.get('id'):
                defs_map['#' + a['id']] = a

    def _transform_attrs(attrs, matrix):
        a, b, c, d, e, f = matrix
        scale = math.sqrt(a * a + b * b)
        # Dimensions and font sizes absorb uniform scale below; retain the
        # remaining linear part so rotated components stay rotated.
        if scale > 0.0001:
            ra, rb, rc, rd = a / scale, b / scale, c / scale, d / scale
        else:
            ra, rb, rc, rd = a, b, c, d

        # Scale width/height — strip px suffix for Android compat
        for dim in ('width', 'height'):
            if dim in attrs:
                try:
                    v = float(_strip_px(attrs[dim])) * scale
                    attrs[dim] = f'{v:.3f}'
                except ValueError:
                    pass

        still_identity = (abs(a - 1) < 0.0001 and abs(b) < 0.0001 and
                          abs(c) < 0.0001 and abs(d - 1) < 0.0001 and
                          abs(e) < 0.0001 and abs(f) < 0.0001)

        if 'x' in attrs and 'y' in attrs:
            try:
                xv = float(_strip_px(attrs['x']))
                yv = float(_strip_px(attrs['y']))
                nx = a * xv + c * yv + e
                ny = b * xv + d * yv + f
                del attrs['x'], attrs['y']
                if abs(nx) > 0.0001 or abs(ny) > 0.0001 or not still_identity:
                    attrs['transform'] = f'matrix({ra:.3f} {rb:.3f} {rc:.3f} {rd:.3f} {nx:.3f} {ny:.3f})'
            except ValueError:
                pass
        else:
            if not still_identity:
                attrs['transform'] = f'matrix({ra:.3f} {rb:.3f} {rc:.3f} {rd:.3f} {e:.3f} {f:.3f})'

        if 'style' in attrs:
            attrs['style'] = re.sub(
                r'font-size:([\d.]+)px',
                lambda m: f'font-size:{float(m.group(1)) * scale:.3f}px',
                attrs['style']
            )
        return attrs

    def _merge_adjacent_text_fragments(inner):
        """Merge Affinity's adjacent same-line text fragments into one node.

        Affinity may export a single visual text run as several ``<text>``
        elements (and split individual letters into ``<tspan>`` elements),
        particularly when the parent group is transformed. Flattening that
        group first turns every fragment into a separate editor layer. Merge
        only adjacent, same-style text with the same baseline and increasing
        x coordinates so unrelated text remains separate.
        """
        text_re = re.compile(r'<text\b([^>]*)>(.*?)</text>', re.DOTALL)
        out = []
        cursor = 0
        pending = None

        def _flush():
            nonlocal pending
            if pending is not None:
                out.append(f'<text {pending["attrs"]}>{pending["content"]}</text>')
                pending = None

        for match in text_re.finditer(inner):
            gap = inner[cursor:match.start()]
            attrs_str = match.group(1)
            attrs = dict(re.findall(r'''(\S+)\s*=\s*"([^"]*)"''', attrs_str))
            payload = re.sub(r'</?tspan\b[^>]*>', '', match.group(2))
            has_only_tspans = '<' not in payload and '>' not in payload

            try:
                x = float(_strip_px(attrs['x'].strip().split()[0]))
            except (KeyError, ValueError, IndexError):
                x = None

            # x and y are positional; all remaining attributes must match.
            key_attrs = {k: v for k, v in attrs.items() if k != 'x'}
            key = tuple(sorted(key_attrs.items()))
            can_merge = (
                pending is not None and not gap.strip() and has_only_tspans
                and x is not None and key == pending['key'] and x > pending['last_x']
            )

            if can_merge:
                pending['content'] += payload
                pending['last_x'] = x
            else:
                _flush()
                out.append(inner[cursor:match.start()])
                if has_only_tspans and x is not None:
                    pending = {
                        'attrs': attrs_str.strip(), 'content': payload,
                        'key': key, 'last_x': x,
                    }
                else:
                    out.append(match.group(0))
            cursor = match.end()

        _flush()
        out.append(inner[cursor:])
        return ''.join(out)

    def _flatten_group(match):
        g_attrs_str = match.group(1)
        inner = match.group(2)

        g_attrs = dict(re.findall(r'''(\S+)\s*=\s*"([^"]*)"''', g_attrs_str))
        tv = g_attrs.get('transform', '')
        matrix = _parse_matrix(tv)
        if matrix is None:
            return match.group(0)

        keep_g = bool(g_attrs.get('id')) and g_attrs['id'] != ''
        g_attrs.pop('transform', None)

        # Do this before applying the group matrix, otherwise each fragment
        # becomes its own positioned text layer.
        inner = _merge_adjacent_text_fragments(inner)

        # Process child elements (both paired and self-closing)
        def _proc_paired(e):
            tag = e.group(1)
            astr = e.group(2)
            inner = e.group(3)
            ca = dict(re.findall(r'''(\S+)\s*=\s*"([^"]*)"''', astr))

            orig_tx = None
            orig_ty = None
            if tag == 'text' and 'x' in ca and 'y' in ca:
                try:
                    orig_tx = float(_strip_px(ca['x']))
                    orig_ty = float(_strip_px(ca['y']))
                except ValueError:
                    pass

            ca = _transform_attrs(ca, matrix)
            na = ' '.join(f'{k}="{v}"' for k, v in ca.items())

            # Fix tspan positions relative to the text's new origin
            if tag == 'text' and orig_tx is not None and orig_ty is not None:
                inner = re.sub(r'<tspan\b([^>]*)>', lambda m: _fix_tspan(m, orig_tx, orig_ty, matrix), inner)

            return f'<{tag} {na}>{inner}</{tag}>'

        def _proc_self(e):
            tag = e.group(1)
            astr = e.group(2)
            ca = dict(re.findall(r'''(\S+)\s*=\s*"([^"]*)"''', astr))
            ca = _transform_attrs(ca, matrix)
            na = ' '.join(f'{k}="{v}"' for k, v in ca.items())
            return f'<{tag} {na} />'

        inner = re.sub(r'<(\w+)([^>]*)>(.*?)</\1>', _proc_paired, inner, flags=re.DOTALL)
        inner = re.sub(r'<(\w+)([^>]*?)\s/>', _proc_self, inner)

        if keep_g:
            rem = ' '.join(f'{k}="{v}"' for k, v in g_attrs.items())
            tag = f'<g {rem}>' if rem else '<g>'
            return f'{tag}\n{inner}\n</g>'

        return inner

    body = re.sub(
        r'<g\b([^>]*?transform="matrix\([^)]+\)"[^>]*)>(.*?)</g>',
        _flatten_group,
        body,
        flags=re.DOTALL
    )

    # Convert <use> to <image> using defs data
    def _use_to_image(m):
        astr = m.group(1)
        close = ' />' if m.group(2) else '>'
        ua = dict(re.findall(r'''(\S+)\s*=\s*"([^"]*)"''', astr))

        # SVG 2 uses ``href`` while older Affinity exports use
        # ``xlink:href``. Treat them equivalently when resolving backgrounds.
        href = ua.get('href') or ua.get('xlink:href')

        if href and href in defs_map:
            ia = dict(defs_map[href])
            ia.pop('id', None)
            for k in ('x', 'y', 'width', 'height', 'transform', 'style'):
                if k in ua:
                    ia[k] = ua[k]
            if inlined_ids is not None:
                inlined_ids.add(href[1:])
            na = ' '.join(f'{k}="{v}"' for k, v in ia.items())
            return f'<image {na}{close}'

        # Do not turn unresolved references into an empty <image>. They may
        # refer to a pattern, symbol, or other non-image definition.
        return m.group(0)

    body = re.sub(r'<use\b([^>]*?)(\s*/)?>', _use_to_image, body)
    return body


def _rescale_body(body, orig_w, orig_h):
    """Scale all coordinates, font sizes, and image dimensions from orig_w×orig_h
    space to a 1500px-wide canvas with the same aspect ratio."""
    TARGET_W = 1500.0
    TARGET_H = TARGET_W * orig_h / orig_w
    scale = TARGET_W / orig_w

    def _scale_attr_val(m):
        try:
            return f'{m.group(1)}="{float(m.group(2)) * scale:.3f}"'
        except (ValueError, TypeError):
            return m.group(0)

    def _scale_px_val(m):
        try:
            return f'{float(m.group(1)) * scale:.3f}px'
        except (ValueError, TypeError):
            return m.group(0)

    # Scale transform matrix translate values: matrix(1 0 0 1 tx ty)
    body = re.sub(r'(matrix\([\d.eE+-]+\s+[\d.eE+-]+\s+[\d.eE+-]+\s+[\d.eE+-]+\s+)([\d.eE+-]+)(\s+)([\d.eE+-]+)(\))',
                  lambda m: f'{m.group(1)}{float(m.group(2)) * scale:.3f}{m.group(3)}{float(m.group(4)) * scale:.3f}{m.group(5)}',
                  body)

    # Scale width="N" and height="N" (with or without px suffix)
    for attr in ('width', 'height'):
        body = re.sub(rf'\b({attr})="([\d.]+)(?:px)?"', lambda m: f'{m.group(1)}="{float(m.group(2)) * scale:.3f}"', body)

    # Scale font-size:Npx in style
    body = re.sub(r'(font-size:)([\d.]+)(px)', lambda m: f'{m.group(1)}{float(m.group(2)) * scale:.3f}px', body)

    # Scale x="N" and y="N" (no px suffix)
    for attr in ('x', 'y'):
        body = re.sub(rf'\b({attr})="([\d.]+)"', _scale_attr_val, body)

    def _resize_raw_image(raw, fmt, width, height):
        if HAS_PIL:
            try:
                img = Image.open(io.BytesIO(raw))
                img = img.resize((width, height), Image.LANCZOS)
                buf = io.BytesIO()
                save_fmt = 'JPEG' if fmt in ('jpg', 'jpeg') else 'PNG'
                img.save(buf, save_fmt, quality=95)
                return buf.getvalue()
            except Exception:
                pass

        # macOS fallback. The Android editor uses decoded bitmap dimensions,
        # so conversion must still work on machines without Pillow installed.
        ext = 'jpg' if fmt in ('jpg', 'jpeg') else 'png'
        try:
            with tempfile.TemporaryDirectory() as tmp:
                src = os.path.join(tmp, f'in.{ext}')
                dst = os.path.join(tmp, f'out.{ext}')
                with open(src, 'wb') as fh:
                    fh.write(raw)
                subprocess.run(
                    ['sips', '-z', str(height), str(width), src, '--out', dst],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=True,
                )
                with open(dst, 'rb') as fh:
                    return fh.read()
        except Exception:
            return raw

    def _resize_img_tag(m):
        tag = m.group(0)
        attr_items = re.findall(r'([A-Za-z_:][-A-Za-z0-9_:.]*)\s*=\s*"([^"]*)"', tag)
        attrs = {}
        order = []
        for key, value in attr_items:
            if key not in attrs:
                order.append(key)
            attrs[key] = value

        if 'width' not in attrs or 'height' not in attrs:
            return tag
        try:
            tw = float(attrs['width'].replace('px', ''))
            th = float(attrs['height'].replace('px', ''))
        except ValueError:
            return tag

        href_value = attrs.get('xlink:href') or attrs.get('href') or ''
        is_full_canvas_image = (
            href_value.startswith('data:image/')
            and abs(tw - TARGET_W) < 1
            and abs(th - TARGET_H) < 1
        )
        if is_full_canvas_image:
            tw, th = TARGET_W, TARGET_H

        if href_value.startswith('data:image/') and not is_full_canvas_image:
            header, _, b64data = href_value.partition(',')
            fmt = header.replace('data:image/', '').split(';')[0].lower()
            try:
                raw = base64.b64decode(re.sub(r'\s+', '', b64data), validate=False)
                resized = _resize_raw_image(raw, fmt, int(round(tw)), int(round(th)))
                b64_new = base64.b64encode(resized).decode('ascii')
                href_value = f'{header},{b64_new}'
            except Exception:
                pass

        attrs['width'] = _fmt_num(tw)
        attrs['height'] = _fmt_num(th)
        if href_value:
            attrs['xlink:href'] = _wrap_data_uri(href_value)
        attrs.pop('href', None)

        if is_full_canvas_image:
            attrs.pop('transform', None)
        elif 'transform' not in attrs and ('x' in attrs or 'y' in attrs):
            try:
                tx = float(str(attrs.get('x', '0')).replace('px', ''))
                ty = float(str(attrs.get('y', '0')).replace('px', ''))
                attrs['transform'] = f'matrix(1 0 0 1 {_fmt_num(tx)} {_fmt_num(ty)})'
                attrs.pop('x', None)
                attrs.pop('y', None)
            except ValueError:
                pass

        # Keep a predictable attribute order and write one canonical image href.
        ordered_keys = []
        for key in order:
            if key in ('href', 'xlink:href'):
                continue
            if key in attrs and key not in ordered_keys:
                ordered_keys.append(key)
        if 'xlink:href' in attrs:
            insert_at = len(ordered_keys)
            for candidate in ('preserveAspectRatio', 'height', 'width'):
                if candidate in ordered_keys:
                    insert_at = ordered_keys.index(candidate) + 1
            ordered_keys.insert(insert_at, 'xlink:href')
        for key in attrs:
            if key not in ordered_keys:
                ordered_keys.append(key)

        attr_text = ' '.join(f'{key}="{attrs[key]}"' for key in ordered_keys)
        closing = ' />' if tag.rstrip().endswith('/>') else '>'
        return f'<image {attr_text}{closing}'

    body = re.sub(r'<image\s+[^>]*>', _resize_img_tag, body)

    return body, TARGET_W, TARGET_H


def _flatten_tspans(body):
    """Remove <tspan> tags inside <text> elements, merging their text content."""
    def _merge_text(m):
        tag_attrs = m.group(1)
        content = m.group(2)
        content = re.sub(r'<tspan\b[^>]*>', '', content)
        content = re.sub(r'</tspan>', '', content)
        return f'<text{tag_attrs}>{content}</text>'

    return re.sub(r'<text\b([^>]*)>(.*?)</text>', _merge_text, body, flags=re.DOTALL)


def _clean_font_families(body):
    """Simplify font-family: keep first value only, remove quotes and hyphens."""
    def _clean(m):
        val = m.group(1)
        first = val.split(',')[0].strip().strip("'")
        first = first.replace('-', '')
        return f'font-family:{first}'

    body = re.sub(r'font-family:([^;]+)', _clean, body)
    body = re.sub(r'font-family="([^"]+)"', lambda m: f'font-family="' + m.group(1).split(',')[0].strip().strip("'").replace('-', '') + '"', body)
    return body


def _normalize_text_nodes_for_editor(body):
    """Make text nodes closer to the Illustrator SVGs the editor expects."""
    illustrator_text_scale_x = 1.0071

    def _normalize_text_content(text):
        # Affinity sometimes inserts spaces inside phone-number-like fragments.
        return re.sub(r'(?<=\d)-\s+(?=\d)', '-', text)

    def _normalize_text_tag(m):
        tag = m.group(1)
        content = _normalize_text_content(m.group(2))

        # Illustrator stores a very small horizontal stretch in the transform
        # and correspondingly smaller font-size. The editor ignores text
        # matrix scale, so preserving that shape avoids width/baseline drift.
        def _font_size(mm):
            value = float(mm.group(1)) / illustrator_text_scale_x
            return f'font-size:{value:.4f}px'

        tag = re.sub(r'font-size:([\d.]+)px', _font_size, tag)

        def _matrix(mm):
            b, c, d, e, f = mm.groups()
            return f'matrix({illustrator_text_scale_x:.4f} {b} {c} {d} {e} {f})'

        tag = re.sub(
            r'matrix\(1(?:\.0+)?\s+([\d.eE+-]+)\s+([\d.eE+-]+)\s+([\d.eE+-]+)\s+([\d.eE+-]+)\s+([\d.eE+-]+)\)',
            _matrix,
            tag,
            count=1,
        )
        return f'<text{tag}>{content}</text>'

    return re.sub(r'<text\b([^>]*)>(.*?)</text>', _normalize_text_tag, body, flags=re.DOTALL)


def _split_top_level_elements(inner):
    """Split SVG body into complete top-level elements without breaking tspans."""
    token_re = re.compile(r'<(/?)([A-Za-z_][A-Za-z0-9_:.-]*)(?:\s[^<>]*?)?(/?)>', re.DOTALL)
    elems = []
    pos = 0
    length = len(inner)

    while pos < length:
        start = inner.find('<', pos)
        if start == -1:
            break
        if inner.startswith('<!--', start):
            end = inner.find('-->', start + 4)
            if end == -1:
                break
            pos = end + 3
            continue

        match = token_re.match(inner, start)
        if not match:
            pos = start + 1
            continue
        if match.group(1):
            pos = match.end()
            continue

        tag_stack = [match.group(2)]
        scan = match.end()
        if match.group(3) or inner[match.start():match.end()].rstrip().endswith('/>'):
            elems.append(inner[start:match.end()].strip())
            pos = match.end()
            continue

        while tag_stack:
            next_match = token_re.search(inner, scan)
            if not next_match:
                elems.append(inner[start:].strip())
                return elems
            token_text = next_match.group(0)
            is_closing = bool(next_match.group(1))
            tag_name = next_match.group(2)
            is_self_closing = bool(next_match.group(3)) or token_text.rstrip().endswith('/>')

            if is_closing:
                if tag_stack and tag_stack[-1] == tag_name:
                    tag_stack.pop()
            elif not is_self_closing:
                tag_stack.append(tag_name)
            scan = next_match.end()

        elems.append(inner[start:scan].strip())
        pos = scan

    return elems


def transform_svg(content: str) -> str:
    """Return the transformed SVG string."""

    # Skip if already converted (idempotent guard)
    if (
        re.search(r'\bviewBox="0\s+0\s+1500(?:\.0+)?\s+\d+(?:\.\d+)?"', content)
        and 'id="Layer_1"' in content
    ):
        return content

    # ----------------------------------------------------------------
    # 1. Pre-processing (strip declaration, doctype, comments, serif)
    # ----------------------------------------------------------------
    content = re.sub(r'<\?xml[^>]*\?>', '', content)
    content = re.sub(r'<!DOCTYPE[^>]*>', '', content)
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)
    content = re.sub(r'\s+xmlns:serif="[^"]*"', '', content)
    content = re.sub(r'\s+serif:[a-zA-Z]+="[^"]*"', '', content)
    content = content.strip()

    if not content:
        return "<?xml version='1.0' encoding='utf-8'?>\n<svg xmlns='http://www.w3.org/2000/svg' />\n"

    # ----------------------------------------------------------------
    # 2. Locate the <svg> opening tag
    # ----------------------------------------------------------------
    m_svg = re.search(r'<svg\b([^>]*)>', content)
    if not m_svg:
        return "<?xml version='1.0' encoding='utf-8'?>\n" + content + '\n'

    old_svg_str = m_svg.group(0)
    attrs = _get_attrs(old_svg_str)

    # ----------------------------------------------------------------
    # 3. Fix attributes
    # ----------------------------------------------------------------
    vb = attrs.get('viewBox', '')
    vb_parts = vb.strip().split() if vb else []

    # Store original viewBox dimensions for later rescaling
    orig_vb_w = float(vb_parts[2]) if len(vb_parts) == 4 else None
    orig_vb_h = float(vb_parts[3]) if len(vb_parts) == 4 else None

    # Use viewBox dimensions for width/height (canvas needs pixel values, not %)
    for attr, idx in [('width', 2), ('height', 3)]:
        val = attrs.get(attr, '')
        if not val or val.endswith('%'):
            if len(vb_parts) == 4:
                attrs[attr] = f'{vb_parts[idx]}px'

    for attr in ('x', 'y'):
        if attr not in attrs:
            attrs[attr] = '0px'

    style = attrs.get('style', '')
    if vb and 'enable-background' not in style:
        style = f'enable-background:new {vb};'
        attrs['style'] = style

    attrs.pop('xmlns:serif', None)

    # ----------------------------------------------------------------
    # 4. Extract defs section (include leading whitespace)
    # ----------------------------------------------------------------
    defs_match = re.search(r'([ \t]*<defs>.*?</defs>)', content, re.DOTALL)
    defs_raw = defs_match.group(1) if defs_match else ''

    # ----------------------------------------------------------------
    # 5. Extract body (content between <svg> and </svg>)
    # ----------------------------------------------------------------
    body = re.sub(r'</svg>', '', content)
    body = body.replace(old_svg_str, '', 1)

    # Remove defs from body
    if defs_raw:
        if defs_raw in body:
            body = body.replace(defs_raw, '')
        else:
            body = body.replace(defs_raw.strip(), '')

    # ----------------------------------------------------------------
    # 6. Fix self-closing tags
    # ----------------------------------------------------------------
    body = re.sub(r'([^ ])/>', r'\1 />', body)
    if defs_raw:
        defs_raw = re.sub(r'([^ ])/>', r'\1 />', defs_raw)

    # ----------------------------------------------------------------
    # 7. Flatten transform matrices and convert <use> to <image>
    # ----------------------------------------------------------------
    # Some processed Affinity exports contain empty transformed groups next to
    # text. Remove them first so the parent transform can be flattened safely.
    while True:
        cleaned_body = re.sub(r'<g\b[^>]*>\s*</g>', '', body, flags=re.DOTALL)
        if cleaned_body == body:
            break
        body = cleaned_body

    # Record exactly which defs images are copied into the body. This lets us
    # retain definitions still needed for SVG backgrounds and other effects.
    inlined_defs_image_ids = set()
    body = _flatten_transforms(body, defs_raw, inlined_defs_image_ids)

    # Strip px units from x/y attributes on all elements (canvas app compat)
    body = re.sub(r'\b(x|y)="([\d.]+)px"', r'\1="\2"', body)

    # Remove empty <g> wrappers left by nested-group flattening.
    # Match a bare <g> (no attributes) wrapping exactly one child element, then </g>.
    # This avoids eating closing tags of legitimate groups like <g id="Document.jpg">.
    body = re.sub(r'<g>\s*(<[^>]+>.*?</\w+>)\s*</g>', r'\1', body, flags=re.DOTALL)

    # ----------------------------------------------------------------
    # 8. Rescale content to a 1500px-wide canvas while keeping the original ratio
    # ----------------------------------------------------------------
    if orig_vb_w and orig_vb_h and orig_vb_w > 0 and orig_vb_h > 0:
        body, target_w, target_h = _rescale_body(body, orig_vb_w, orig_vb_h)
        attrs['width'] = f'{_fmt_num(target_w)}px'
        attrs['height'] = f'{_fmt_num(target_h)}px'
        attrs['viewBox'] = f'0 0 {_fmt_num(target_w)} {_fmt_num(target_h)}'
        # Update enable-background in style
        style = attrs.get('style', '')
        attrs['style'] = (
            f'enable-background:new 0 0 {_fmt_num(target_w)} {_fmt_num(target_h)};'
        )

    body = _flatten_tspans(body)
    body = _clean_font_families(body)
    body = _normalize_text_nodes_for_editor(body)

    new_svg_tag = _make_svg_tag(attrs)

    # ----------------------------------------------------------------
    # 9. Restructure into per-element layer groups (like AI exports)
    #    Each element gets its own <g id="Layer_X"> wrapper.
    # ----------------------------------------------------------------
    body_stripped = body.strip()

    # Extract top-level children from the main <g id="Layer_1"> if present
    m_layer1 = re.match(r'^<g\s+id="Layer_1">\s*(.*?)\s*</g>$', body_stripped, re.DOTALL)
    if m_layer1:
        inner = m_layer1.group(1).strip()
    else:
        inner = body_stripped

    # Split into top-level elements without breaking nested <tspan> content.
    top_elems = _split_top_level_elements(inner)

    layers = []
    for idx, elem in enumerate(top_elems, start=1):
        content = elem.strip()
        # Unwrap named-<g> wrappers (like <g id="Document.jpg">...) that don't have Layer_X id
        g_unwrap = re.match(r'^<g\s+id="[^"]*"\s*>(.*)</g>$', content, re.DOTALL)
        if g_unwrap:
            inner_content = g_unwrap.group(1).strip()
            # Only unwrap if the group has no transform (it's just a container)
            if 'transform' not in content[:content.index('>')]:
                content = inner_content
        # Add style="overflow:visible;" to image elements
        if content.startswith('<image '):
            if 'style=' not in content[:200]:
                content = content.replace('<image ', '<image style="overflow:visible;" ')
        # Convert rgb(r,g,b) to hex in style attributes
        def _rgb_to_hex(m):
            r, g, b = int(m.group(1)), int(m.group(2)), int(m.group(3))
            return f'#{r:02x}{g:02x}{b:02x}'
        content = re.sub(r'rgb\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*\)', _rgb_to_hex, content)
        layer_type = 2
        if content.startswith('<image '):
            layer_type = 0 if idx == 1 else 1
        elif content.startswith('<text '):
            layer_type = 2
        layers.append((layer_type, idx, f'\t<g id="Layer_{idx}">\n\t\t{content}\n\t</g>'))

    # If no layers found (fallback), wrap whole body as Layer_1
    if not layers:
        inner_reindent = _reindent(inner, new_base=2).rstrip()
        layers.append((2, 1, f'\t<g id="Layer_1">\n{inner_reindent}\n\t</g>'))

    # Keep the same general ordering as Illustrator exports:
    # page image first, other imagery next, text layers last.
    wrapped = '\n'.join(layer for _, _, layer in sorted(layers, key=lambda item: (item[0], item[1])))

    # ----------------------------------------------------------------
    # 9. Assemble the final document
    # ----------------------------------------------------------------
    result = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n"
    result += new_svg_tag + '\n'

    # Strip only images that were actually inlined into the body. Removing all
    # defs images breaks backgrounds that still reference a definition.
    if defs_raw:
        for rid in inlined_defs_image_ids:
            # A definition can be used by more than one construct. Keep it if
            # a remaining <use> or CSS/SVG url(#...) reference still needs it.
            reference_re = rf'(?:xlink:)?href="#{re.escape(rid)}"|url\(#{re.escape(rid)}\)'
            if re.search(reference_re, body) or re.search(reference_re, defs_raw):
                continue
            defs_raw = re.sub(rf'[ \t]*<image[^>]*id="{re.escape(rid)}"[^>]*>\s*', '', defs_raw)
        # Check if defs has any real content left (non-whitespace, non-tag markup)
        inner = re.search(r'<defs>(.*?)</defs>', defs_raw, re.DOTALL)
        has_content = inner and len(inner.group(1).strip()) > 0
        if has_content and defs_raw.strip():
            result += _reindent(defs_raw, new_base=1) + '\n'

    result += wrapped + '\n'
    result += '</svg>\n'

    return result


# ---------------------------------------------------------------------------
# Folder processing
# ---------------------------------------------------------------------------
def process_folder(input_dir: str, output_dir: str, log_callback=None):
    ok = fail = 0
    os.makedirs(output_dir, exist_ok=True)
    for fname in os.listdir(input_dir):
        if not fname.lower().endswith('.svg'):
            continue
        if fname == 'old_structure.svg':
            continue
        src = os.path.join(input_dir, fname)
        if not os.path.isfile(src):
            continue
        dst = os.path.join(output_dir, fname)
        try:
            with open(src, 'r', encoding='utf-8') as fh:
                transformed = transform_svg(fh.read())
            with open(dst, 'w', encoding='utf-8') as fh:
                fh.write(transformed)
            ok += 1
            if log_callback:
                log_callback(f'  OK  {fname}')
        except Exception as e:
            fail += 1
            if log_callback:
                log_callback(f'FAIL  {fname}  –  {e}')
    return ok, fail


# ---------------------------------------------------------------------------
# Web-based GUI (mirrors the original tkinter layout)
# ---------------------------------------------------------------------------
def _start_webui():
    import http.server
    import json
    import urllib.parse
    import webbrowser
    import threading
    import subprocess
    import socketserver

    HOST, PORT = '127.0.0.1', 8080

    HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>SVG Format Converter</title>
<style>
  *{{box-sizing:border-box;margin:0;padding:0}}
  body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
       background:#f0f0f0;padding:20px;font-size:13px}}
  .window{{max-width:700px;margin:0 auto}}
  h1{{font-size:18px;font-weight:600;color:#1d1d1f;margin-bottom:12px}}
  .section{{border:1px solid #d2d2d7;border-radius:6px;background:#fff;margin-bottom:10px;overflow:hidden}}
  .section-title{{font-size:11px;font-weight:600;color:#6e6e73;text-transform:uppercase;
                 letter-spacing:.5px;padding:8px 12px;background:#f5f5f7;border-bottom:1px solid #d2d2d7}}
  .section-body{{display:flex;align-items:center;gap:8px;padding:8px 12px}}
  .section-body input{{flex:1;height:28px;border:1px solid #d2d2d7;border-radius:4px;padding:0 8px;font-size:13px;
                       outline:none;background:#fff}}
  .section-body input:focus{{border-color:#0071e3;box-shadow:0 0 0 2px rgba(0,113,227,.2)}}
  .btn-browse{{height:28px;padding:0 14px;border:1px solid #d2d2d7;border-radius:4px;background:#fff;
              font-size:13px;cursor:pointer;white-space:nowrap;color:#1d1d1f}}
  .btn-browse:hover{{background:#f5f5f7}}
  .btn-convert{{display:block;width:100%;height:32px;border:none;border-radius:6px;
               background:#0071e3;color:#fff;font-size:13px;font-weight:500;cursor:pointer;margin-bottom:10px}}
  .btn-convert:hover{{background:#0077ed}}
  .btn-convert:disabled{{opacity:.4;cursor:default}}
  .log-section{{border:1px solid #d2d2d7;border-radius:6px;background:#fff;overflow:hidden}}
  .log-header{{font-size:11px;font-weight:600;color:#6e6e73;text-transform:uppercase;
              letter-spacing:.5px;padding:8px 12px;background:#f5f5f7;border-bottom:1px solid #d2d2d7}}
  #log{{font-family:Menlo,Consolas,monospace;font-size:11px;padding:8px 12px;height:260px;
       overflow-y:auto;white-space:pre-wrap;line-height:1.6;background:#fff;color:#1d1d1f}}
  #log:empty{{color:#86868b}}
  #log:empty::after{{content:'Ready'}}
  .lg-ok{{color:#248a3d}}
  .lg-fail{{color:#bf4800}}
  .lg-sep{{color:#86868b;border-top:1px solid #e8e8ed;display:block;margin:4px 0;padding-top:4px}}
</style>
</head>
<body>
<div class="window">
<h1>SVG Format Converter</h1>

<div class="section">
  <div class="section-title">Input folder</div>
  <div class="section-body">
    <input type="text" id="input_dir" placeholder="/path/to/svg/files" spellcheck="false">
    <button class="btn-browse" onclick="browse('input_dir')">Browse…</button>
  </div>
</div>

<div class="section">
  <div class="section-title">Output folder</div>
  <div class="section-body">
    <input type="text" id="output_dir" value="{_DEFAULT_OUTPUT}" spellcheck="false">
    <button class="btn-browse" onclick="browse('output_dir')">Browse…</button>
  </div>
</div>

<button class="btn-convert" id="btn" onclick="convert()">Convert SVGs</button>

<div class="log-section">
  <div class="log-header">Log</div>
  <div id="log"></div>
</div>
</div>

<script>
var inputDir=document.getElementById('input_dir'),
    outputDir=document.getElementById('output_dir'),
    btn=document.getElementById('btn'),
    logEl=document.getElementById('log');

async function browse(id){{
  try{{
    var r=await fetch('/browse');
    var data=await r.json();
    if(data.path)document.getElementById(id).value=data.path;
    else logEl.innerHTML='<span class="lg-fail">'+(data.error?'Browse: '+data.error:'Browse cancelled or failed')+'</span>';
  }}catch(e){{
    logEl.innerHTML='<span class="lg-fail">Browse error: '+e.message+'</span>';
  }}
}}

async function convert(){{
  btn.disabled=true;btn.textContent='Converting…';
  logEl.innerHTML='';
  try{{
    var r=await fetch('/convert?input='+encodeURIComponent(inputDir.value)+'&output='+encodeURIComponent(outputDir.value));
    var data=await r.json();
    var html='';
    data.logs.forEach(function(l){{
      if(l.startsWith('  OK'))html+='<span class="lg-ok">'+l+'</span>\\n';
      else if(l.startsWith('FAIL'))html+='<span class="lg-fail">'+l+'</span>\\n';
      else if(l.startsWith('\\nDone')||l.startsWith('='))html+='<span class="lg-sep"></span>'+l+'\\n';
      else html+=l+'\\n';
    }});
    logEl.innerHTML=html;
  }}catch(e){{logEl.innerHTML='<span class="lg-fail">Error: '+e.message+'</span>'}}
  btn.disabled=false;btn.textContent='Convert SVGs';
}}
</script>
</body>
</html>"""

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            parsed = urllib.parse.urlparse(self.path)
            if parsed.path == '/':
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.send_header('Cache-Control', 'no-cache')
                self.end_headers()
                self.wfile.write(HTML.encode())
            elif parsed.path == '/check':
                info = {}
                try:
                    r = subprocess.run(['xcrun', '--find', 'swift'], capture_output=True, text=True, timeout=5)
                    info['swift_path'] = r.stdout.strip()
                    info['swift_found'] = r.returncode == 0
                except Exception as e:
                    info['swift_error'] = str(e)
                try:
                    r = subprocess.run(['osascript', '-e', 'return "ok"'], capture_output=True, text=True, timeout=5)
                    info['osascript_ok'] = r.returncode == 0 and r.stdout.strip() == 'ok'
                except Exception as e:
                    info['osascript_error'] = str(e)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(info).encode())
            elif parsed.path == '/browse':
                path = ''
                error = ''
                try:
                    # Platform-specific folder picker. Use macOS Swift code where
                    # available; on Windows use tkinter; on other Unix try zenity.
                    if sys.platform == 'darwin':
                        swift_code = (
                            'import Cocoa\n'
                            'let app = NSApplication.shared\n'
                            'app.setActivationPolicy(.regular)\n'
                            'app.activate(ignoringOtherApps: true)\n'
                            'let panel = NSOpenPanel()\n'
                            'panel.canChooseFiles = false\n'
                            'panel.canChooseDirectories = true\n'
                            'panel.allowsMultipleSelection = false\n'
                            'panel.prompt = "Select"\n'
                            'panel.level = .modalPanel\n'
                            'if panel.runModal() == .OK, let url = panel.url {\n'
                            '    print(url.path, terminator: "")\n'
                            '}\n'
                            'NSApplication.shared.terminate(nil)\n'
                        )
                        result = subprocess.run(
                            ['xcrun', 'swift', '-'],
                            input=swift_code, capture_output=True, text=True, timeout=120
                        )
                        if result.returncode == 0:
                            path = result.stdout.strip()
                        else:
                            error = f'rc={result.returncode} stderr={result.stderr.strip()}'
                    elif sys.platform.startswith('win'):
                        try:
                            import tkinter as tk
                            from tkinter import filedialog

                            root = tk.Tk()
                            root.withdraw()
                            sel = filedialog.askdirectory()
                            try:
                                root.destroy()
                            except Exception:
                                pass
                            path = sel or ''
                        except Exception as e:
                            # Fallback to PowerShell FolderBrowserDialog if tkinter fails
                            try:
                                ps_cmd = ['powershell', '-NoProfile', '-Command',
                                          "Add-Type -AssemblyName System.Windows.Forms; $f = New-Object System.Windows.Forms.FolderBrowserDialog; if($f.ShowDialog() -eq 'OK'){ Write-Output $f.SelectedPath }"
                                          ]
                                result = subprocess.run(ps_cmd, capture_output=True, text=True, timeout=60)
                                if result.returncode == 0:
                                    path = result.stdout.strip()
                                else:
                                    error = f'rc={result.returncode} stderr={result.stderr.strip()}'
                            except Exception as e2:
                                error = str(e2)
                    else:
                        # Try zenity (common on Linux desktop environments)
                        try:
                            result = subprocess.run(['zenity', '--file-selection', '--directory'], capture_output=True, text=True, timeout=60)
                            if result.returncode == 0:
                                path = result.stdout.strip()
                            else:
                                error = f'rc={result.returncode} stderr={result.stderr.strip()}'
                        except Exception as e:
                            error = str(e)
                except subprocess.TimeoutExpired:
                    error = 'timed out'
                except Exception as e:
                    error = str(e)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'path': path, 'error': error}).encode())
            elif parsed.path == '/convert':
                qs = urllib.parse.parse_qs(parsed.query)
                in_dir = qs.get('input', [''])[0]
                out_dir = qs.get('output', [''])[0]
                logs = []
                ok = fail = 0
                if in_dir and out_dir:
                    try:
                        ok, fail = process_folder(in_dir, out_dir, log_callback=lambda m: logs.append(m))
                    except Exception as e:
                        logs.append(f'Error: {e}')
                logs.append(f'\n{"=" * 40}')
                logs.append(f'Done: {ok+fail} file(s)  —  {ok} OK  /  {fail} FAIL')
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'logs': logs}).encode())
            else:
                self.send_response(404)
                self.end_headers()
        def log_message(self, fmt, *args):
            pass

    socketserver.ThreadingTCPServer.allow_reuse_address = True
    for port in range(PORT, PORT + 100):
        try:
            server = socketserver.ThreadingTCPServer((HOST, port), Handler)
            PORT = port
            break
        except OSError:
            continue
    else:
        print('No available port found.')
        return
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    webbrowser.open(f'http://{HOST}:{PORT}')
    print(f'Open http://{HOST}:{PORT} in your browser (Ctrl+C to stop)')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print()
        server.shutdown()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert SVGs to canvas-compatible format.')
    parser.add_argument('input_dir', nargs='?', help='Input folder containing SVG files')
    parser.add_argument('output_dir', nargs='?', default=_DEFAULT_OUTPUT,
                        help=f'Output folder (default: {_DEFAULT_OUTPUT})')
    args = parser.parse_args()

    if args.input_dir:
        ok, fail = process_folder(args.input_dir, args.output_dir, log_callback=print)
        print(f'\nDone: {ok + fail} file(s) — {ok} OK / {fail} FAIL')
        sys.exit(0 if fail == 0 else 1)
    else:
        _start_webui()
