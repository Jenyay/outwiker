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

from __future__ import division

import pkg_resources

renderers = {}
searchpath = []


def init_renderers():
    for plugin in pkg_resources.iter_entry_points('blockdiag_noderenderer'):
        module = plugin.load()
        if hasattr(module, 'setup'):
            module.setup(module)


def install_renderer(name, renderer):
    renderers[name] = renderer


def set_default_namespace(path):
    searchpath[:] = []
    for path in path.split(','):
        searchpath.append(path)


def get(shape):
    if not renderers:
        init_renderers()

    for path in searchpath:
        name = "%s.%s" % (path, shape)
        if name in renderers:
            return renderers[name]

    return renderers.get(shape)
