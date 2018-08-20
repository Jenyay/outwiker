# -*- coding: utf-8 -*-

import os
import unittest
from tempfile import mkdtemp

from test.utils import removeDir

from outwiker.core.tree import WikiDocument
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.wikistyleutils import (getCustomStylesNames,
                                                loadCustomStyles,
                                                loadCustomStylesFromConfig,
                                                saveCustomStylesToConfig)
from outwiker.utilites.textfile import writeTextFile


class WikiStyleUtilsTest(unittest.TestCase):
    def setUp(self):
        self._tmp_dirs = []

        self.path = mkdtemp(prefix='WikiStyleUtilsTest_')
        self.wikiroot = WikiDocument.create(self.path)
        self.testPage = WikiPageFactory().create(self.wikiroot, "Страница", [])

    def tearDown(self):
        removeDir(self.path)
        for dirname in self._tmp_dirs:
            removeDir(dirname)

    def test_getCustomStylesNames_empty(self):
        styles = getCustomStylesNames(self._tmp_dirs)
        self.assertEqual(styles, [])

    def test_getCustomStylesNames_empty_dirs(self):
        for n in range(5):
            dirname = mkdtemp()
            self._tmp_dirs.append(dirname)

        styles = getCustomStylesNames(self._tmp_dirs)
        self.assertEqual(styles, [])

    def test_getCustomStylesNames_single_dir(self):
        dirname = mkdtemp()
        self._tmp_dirs.append(dirname)

        writeTextFile(os.path.join(dirname, 'style-1.css'), '')
        writeTextFile(os.path.join(dirname, 'style-2.css'), '')
        writeTextFile(os.path.join(dirname, 'style-3.css'), '')

        styles = sorted(getCustomStylesNames(self._tmp_dirs))
        self.assertEqual(styles, ['style-1', 'style-2', 'style-3'])

    def test_getCustomStylesNames_more_dirs(self):
        dirname_1 = mkdtemp()
        dirname_2 = mkdtemp()
        self._tmp_dirs.append(dirname_1)
        self._tmp_dirs.append(dirname_2)

        writeTextFile(os.path.join(dirname_1, 'style-1.css'), '')
        writeTextFile(os.path.join(dirname_1, 'style-2.css'), '')
        writeTextFile(os.path.join(dirname_1, 'style-3.css'), '')

        writeTextFile(os.path.join(dirname_2, 'style-4.css'), '')
        writeTextFile(os.path.join(dirname_2, 'style-5.css'), '')

        styles = sorted(getCustomStylesNames(self._tmp_dirs))
        self.assertEqual(styles, ['style-1', 'style-2', 'style-3',
                                  'style-4', 'style-5'])

    def test_getCustomStylesNames_more_dirs_repeat_names(self):
        dirname_1 = mkdtemp()
        dirname_2 = mkdtemp()
        self._tmp_dirs.append(dirname_1)
        self._tmp_dirs.append(dirname_2)

        writeTextFile(os.path.join(dirname_1, 'style-1.css'), '')
        writeTextFile(os.path.join(dirname_1, 'style-2.css'), '')
        writeTextFile(os.path.join(dirname_1, 'style-3.css'), '')

        writeTextFile(os.path.join(dirname_2, 'style-1.css'), '')
        writeTextFile(os.path.join(dirname_2, 'style-5.css'), '')

        styles = sorted(getCustomStylesNames(self._tmp_dirs))
        self.assertEqual(styles, ['style-1', 'style-2', 'style-3', 'style-5'])

    def test_loadCustomStyles_empty(self):
        styles = loadCustomStyles(self._tmp_dirs)
        self.assertEqual(styles, {})

    def test_loadCustomStyles_empty_dirs(self):
        for n in range(5):
            dirname = mkdtemp()
            self._tmp_dirs.append(dirname)

        styles = loadCustomStyles(self._tmp_dirs)
        self.assertEqual(styles, {})

    def test_loadCustomStyles_single_dir(self):
        dirname = mkdtemp()
        self._tmp_dirs.append(dirname)

        writeTextFile(os.path.join(dirname, 'style-1.css'), 'test-1')
        writeTextFile(os.path.join(dirname, 'style-2.css'), 'test-2')
        writeTextFile(os.path.join(dirname, 'style-3.css'), 'test-3')

        styles = loadCustomStyles(self._tmp_dirs)
        self.assertEqual(styles, {'style-1': 'test-1',
                                  'style-2': 'test-2',
                                  'style-3': 'test-3',
                                  })

    def test_loadCustomStyles_more_dirs(self):
        dirname_1 = mkdtemp()
        dirname_2 = mkdtemp()
        self._tmp_dirs.append(dirname_1)
        self._tmp_dirs.append(dirname_2)

        writeTextFile(os.path.join(dirname_1, 'style-1.css'), 'test-1')
        writeTextFile(os.path.join(dirname_1, 'style-2.css'), 'test-2')
        writeTextFile(os.path.join(dirname_1, 'style-3.css'), 'test-3')

        writeTextFile(os.path.join(dirname_2, 'style-4.css'), 'test-4')
        writeTextFile(os.path.join(dirname_2, 'style-5.css'), 'test-5')

        styles = loadCustomStyles(self._tmp_dirs)
        self.assertEqual(styles, {'style-1': 'test-1',
                                  'style-2': 'test-2',
                                  'style-3': 'test-3',
                                  'style-4': 'test-4',
                                  'style-5': 'test-5',
                                  })

    def test_loadCustomStyles_more_dirs_repeat_names(self):
        dirname_1 = mkdtemp()
        dirname_2 = mkdtemp()
        self._tmp_dirs.append(dirname_1)
        self._tmp_dirs.append(dirname_2)

        writeTextFile(os.path.join(dirname_1, 'style-1.css'), 'test-1')
        writeTextFile(os.path.join(dirname_1, 'style-2.css'), 'test-2')
        writeTextFile(os.path.join(dirname_1, 'style-3.css'), 'test-3')

        writeTextFile(os.path.join(dirname_2, 'style-1.css'), 'test-1-new')
        writeTextFile(os.path.join(dirname_2, 'style-5.css'), 'test-5')

        styles = loadCustomStyles(self._tmp_dirs)
        self.assertEqual(styles, {'style-1': 'test-1-new',
                                  'style-2': 'test-2',
                                  'style-3': 'test-3',
                                  'style-5': 'test-5',
                                  })

    def test_load_styles_from_config_01(self):
        styles = {'text': 'test: div.test {}'}
        section_name = 'wiki'
        option_name = 'styles'

        saveCustomStylesToConfig(self.testPage.params,
                                 section_name,
                                 option_name,
                                 styles)

        loaded_styles = loadCustomStylesFromConfig(self.testPage.params,
                                                   section_name,
                                                   option_name)

        self.assertEqual(loaded_styles, styles)

    def test_load_styles_from_config_02_invalid(self):
        section_name = 'wiki'
        option_name = 'styles'

        styles = None
        saveCustomStylesToConfig(self.testPage.params,
                                 section_name,
                                 option_name,
                                 styles)

        loaded_styles = loadCustomStylesFromConfig(self.testPage.params,
                                                   section_name,
                                                   option_name)

        self.assertEqual(loaded_styles, {})

    def test_load_styles_from_config_03_empty(self):
        section_name = 'wiki'
        option_name = 'styles'

        styles = {}
        saveCustomStylesToConfig(self.testPage.params,
                                 section_name,
                                 option_name,
                                 styles)

        loaded_styles = loadCustomStylesFromConfig(self.testPage.params,
                                                   section_name,
                                                   option_name)

        self.assertEqual(loaded_styles, {})
