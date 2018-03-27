#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from test.plugins.source.test_source import SourcePluginTest
from test.plugins.source.test_sourceencoding import SourceEncodingPluginTest
from test.plugins.source.test_sourcefile import SourceFilePluginTest
from test.plugins.source.test_sourcegui import SourceGuiPluginTest
from test.plugins.source.test_sourceattachment import SourceAttachmentPluginTest
from test.plugins.source.test_sourcestyle import SourceStyleTest
from test.plugins.source.test_loading import SourceLoadingTest


if __name__ == '__main__':
    unittest.main()
