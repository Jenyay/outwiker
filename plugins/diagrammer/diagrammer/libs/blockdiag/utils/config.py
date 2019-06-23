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

import io
import sys
try:
    from configparser import SafeConfigParser
except ImportError:
    from ConfigParser import SafeConfigParser


class ConfigParser(SafeConfigParser):
    def __init__(self):
        if sys.version_info > (2, 6) and sys.version_info < (2, 7):
            # only for Python2.6
            # - dict_type argument is supported py2.6 or later
            # - SafeConfigParser of py2.7 uses OrderedDict as default
            from ordereddict import OrderedDict
            SafeConfigParser.__init__(self, dict_type=OrderedDict)
        else:
            SafeConfigParser.__init__(self)

    def read(self, path):
        fd = io.open(path, 'r', encoding='utf-8-sig')
        self.readfp(fd)
        fd.close()
