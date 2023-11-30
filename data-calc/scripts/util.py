#!/usr/bin/env python3
# -*- coding: utf8 -*-

import unicodedata

WIDTHS = {
    'F': 2,
    'H': 1,
    'W': 2,
    'N': 1,
    'A': 1,  # Not really correct...
    'Na': 1,
}


def tab_str(text, width=16):
    # 制表 默认一个制表符长度为 4
    if not isinstance(text, str):
        text = str(text)

    text_width = 0
    for ch in text:
        width_class = unicodedata.east_asian_width(ch)
        text_width += WIDTHS[width_class]
    if width <= text_width:
        return text
    return text + ' ' * (width - text_width)
