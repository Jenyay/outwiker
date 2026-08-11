# -*- coding: utf-8 -*-

import os
import os.path
from tempfile import mkdtemp
from unittest import TestCase

from outwiker.api.core.tree import createNotesTree
from outwiker.core.attachment import Attachment
from outwiker.core.style import Style
from outwiker.core.defines import PAGE_RESULT_HTML
from outwiker.gui.guiconfig import HtmlRenderConfig
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.htmlcache import HtmlCache
from outwiker.pages.wiki.emptycontent import EmptyContent
from outwiker.pages.wiki.wikiconfig import WikiConfig
from outwiker.tests.utils import removeDir
from outwiker.tests.basetestcases import BaseOutWikerMixin


class WikiHtmlCacheTest(BaseOutWikerMixin, TestCase):
    def setUp(self):
        self.initApplication()
        self.filesPath = "testdata/samplefiles/"
        self.__createWiki()

        files = ["image.jpg", "dir"]

        fullFilesPath = [os.path.join(self.filesPath, fname) for fname in files]

        self.attach_page2 = Attachment(self.wikiroot["Страница 2"])

        # Attach files to two pages
        Attachment(self.testPage).attach(fullFilesPath)

        self.wikitext = """Бла-бла-бла
        %thumb maxsize=250%Attach:image.jpg%%
        Бла-бла-бла"""

        self.testPage.content = self.wikitext

        self.__setDefaultConfig()

        self.resultPath = os.path.join(self.testPage.path, PAGE_RESULT_HTML)

    def __setDefaultConfig(self):
        # Set thumbnail size that differs from the default size
        self.application.config.set(
            WikiConfig.WIKI_SECTION,
            WikiConfig.THUMB_SIZE_PARAM,
            WikiConfig.THUMB_SIZE_DEFAULT,
        )

        self.application.config.set(
            HtmlRenderConfig.HTML_SECTION,
            HtmlRenderConfig.FONT_FACE_NAME_PARAM,
            HtmlRenderConfig.FONT_NAME_DEFAULT,
        )

    def __createWiki(self):
        # Wiki will be created here
        self.path = mkdtemp(prefix="Абырвалг абыр")

        self.wikiroot = createNotesTree(self.path)

        WikiPageFactory().create(self.wikiroot, "Страница 2", [])
        self.testPage = self.wikiroot["Страница 2"]

    def tearDown(self):
        self.destroyApplication()
        removeDir(self.path)

    def testCache1(self):
        # Just created the page, cannot cache
        cache = HtmlCache(self.testPage, self.application)
        self.assertFalse(cache.canReadFromCache())

        # After generating the page once, if nothing changed, can cache
        cache.saveHash()
        self.assertTrue(cache.canReadFromCache())


        self.testPage.content = "бла-бла-бла"

        # Changed page content, cannot cache again
        self.assertFalse(cache.canReadFromCache())

        cache.saveHash()

        self.assertTrue(cache.canReadFromCache())

        # Add a file
        attach = Attachment(self.testPage)
        attach.attach([os.path.join(self.filesPath, "add.png")])

        self.assertFalse(cache.canReadFromCache())
        cache.saveHash()

        self.assertTrue(cache.canReadFromCache())

    def testCacheRename(self):
        # Just created the page, cannot cache
        cache = HtmlCache(self.testPage, self.application)
        self.assertFalse(cache.canReadFromCache())

        cache.saveHash()

        # After generating the page once, if nothing changed, can cache
        self.assertTrue(cache.canReadFromCache())

        self.testPage.content = "бла-бла-бла"

        # Changed page content, cannot cache again
        self.assertFalse(cache.canReadFromCache())
        cache.saveHash()

        self.assertTrue(cache.canReadFromCache())

        # Changed the title
        self.testPage.title = "Новый заголовок"

        self.assertFalse(cache.canReadFromCache())
        cache.saveHash()

        self.assertTrue(cache.canReadFromCache())

    def testCacheEmpty(self):
        emptycontent = EmptyContent(self.application.config)
        self.testPage.content = ""

        # Just created the page, cannot cache
        cache = HtmlCache(self.testPage, self.application)

        self.assertFalse(cache.canReadFromCache())
        cache.saveHash()

        # Page is empty, the template for empty content changed
        emptycontent.content = "1111"
        self.assertFalse(cache.canReadFromCache())

        cache.saveHash()

        # Page content changed
        self.testPage.content = "Бла-бла-бла"
        self.assertFalse(cache.canReadFromCache())

        cache.saveHash()

        self.assertTrue(cache.canReadFromCache())
        cache.saveHash()

        # Page template changed, but the page is no longer empty
        emptycontent.content = "2222"
        self.assertTrue(cache.canReadFromCache())

    def testCacheSubdir(self):
        attach = Attachment(self.testPage)

        # Just created the page, cannot cache
        cache = HtmlCache(self.testPage, self.application)
        self.assertFalse(cache.canReadFromCache())

        cache.saveHash()

        # After generating the page once, if nothing changed, can cache
        self.assertTrue(cache.canReadFromCache())

        # Add a file to dir
        with open(os.path.join(attach.getAttachPath(), "dir", "temp.tmp"), "w") as fp:
            fp.write("bla-bla-bla")

        self.assertFalse(cache.canReadFromCache())

        cache.saveHash()

        # Add another nested directory
        subdir = os.path.join(attach.getAttachPath(), "dir", "subdir_2")
        os.mkdir(subdir)
        self.assertFalse(cache.canReadFromCache())

        cache.saveHash()

        # Add a file to dir/subdir_2
        with open(os.path.join(subdir, "temp2.tmp"), "w") as fp:
            fp.write("bla-bla-bla")

        self.assertFalse(cache.canReadFromCache())

    def testCacheSubpages(self):
        """
        Test caching when adding new subpages
        """
        # Just created the page, cannot cache
        cache = HtmlCache(self.testPage, self.application)
        self.assertFalse(cache.canReadFromCache())

        cache.saveHash()

        self.assertTrue(cache.canReadFromCache())

        # Add a new subpage
        WikiPageFactory().create(self.testPage, "Подстраница 1", [])
        self.assertFalse(cache.canReadFromCache())

        cache.saveHash()
        self.assertTrue(cache.canReadFromCache())

    def testCacheStyle(self):
        """
        Test that changing the page style resets the cache
        """
        style = Style()

        # Just created the page, cannot cache
        cache = HtmlCache(self.testPage, self.application)
        self.assertFalse(cache.canReadFromCache())

        cache.saveHash()
        self.assertTrue(cache.canReadFromCache())

        exampleStyleDir = "testdata/styles/example_jblog/example_jblog"
        exampleStyleDir2 = "testdata/styles/example_jnet/example_jnet"

        # Change page style
        style.setPageStyle(self.testPage, exampleStyleDir)

        self.assertFalse(cache.canReadFromCache())

        cache.saveHash()
        self.assertTrue(cache.canReadFromCache())

        # Change the style once more
        style.setPageStyle(self.testPage, exampleStyleDir2)

        self.assertFalse(cache.canReadFromCache())

        cache.saveHash()
        self.assertTrue(cache.canReadFromCache())

        # Set default style
        style.setPageStyleDefault(self.testPage)

        self.assertFalse(cache.canReadFromCache())

        cache.saveHash()
        self.assertTrue(cache.canReadFromCache())

    def testCacheLoadPlugins1(self):
        """
        Test that caching doesn't work when the list of installed plugins changes
        """
        # Just created the page, cannot cache
        cache = HtmlCache(self.testPage, self.application)
        self.assertFalse(cache.canReadFromCache())

        cache.saveHash()

        # After generating the page once, if nothing changed, can cache
        self.assertTrue(cache.canReadFromCache())

        # Loaded a plugin. Cache should not work
        self.application.plugins.load(["testdata/plugins/testempty1"])
        self.assertFalse(cache.canReadFromCache())

        cache.saveHash()

        # Loaded another plugin
        self.application.plugins.load(["testdata/plugins/testempty2"])
        self.assertFalse(cache.canReadFromCache())

    def testCacheLoadPlugins2(self):
        """
        Test that caching doesn't work when the list of installed plugins changes
        """
        self.application.plugins.clear()
        self.application.plugins.load(["testdata/plugins/testempty1"])
        self.application.plugins.load(["testdata/plugins/testempty2"])

        # Just created the page, cannot cache
        cache = HtmlCache(self.testPage, self.application)
        self.assertFalse(cache.canReadFromCache())

        cache.saveHash()

        self.application.plugins.clear()

        self.assertFalse(cache.canReadFromCache())

        # Reload plugins in different order
        self.application.plugins.load(["testdata/plugins/testempty2"])
        self.application.plugins.load(["testdata/plugins/testempty1"])

        self.assertEqual(len(self.application.plugins), 2)
        self.assertTrue(cache.canReadFromCache())
        self.application.plugins.clear()

    def testConfigThumbSizeCache(self):
        """
        Test that changing the default thumbnail size affects caching
        """
        # Just created the page, cannot cache
        cache = HtmlCache(self.testPage, self.application)
        self.assertFalse(cache.canReadFromCache())

        cache.saveHash()

        # After generating the page once, if nothing changed, can cache
        self.assertTrue(cache.canReadFromCache())

        self.application.config.set(
            WikiConfig.WIKI_SECTION,
            WikiConfig.THUMB_SIZE_PARAM,
            WikiConfig.THUMB_SIZE_DEFAULT + 100,
        )

        self.assertFalse(cache.canReadFromCache())

        cache.saveHash()
        self.assertTrue(cache.canReadFromCache())

        self.application.config.set(
            WikiConfig.WIKI_SECTION, WikiConfig.THUMB_SIZE_PARAM, "Бла-бла-бла"
        )
        self.assertFalse(cache.canReadFromCache())

        cache.saveHash()
        self.application.config.set(
            WikiConfig.WIKI_SECTION,
            WikiConfig.THUMB_SIZE_PARAM,
            WikiConfig.THUMB_SIZE_DEFAULT,
        )
        self.assertTrue(cache.canReadFromCache())

    def testConfigFontNameCache(self):
        """
        Test that changing the default thumbnail size affects caching
        """
        # Just created the page, cannot cache
        cache = HtmlCache(self.testPage, self.application)
        self.assertFalse(cache.canReadFromCache())

        cache.saveHash()

        # After generating the page once, if nothing changed, can cache
        self.assertTrue(cache.canReadFromCache())

        self.application.config.set(
            HtmlRenderConfig.HTML_SECTION,
            HtmlRenderConfig.FONT_FACE_NAME_PARAM,
            "Бла-бла-бла",
        )

        self.assertFalse(cache.canReadFromCache())

        cache.saveHash()
        self.assertTrue(cache.canReadFromCache())

    def testResetHash1(self):
        # Just created the page, cannot cache
        cache = HtmlCache(self.testPage, self.application)
        self.assertFalse(cache.canReadFromCache())

        cache.saveHash()

        # After generating the page once, if nothing changed, can cache
        self.assertTrue(cache.canReadFromCache())

        cache.resetHash()
        self.assertFalse(cache.canReadFromCache())

    def testResetHash2(self):
        # Just created the page, cannot cache
        cache = HtmlCache(self.testPage, self.application)

        self.assertFalse(cache.canReadFromCache())
        cache.resetHash()

        cache.saveHash()

        # After generating the page once, if nothing changed, can cache
        self.assertTrue(cache.canReadFromCache())

        cache.resetHash()
        self.assertFalse(cache.canReadFromCache())
