# -*- coding: UTF-8 -*-

from tempfile import mkdtemp

import wx

from outwiker.core.application import Application
from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.pages.wiki.wikipage import WikiPageFactory
from test.guitests.basemainwnd import BaseMainWndTest
from test.utils import removeDir


class SnippetsVarDialogControllerTest(BaseMainWndTest):
    def setUp(self):
        BaseMainWndTest.setUp(self)
        plugins_dir = [u"../plugins/snippets"]
        self._createWiki()
        self._application = Application
        self._createWiki()
        self._application.wikiroot = self.wikiroot

        self.loader = PluginsLoader(Application)
        self.loader.load(plugins_dir)

        from snippets.gui.variablesdialog import VariablesDialogController
        self._controller = VariablesDialogController(self._application)

    def tearDown(self):
        self._controller.destroy()
        BaseMainWndTest.tearDown(self)
        removeDir(self.path)
        self.loader.clear()

    def _createWiki(self):
        self.path = mkdtemp(prefix=u'Абырвалг абыр')

        self.wikiroot = WikiDocument.create(self.path)

        WikiPageFactory().create(self.wikiroot, u"Страница 1", [])
        self.testPage = self.wikiroot[u"Страница 1"]

    def test_empty(self):
        seltext = u''
        template = u''
        template_name = u'template'
        self._application.selectedPage = self.testPage

        right_result = u''

        self._controller.ShowDialog(seltext, template, template_name)
        self._controller.FinishDialog()
        result = self._controller.GetResult()

        self.assertEqual(result, right_result)

    def test_simple(self):
        seltext = u''
        template = u'Шаблон'
        template_name = u'template'
        self._application.selectedPage = self.testPage

        right_result = u'Шаблон'

        self._controller.ShowDialog(seltext, template, template_name)
        self._controller.FinishDialog()
        result = self._controller.GetResult()

        self.assertEqual(result, right_result)

    def test_global_var_title(self):
        seltext = u''
        template = u'{{__title}}'
        template_name = u'template'
        self._application.selectedPage = self.testPage

        right_result = u'Страница 1'

        self._controller.ShowDialog(seltext, template, template_name)
        self._controller.FinishDialog()
        result = self._controller.GetResult()

        self.assertEqual(result, right_result)

    def test_global_var_title_alias(self):
        self.testPage.alias = u'Псевдоним'

        seltext = u''
        template = u'{{__title}}'
        template_name = u'template'
        self._application.selectedPage = self.testPage

        right_result = u'Псевдоним'

        self._controller.ShowDialog(seltext, template, template_name)
        self._controller.FinishDialog()
        result = self._controller.GetResult()

        self.assertEqual(result, right_result)

    def test_page_none_01(self):
        seltext = u''
        template = u'Шаблон'
        template_name = u'template'
        self._application.selectedPage = None

        right_result = u'Шаблон'

        self._controller.ShowDialog(seltext, template, template_name)
        self._controller.FinishDialog()
        result = self._controller.GetResult()

        self.assertEqual(result, right_result)

    def test_var_01(self):
        seltext = u''
        template = u'Переменная = {{varname}}'
        template_name = u'template'
        self._application.selectedPage = None

        right_result = u'Переменная = Абырвалг'

        self._controller.ShowDialog(seltext, template, template_name)
        self._controller.dialog.setStringVariable(u'varname', u'Абырвалг')

        # To process EVT_VAR_CHANGE event
        wx.GetApp().Yield()

        self._controller.FinishDialog()
        result = self._controller.GetResult()

        self.assertEqual(result, right_result)

    def test_var_02(self):
        seltext = u''
        template = u'Переменная = {{varname1}} = {{varname2}}'
        template_name = u'template'
        self._application.selectedPage = None

        right_result = u'Переменная = Абырвалг1 = Абырвалг2'

        self._controller.ShowDialog(seltext, template, template_name)

        self._controller.dialog.setStringVariable(u'varname1', u'Абырвалг1')
        wx.GetApp().Yield()

        self._controller.dialog.setStringVariable(u'varname2', u'Абырвалг2')
        wx.GetApp().Yield()

        self._controller.FinishDialog()
        result = self._controller.GetResult()

        self.assertEqual(result, right_result)

    def test_wiki_command_01(self):
        seltext = u''
        template = u''
        template_name = u'template'
        self._application.selectedPage = None

        right_result = u'(:snip file="template":)(:snipend:)'

        self._controller.ShowDialog(seltext, template, template_name)
        self._controller.dialog.wikiCommandChecked = True
        self._controller.FinishDialog()
        result = self._controller.GetResult()

        self.assertEqual(result, right_result)

    def test_wiki_command_02(self):
        seltext = u''
        template = u''
        template_name = u'template'
        self._application.selectedPage = None

        right_result = u'(:snip file="template":)(:snipend:)'

        self._controller.ShowDialog(seltext, template, template_name)
        self._controller.dialog.wikiCommandChecked = True
        self._controller.FinishDialog()
        result = self._controller.GetResult()

        self.assertEqual(result, right_result)

    def test_wiki_command_03(self):
        seltext = u''
        template = u''
        template_name = u'snippets\\template'
        self._application.selectedPage = None

        right_result = u'(:snip file="snippets/template":)(:snipend:)'

        self._controller.ShowDialog(seltext, template, template_name)
        self._controller.dialog.wikiCommandChecked = True
        self._controller.FinishDialog()
        result = self._controller.GetResult()

        self.assertEqual(result, right_result)

    def test_wiki_command_04(self):
        seltext = u''
        template = u'{{varname}}'
        template_name = u'template'
        self._application.selectedPage = None

        right_result = u'(:snip file="template" varname="Абырвалг":)(:snipend:)'

        self._controller.ShowDialog(seltext, template, template_name)
        self._controller.dialog.wikiCommandChecked = True

        self._controller.dialog.setStringVariable(u'varname', u'Абырвалг')
        wx.GetApp().Yield()

        self._controller.FinishDialog()
        result = self._controller.GetResult()

        self.assertEqual(result, right_result)

    def test_wiki_command_05(self):
        seltext = u''
        template = u'{{aaa}} {{ccc}} {{x}} {{a}}'
        template_name = u'template'
        self._application.selectedPage = None

        right_result = u'(:snip file="template" a="aaaaa" aaa="aaaaa" ccc="ccccc" x="xxxxx":)(:snipend:)'

        self._controller.ShowDialog(seltext, template, template_name)
        self._controller.dialog.wikiCommandChecked = True

        self._controller.dialog.setStringVariable(u'aaa', u'aaaaa')
        self._controller.dialog.setStringVariable(u'ccc', u'ccccc')
        self._controller.dialog.setStringVariable(u'x', u'xxxxx')
        self._controller.dialog.setStringVariable(u'a', u'aaaaa')
        wx.GetApp().Yield()

        self._controller.FinishDialog()
        result = self._controller.GetResult()

        self.assertEqual(result, right_result)
