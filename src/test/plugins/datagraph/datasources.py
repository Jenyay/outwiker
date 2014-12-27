# -*- coding: UTF-8 -*-

import unittest
from tempfile import NamedTemporaryFile

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application


class FileSourceTest (unittest.TestCase):
    def setUp (self):
        dirlist = [u"../plugins/datagraph"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)

        self.FileSource = self.loader[u'DataGraph'].FileSource

        self._dataFile = NamedTemporaryFile()


    def tearDown (self):
        self.loader.clear()
        self._dataFile = None


    def testFileSource_empty_01 (self):
        data = u''''''

        self._dataFile.write (data)
        self._dataFile.flush()
        source = self.FileSource (self._dataFile.name)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 0, items)


    def testFileSource_empty_02 (self):
        data = u'''
        
        
'''
        self._dataFile.write (data)
        self._dataFile.flush()
        source = self.FileSource (self._dataFile.name)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 0)


    def testFileSource_single_01 (self):
        data = u'''123'''
        self._dataFile.write (data)
        self._dataFile.flush()
        source = self.FileSource (self._dataFile.name)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 1)
        self.assertEqual (items[0], [u'123'])


    def testFileSource_single_02 (self):
        data = u'''123    '''
        self._dataFile.write (data)
        self._dataFile.flush()
        source = self.FileSource (self._dataFile.name)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 1)
        self.assertEqual (items[0], [u'123'])


    def testFileSource_single_03 (self):
        data = u'''   123    '''
        self._dataFile.write (data)
        self._dataFile.flush()
        source = self.FileSource (self._dataFile.name)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 1)
        self.assertEqual (items[0], [u'123'])


    def testFileSource_single_04 (self):
        data = u'''123
        
        '''
        self._dataFile.write (data)
        self._dataFile.flush()
        source = self.FileSource (self._dataFile.name)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 1)
        self.assertEqual (items[0], [u'123'])


    def testFileSource_single_05 (self):
        data = u'''123
'''
        self._dataFile.write (data)
        self._dataFile.flush()
        source = self.FileSource (self._dataFile.name)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 1)
        self.assertEqual (items[0], [u'123'])


    def testFileSource_one_col_01 (self):
        data = u'''123
234
456'''
        self._dataFile.write (data)
        self._dataFile.flush()
        source = self.FileSource (self._dataFile.name)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 3)
        self.assertEqual (items[0], [u'123'])
        self.assertEqual (items[1], [u'234'])
        self.assertEqual (items[2], [u'456'])


    def testFileSource_one_col_02 (self):
        data = u'''123
234
456
'''
        self._dataFile.write (data)
        self._dataFile.flush()
        source = self.FileSource (self._dataFile.name)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 3)
        self.assertEqual (items[0], [u'123'])
        self.assertEqual (items[1], [u'234'])
        self.assertEqual (items[2], [u'456'])


    def testFileSource_one_col_03 (self):
        data = u'''123
234
456

'''
        self._dataFile.write (data)
        self._dataFile.flush()
        source = self.FileSource (self._dataFile.name)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 3)
        self.assertEqual (items[0], [u'123'])
        self.assertEqual (items[1], [u'234'])
        self.assertEqual (items[2], [u'456'])


    def testFileSource_one_col_04 (self):
        data = u'''
    
123
234
4560

1000
'''
        self._dataFile.write (data)
        self._dataFile.flush()
        source = self.FileSource (self._dataFile.name)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 4)
        self.assertEqual (items[0], [u'123'])
        self.assertEqual (items[1], [u'234'])
        self.assertEqual (items[2], [u'4560'])
        self.assertEqual (items[3], [u'1000'])


    def testFileSource_col_01 (self):
        data = u'''123    456    789
234    100      111
456    101   99
-10\t55    66
20    30    40    '''
        self._dataFile.write (data)
        self._dataFile.flush()
        source = self.FileSource (self._dataFile.name)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 5)

        self.assertEqual (items[0], [u'123', u'456', u'789'])
        self.assertEqual (items[1], [u'234', u'100', u'111'])
        self.assertEqual (items[2], [u'456', u'101', u'99'])
        self.assertEqual (items[3], [u'-10', u'55', u'66'])
        self.assertEqual (items[4], [u'20', u'30', u'40'])


    def testFileSource_col_02 (self):
        data = u'''
123    456    789
234    100      111
456    101   99
-10\t55    66
20    30    40    


'''
        self._dataFile.write (data)
        self._dataFile.flush()
        source = self.FileSource (self._dataFile.name)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 5)

        self.assertEqual (items[0], [u'123', u'456', u'789'])
        self.assertEqual (items[1], [u'234', u'100', u'111'])
        self.assertEqual (items[2], [u'456', u'101', u'99'])
        self.assertEqual (items[3], [u'-10', u'55', u'66'])
        self.assertEqual (items[4], [u'20', u'30', u'40'])


    def testFileSource_col_03 (self):
        data = u'''123    456    789
234    100      111
456    101
'''
        self._dataFile.write (data)
        self._dataFile.flush()
        source = self.FileSource (self._dataFile.name)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 2)

        self.assertEqual (items[0], [u'123', u'456', u'789'])
        self.assertEqual (items[1], [u'234', u'100', u'111'])


    def testFileSource_col_04 (self):
        data = u'''123    456    789
234    100      111
456    101    99      78
'''
        self._dataFile.write (data)
        self._dataFile.flush()
        source = self.FileSource (self._dataFile.name)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 2)

        self.assertEqual (items[0], [u'123', u'456', u'789'])
        self.assertEqual (items[1], [u'234', u'100', u'111'])


    def testFileSource_skiprows_01 (self):
        data = u'''
123    456    789
234    100      111
456    101    99
'''
        self._dataFile.write (data)
        self._dataFile.flush()
        source = self.FileSource (self._dataFile.name)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 3)

        self.assertEqual (items[0], [u'123', u'456', u'789'])
        self.assertEqual (items[1], [u'234', u'100', u'111'])


    def testFileSource_skiprows_02 (self):
        data = u'''Абырвалг
----
123    456    789
234    100      111
456    101    99
'''
        self._dataFile.write (data.encode (u"utf8"))
        self._dataFile.flush()
        source = self.FileSource (self._dataFile.name, skiprows=2)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 3)

        self.assertEqual (items[0], [u'123', u'456', u'789'])
        self.assertEqual (items[1], [u'234', u'100', u'111'])


    def testFileSource_skiprows_03 (self):
        data = u'''Абырвалг Абыр
----
123    456    789
234    100      111
456    101    99
'''
        self._dataFile.write (data.encode (u"utf8"))
        self._dataFile.flush()
        source = self.FileSource (self._dataFile.name, skiprows=0)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 1)

        self.assertEqual (items[0], [u'Абырвалг', u'Абыр'])


    def testFileSource_skiprows_04 (self):
        data = u'''Абырвалг Абыр
----
123    456    789
234    100      111
456    101    99
'''
        self._dataFile.write (data.encode (u"utf8"))
        self._dataFile.flush()
        source = self.FileSource (self._dataFile.name, skiprows=5)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 0)


    def testFileSource_invalid_01 (self):
        source = self.FileSource (u'invalid_fname.txt')

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 0)


    def testFileSource_invalid_02 (self):
        source = self.FileSource (u'../test/samplefiles/image.png')

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 0)


    def testFileSource_invalid_03 (self):
        source = self.FileSource (u'../test/samplefiles/invalid.exe')

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 0)


    def testFileSource_invalid_04 (self):
        source = self.FileSource (u'../test/samplefiles/text_1251.txt')

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 0)



