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


    def tearDown (self):
        self.loader.clear()


    def testEmpty (self):
        from tableofcontents.tocwikimaker import TocWikiMaker

        text = u''''''
        maker = TocWikiMaker (Application.config)
        result = maker.make (text)

        result_valid = u''''''

        self.assertEqual (result, result_valid)


    def test_01 (self):
        from tableofcontents.tocwikimaker import TocWikiMaker

        text = u'''  !! Абырвалг'''
        maker = TocWikiMaker (Application.config)
        result = maker.make (text)

        result_valid = u''''''

        self.assertEqual (result, result_valid)


    def test_02 (self):
        from tableofcontents.tocwikimaker import TocWikiMaker

        text = u'''!! Абырвалг'''
        maker = TocWikiMaker (Application.config)
        result = maker.make (text)

        result_valid = u'''* Абырвалг'''

        self.assertEqual (result, result_valid)


    def test_03 (self):
        from tableofcontents.tocwikimaker import TocWikiMaker

        text = u'''!!    Абырвалг    '''
        maker = TocWikiMaker (Application.config)
        result = maker.make (text)

        result_valid = u'''* Абырвалг'''

        self.assertEqual (result, result_valid)


    def test_04 (self):
        from tableofcontents.tocwikimaker import TocWikiMaker

        text = u'''!! Абырвалг\\
 123'''

        maker = TocWikiMaker (Application.config)
        result = maker.make (text)

        result_valid = u'''* Абырвалг 123'''

        self.assertEqual (result, result_valid)


    def test_05 (self):
        from tableofcontents.tocwikimaker import TocWikiMaker

        text = u'''!! Абырвалг 123
!!! Абырвалг 234'''

        maker = TocWikiMaker (Application.config)
        result = maker.make (text)

        result_valid = u'''* Абырвалг 123
** Абырвалг 234'''

        self.assertEqual (result, result_valid)


    def test_06 (self):
        from tableofcontents.tocwikimaker import TocWikiMaker

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

        maker = TocWikiMaker (Application.config)
        result = maker.make (text)

        result_valid = u'''* Абырвалг 123
** Абырвалг 234'''

        self.assertEqual (result, result_valid)


    def test_07 (self):
        from tableofcontents.tocwikimaker import TocWikiMaker

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

        maker = TocWikiMaker (Application.config)
        result = maker.make (text)

        result_valid = u'''* [[Абырвалг 123 -> #якорь1]]
** [[Абырвалг 234 -> #якорь2]]'''

        self.assertEqual (result, result_valid)


    def test_08 (self):
        from tableofcontents.tocwikimaker import TocWikiMaker

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

        maker = TocWikiMaker (Application.config)
        result = maker.make (text)

        result_valid = u'''* [[#якорь1 | Абырвалг 123]]
** [[#якорь2 | Абырвалг 234]]'''

        self.assertEqual (result, result_valid)


    def test_09 (self):
        from tableofcontents.tocwikimaker import TocWikiMaker

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

        maker = TocWikiMaker (Application.config)
        result = maker.make (text)

        result_valid = u'''* [[Абырвалг 123 -> #якорь1]]
** [[Абырвалг 234 -> #якорь2]]'''

        self.assertEqual (result, result_valid)


    def test_10 (self):
        from tableofcontents.tocwikimaker import TocWikiMaker

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

        maker = TocWikiMaker (Application.config)
        result = maker.make (text)

        result_valid = u'''* [[#якорь1 | Абырвалг 123]]
** [[#якорь2 | Абырвалг 234]]'''

        self.assertEqual (result, result_valid)


    def test_11 (self):
        from tableofcontents.tocwikimaker import TocWikiMaker

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

        maker = TocWikiMaker (Application.config)
        result = maker.make (text)

        result_valid = u'''* [[#якорь1 | Абырвалг 123]]
** [[#якорь2 | Абырвалг 234]]'''

        self.assertEqual (result, result_valid)
