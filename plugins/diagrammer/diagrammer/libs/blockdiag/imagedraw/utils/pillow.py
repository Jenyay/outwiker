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


def patch_FreeTypeFont_getsize():
    try:
        from PIL import PILLOW_VERSION
        from PIL.ImageFont import FreeTypeFont

        # Avoid offset problem in Pillow (>= 2.2.0, < 2.6.0)
        if "2.2.0" <= PILLOW_VERSION < "2.6.0":
            original_getsize = FreeTypeFont.getsize

            def getsize(self, string):
                size = original_getsize(self, string)
                offset = self.getoffset(string)

                return (size[0] + offset[0], size[1] + offset[1])

            FreeTypeFont.getsize = getsize
    except ImportError:
        pass


def apply_patch():
    patch_FreeTypeFont_getsize()