class StringSourceTest (unittest.TestCase):
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
        self.assertEqual (len (items), 0)


    def testStringSource_empty_02 (self):
        data = u'''
        
        
'''
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


    def testStringSource_skiprows_01 (self):
        data = u'''
123    456    789
234    100      111
456    101    99
'''
        source = self.StringSource (data)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 3)

        self.assertEqual (items[0], [u'123', u'456', u'789'])
        self.assertEqual (items[1], [u'234', u'100', u'111'])


    def testStringSource_skiprows_02 (self):
        data = u'''Абырвалг
----
123    456    789
234    100      111
456    101    99
'''
        source = self.StringSource (data, skiprows=2)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 3)

        self.assertEqual (items[0], [u'123', u'456', u'789'])
        self.assertEqual (items[1], [u'234', u'100', u'111'])


    def testStringSource_skiprows_03 (self):
        data = u'''Абырвалг Абыр
----
123    456    789
234    100      111
456    101    99
'''
        source = self.StringSource (data, skiprows=0)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 1)

        self.assertEqual (items[0], [u'Абырвалг', u'Абыр'])


    def testStringSource_skiprows_04 (self):
        data = u'''Абырвалг Абыр
----
123    456    789
234    100      111
456    101    99
'''
        source = self.StringSource (data, skiprows=5)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 0)
