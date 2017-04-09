# -*- coding: UTF-8 -*-

from math import floor
import random


def find_farthest_color(colors_rgb):
    colors_hsv_src = [_rgb_2_hsv(*color) for color in colors_rgb]
    hue_list = [color[0] for color in colors_hsv_src]

    if colors_hsv_src:
        sat_middle = sum(map(lambda x: x[1], colors_hsv_src)) / len(colors_hsv_src)
        sat_middle += random.random() * (0.3) - 0.15
        val_middle = sum(map(lambda x: x[2], colors_hsv_src)) / len(colors_hsv_src)
    else:
        sat_middle = 0.35
        val_middle = 0.90

    hue_farthest = _find_farthest_hue(hue_list)
    new_color_hsv = (hue_farthest, sat_middle, val_middle)
    return _hsv_2_rgb(*new_color_hsv)


def _rgb_2_hsv(r, g, b):
    r = r / 255.0
    g = g / 255.0
    b = b / 255.0
    min_val = min(r, g, b)
    max_val = max(r, g, b)

    if min_val == max_val:
        h = 0
    elif max_val == r and g >= b:
        h = 60 * (g - b) / (max_val - min_val)
    elif max_val == r and g < b:
        h = 60 * (g - b) / (max_val - min_val) + 360
    elif max_val == g:
        h = 60 * (b - r) / (max_val - min_val) + 120
    else:
        h = 60 * (r - g) / (max_val - min_val) + 240

    s = 0.0 if max_val == 0 else 1 - min_val / max_val

    v = max_val

    return (h, s, v)


def _hsv_2_rgb(h, s, v):
    hi = int(floor(h / 60)) % 6
    vmin = (1 - s) * v
    a = (v - vmin) * ((h % 60) / 60)
    vinc = vmin + a
    vdec = v - a

    v = int(v * 255)
    vinc = int(vinc * 255)
    vmin = int(vmin * 255)
    vdec = int(vdec * 255)

    if hi == 0:
        return (v, vinc, vmin)
    elif hi == 1:
        return (vdec, v, vmin)
    elif hi == 2:
        return (vmin, v, vinc)
    elif hi == 3:
        return (vmin, vdec, v)
    elif hi == 4:
        return (vinc, vmin, v)
    else:
        return (v, vmin, vdec)


def _find_farthest_hue(hue_list):
    if not hue_list:
        return int(random.random() * 360)

    hue_list_sorted = sorted(hue_list)
    h_cycled = hue_list_sorted[:] + [hue_list_sorted[0] + 360.0]
    diff = []
    for n in range(len(hue_list_sorted)):
        diff.append((h_cycled[n + 1] - h_cycled[n]))

    max_diff_index = diff.index(max(diff))
    return ((h_cycled[max_diff_index] + h_cycled[max_diff_index + 1]) / 2.0) % 360
