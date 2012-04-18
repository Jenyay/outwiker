#!/usr/bin/env python
#-*- coding: utf-8 -*-

import unittest
import os.path

from outwiker.core.styleslist import StylesList


class StylesListTest (unittest.TestCase):
    def setUp (self):
        self._dirlist = [
                u"../test/styles/example_jblog/",
                u"../test/styles/example_jnet/"
                ]
    
        
    def testEmpty (self):
        styleslist = StylesList ([])
        self.assertEqual (len (styleslist), 0)


    def testInvalidPath (self):
        styleslist = StylesList ([u"../test/styles/invalid_not_exists"])
        self.assertEqual (len (styleslist), 0)


    def testLoad (self):
        styleslist = StylesList (self._dirlist)
        self.assertEqual (len (styleslist), 2)

        style1 = os.path.join (self._dirlist[0], u"example_jblog")
        style2 = os.path.join (self._dirlist[1], u"example_jnet")

        self.assertEqual (os.path.abspath (style1), os.path.abspath (styleslist[0]))
        self.assertEqual (os.path.abspath (style2), os.path.abspath (styleslist[1]))
