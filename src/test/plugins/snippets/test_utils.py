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

    def test_moveSnippetsTo_01(self):
        from snippets.utils import moveSnippetsTo, createFile
        fname = os.path.join(self._tmpdir, u'snippet.tpl')

        createFile(fname)
        moveSnippetsTo(fname, self._tmpdir)

        self.assertTrue(os.path.exists(fname))

    def test_moveSnippetsTo_02(self):
        from snippets.utils import moveSnippetsTo, createFile
        fname = os.path.join(self._tmpdir, u'snippet.tpl')
        createFile(fname)
        dest = os.path.join(self._tmpdir, u'Поддиректория')
        os.mkdir(dest)

        result = moveSnippetsTo(fname, dest)

        self.assertEqual(result, os.path.join(dest, u'snippet.tpl'))
        self.assertFalse(os.path.exists(fname))
        self.assertTrue(os.path.exists(result))

    def test_moveSnippetsTo_03(self):
        from snippets.utils import moveSnippetsTo, createFile
        fname = os.path.join(self._tmpdir, u'snippet.tpl')
        createFile(fname)
        dest = os.path.join(self._tmpdir, u'Поддиректория')
        os.mkdir(dest)

        createFile(os.path.join(dest, u'snippet.tpl'))

        result = moveSnippetsTo(fname, dest)

        self.assertEqual(result, os.path.join(dest, u'snippet (1).tpl'))

        self.assertTrue(os.path.exists(os.path.join(dest, u'snippet.tpl')))
        self.assertFalse(os.path.exists(fname))
        self.assertTrue(os.path.exists(result))

    def test_moveSnippetsTo_04(self):
        from snippets.utils import moveSnippetsTo, createFile
        fname = os.path.join(self._tmpdir, u'snippet.tpl')
        createFile(fname)
        dest = os.path.join(self._tmpdir, u'Поддиректория')
        os.mkdir(dest)

        createFile(os.path.join(dest, u'snippet.tpl'))
        createFile(os.path.join(dest, u'snippet (1).tpl'))

        result = moveSnippetsTo(fname, dest)

        self.assertEqual(result, os.path.join(dest, u'snippet (2).tpl'))

        self.assertTrue(os.path.exists(os.path.join(dest, u'snippet.tpl')))
        self.assertTrue(os.path.exists(os.path.join(dest, u'snippet (1).tpl')))
        self.assertFalse(os.path.exists(fname))
        self.assertTrue(os.path.exists(result))

    def test_moveSnippetsTo_05(self):
        from snippets.utils import moveSnippetsTo, createFile
        fname = os.path.join(self._tmpdir, u'snippet.tpl')
        createFile(fname)
        dest = os.path.join(self._tmpdir, u'Поддиректория')
        os.mkdir(dest)

        os.mkdir(os.path.join(dest, u'snippet.tpl'))

        result = moveSnippetsTo(fname, dest)

        self.assertEqual(result, os.path.join(dest, u'snippet (1).tpl'))

        self.assertTrue(os.path.exists(os.path.join(dest, u'snippet.tpl')))
        self.assertFalse(os.path.exists(fname))
        self.assertTrue(os.path.exists(result))

    def test_moveSnippetsTo_06(self):
        from snippets.utils import moveSnippetsTo, createFile
        dirname = os.path.join(self._tmpdir, u'дир_1', u'дир_2', u'дир_3')

        os.makedirs(dirname)
        fname = os.path.join(dirname, u'snippet.tpl')
        createFile(fname)

        dest = os.path.join(self._tmpdir, u'дир_1')

        result = moveSnippetsTo(fname, dest)

        self.assertEqual(result, os.path.join(dest, u'snippet.tpl'))

        self.assertTrue(os.path.exists(os.path.join(dest, u'snippet.tpl')))
        self.assertFalse(os.path.exists(fname))
        self.assertTrue(os.path.exists(result))

    def test_moveSnippetsTo_07(self):
        from snippets.utils import moveSnippetsTo, createFile

        fname = os.path.join(self._tmpdir, 'snippet.tpl')
        dirname = os.path.join(self._tmpdir, u'subdir')

        os.makedirs(dirname)
        createFile(fname)

        result = moveSnippetsTo(fname, dirname)

        self.assertEqual(result, os.path.join(dirname, u'snippet.tpl'))
        self.assertTrue(os.path.exists(result))
        self.assertFalse(os.path.exists(fname))

    def test_moveSnippetsTo_08(self):
        from snippets.utils import moveSnippetsTo
        dirname = os.path.join(self._tmpdir, u'subdir')

        os.makedirs(dirname)
        moveSnippetsTo(dirname, self._tmpdir)

        self.assertTrue(os.path.exists(dirname))

    def test_moveSnippetsTo_09(self):
        from snippets.utils import moveSnippetsTo, createFile

        dirname_1 = os.path.join(self._tmpdir, u'subdir_1')
        fname = os.path.join(dirname_1, 'snippet.tpl')

        dirname_2 = os.path.join(self._tmpdir, u'subdir_2')

        os.makedirs(dirname_1)
        os.makedirs(dirname_2)
        createFile(fname)

        result = moveSnippetsTo(dirname_1, dirname_2)

        self.assertEqual(result, os.path.join(dirname_2, u'subdir_1'))
        self.assertTrue(os.path.exists(result))
        self.assertTrue(os.path.exists(os.path.join(dirname_2, u'subdir_1', u'snippet.tpl')))
        self.assertFalse(os.path.exists(fname))
