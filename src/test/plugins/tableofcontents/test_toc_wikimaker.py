# -*- coding: utf-8 -*-

import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.pages.wiki.wikiconfig import WikiConfig
from test.basetestcases import BaseOutWikerGUIMixin


class TOC_WikiMakerTest (unittest.TestCase, BaseOutWikerGUIMixin):
    """Тесты плагина TableOfContents"""

    def setUp(self):
        self.initApplication()

        dirlist = ["../plugins/tableofcontents"]

        self.loader = PluginsLoader(self.application)
        self.loader.load(dirlist)

    def tearDown(self):
        self.loader.clear()
        self.destroyApplication()

    def testEmpty(self):
        from tableofcontents.tocwikimaker import TocWikiMaker

        text = ''''''
        maker = TocWikiMaker(self.application.config)
        result = maker.make(text)

        result_valid = ''''''

        self.assertEqual(result, result_valid)

    def test_01(self):
        from tableofcontents.tocwikimaker import TocWikiMaker

        text = '''  !! Абырвалг'''
        maker = TocWikiMaker(self.application.config)
        result = maker.make(text)

        result_valid = ''''''

        self.assertEqual(result, result_valid)

    def test_02(self):
        from tableofcontents.tocwikimaker import TocWikiMaker

        text = '''!! Абырвалг'''
        maker = TocWikiMaker(self.application.config)
        result = maker.make(text)

        result_valid = '''* Абырвалг'''

        self.assertEqual(result, result_valid)

    def test_03(self):
        from tableofcontents.tocwikimaker import TocWikiMaker

        text = '''!!    Абырвалг    '''
        maker = TocWikiMaker(self.application.config)
        result = maker.make(text)

        result_valid = '''* Абырвалг'''

        self.assertEqual(result, result_valid)

    def test_04(self):
        from tableofcontents.tocwikimaker import TocWikiMaker

        text = '''!! Абырвалг\\
 123'''

        maker = TocWikiMaker(self.application.config)
        result = maker.make(text)

        result_valid = '''* Абырвалг 123'''

        self.assertEqual(result, result_valid)

    def test_05(self):
        from tableofcontents.tocwikimaker import TocWikiMaker

        text = '''!! Абырвалг 123
!!! Абырвалг 234'''

        maker = TocWikiMaker(self.application.config)
        result = maker.make(text)

        result_valid = '''* Абырвалг 123
** Абырвалг 234'''

        self.assertEqual(result, result_valid)

    def test_06(self):
        from tableofcontents.tocwikimaker import TocWikiMaker

        text = '''ывп ыфвп ваы

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

        maker = TocWikiMaker(self.application.config)
        result = maker.make(text)

        result_valid = '''* Абырвалг 123
** Абырвалг 234'''

        self.assertEqual(result, result_valid)

    def test_07(self):
        from tableofcontents.tocwikimaker import TocWikiMaker

        WikiConfig(self.application.config).linkStyleOptions.value = 0
        text = '''ывп ыфвп ваы

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

        maker = TocWikiMaker(self.application.config)
        result = maker.make(text)

        result_valid = '''* [[Абырвалг 123 -> #якорь1]]
** [[Абырвалг 234 -> #якорь2]]'''

        self.assertEqual(result, result_valid)

    def test_08(self):
        from tableofcontents.tocwikimaker import TocWikiMaker

        WikiConfig(self.application.config).linkStyleOptions.value = 1
        text = '''ывп ыфвп ваы

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

        maker = TocWikiMaker(self.application.config)
        result = maker.make(text)

        result_valid = '''* [[#якорь1 | Абырвалг 123]]
** [[#якорь2 | Абырвалг 234]]'''

        self.assertEqual(result, result_valid)

    def test_09(self):
        from tableofcontents.tocwikimaker import TocWikiMaker

        WikiConfig(self.application.config).linkStyleOptions.value = 0
        text = '''ывп ыфвп ваы

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

        maker = TocWikiMaker(self.application.config)
        result = maker.make(text)

        result_valid = '''* [[Абырвалг 123 -> #якорь1]]
** [[Абырвалг 234 -> #якорь2]]'''

        self.assertEqual(result, result_valid)

    def test_10(self):
        from tableofcontents.tocwikimaker import TocWikiMaker

        WikiConfig(self.application.config).linkStyleOptions.value = 1
        text = '''ывп ыфвп ваы

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

        maker = TocWikiMaker(self.application.config)
        result = maker.make(text)

        result_valid = '''* [[#якорь1 | Абырвалг 123]]
** [[#якорь2 | Абырвалг 234]]'''

        self.assertEqual(result, result_valid)

    def test_11(self):
        from tableofcontents.tocwikimaker import TocWikiMaker

        WikiConfig(self.application.config).linkStyleOptions.value = 1
        text = '''ывп ыфвп ваы

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

        maker = TocWikiMaker(self.application.config)
        result = maker.make(text)

        result_valid = '''* [[#якорь1 | Абырвалг 123]]
** [[#якорь2 | Абырвалг 234]]'''

        self.assertEqual(result, result_valid)
