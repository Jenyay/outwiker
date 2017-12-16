# -*- coding: UTF-8 -*-

import os
import unittest
from tempfile import NamedTemporaryFile

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application


class FileSourceTest (unittest.TestCase):
    def setUp (self):
        dirlist = ["../plugins/datagraph"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)

        self._dataFile = NamedTemporaryFile(delete=False)


    def tearDown (self):
        self.loader.clear()
        self._dataFile.close()
        os.remove (self._dataFile.name)
        self._dataFile = None


    def testFileSource_empty_01 (self):
        from datagraph.datasources import FileSource
        data = ''''''

        self._dataFile.write (data)
        self._dataFile.flush()
        source = FileSource (self._dataFile.name)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 0, items)


    def testFileSource_empty_02 (self):
        from datagraph.datasources import FileSource
        data = '''
        
        
'''
        self._dataFile.write (data)
        self._dataFile.flush()
        source = FileSource (self._dataFile.name)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 0)


    def testFileSource_single_01 (self):
        from datagraph.datasources import FileSource
        data = '''123'''
        self._dataFile.write (data)
        self._dataFile.flush()
        source = FileSource (self._dataFile.name)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 1)
        self.assertEqual (items[0], ['123'])


    def testFileSource_single_02 (self):
        from datagraph.datasources import FileSource
        data = '''123    '''
        self._dataFile.write (data)
        self._dataFile.flush()
        source = FileSource (self._dataFile.name)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 1)
        self.assertEqual (items[0], ['123'])


    def testFileSource_single_03 (self):
        from datagraph.datasources import FileSource
        data = '''   123    '''
        self._dataFile.write (data)
        self._dataFile.flush()
        source = FileSource (self._dataFile.name)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 1)
        self.assertEqual (items[0], ['123'])


    def testFileSource_single_04 (self):
        from datagraph.datasources import FileSource
        data = '''123
        
        '''
        self._dataFile.write (data)
        self._dataFile.flush()
        source = FileSource (self._dataFile.name)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 1)
        self.assertEqual (items[0], ['123'])


    def testFileSource_single_05 (self):
        from datagraph.datasources import FileSource
        data = '''123
'''
        self._dataFile.write (data)
        self._dataFile.flush()
        source = FileSource (self._dataFile.name)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 1)
        self.assertEqual (items[0], ['123'])


    def testFileSource_one_col_01 (self):
        from datagraph.datasources import FileSource
        data = '''123
234
456'''
        self._dataFile.write (data)
        self._dataFile.flush()
        source = FileSource (self._dataFile.name)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 3)
        self.assertEqual (items[0], ['123'])
        self.assertEqual (items[1], ['234'])
        self.assertEqual (items[2], ['456'])


    def testFileSource_one_col_02 (self):
        from datagraph.datasources import FileSource
        data = '''123
234
456
'''
        self._dataFile.write (data)
        self._dataFile.flush()
        source = FileSource (self._dataFile.name)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 3)
        self.assertEqual (items[0], ['123'])
        self.assertEqual (items[1], ['234'])
        self.assertEqual (items[2], ['456'])


    def testFileSource_one_col_03 (self):
        from datagraph.datasources import FileSource
        data = '''123
234
456

'''
        self._dataFile.write (data)
        self._dataFile.flush()
        source = FileSource (self._dataFile.name)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 3)
        self.assertEqual (items[0], ['123'])
        self.assertEqual (items[1], ['234'])
        self.assertEqual (items[2], ['456'])


    def testFileSource_one_col_04 (self):
        from datagraph.datasources import FileSource
        data = '''
    
123
234
4560

1000
'''
        self._dataFile.write (data)
        self._dataFile.flush()
        source = FileSource (self._dataFile.name)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 4)
        self.assertEqual (items[0], ['123'])
        self.assertEqual (items[1], ['234'])
        self.assertEqual (items[2], ['4560'])
        self.assertEqual (items[3], ['1000'])


    def testFileSource_col_01 (self):
        from datagraph.datasources import FileSource
        data = '''123    456    789
234    100      111
456    101   99
-10\t55    66
20    30    40    '''
        self._dataFile.write (data)
        self._dataFile.flush()
        source = FileSource (self._dataFile.name)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 5)

        self.assertEqual (items[0], ['123', '456', '789'])
        self.assertEqual (items[1], ['234', '100', '111'])
        self.assertEqual (items[2], ['456', '101', '99'])
        self.assertEqual (items[3], ['-10', '55', '66'])
        self.assertEqual (items[4], ['20', '30', '40'])


    def testFileSource_col_02 (self):
        from datagraph.datasources import FileSource
        data = '''
123    456    789
234    100      111
456    101   99
-10\t55    66
20    30    40    


'''
        self._dataFile.write (data)
        self._dataFile.flush()
        source = FileSource (self._dataFile.name)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 5)

        self.assertEqual (items[0], ['123', '456', '789'])
        self.assertEqual (items[1], ['234', '100', '111'])
        self.assertEqual (items[2], ['456', '101', '99'])
        self.assertEqual (items[3], ['-10', '55', '66'])
        self.assertEqual (items[4], ['20', '30', '40'])


    def testFileSource_col_03 (self):
        from datagraph.datasources import FileSource
        data = '''123    456    789
234    100      111
456    101
'''
        self._dataFile.write (data)
        self._dataFile.flush()
        source = FileSource (self._dataFile.name)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 2)

        self.assertEqual (items[0], ['123', '456', '789'])
        self.assertEqual (items[1], ['234', '100', '111'])


    def testFileSource_col_04 (self):
        from datagraph.datasources import FileSource
        data = '''123    456    789
234    100      111
456    101    99      78
'''
        self._dataFile.write (data)
        self._dataFile.flush()
        source = FileSource (self._dataFile.name)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 2)

        self.assertEqual (items[0], ['123', '456', '789'])
        self.assertEqual (items[1], ['234', '100', '111'])


    def testFileSource_skiprows_01 (self):
        from datagraph.datasources import FileSource
        data = '''
123    456    789
234    100      111
456    101    99
'''
        self._dataFile.write (data)
        self._dataFile.flush()
        source = FileSource (self._dataFile.name)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 3)

        self.assertEqual (items[0], ['123', '456', '789'])
        self.assertEqual (items[1], ['234', '100', '111'])


    def testFileSource_skiprows_02 (self):
        from datagraph.datasources import FileSource
        data = '''Абырвалг
----
123    456    789
234    100      111
456    101    99
'''
        self._dataFile.write (data.encode ("utf8"))
        self._dataFile.flush()
        source = FileSource (self._dataFile.name, skiprows=2)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 3)

        self.assertEqual (items[0], ['123', '456', '789'])
        self.assertEqual (items[1], ['234', '100', '111'])


    def testFileSource_skiprows_03 (self):
        from datagraph.datasources import FileSource
        data = '''Абырвалг Абыр
----
123    456    789
234    100      111
456    101    99
'''
        self._dataFile.write (data.encode ("utf8"))
        self._dataFile.flush()
        source = FileSource (self._dataFile.name, skiprows=0)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 1)

        self.assertEqual (items[0], ['Абырвалг', 'Абыр'])


    def testFileSource_skiprows_04 (self):
        from datagraph.datasources import FileSource
        data = '''Абырвалг Абыр
----
123    456    789
234    100      111
456    101    99
'''
        self._dataFile.write (data.encode ("utf8"))
        self._dataFile.flush()
        source = FileSource (self._dataFile.name, skiprows=5)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 0)


    def testFileSource_invalid_01 (self):
        from datagraph.datasources import FileSource
        source = FileSource ('invalid_fname.txt')

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 0)


    def testFileSource_invalid_02 (self):
        from datagraph.datasources import FileSource
        source = FileSource ('../test/samplefiles/image.png')

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 0)


    def testFileSource_invalid_03 (self):
        from datagraph.datasources import FileSource
        source = FileSource ('../test/samplefiles/invalid.exe')

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 0)


    def testFileSource_invalid_04 (self):
        from datagraph.datasources import FileSource
        source = FileSource ('../test/samplefiles/text_1251.txt')

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 0)



