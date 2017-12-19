# -*- coding: UTF-8 -*-

import unittest
from tempfile import mkdtemp
import os

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application
from test.utils import removeDir


class SnippetsUtilsTest(unittest.TestCase):
    def setUp(self):
        dirlist = ["../plugins/snippets"]

        self.loader = PluginsLoader(Application)
        self.loader.load(dirlist)
        self._tmpdir = mkdtemp('outwiker_snippets_tmp')

    def tearDown(self):
        self.loader.clear()
        removeDir(self._tmpdir)

    def test_createFile_01(self):
        from snippets.utils import createFile
        fname = os.path.join(self._tmpdir, 'Имя файла.txt')
        createFile(fname)
        self.assertTrue(os.path.exists(fname))

    def test_createFile_02(self):
        from snippets.utils import createFile
        fname = os.path.join(self._tmpdir, 'Имя файла.txt')
        createFile(fname)
        createFile(fname)
        self.assertTrue(os.path.exists(fname))

    def test_findUniquePath_01(self):
        from snippets.utils import findUniquePath
        fname = 'Имя файла.txt'

        uniquePath = findUniquePath(self._tmpdir, fname)
        self.assertEqual(uniquePath, os.path.join(self._tmpdir, fname))

    def test_findUniquePath_02_invalid(self):
        from snippets.utils import findUniquePath
        self.assertRaises(ValueError, findUniquePath, self._tmpdir, '')

    def test_findUniquePath_03(self):
        from snippets.utils import findUniquePath, createFile
        fname = 'Имя файла'

        createFile(os.path.join(self._tmpdir, fname))

        uniquePath = findUniquePath(self._tmpdir, fname)
        self.assertEqual(uniquePath,
                         os.path.join(self._tmpdir, fname + ' (1)'))

    def test_findUniquePath_04(self):
        from snippets.utils import findUniquePath, createFile
        fname = 'Имя файла'

        createFile(os.path.join(self._tmpdir, fname))
        createFile(os.path.join(self._tmpdir, fname + ' (1)'))
        createFile(os.path.join(self._tmpdir, fname + ' (2)'))

        uniquePath = findUniquePath(self._tmpdir, fname)
        self.assertEqual(uniquePath,
                         os.path.join(self._tmpdir, fname + ' (3)'))

    def test_findUniquePath_05(self):
        from snippets.utils import findUniquePath
        fname = 'Имя файла.txt'

        uniquePath = findUniquePath(self._tmpdir, fname, '.txt')
        self.assertEqual(uniquePath, os.path.join(self._tmpdir, fname))

    def test_findUniquePath_06(self):
        from snippets.utils import findUniquePath, createFile
        fname = 'Имя файла.txt'

        createFile(os.path.join(self._tmpdir, fname))

        uniquePath = findUniquePath(self._tmpdir, fname, '.txt')
        self.assertEqual(uniquePath,
                         os.path.join(self._tmpdir, 'Имя файла (1).txt'))

    def test_findUniquePath_07(self):
        from snippets.utils import findUniquePath, createFile
        fname = 'Имя файла.txt'

        createFile(os.path.join(self._tmpdir, fname))
        createFile(os.path.join(self._tmpdir, 'Имя файла (1).txt'))
        createFile(os.path.join(self._tmpdir, 'Имя файла (2).txt'))

        uniquePath = findUniquePath(self._tmpdir, fname, '.txt')
        self.assertEqual(uniquePath,
                         os.path.join(self._tmpdir, 'Имя файла (3).txt'))

    def test_findUniquePath_08(self):
        from snippets.utils import findUniquePath, createFile
        fname = 'Имя файла.txt'

        createFile(os.path.join(self._tmpdir, fname))

        uniquePath = findUniquePath(self._tmpdir, fname, '.dat')
        self.assertEqual(uniquePath,
                         os.path.join(self._tmpdir, 'Имя файла.txt (1).dat'))

    def test_moveSnippetsTo_01(self):
        from snippets.utils import moveSnippetsTo, createFile
        fname = os.path.join(self._tmpdir, 'snippet')

        createFile(fname)
        moveSnippetsTo(fname, self._tmpdir)

        self.assertTrue(os.path.exists(fname))

    def test_moveSnippetsTo_02(self):
        from snippets.utils import moveSnippetsTo, createFile
        fname = os.path.join(self._tmpdir, 'snippet')
        createFile(fname)
        dest = os.path.join(self._tmpdir, 'Поддиректория')
        os.mkdir(dest)

        result = moveSnippetsTo(fname, dest)

        self.assertEqual(result, os.path.join(dest, 'snippet'))
        self.assertFalse(os.path.exists(fname))
        self.assertTrue(os.path.exists(result))

    def test_moveSnippetsTo_03(self):
        from snippets.utils import moveSnippetsTo, createFile
        fname = os.path.join(self._tmpdir, 'snippet')
        createFile(fname)
        dest = os.path.join(self._tmpdir, 'Поддиректория')
        os.mkdir(dest)

        createFile(os.path.join(dest, 'snippet'))

        result = moveSnippetsTo(fname, dest)

        self.assertEqual(result, os.path.join(dest, 'snippet (1)'))

        self.assertTrue(os.path.exists(os.path.join(dest, 'snippet')))
        self.assertFalse(os.path.exists(fname))
        self.assertTrue(os.path.exists(result))

    def test_moveSnippetsTo_04(self):
        from snippets.utils import moveSnippetsTo, createFile
        fname = os.path.join(self._tmpdir, 'snippet')
        createFile(fname)
        dest = os.path.join(self._tmpdir, 'Поддиректория')
        os.mkdir(dest)

        createFile(os.path.join(dest, 'snippet'))
        createFile(os.path.join(dest, 'snippet (1)'))

        result = moveSnippetsTo(fname, dest)

        self.assertEqual(result, os.path.join(dest, 'snippet (2)'))

        self.assertTrue(os.path.exists(os.path.join(dest, 'snippet')))
        self.assertTrue(os.path.exists(os.path.join(dest, 'snippet (1)')))
        self.assertFalse(os.path.exists(fname))
        self.assertTrue(os.path.exists(result))

    def test_moveSnippetsTo_05(self):
        from snippets.utils import moveSnippetsTo, createFile
        fname = os.path.join(self._tmpdir, 'snippet')
        createFile(fname)
        dest = os.path.join(self._tmpdir, 'Поддиректория')
        os.mkdir(dest)

        os.mkdir(os.path.join(dest, 'snippet'))

        result = moveSnippetsTo(fname, dest)

        self.assertEqual(result, os.path.join(dest, 'snippet (1)'))

        self.assertTrue(os.path.exists(os.path.join(dest, 'snippet')))
        self.assertFalse(os.path.exists(fname))
        self.assertTrue(os.path.exists(result))

    def test_moveSnippetsTo_06(self):
        from snippets.utils import moveSnippetsTo, createFile
        dirname = os.path.join(self._tmpdir, 'дир_1', 'дир_2', 'дир_3')

        os.makedirs(dirname)
        fname = os.path.join(dirname, 'snippet')
        createFile(fname)

        dest = os.path.join(self._tmpdir, 'дир_1')

        result = moveSnippetsTo(fname, dest)

        self.assertEqual(result, os.path.join(dest, 'snippet'))

        self.assertTrue(os.path.exists(os.path.join(dest, 'snippet')))
        self.assertFalse(os.path.exists(fname))
        self.assertTrue(os.path.exists(result))

    def test_moveSnippetsTo_07(self):
        from snippets.utils import moveSnippetsTo, createFile

        fname = os.path.join(self._tmpdir, 'snippet')
        dirname = os.path.join(self._tmpdir, 'subdir')

        os.makedirs(dirname)
        createFile(fname)

        result = moveSnippetsTo(fname, dirname)

        self.assertEqual(result, os.path.join(dirname, 'snippet'))
        self.assertTrue(os.path.exists(result))
        self.assertFalse(os.path.exists(fname))

    def test_moveSnippetsTo_08(self):
        from snippets.utils import moveSnippetsTo
        dirname = os.path.join(self._tmpdir, 'subdir')

        os.makedirs(dirname)
        moveSnippetsTo(dirname, self._tmpdir)

        self.assertTrue(os.path.exists(dirname))

    def test_moveSnippetsTo_09(self):
        from snippets.utils import moveSnippetsTo, createFile

        dirname_1 = os.path.join(self._tmpdir, 'subdir_1')
        fname = os.path.join(dirname_1, 'snippet')

        dirname_2 = os.path.join(self._tmpdir, 'subdir_2')

        os.makedirs(dirname_1)
        os.makedirs(dirname_2)
        createFile(fname)

        result = moveSnippetsTo(dirname_1, dirname_2)

        self.assertEqual(result, os.path.join(dirname_2, 'subdir_1'))
        self.assertTrue(os.path.exists(result))
        self.assertTrue(os.path.exists(os.path.join(dirname_2, 'subdir_1', 'snippet')))
        self.assertFalse(os.path.exists(fname))
