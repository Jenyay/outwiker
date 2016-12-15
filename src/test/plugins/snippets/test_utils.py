# -*- coding: UTF-8 -*-

import unittest
from tempfile import mkdtemp
import os

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application
from test.utils import removeDir


class SnippetsUtilsTest(unittest.TestCase):
    def setUp(self):
        dirlist = [u"../plugins/snippets"]

        self.loader = PluginsLoader(Application)
        self.loader.load(dirlist)
        self._tmpdir = mkdtemp(u'outwiker_snippets_tmp')

    def tearDown(self):
        self.loader.clear()
        removeDir(self._tmpdir)

    def test_createFile_01(self):
        from snippets.utils import createFile
        fname = os.path.join(self._tmpdir, u'Имя файла.txt')
        createFile(fname)
        self.assertTrue(os.path.exists(fname))

    def test_createFile_02(self):
        from snippets.utils import createFile
        fname = os.path.join(self._tmpdir, u'Имя файла.txt')
        createFile(fname)
        createFile(fname)
        self.assertTrue(os.path.exists(fname))

    def test_findUniquePath_01(self):
        from snippets.utils import findUniquePath
        fname = u'Имя файла.txt'

        uniquePath = findUniquePath(self._tmpdir, fname)
        self.assertEqual(uniquePath, os.path.join(self._tmpdir, fname))

    def test_findUniquePath_02_invalid(self):
        from snippets.utils import findUniquePath
        self.assertRaises(ValueError, findUniquePath, self._tmpdir, u'')

    def test_findUniquePath_03(self):
        from snippets.utils import findUniquePath, createFile
        fname = u'Имя файла'

        createFile(os.path.join(self._tmpdir, fname))

        uniquePath = findUniquePath(self._tmpdir, fname)
        self.assertEqual(uniquePath,
                         os.path.join(self._tmpdir, fname + u' (1)'))

    def test_findUniquePath_04(self):
        from snippets.utils import findUniquePath, createFile
        fname = u'Имя файла'

        createFile(os.path.join(self._tmpdir, fname))
        createFile(os.path.join(self._tmpdir, fname + u' (1)'))
        createFile(os.path.join(self._tmpdir, fname + u' (2)'))

        uniquePath = findUniquePath(self._tmpdir, fname)
        self.assertEqual(uniquePath,
                         os.path.join(self._tmpdir, fname + u' (3)'))

    def test_findUniquePath_05(self):
        from snippets.utils import findUniquePath
        fname = u'Имя файла.txt'

        uniquePath = findUniquePath(self._tmpdir, fname, u'.txt')
        self.assertEqual(uniquePath, os.path.join(self._tmpdir, fname))

    def test_findUniquePath_06(self):
        from snippets.utils import findUniquePath, createFile
        fname = u'Имя файла.txt'

        createFile(os.path.join(self._tmpdir, fname))

        uniquePath = findUniquePath(self._tmpdir, fname, u'.txt')
        self.assertEqual(uniquePath,
                         os.path.join(self._tmpdir, u'Имя файла (1).txt'))

    def test_findUniquePath_07(self):
        from snippets.utils import findUniquePath, createFile
        fname = u'Имя файла.txt'

        createFile(os.path.join(self._tmpdir, fname))
        createFile(os.path.join(self._tmpdir, u'Имя файла (1).txt'))
        createFile(os.path.join(self._tmpdir, u'Имя файла (2).txt'))

        uniquePath = findUniquePath(self._tmpdir, fname, u'.txt')
        self.assertEqual(uniquePath,
                         os.path.join(self._tmpdir, u'Имя файла (3).txt'))

    def test_findUniquePath_08(self):
        from snippets.utils import findUniquePath, createFile
        fname = u'Имя файла.txt'

        createFile(os.path.join(self._tmpdir, fname))

        uniquePath = findUniquePath(self._tmpdir, fname, u'.dat')
        self.assertEqual(uniquePath,
                         os.path.join(self._tmpdir, u'Имя файла.txt (1).dat'))
