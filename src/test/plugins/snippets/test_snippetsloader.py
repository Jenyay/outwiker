# -*- coding: utf-8 -*-

from tempfile import mkdtemp
import os
import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application
from test.utils import removeDir
from test.basetestcases import BaseOutWikerGUIMixin


class SnippetsLoaderTest(unittest.TestCase, BaseOutWikerGUIMixin):
    def setUp(self):
        self.initApplication()
        dirlist = ["../plugins/snippets"]

        self.loader = PluginsLoader(Application)
        self.loader.load(dirlist)
        self._dir_snippets = mkdtemp('outwiker_snippets')

    def tearDown(self):
        self.loader.clear()
        removeDir(self._dir_snippets)
        self.destroyApplication()

    def _create(self, fname):
        with open(fname, 'w'):
            pass

    def test_empty_01(self):
        from snippets.snippetsloader import SnippetsLoader
        loader = SnippetsLoader(self._dir_snippets)
        snippets = loader.getSnippets()

        self.assertEqual(snippets.name, os.path.basename(self._dir_snippets))
        self.assertEqual(len(snippets), 0)
        self.assertEqual(snippets.dirs, [])
        self.assertEqual(snippets.snippets, [])

    def test_empty_02_invalid(self):
        from snippets.snippetsloader import SnippetsLoader
        loader = SnippetsLoader('Invalid dir')
        snippets = loader.getSnippets()

        self.assertEqual(snippets.name, 'Invalid dir')
        self.assertEqual(len(snippets), 0)
        self.assertEqual(snippets.dirs, [])
        self.assertEqual(snippets.snippets, [])

    def test_snippets_01(self):
        from snippets.snippetsloader import SnippetsLoader
        files = ['Шаблон']
        for fname in files:
            self._create(os.path.join(self._dir_snippets, fname))

        loader = SnippetsLoader(self._dir_snippets)
        snippets = loader.getSnippets()
        self.assertEqual(snippets.dirs, [])
        self.assertEqual(snippets.snippets,
                         [os.path.join(self._dir_snippets, 'Шаблон')])
        self.assertEqual(len(snippets), 1)

    def test_snippets_02(self):
        from snippets.snippetsloader import SnippetsLoader
        files = ['Шаблон 01', 'Шаблон 02', 'Шаблон 03.txt']
        for fname in files:
            self._create(os.path.join(self._dir_snippets, fname))

        loader = SnippetsLoader(self._dir_snippets)
        snippets = loader.getSnippets()
        self.assertEqual(snippets.dirs, [])

        self.assertIn(
            os.path.join(self._dir_snippets, 'Шаблон 01'),
            snippets.snippets)

        self.assertIn(
            os.path.join(self._dir_snippets, 'Шаблон 02'),
            snippets.snippets)

        self.assertIn(
            os.path.join(self._dir_snippets, 'Шаблон 03.txt'),
            snippets.snippets)

        self.assertEqual(len(snippets), 3)

    def test_subdir_01(self):
        from snippets.snippetsloader import SnippetsLoader
        subdir = os.path.join(self._dir_snippets, 'Поддиректория 01')
        os.mkdir(subdir)

        loader = SnippetsLoader(self._dir_snippets)
        snippets = loader.getSnippets()
        self.assertEqual(len(snippets.dirs), 1)

        subdir = snippets.dirs[0]
        self.assertEqual(len(subdir), 0)
        self.assertEqual(subdir.name, 'Поддиректория 01')

    def test_subdir_02(self):
        from snippets.snippetsloader import SnippetsLoader
        subdir_1 = os.path.join(self._dir_snippets, 'Поддиректория 01')
        subdir_2 = os.path.join(self._dir_snippets, 'Поддиректория 02')
        os.mkdir(subdir_1)
        os.mkdir(subdir_2)

        loader = SnippetsLoader(self._dir_snippets)
        snippets = loader.getSnippets()

        self.assertEqual(len(snippets), 2)
        self.assertEqual(len(snippets.dirs), 2)

        self.assertEqual(len(snippets.dirs[0]), 0)
        self.assertEqual(len(snippets.dirs[1]), 0)

    def test_subdir_03(self):
        from snippets.snippetsloader import SnippetsLoader
        subdir_1 = os.path.join(self._dir_snippets, 'Поддиректория 01')
        subdir_2 = os.path.join(subdir_1, 'Поддиректория 02')
        os.mkdir(subdir_1)
        os.mkdir(subdir_2)

        loader = SnippetsLoader(self._dir_snippets)
        snippets = loader.getSnippets()

        self.assertEqual(len(snippets), 1)
        self.assertEqual(len(snippets.dirs), 1)

        self.assertEqual(len(snippets.dirs[0]), 1)
        self.assertEqual(len(snippets.dirs[0].dirs[0]), 0)

    def test_full_01(self):
        from snippets.snippetsloader import SnippetsLoader
        subdir_1 = os.path.join(self._dir_snippets, 'Поддиректория 01')
        subdir_2 = os.path.join(subdir_1, 'Поддиректория 02')
        os.mkdir(subdir_1)
        os.mkdir(subdir_2)

        files = [os.path.join(self._dir_snippets, 'root_01'),
                 os.path.join(self._dir_snippets, 'root_02'),
                 os.path.join(subdir_1, 'dir_01_01'),
                 os.path.join(subdir_1, 'dir_01_02'),
                 os.path.join(subdir_2, 'dir_02_01'),
                 os.path.join(subdir_2, 'dir_02_02'),
                 ]

        list([self._create(fname) for fname in files])
        loader = SnippetsLoader(self._dir_snippets)
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
