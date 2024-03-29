# -*- coding: utf-8 -*-

import unittest
import os.path

from outwiker.core.styleslist import StylesList


class StylesListTest (unittest.TestCase):
    def setUp(self):
        self._dirlist = [
            "testdata/styles/example_jblog/",
            "testdata/styles/example_jnet/"
        ]

    def testEmpty(self):
        styleslist = StylesList([])
        self.assertEqual(len(styleslist), 0)

    def testInvalidPath(self):
        styleslist = StylesList(["testdata/styles/invalid_not_exists"])
        self.assertEqual(len(styleslist), 0)

    def testLoad(self):
        styleslist = StylesList(self._dirlist)
        self.assertEqual(len(styleslist), 2)

        style1 = os.path.join(self._dirlist[0], "example_jblog")
        style2 = os.path.join(self._dirlist[1], "example_jnet")

        self.assertEqual(os.path.abspath(style1),
                         os.path.abspath(styleslist[0]))
        self.assertEqual(os.path.abspath(style2),
                         os.path.abspath(styleslist[1]))

    def testIter(self):
        styleslist = StylesList(self._dirlist)
        styles = [style for style in styleslist]
        self.assertEqual(len(styles), 2)
