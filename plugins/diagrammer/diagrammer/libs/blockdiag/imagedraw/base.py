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

from functools import partial

from blockdiag.imagedraw import textfolder
from blockdiag.utils import Box


class ImageDraw(object):
    self_generative_methods = []
    nosideeffect_methods = ['set_canvas_size', 'textsize', 'textlinesize']
    supported_path = False
    baseline_text_rendering = False

    def set_canvas_size(self, size):
        pass

    def set_options(self, **kwargs):
        pass

    def line(self, xy, **kwargs):
        pass

    def rectangle(self, box, **kwargs):
        pass

    def polygon(self, xy, **kwargs):
        pass

    def arc(self, xy, start, end, **kwargs):
        pass

    def ellipse(self, xy, **kwargs):
        pass

    def textsize(self, string, font, maxwidth=None, **kwargs):
        if maxwidth is None:
            maxwidth = 65535

        box = Box(0, 0, maxwidth, 65535)
        textbox = self.textfolder(box, string, font, **kwargs)
        return textbox.outlinebox.size

    @property
    def textfolder(self):
        return partial(textfolder.get, self,
                       adjustBaseline=self.baseline_text_rendering)

    def textlinesize(self, string, font, **kwargs):
        pass

    def text(self, xy, string, font, **kwargs):
        pass

    def textarea(self, box, string, font, **kwargs):
        pass

    def image(self, box, url):
        pass

    def save(self, filename, size, _format):
        pass
