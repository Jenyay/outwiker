# -*- coding: utf-8 -*-

import unittest

import wx

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.pages.wiki.wikipage import WikiPageFactory
from test.basetestcases import BaseOutWikerGUIMixin


class SnippetsVarDialogControllerTest(unittest.TestCase, BaseOutWikerGUIMixin):
    def setUp(self):
        self.initApplication()
        self.wikiroot = self.createWiki()
        self.testPage = WikiPageFactory().create(self.wikiroot,
                                                 "Страница 1",
                                                 [])
        plugins_dir = ["../plugins/snippets"]
        self.application.wikiroot = self.wikiroot

        self.loader = PluginsLoader(self.application)
        self.loader.load(plugins_dir)

        from snippets.gui.variablesdialog import VariablesDialogController
        self._controller = VariablesDialogController(self.application)

    def tearDown(self):
        self._controller.destroy()
        self.loader.clear()
        self.destroyApplication()
        self.destroyWiki(self.wikiroot)

    def test_empty(self):
        seltext = ''
        template = ''
        template_name = 'template'
        self.application.selectedPage = self.testPage

        right_result = ''

        self._controller.ShowDialog(seltext, template, template_name)
        self._controller.FinishDialog()
        result = self._controller.GetResult()

        self.assertEqual(result, right_result)

    def test_simple(self):
        seltext = ''
        template = 'Шаблон'
        template_name = 'template'
        self.application.selectedPage = self.testPage

        right_result = 'Шаблон'

        self._controller.ShowDialog(seltext, template, template_name)
        self._controller.FinishDialog()
        result = self._controller.GetResult()

        self.assertEqual(result, right_result)

    def test_global_var_title(self):
        seltext = ''
        template = '{{__title}}'
        template_name = 'template'
        self.application.selectedPage = self.testPage

        right_result = 'Страница 1'

        self._controller.ShowDialog(seltext, template, template_name)
        self._controller.FinishDialog()
        result = self._controller.GetResult()

        self.assertEqual(result, right_result)

    def test_global_var_title_alias(self):
        self.testPage.alias = 'Псевдоним'

        seltext = ''
        template = '{{__title}}'
        template_name = 'template'
        self.application.selectedPage = self.testPage

        right_result = 'Псевдоним'

        self._controller.ShowDialog(seltext, template, template_name)
        self._controller.FinishDialog()
        result = self._controller.GetResult()

        self.assertEqual(result, right_result)

    def test_page_none_01(self):
        seltext = ''
        template = 'Шаблон'
        template_name = 'template'
        self.application.selectedPage = None

        right_result = 'Шаблон'

        self._controller.ShowDialog(seltext, template, template_name)
        self._controller.FinishDialog()
        result = self._controller.GetResult()

        self.assertEqual(result, right_result)

    def test_var_01(self):
        seltext = ''
        template = 'Переменная = {{varname}}'
        template_name = 'template'
        self.application.selectedPage = None

        right_result = 'Переменная = Абырвалг'

        self._controller.ShowDialog(seltext, template, template_name)
        self._controller.dialog.setStringVariable('varname', 'Абырвалг')

        # To process EVT_VAR_CHANGE event
        wx.GetApp().Yield()

        self._controller.FinishDialog()
        result = self._controller.GetResult()

        self.assertEqual(result, right_result)

    def test_var_02(self):
        seltext = ''
        template = 'Переменная = {{varname1}} = {{varname2}}'
        template_name = 'template'
        self.application.selectedPage = None

        right_result = 'Переменная = Абырвалг1 = Абырвалг2'

        self._controller.ShowDialog(seltext, template, template_name)

        self._controller.dialog.setStringVariable('varname1', 'Абырвалг1')
        wx.GetApp().Yield()

        self._controller.dialog.setStringVariable('varname2', 'Абырвалг2')
        wx.GetApp().Yield()

        self._controller.FinishDialog()
        result = self._controller.GetResult()

        self.assertEqual(result, right_result)

    def test_wiki_command_01(self):
        seltext = ''
        template = ''
        template_name = 'template'
        self.application.selectedPage = None

        right_result = '(:snip file="template":)(:snipend:)'

        self._controller.ShowDialog(seltext, template, template_name)
        self._controller.dialog.wikiCommandChecked = True
        self._controller.FinishDialog()
        result = self._controller.GetResult()

        self.assertEqual(result, right_result)

    def test_wiki_command_02(self):
        seltext = ''
        template = ''
        template_name = 'template'
        self.application.selectedPage = None

        right_result = '(:snip file="template":)(:snipend:)'

        self._controller.ShowDialog(seltext, template, template_name)
        self._controller.dialog.wikiCommandChecked = True
        self._controller.FinishDialog()
        result = self._controller.GetResult()

        self.assertEqual(result, right_result)

    def test_wiki_command_03(self):
        seltext = ''
        template = ''
        template_name = 'snippets\\template'
        self.application.selectedPage = None

        right_result = '(:snip file="snippets/template":)(:snipend:)'

        self._controller.ShowDialog(seltext, template, template_name)
        self._controller.dialog.wikiCommandChecked = True
        self._controller.FinishDialog()
        result = self._controller.GetResult()

        self.assertEqual(result, right_result)

    def test_wiki_command_04(self):
        seltext = ''
        template = '{{varname}}'
        template_name = 'template'
        self.application.selectedPage = None

        right_result = '(:snip file="template" varname="Абырвалг":)(:snipend:)'

        self._controller.ShowDialog(seltext, template, template_name)
        self._controller.dialog.wikiCommandChecked = True

        self._controller.dialog.setStringVariable('varname', 'Абырвалг')
        wx.GetApp().Yield()

        self._controller.FinishDialog()
        result = self._controller.GetResult()

        self.assertEqual(result, right_result)

    def test_wiki_command_05(self):
        seltext = ''
        template = '{{aaa}} {{ccc}} {{x}} {{a}}'
        template_name = 'template'
        self.application.selectedPage = None

        right_result = '(:snip file="template" a="aaaaa" aaa="aaaaa" ccc="ccccc" x="xxxxx":)(:snipend:)'

        self._controller.ShowDialog(seltext, template, template_name)
        self._controller.dialog.wikiCommandChecked = True

        self._controller.dialog.setStringVariable('aaa', 'aaaaa')
        self._controller.dialog.setStringVariable('ccc', 'ccccc')
        self._controller.dialog.setStringVariable('x', 'xxxxx')
        self._controller.dialog.setStringVariable('a', 'aaaaa')
        wx.GetApp().Yield()

        self._controller.FinishDialog()
        result = self._controller.GetResult()

        self.assertEqual(result, right_result)
