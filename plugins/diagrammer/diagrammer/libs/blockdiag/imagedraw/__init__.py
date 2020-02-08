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

import pkg_resources

from blockdiag.utils.logging import warning

drawers = {}


def init_imagedrawers(debug=False):
    for drawer in pkg_resources.iter_entry_points('blockdiag_imagedrawers'):
        try:
            module = drawer.load()
            if hasattr(module, 'setup'):
                module.setup(module)
        except Exception as exc:
            if debug:
                warning('Failed to load %s: %r' % (drawer.module_name, exc))


def install_imagedrawer(ext, drawer):
    drawers[ext] = drawer


def create(_format, filename, **kwargs):
    if len(drawers) == 0:
        init_imagedrawers(debug=kwargs.get('debug'))

    _format = _format.lower()
    if _format in drawers:
        drawer = drawers[_format](filename, **kwargs)
    else:
        msg = 'failed to load %s image driver' % _format
        raise RuntimeError(msg)

    if 'linejump' in kwargs.get('filters', []):
        from blockdiag.imagedraw.filters.linejump import LineJumpDrawFilter
        jumpsize = kwargs.get('jumpsize', 0)
        drawer = LineJumpDrawFilter(drawer, jumpsize)

    return drawer
