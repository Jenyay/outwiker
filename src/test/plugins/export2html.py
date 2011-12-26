#!/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.tree import WikiDocument
from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application


class Export2HtmlTest (unittest.TestCase):
    def setUp(self):
        self.path = u"../test/samplewiki"
        self.root = WikiDocument.load (self.path)
        
        dirlist = [u"../plugins/export2html"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)


    def testLoading (self):
        self.assertEqual (len (self.loader), 1)
        self.loader[u"Export to HTML"]
