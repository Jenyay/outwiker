# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application
from outwiker.pages.wiki.wikiconfig import WikiConfig


class TOC_WikiMakerTest (unittest.TestCase):
    """Тесты плагина TableOfContents"""
    def setUp (self):
        dirlist = [u"../plugins/tableofcontents"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)
        self.plugin = self.loader[u"TableOfContents"]


    def tearDown (self):
        self.loader.clear()


    def testEmpty (self):
        text = u''''''
        maker = self.plugin.TocWikiMaker (Application.config)
        result = maker.make (text)

        result_valid = u''''''

        self.assertEqual (result, result_valid)


    def test_01 (self):
        text = u'''  !! Абырвалг'''
        maker = self.plugin.TocWikiMaker (Application.config)
        result = maker.make (text)

        result_valid = u''''''

        self.assertEqual (result, result_valid)


    def test_02 (self):
        text = u'''!! Абырвалг'''
        maker = self.plugin.TocWikiMaker (Application.config)
        result = maker.make (text)

        result_valid = u'''* Абырвалг'''

        self.assertEqual (result, result_valid)


    def test_03 (self):
        text = u'''!!    Абырвалг    '''
        maker = self.plugin.TocWikiMaker (Application.config)
        result = maker.make (text)

        result_valid = u'''* Абырвалг'''

        self.assertEqual (result, result_valid)


    def test_04 (self):
        text = u'''!! Абырвалг\\
 123'''

        maker = self.plugin.TocWikiMaker (Application.config)
        result = maker.make (text)

        result_valid = u'''* Абырвалг 123'''

        self.assertEqual (result, result_valid)


    def test_05 (self):
        text = u'''!! Абырвалг 123
!!! Абырвалг 234'''

        maker = self.plugin.TocWikiMaker (Application.config)
        result = maker.make (text)

        result_valid = u'''* Абырвалг 123
** Абырвалг 234'''

        self.assertEqual (result, result_valid)


    def test_06 (self):
        text = u'''ывп ыфвп ваы

[=
ывп ывап ыва
=]

!! Абырвалг 123

[=
!! Это не заголовок
=]

ывапыва ывп выап
выапывп ываап ывап

!!! Абырвалг 234'''

        maker = self.plugin.TocWikiMaker (Application.config)
        result = maker.make (text)

        result_valid = u'''* Абырвалг 123
** Абырвалг 234'''

        self.assertEqual (result, result_valid)


    def test_07 (self):
        WikiConfig (Application.config).linkStyleOptions.value = 0
        text = u'''ывп ыфвп ваы

[=
ывп ывап ыва
=]

!! [[#якорь1]]  Абырвалг 123

[=
!! Это не заголовок
=]

ывапыва ывп выап
выапывп ываап ывап

[[#якорь2]]
!!! Абырвалг 234'''

        maker = self.plugin.TocWikiMaker (Application.config)
        result = maker.make (text)

        result_valid = u'''* [[Абырвалг 123 -> #якорь1]]
** [[Абырвалг 234 -> #якорь2]]'''

        self.assertEqual (result, result_valid)


    def test_08 (self):
        WikiConfig (Application.config).linkStyleOptions.value = 1
        text = u'''ывп ыфвп ваы

[=
ывп ывап ыва
=]

!! [[#якорь1]]  Абырвалг 123

[=
!! Это не заголовок
=]

ывапыва ывп выап
выапывп ываап ывап

[[#якорь2]]
!!! Абырвалг 234'''

        maker = self.plugin.TocWikiMaker (Application.config)
        result = maker.make (text)

        result_valid = u'''* [[#якорь1 | Абырвалг 123]]
** [[#якорь2 | Абырвалг 234]]'''

        self.assertEqual (result, result_valid)


    def test_09 (self):
        WikiConfig (Application.config).linkStyleOptions.value = 0
        text = u'''ывп ыфвп ваы

[=
ывп ывап ыва
=]

!! Абырвалг 123 [[#якорь1]]

[=
!! Это не заголовок
=]

ывапыва ывп выап
выапывп ываап ывап

[[#якорь2]]
!!! Абырвалг 234'''

        maker = self.plugin.TocWikiMaker (Application.config)
        result = maker.make (text)

        result_valid = u'''* [[Абырвалг 123 -> #якорь1]]
** [[Абырвалг 234 -> #якорь2]]'''

        self.assertEqual (result, result_valid)


    def test_10 (self):
        WikiConfig (Application.config).linkStyleOptions.value = 1
        text = u'''ывп ыфвп ваы

[=
ывп ывап ыва
=]

!! Абырвалг 123 [[#якорь1]]

[=
!! Это не заголовок
=]

ывапыва ывп выап
выапывп ываап ывап

[[#якорь2]]
!!! Абырвалг 234'''

        maker = self.plugin.TocWikiMaker (Application.config)
        result = maker.make (text)

        result_valid = u'''* [[#якорь1 | Абырвалг 123]]
** [[#якорь2 | Абырвалг 234]]'''

        self.assertEqual (result, result_valid)


    def test_11 (self):
        WikiConfig (Application.config).linkStyleOptions.value = 1
        text = u'''ывп ыфвп ваы

[=
ывп ывап ыва
=]

!!!! Абырвалг 123 [[#якорь1]]

[=
!! Это не заголовок
=]

ывапыва ывп выап
выапывп ываап ывап

[[#якорь2]]
!!!!! Абырвалг 234'''

        maker = self.plugin.TocWikiMaker (Application.config)
        result = maker.make (text)

        result_valid = u'''* [[#якорь1 | Абырвалг 123]]
** [[#якорь2 | Абырвалг 234]]'''

        self.assertEqual (result, result_valid)
