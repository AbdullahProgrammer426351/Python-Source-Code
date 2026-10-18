#!/usr/bin/env python3
"""
Test script: converts demo/01.svg and analyzes output for issues.
Hardcoded paths, no tkinter dependency.
"""
import sys, os, re, tempfile

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE)
import main

INPUT = os.path.join(BASE, 'demo', '01.svg')
OUTPUT = os.path.join(tempfile.mkdtemp(), '01.svg')

with open(INPUT, 'r') as f:
    raw = f.read()

result = main.transform_svg(raw)
with open(OUTPUT, 'w') as f:
    f.write(result)

print("=" * 60)
print("  CONVERSION TEST REPORT")
print("=" * 60)

issues = []

# --- 1. SVG tag analysis ---
svg_match = re.search(r'<svg\b([^>]*)>', result)
svg_attrs = dict(re.findall(r'''(\S+)\s*=\s*"([^"]*)"''', svg_match.group(1))) if svg_match else {}
w = svg_attrs.get('width', '')
h = svg_attrs.get('height', '')
print(f"\n[1] SVG dimensions: width={w}  height={h}")
if w.endswith('px') or h.endswith('px'):
    print(f"    WARNING: Using fixed pixels instead of 100% — will appear zoomed in on browser/canvas")
    issues.append("width/height are fixed px values (use 100%)")
else:
    print(f"    OK: responsive dimensions")

# --- 2. Image duplication (defs vs body) ---
all_images = list(re.finditer(r'<image\b', result))
print(f"\n[2] Total <image> elements: {len(all_images)}")

# Find which images are in defs vs body
defs_section = re.search(r'<defs>(.*?)</defs>', result, re.DOTALL)
defs_images = len(re.findall(r'<image\b', defs_section.group(1))) if defs_section else 0
body_section = re.sub(r'<defs>.*?</defs>', '', result, flags=re.DOTALL) if defs_section else result
body_images = len(re.findall(r'<image\b', body_section))

print(f"    In <defs>: {defs_images}")
print(f"    In <body>: {body_images}")

# Check for duplicate image references (same base64 data appearing in both defs and body)
def parse_href(img_match):
    m = re.search(r'xlink:href="([^"]*)"', img_match.group(0))
    return m.group(1)[:80] if m else 'N/A'

img_tags = list(re.finditer(r'<image\b[^>]*>', result))
body_img_data = set()
defs_img_data = set()
for img in img_tags:
    href = parse_href(img)
    img_str = img.group(0)
    if defs_section and '<defs>' in img_str[:20]:
        # Determine position
        pass
    # Check if within defs or not
    pos = img.start()
    if defs_section and defs_section.start() < pos < defs_section.end():
        defs_img_data.add(href)
    else:
        body_img_data.add(href)

duplicates = defs_img_data & body_img_data
if duplicates:
    print(f"    BUG: {len(duplicates)} image(s) appear in BOTH <defs> and <body>:" )
    for d in duplicates:
        print(f"      - {d[:60]}...")
    issues.append(f"{len(duplicates)} image(s) duplicated in defs + body (canvas app renders both)")
else:
    print(f"    OK: no image duplication")

# --- 3. Redundant empty <g> wrappers ---
empty_gs = re.findall(r'<g>\s*\n\s*<(text|image|use)', result)
print(f"\n[3] Empty <g> wrappers around content: {len(empty_gs)}")
if empty_gs:
    print(f"    NOTE: {len(empty_gs)} empty <g> tags wrapping content (harmless but unnecessary)")
    issues.append(f"{len(empty_gs)} empty <g> wrappers could confuse canvas component detection")

# --- 4. Text transform analysis ---
text_tags = list(re.finditer(r'<text\b([^>]*)>', result))
print(f"\n[4] Text elements: {len(text_tags)}")
for t in text_tags:
    attrs = t.group(1)
    font = re.search(r'font-size:([\d.]+)', attrs)
    xf = re.search(r'transform="([^"]*)"', attrs)
    print(f"    font-size={font.group(1) if font else '?'}px  transform={xf.group(1) if xf else 'none'}")

# --- 5. Defs position ---
if defs_section:
    body_before_defs = result[:defs_section.start()]
    layer1_before_defs = bool(re.search(r'<g\s+id="Layer_1"', body_before_defs))
    print(f"\n[5] <defs> position: BEFORE <g id='Layer_1'>" if layer1_before_defs else f"    <defs> position: AFTER <g id='Layer_1'>")

# --- 6. Layer_1 wrapper ---
has_layer1 = bool(re.search(r'<g\s+id="Layer_1"', result))
print(f"\n[6] <g id='Layer_1'> wrapper: {'PRESENT' if has_layer1 else 'MISSING'}")

# --- 7. Summary ---
print(f"\n{'=' * 60}")
print(f"  ISSUES FOUND: {len(issues)}")
print(f"{'=' * 60}")
for i, issue in enumerate(issues, 1):
    print(f"  {i}. {issue}")
if not issues:
    print("  All checks passed!")

print(f"\nInput:  {INPUT}")
print(f"Output: {OUTPUT}")
