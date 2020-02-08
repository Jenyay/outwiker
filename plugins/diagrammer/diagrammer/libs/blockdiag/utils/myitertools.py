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

from itertools import cycle, islice


def istep(seq, step=2):
    iterable = iter(seq)
    while True:
        item = list(islice(iterable, step))
        if len(item) < step:
            break
        yield item


def stepslice(iterable, steps):
    try:
        iterable = iter(iterable)
        step = cycle(steps)

        while True:
            # skip (1)
            n = next(step)
            if n == 0:
                pass
            elif n == 1:
                o = next(iterable)
                yield o
                yield o
            else:
                yield next(iterable)
                for _ in range(n - 2):
                    next(iterable)
                yield next(iterable)

            # skip (2)
            for _ in range(next(step)):
                next(iterable)
    except StopIteration:
        return