class StringSourceTest (unittest.TestCase):
    def setUp (self):
        dirlist = ["../plugins/datagraph"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)


    def tearDown (self):
        self.loader.clear()


    def testStringSource_empty_01 (self):
        from datagraph.datasources import StringSource
        data = ''''''
        source = StringSource (data)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 0)


    def testStringSource_empty_02 (self):
        from datagraph.datasources import StringSource
        data = '''
        
        
'''
        source = StringSource (data)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 0)


    def testStringSource_single_01 (self):
        from datagraph.datasources import StringSource
        data = '''123'''
        source = StringSource (data)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 1)
        self.assertEqual (items[0], ['123'])


    def testStringSource_single_02 (self):
        from datagraph.datasources import StringSource
        data = '''123    '''
        source = StringSource (data)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 1)
        self.assertEqual (items[0], ['123'])


    def testStringSource_single_03 (self):
        from datagraph.datasources import StringSource
        data = '''   123    '''
        source = StringSource (data)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 1)
        self.assertEqual (items[0], ['123'])


    def testStringSource_single_04 (self):
        from datagraph.datasources import StringSource
        data = '''123
        
        '''
        source = StringSource (data)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 1)
        self.assertEqual (items[0], ['123'])


    def testStringSource_single_05 (self):
        from datagraph.datasources import StringSource
        data = '''123
'''
        source = StringSource (data)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 1)
        self.assertEqual (items[0], ['123'])


    def testStringSource_one_col_01 (self):
        from datagraph.datasources import StringSource
        data = '''123
234
456'''
        source = StringSource (data)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 3)
        self.assertEqual (items[0], ['123'])
        self.assertEqual (items[1], ['234'])
        self.assertEqual (items[2], ['456'])


    def testStringSource_one_col_02 (self):
        from datagraph.datasources import StringSource
        data = '''123
234
456
'''
        source = StringSource (data)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 3)
        self.assertEqual (items[0], ['123'])
        self.assertEqual (items[1], ['234'])
        self.assertEqual (items[2], ['456'])


    def testStringSource_one_col_03 (self):
        from datagraph.datasources import StringSource
        data = '''123
234
456

'''
        source = StringSource (data)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 3)
        self.assertEqual (items[0], ['123'])
        self.assertEqual (items[1], ['234'])
        self.assertEqual (items[2], ['456'])


    def testStringSource_one_col_04 (self):
        from datagraph.datasources import StringSource
        data = '''
    
123
234
4560

1000
'''
        source = StringSource (data)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 4)
        self.assertEqual (items[0], ['123'])
        self.assertEqual (items[1], ['234'])
        self.assertEqual (items[2], ['4560'])
        self.assertEqual (items[3], ['1000'])


    def testStringSource_col_01 (self):
        from datagraph.datasources import StringSource
        data = '''123    456    789
234    100      111
456    101   99
-10\t55    66
20    30    40    '''
        source = StringSource (data)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 5)

        self.assertEqual (items[0], ['123', '456', '789'])
        self.assertEqual (items[1], ['234', '100', '111'])
        self.assertEqual (items[2], ['456', '101', '99'])
        self.assertEqual (items[3], ['-10', '55', '66'])
        self.assertEqual (items[4], ['20', '30', '40'])


    def testStringSource_col_02 (self):
        from datagraph.datasources import StringSource
        data = '''
123    456    789
234    100      111
456    101   99
-10\t55    66
20    30    40    


'''
        source = StringSource (data)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 5)

        self.assertEqual (items[0], ['123', '456', '789'])
        self.assertEqual (items[1], ['234', '100', '111'])
        self.assertEqual (items[2], ['456', '101', '99'])
        self.assertEqual (items[3], ['-10', '55', '66'])
        self.assertEqual (items[4], ['20', '30', '40'])


    def testStringSource_col_03 (self):
        from datagraph.datasources import StringSource
        data = '''123    456    789
234    100      111
456    101
'''
        source = StringSource (data)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 2)

        self.assertEqual (items[0], ['123', '456', '789'])
        self.assertEqual (items[1], ['234', '100', '111'])


    def testStringSource_col_04 (self):
        from datagraph.datasources import StringSource
        data = '''123    456    789
234    100      111
456    101    99      78
'''
        source = StringSource (data)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 2)

        self.assertEqual (items[0], ['123', '456', '789'])
        self.assertEqual (items[1], ['234', '100', '111'])


    def testStringSource_skiprows_01 (self):
        from datagraph.datasources import StringSource
        data = '''
123    456    789
234    100      111
456    101    99
'''
        source = StringSource (data)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 3)

        self.assertEqual (items[0], ['123', '456', '789'])
        self.assertEqual (items[1], ['234', '100', '111'])


    def testStringSource_skiprows_02 (self):
        from datagraph.datasources import StringSource
        data = '''Абырвалг
----
123    456    789
234    100      111
456    101    99
'''
        source = StringSource (data, skiprows=2)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 3)

        self.assertEqual (items[0], ['123', '456', '789'])
        self.assertEqual (items[1], ['234', '100', '111'])


    def testStringSource_skiprows_03 (self):
        from datagraph.datasources import StringSource
        data = '''Абырвалг Абыр
----
123    456    789
234    100      111
456    101    99
'''
        source = StringSource (data, skiprows=0)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 1)

        self.assertEqual (items[0], ['Абырвалг', 'Абыр'])


    def testStringSource_skiprows_04 (self):
        from datagraph.datasources import StringSource
        data = '''Абырвалг Абыр
----
123    456    789
234    100      111
456    101    99
'''
        source = StringSource (data, skiprows=5)

        items = list (source.getRowsIterator())
        self.assertEqual (len (items), 0)
