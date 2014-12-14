# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application


class GraphBuilderTest (unittest.TestCase):
    def setUp(self):
        dirlist = [u"../plugins/datagraph"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)
        self.GraphBuilder = self.loader[u'DataGraph'].GraphBuilder

        self._defaultWidth = 700
        self._defaultHeight = 400


    def tearDown (self):
        self.loader.clear()


    def testEmpty (self):
        builder = self.GraphBuilder({})
        graph = builder.graph

        self.assertEqual (graph.getValue (u'width'), self._defaultWidth)
        self.assertEqual (graph.getValue (u'height'), self._defaultHeight)

        self.assertEqual (graph.getValue (u'Width'), self._defaultWidth)
        self.assertEqual (graph.getValue (u'HEIGHT'), self._defaultHeight)
