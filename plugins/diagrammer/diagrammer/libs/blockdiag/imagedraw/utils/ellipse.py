# -*- coding: utf-8 -*-
#  Copyright 2011 Takeshi KOMIYA
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import math

from blockdiag.utils import XY

DIVISION = 1000.0
CYCLE = 10


def _angles(du, a, b, start, end):
    phi = (start / 180.0) * math.pi
    while phi <= (end / 180.0) * math.pi:
        yield phi
        phi += du / math.sqrt((a * math.sin(phi)) ** 2 +
                              (b * math.cos(phi)) ** 2)


def _coordinates(du, a, b, start, end):
    for angle in _angles(du, a, b, start, end):
        yield (a * math.cos(angle), b * math.sin(angle))


def endpoints(du, a, b, start, end):
    pt1 = next(iter(_coordinates(du, a, b, start, start + 1)))
    pt2 = next(iter(_coordinates(du, a, b, end, end + 1)))

    return [XY(*pt1), XY(*pt2)]


def dots(box, cycle, start=0, end=360):
    # calcrate rendering pattern from cycle
    base = 0
    rendered = []
    for index in range(0, len(cycle), 2):
        i, j = cycle[index:index + 2]
        for n in range(base * 2, (base + i) * 2):
            rendered.append(n)
        base += i + j

    a = float(box.width) / 2
    b = float(box.height) / 2
    du = 1
    _max = sum(cycle) * 2
    center = box.center
    for i, coord in enumerate(_coordinates(du, a, b, start, end)):
        if i % _max in rendered:
            yield XY(center.x + coord[0], center.y + coord[1])
