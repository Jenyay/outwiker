# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application


class DataSourcesTest (unittest.TestCase):
    def setUp (self):
        dirlist = [u"../plugins/datagraph"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)

        self.StringSource = self.loader[u'DataGraph'].StringSource
        self.FileSource = self.loader[u'DataGraph'].FileSource


    def tearDown (self):
        self.loader.clear()


    def testStringSource_empty_01 (self):
        data = u''''''
        source = self.StringSource (data)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 0, items)


    def testStringSource_empty_02 (self):
        data = u''''''
        source = self.StringSource (data)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 0)


    def testStringSource_single_01 (self):
        data = u'''123'''
        source = self.StringSource (data)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 1)
        self.assertEqual (items[0], u'123')


    def testStringSource_single_02 (self):
        data = u'''123    '''
        source = self.StringSource (data)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 1)
        self.assertEqual (items[0], u'123')


    def testStringSource_single_03 (self):
        data = u'''   123    '''
        source = self.StringSource (data)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 1)
        self.assertEqual (items[0], u'123')


    def testStringSource_single_04 (self):
        data = u'''123
        
        '''
        source = self.StringSource (data)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 1)
        self.assertEqual (items[0], u'123')


    def testStringSource_single_05 (self):
        data = u'''123
'''
        source = self.StringSource (data)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 1)
        self.assertEqual (items[0], u'123')
