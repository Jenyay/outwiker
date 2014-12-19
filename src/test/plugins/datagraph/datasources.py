# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application


class StringSourcesTest (unittest.TestCase):
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
        self.assertEqual (items[0], [u'123'])


    def testStringSource_single_02 (self):
        data = u'''123    '''
        source = self.StringSource (data)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 1)
        self.assertEqual (items[0], [u'123'])


    def testStringSource_single_03 (self):
        data = u'''   123    '''
        source = self.StringSource (data)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 1)
        self.assertEqual (items[0], [u'123'])


    def testStringSource_single_04 (self):
        data = u'''123
        
        '''
        source = self.StringSource (data)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 1)
        self.assertEqual (items[0], [u'123'])


    def testStringSource_single_05 (self):
        data = u'''123
'''
        source = self.StringSource (data)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 1)
        self.assertEqual (items[0], [u'123'])


    def testStringSource_one_col_01 (self):
        data = u'''123
234
456'''
        source = self.StringSource (data)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 3)
        self.assertEqual (items[0], [u'123'])
        self.assertEqual (items[1], [u'234'])
        self.assertEqual (items[2], [u'456'])


    def testStringSource_one_col_02 (self):
        data = u'''123
234
456
'''
        source = self.StringSource (data)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 3)
        self.assertEqual (items[0], [u'123'])
        self.assertEqual (items[1], [u'234'])
        self.assertEqual (items[2], [u'456'])


    def testStringSource_one_col_03 (self):
        data = u'''123
234
456

'''
        source = self.StringSource (data)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 3)
        self.assertEqual (items[0], [u'123'])
        self.assertEqual (items[1], [u'234'])
        self.assertEqual (items[2], [u'456'])


    def testStringSource_one_col_04 (self):
        data = u'''
    
123
234
4560

1000
'''
        source = self.StringSource (data)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 4)
        self.assertEqual (items[0], [u'123'])
        self.assertEqual (items[1], [u'234'])
        self.assertEqual (items[2], [u'4560'])
        self.assertEqual (items[3], [u'1000'])


    def testStringSource_col_01 (self):
        data = u'''123    456    789
234    100      111
456    101   99
-10\t55    66
20    30    40    '''
        source = self.StringSource (data)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 5)

        self.assertEqual (items[0], [u'123', u'456', u'789'])
        self.assertEqual (items[1], [u'234', u'100', u'111'])
        self.assertEqual (items[2], [u'456', u'101', u'99'])
        self.assertEqual (items[3], [u'-10', u'55', u'66'])
        self.assertEqual (items[4], [u'20', u'30', u'40'])


    def testStringSource_col_02 (self):
        data = u'''
123    456    789
234    100      111
456    101   99
-10\t55    66
20    30    40    


'''
        source = self.StringSource (data)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 5)

        self.assertEqual (items[0], [u'123', u'456', u'789'])
        self.assertEqual (items[1], [u'234', u'100', u'111'])
        self.assertEqual (items[2], [u'456', u'101', u'99'])
        self.assertEqual (items[3], [u'-10', u'55', u'66'])
        self.assertEqual (items[4], [u'20', u'30', u'40'])


    def testStringSource_col_03 (self):
        data = u'''123    456    789
234    100      111
456    101
'''
        source = self.StringSource (data)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 2)

        self.assertEqual (items[0], [u'123', u'456', u'789'])
        self.assertEqual (items[1], [u'234', u'100', u'111'])


    def testStringSource_col_04 (self):
        data = u'''123    456    789
234    100      111
456    101    99      78
'''
        source = self.StringSource (data)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 2)

        self.assertEqual (items[0], [u'123', u'456', u'789'])
        self.assertEqual (items[1], [u'234', u'100', u'111'])
