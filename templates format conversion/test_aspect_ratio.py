#!/usr/bin/env python3
"""Regression tests for preserving source SVG aspect ratios."""

import re
import unittest

import main


def _root_attributes(svg):
    match = re.search(r'<svg\b([^>]*)>', svg)
    return dict(re.findall(r'''(\S+)\s*=\s*"([^"]*)"''', match.group(1)))


class AspectRatioTests(unittest.TestCase):
    def _convert(self, width, height):
        source = f'''<svg width="100%" height="100%"
            viewBox="0 0 {width} {height}"
            xmlns="http://www.w3.org/2000/svg">
            <rect x="0" y="0" width="{width}" height="{height}" />
        </svg>'''
        return main.transform_svg(source)

    def assert_ratio_preserved(self, width, height):
        attrs = _root_attributes(self._convert(width, height))
        output_width = float(attrs['width'].removesuffix('px'))
        output_height = float(attrs['height'].removesuffix('px'))
        self.assertAlmostEqual(output_width / output_height, width / height, places=6)
        self.assertAlmostEqual(output_width, 1500.0)

        viewbox = [float(value) for value in attrs['viewBox'].split()]
        self.assertAlmostEqual(viewbox[2], output_width)
        self.assertAlmostEqual(viewbox[3], output_height)

    def test_landscape_source(self):
        self.assert_ratio_preserved(2000, 1000)

    def test_portrait_source(self):
        self.assert_ratio_preserved(2480, 3496)


if __name__ == '__main__':
    unittest.main()
