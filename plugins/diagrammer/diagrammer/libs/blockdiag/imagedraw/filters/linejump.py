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

import functools

from blockdiag.utils import XY, Box


class LazyReceiver(object):
    def __init__(self, target):
        self.target = target
        self.calls = []

    def __getattr__(self, name):
        return self.get_lazy_method(name)

    def get_lazy_method(self, name):
        if name in self.target.nosideeffect_methods:
            method = self._find_method(name)
            return functools.partial(method, self.target)
        elif name in self.target.self_generative_methods:
            def _(*args, **kwargs):
                receiver = LazySubReceiver(name, self.target, *args, **kwargs)
                self.calls.append((receiver, args, kwargs))
                return receiver

            return _
        else:
            def _(*args, **kwargs):
                self.calls.append((name, args, kwargs))
                return self

            return _

    def _find_method(self, name):
        if isinstance(name, LazyReceiver):
            return name

        for p in self.target.__class__.__mro__:
            if name in p.__dict__:
                return p.__dict__[name]

        raise AttributeError("%s instance has no attribute '%s'" %
                             (self.target.__class__.__name__, name))

    def _run(self):
        for name, args, kwargs in self.calls:
            method = self._find_method(name)
            method(self.target, *args, **kwargs)


class LazySubReceiver(LazyReceiver):
    def __init__(self, name, target, *args, **kwargs):
        self.name = name
        self.args = args
        self.kwargs = kwargs
        super(LazySubReceiver, self).__init__(target)

    def __call__(self, target, *args, **kwargs):
        method = self._find_method(self.name)
        self.target = method(self.target, *self.args, **self.kwargs)
        self._run()


class LineJumpDrawFilter(LazyReceiver):
    def __init__(self, target, jump_radius):
        super(LineJumpDrawFilter, self).__init__(target)
        self.ytree = []
        self.x_cross = {}
        self.y_cross = {}
        self.forward = 'holizonal'
        self.jump_radius = jump_radius
        self.jump_shift = 0

    def set_options(self, **kwargs):
        if 'jump_forward' in kwargs:
            self.forward = kwargs['jump_forward']

        if 'jump_radius' in kwargs:
            self.jump_radius = kwargs['jump_radius']

        if 'jump_shift' in kwargs:
            self.jump_shift = kwargs['jump_shift']

    def _run(self):
        for name, args, kwargs in self.calls:
            if name == 'line' and kwargs.get('jump'):
                ((x1, y1), (x2, y2)) = args[0]
                if self.forward == 'holizonal' and y1 == y2:
                    self._holizonal_jumpline(x1, y1, x2, y2, **kwargs)
                    continue
                elif self.forward == 'vertical' and x1 == x2:
                    self._vertical_jumpline(x1, y1, x2, y2, **kwargs)
                    continue

            method = self._find_method(name)
            method(self.target, *args, **kwargs)

    def _holizonal_jumpline(self, x1, y1, x2, y2, **kwargs):
        y = y1
        if x2 < x1:
            x1, x2 = x2, x1

        for x in sorted(self.x_cross.get(y, [])):
            if x1 < x and x < x2:
                arckwargs = dict(kwargs)
                del arckwargs['jump']

                x += self.jump_shift
                r = self.jump_radius
                line = (XY(x1, y), XY(x - r, y))
                self.target.line(line, **kwargs)
                box = Box(x - r, y - r, x + r, y + r)
                self.target.arc(box, 180, 0, **arckwargs)
                x1 = x + r

        self.target.line((XY(x1, y), XY(x2, y)), **kwargs)

    def _vertical_jumpline(self, x1, y1, x2, y2, **kwargs):
        x = x1
        if y2 < y1:
            y1, y2 = y2, y1

        for y in sorted(self.y_cross.get(x, [])):
            if y1 < y and y < y2:
                arckwargs = dict(kwargs)
                del arckwargs['jump']

                y += self.jump_shift
                r = self.jump_radius
                line = (XY(x, y1), XY(x, y - r))
                self.target.line(line, **kwargs)
                box = Box(x - r, y - r, x + r, y + r)
                self.target.arc(box, 270, 90, **arckwargs)
                y1 = y + r

        self.target.line((XY(x, y1), XY(x, y2)), **kwargs)

    def line(self, xy, **kwargs):
        from bisect import insort
        for st, ed in zip(xy[:-1], xy[1:]):
            self.get_lazy_method("line")((st, ed), **kwargs)

            if 'jump' in kwargs and kwargs['jump'] is True:
                if st.y == ed.y:    # horizonal
                    insort(self.ytree, (st.y, 0, (st, ed)))
                elif st.x == ed.x:  # vertical
                    insort(self.ytree, (max(st.y, ed.y), -1, (st, ed)))
                    insort(self.ytree, (min(st.y, ed.y), +1, (st, ed)))

    def save(self, *args, **kwargs):
        # Search crosspoints
        from bisect import bisect_left, bisect_right, insort
        xtree = []
        for y, _, ((x1, y1), (x2, y2)) in self.ytree:
            if x2 < x1:
                x1, x2 = x2, x1
            if y2 < y1:
                y1, y2 = y2, y1

            if y == y1:
                insort(xtree, x1)

            if y == y2:
                del xtree[bisect_left(xtree, x1)]
                for x in xtree[bisect_right(xtree, x1):bisect_left(xtree, x2)]:
                    self.x_cross.setdefault(y, set()).add(x)
                    self.y_cross.setdefault(x, set()).add(y)

        self._run()
        return self.target.save(*args, **kwargs)
