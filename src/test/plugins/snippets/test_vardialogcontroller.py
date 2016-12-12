# -*- coding: UTF-8 -*-

from tempfile import mkdtemp

from outwiker.core.application import Application
from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.pages.wiki.wikipage import WikiPageFactory
from test.guitests.basemainwnd import BaseMainWndTest
from test.utils import removeDir


class VarDialogControllerTest(BaseMainWndTest):
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
        dirname = u'.'
        self._application.selectedPage = self.testPage

        right_result = u''

        self._controller.ShowDialog(seltext, template, dirname)
        self._controller.FinishDialog()
        result = self._controller.GetResult()

        self.assertEqual(result, right_result)

    def test_simple(self):
        seltext = u''
        template = u'Шаблон'
        dirname = u'.'
        self._application.selectedPage = self.testPage

        right_result = u'Шаблон'

        self._controller.ShowDialog(seltext, template, dirname)
        self._controller.FinishDialog()
        result = self._controller.GetResult()

        self.assertEqual(result, right_result)

    def test_global_var_title(self):
        seltext = u''
        template = u'{{__title}}'
        dirname = u'.'
        self._application.selectedPage = self.testPage

        right_result = u'Страница 1'

        self._controller.ShowDialog(seltext, template, dirname)
        self._controller.FinishDialog()
        result = self._controller.GetResult()

        self.assertEqual(result, right_result)
