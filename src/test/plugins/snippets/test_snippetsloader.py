# -*- coding: UTF-8 -*-

import unittest
from tempfile import mkdtemp
import os

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application
from test.utils import removeDir


class SnippetsLoaderTest(unittest.TestCase):
    def setUp(self):
        dirlist = [u"../plugins/snippets"]

        self.loader = PluginsLoader(Application)
        self.loader.load(dirlist)
        self._dir_snippets = mkdtemp(u'outwiker_snippets')

    def tearDown(self):
        self.loader.clear()
        removeDir(self._dir_snippets)

    def _create(self, fname):
        with open(fname, 'w'):
            pass

    def test_empty_01(self):
        from snippets.snippetsloader import SnippetsLoader
        loader = SnippetsLoader([self._dir_snippets])
        snippets = loader.getSnippets()

        self.assertEqual(snippets.name, None)
        self.assertEqual(len(snippets), 0)
        self.assertEqual(snippets.dirs, [])
        self.assertEqual(snippets.snippets, [])

    def test_empty_02(self):
        from snippets.snippetsloader import SnippetsLoader
        dir_snippets_2 = mkdtemp(u'outwiker_snippets_2')
        loader = SnippetsLoader([self._dir_snippets, dir_snippets_2])
        snippets = loader.getSnippets()

        self.assertEqual(snippets.name, None)
        self.assertEqual(len(snippets), 0)
        self.assertEqual(snippets.dirs, [])
        self.assertEqual(snippets.snippets, [])

    def test_empty_03_invalid(self):
        from snippets.snippetsloader import SnippetsLoader
        loader = SnippetsLoader(['Invalid dir'])
        snippets = loader.getSnippets()

        self.assertEqual(snippets.name, None)
        self.assertEqual(len(snippets), 0)
        self.assertEqual(snippets.dirs, [])
        self.assertEqual(snippets.snippets, [])

    def test_snippets_01(self):
        from snippets.snippetsloader import SnippetsLoader
        files = [u'Шаблон.tpl']
        for fname in files:
            self._create(os.path.join(self._dir_snippets, fname))

        loader = SnippetsLoader([self._dir_snippets])
        snippets = loader.getSnippets()
        self.assertEqual(snippets.dirs, [])
        self.assertEqual(snippets.snippets,
                         [os.path.join(self._dir_snippets, u'Шаблон.tpl')])
        self.assertEqual(len(snippets), 1)

    def test_snippets_02(self):
        from snippets.snippetsloader import SnippetsLoader
        files = [u'Шаблон 01.tpl', u'Шаблон 02.tpl', u'Не шаблон.txt']
        for fname in files:
            self._create(os.path.join(self._dir_snippets, fname))

        loader = SnippetsLoader([self._dir_snippets])
        snippets = loader.getSnippets()
        self.assertEqual(snippets.dirs, [])

        self.assertIn(
            os.path.join(self._dir_snippets, u'Шаблон 01.tpl'),
            snippets.snippets)

        self.assertIn(
            os.path.join(self._dir_snippets, u'Шаблон 02.tpl'),
            snippets.snippets)

        self.assertEqual(len(snippets), 2)

    def test_snippets_03(self):
        from snippets.snippetsloader import SnippetsLoader
        dir_snippets_2 = mkdtemp(u'outwiker_snippets_2')

        files = [os.path.join(self._dir_snippets, u'root_01.tpl'),
                 os.path.join(self._dir_snippets, u'root_02.tpl'),
                 os.path.join(dir_snippets_2, u'root_01.tpl'),
                 os.path.join(dir_snippets_2, u'root_02.tpl'),
                 ]

        map(lambda fname: self._create(fname), files)

        loader = SnippetsLoader([self._dir_snippets, dir_snippets_2])
        snippets = loader.getSnippets()

        self.assertEqual(len(snippets), 4)
        self.assertEqual(len(snippets.dirs), 0)
        self.assertEqual(len(snippets.snippets), 4)

    def test_subdir_01(self):
        from snippets.snippetsloader import SnippetsLoader
        subdir = os.path.join(self._dir_snippets, u'Поддиректория 01')
        os.mkdir(subdir)

        loader = SnippetsLoader([self._dir_snippets])
        snippets = loader.getSnippets()
        self.assertEqual(len(snippets.dirs), 1)

        subdir = snippets.dirs[0]
        self.assertEqual(len(subdir), 0)
        self.assertEqual(subdir.name, u'Поддиректория 01')

    def test_subdir_02(self):
        from snippets.snippetsloader import SnippetsLoader
        subdir_1 = os.path.join(self._dir_snippets, u'Поддиректория 01')
        subdir_2 = os.path.join(self._dir_snippets, u'Поддиректория 02')
        os.mkdir(subdir_1)
        os.mkdir(subdir_2)

        loader = SnippetsLoader([self._dir_snippets])
        snippets = loader.getSnippets()

        self.assertEqual(len(snippets), 2)
        self.assertEqual(len(snippets.dirs), 2)

        self.assertEqual(len(snippets.dirs[0]), 0)
        self.assertEqual(len(snippets.dirs[1]), 0)

    def test_subdir_03(self):
        from snippets.snippetsloader import SnippetsLoader
        subdir_1 = os.path.join(self._dir_snippets, u'Поддиректория 01')
        subdir_2 = os.path.join(subdir_1, u'Поддиректория 02')
        os.mkdir(subdir_1)
        os.mkdir(subdir_2)

        loader = SnippetsLoader([self._dir_snippets])
        snippets = loader.getSnippets()

        self.assertEqual(len(snippets), 1)
        self.assertEqual(len(snippets.dirs), 1)

        self.assertEqual(len(snippets.dirs[0]), 1)
        self.assertEqual(len(snippets.dirs[0].dirs[0]), 0)

    def test_full_01(self):
        from snippets.snippetsloader import SnippetsLoader
        subdir_1 = os.path.join(self._dir_snippets, u'Поддиректория 01')
        subdir_2 = os.path.join(subdir_1, u'Поддиректория 02')
        os.mkdir(subdir_1)
        os.mkdir(subdir_2)

        files = [os.path.join(self._dir_snippets, u'root_01.tpl'),
                 os.path.join(self._dir_snippets, u'root_02.tpl'),
                 os.path.join(subdir_1, u'dir_01_01.tpl'),
                 os.path.join(subdir_1, u'dir_01_02.tpl'),
                 os.path.join(subdir_2, u'dir_02_01.tpl'),
                 os.path.join(subdir_2, u'dir_02_02.tpl'),
                 ]

        map(lambda fname: self._create(fname), files)
        loader = SnippetsLoader([self._dir_snippets])
        snippets = loader.getSnippets()

        self.assertEqual(len(snippets.snippets), 2)
        self.assertEqual(len(snippets.dirs), 1)
        self.assertEqual(len(snippets), 3)

        self.assertEqual(len(snippets.dirs[0].snippets), 2)
        self.assertEqual(len(snippets.dirs[0].dirs), 1)
        self.assertEqual(len(snippets.dirs[0]), 3)

        self.assertEqual(len(snippets.dirs[0].dirs[0].snippets), 2)
        self.assertEqual(len(snippets.dirs[0].dirs[0].dirs), 0)
        self.assertEqual(len(snippets.dirs[0].dirs[0]), 2)
