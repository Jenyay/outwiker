# -*- coding: utf-8 -*-

import os
import os.path
from tempfile import mkdtemp
from unittest import TestCase

from outwiker.api.core.tree import createNotesTree
from outwiker.core.attachment import Attachment
from outwiker.core.style import Style
from outwiker.gui.guiconfig import HtmlRenderConfig
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.emptycontent import EmptyContent
from outwiker.pages.wiki.wikiconfig import WikiConfig
from outwiker.pages.wiki.hashcalculator import WikiHashCalculator
from outwiker.tests.utils import removeDir
from outwiker.tests.basetestcases import BaseOutWikerMixin


class WikiHashTest(BaseOutWikerMixin, TestCase):
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

        self.__htmlconfig = HtmlRenderConfig(self.application.config)
        self.__setDefaultConfig()

    def __setDefaultConfig(self):
        self.__htmlconfig.userStyle.value = ""

        # Set the thumbnail size that matches the default size
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

    def testHash1(self):
        # Page was just created, cannot use cache
        hashCalculator = WikiHashCalculator(self.application)
        hash_src = hashCalculator.getHash(self.testPage)

        self.testPage.content = "бла-бла-бла"
        hash2 = hashCalculator.getHash(self.testPage)

        self.assertNotEqual(hash_src, hash2)

        # Add a file
        attach = Attachment(self.testPage)
        attach.attach([os.path.join(self.filesPath, "add.png")])

        hash3 = hashCalculator.getHash(self.testPage)
        self.assertNotEqual(hash_src, hash3)
        self.assertNotEqual(hash2, hash3)

    def testHash2(self):
        # Page was just created, cannot use cache
        hashCalculator = WikiHashCalculator(self.application)
        hash_src = hashCalculator.getHash(self.testPage)

        self.testPage.content = "бла-бла-бла"
        hash2 = hashCalculator.getHash(self.testPage)

        self.assertNotEqual(hash_src, hash2)

    def testHashRename(self):
        hashCalculator = WikiHashCalculator(self.application)
        hash_src = hashCalculator.getHash(self.testPage)

        self.testPage.title = "Новый заголовок"
        hash2 = hashCalculator.getHash(self.testPage)
        self.assertNotEqual(hash_src, hash2)

    def testCacheEmpty(self):
        emptycontent = EmptyContent(self.application.config)
        self.testPage.content = ""

        hashCalculator = WikiHashCalculator(self.application)
        hash_src = hashCalculator.getHash(self.testPage)

        # Page is empty, template for empty content changed
        emptycontent.content = "1111"
        hash2 = hashCalculator.getHash(self.testPage)
        self.assertNotEqual(hash_src, hash2)

        # Page content changed
        self.testPage.content = "Бла-бла-бла"
        hash3 = hashCalculator.getHash(self.testPage)
        self.assertNotEqual(hash2, hash3)
        self.assertNotEqual(hash_src, hash3)

        # Page template changed, but page is no longer empty
        emptycontent.content = "2222"
        hash4 = hashCalculator.getHash(self.testPage)
        self.assertEqual(hash4, hash3)

    def testCacheSubdir(self):
        attach = Attachment(self.testPage)
        hashCalculator = WikiHashCalculator(self.application)
        hash_src = hashCalculator.getHash(self.testPage)

        # Add a file to dir
        with open(os.path.join(attach.getAttachPath(), "dir", "temp.tmp"), "w") as fp:
            fp.write("bla-bla-bla")

        hash2 = hashCalculator.getHash(self.testPage)
        self.assertNotEqual(hash_src, hash2)

        # Add another nested directory
        subdir = os.path.join(attach.getAttachPath(), "dir", "subdir_2")
        os.mkdir(subdir)

        hash3 = hashCalculator.getHash(self.testPage)
        self.assertNotEqual(hash2, hash3)
        self.assertNotEqual(hash_src, hash3)

        # Add a file to dir/subdir_2
        with open(os.path.join(subdir, "temp2.tmp"), "w") as fp:
            fp.write("bla-bla-bla")

        hash4 = hashCalculator.getHash(self.testPage)
        self.assertNotEqual(hash3, hash4)
        self.assertNotEqual(hash2, hash4)
        self.assertNotEqual(hash_src, hash4)

    def testCacheSubpages(self):
        """
        Test caching when adding new subpages
        """
        hashCalculator = WikiHashCalculator(self.application)
        hash_src = hashCalculator.getHash(self.testPage)

        # Add a new subpage
        WikiPageFactory().create(self.testPage, "Подстраница 1", [])
        hash2 = hashCalculator.getHash(self.testPage)
        self.assertNotEqual(hash2, hash_src)

        # Remove the new page
        self.testPage["Подстраница 1"].remove()

        hash3 = hashCalculator.getHash(self.testPage)
        self.assertEqual(hash3, hash_src)

    def testCacheStyle(self):
        """
        Test that changing the page style resets the cache
        """
        style = Style()
        hashCalculator = WikiHashCalculator(self.application)
        hash_src = hashCalculator.getHash(self.testPage)

        exampleStyleDir = "testdata/styles/example_jblog/example_jblog"
        exampleStyleDir2 = "testdata/styles/example_jnet/example_jnet"

        # Change page style
        style.setPageStyle(self.testPage, exampleStyleDir)
        hash2 = hashCalculator.getHash(self.testPage)
        self.assertNotEqual(hash2, hash_src)

        # Change style again
        style.setPageStyle(self.testPage, exampleStyleDir2)
        hash3 = hashCalculator.getHash(self.testPage)
        self.assertNotEqual(hash2, hash3)
        self.assertNotEqual(hash3, hash_src)

    def testCacheLoadPlugins1(self):
        """
        Test that caching doesn't work when the list of installed plugins changes
        """
        hashCalculator = WikiHashCalculator(self.application)
        hash_src = hashCalculator.getHash(self.testPage)

        # Plugin loaded. Cache should not be used
        self.application.plugins.load(["testdata/plugins/testempty1"])
        hash2 = hashCalculator.getHash(self.testPage)
        self.assertNotEqual(hash2, hash_src)

        # Load another plugin
        self.application.plugins.load(["testdata/plugins/testempty2"])
        hash3 = hashCalculator.getHash(self.testPage)
        self.assertNotEqual(hash3, hash2)
        self.assertNotEqual(hash3, hash_src)

    def testCacheLoadPlugins2(self):
        """
        Test that caching doesn't work when the list of installed plugins changes
        """
        self.application.plugins.clear()
        self.application.plugins.load(["testdata/plugins/testempty1"])
        self.application.plugins.load(["testdata/plugins/testempty2"])

        hashCalculator = WikiHashCalculator(self.application)
        hash_src = hashCalculator.getHash(self.testPage)

        self.application.plugins.clear()
        hash2 = hashCalculator.getHash(self.testPage)
        self.assertNotEqual(hash2, hash_src)

        # Reload plugins in different order
        self.application.plugins.load(["testdata/plugins/testempty1"])
        self.application.plugins.load(["testdata/plugins/testempty2"])

        hash3 = hashCalculator.getHash(self.testPage)
        self.assertNotEqual(hash3, hash2)
        self.assertEqual(hash3, hash_src)

        self.application.plugins.clear()

    def testConfigThumbSizeCache(self):
        """
        Test that changing the default thumbnail size affects caching
        """
        hashCalculator = WikiHashCalculator(self.application)
        hash_src = hashCalculator.getHash(self.testPage)

        self.application.config.set(
            WikiConfig.WIKI_SECTION,
            WikiConfig.THUMB_SIZE_PARAM,
            WikiConfig.THUMB_SIZE_DEFAULT + 100,
        )

        hash2 = hashCalculator.getHash(self.testPage)
        self.assertNotEqual(hash2, hash_src)

        self.application.config.set(
            WikiConfig.WIKI_SECTION, WikiConfig.THUMB_SIZE_PARAM, "Бла-бла-бла"
        )

        hash3 = hashCalculator.getHash(self.testPage)
        self.assertNotEqual(hash3, hash2)
        self.assertEqual(hash3, hash_src)

    def testConfigFontNameCache(self):
        """
        Test that changing the default thumbnail size affects caching
        """
        hashCalculator = WikiHashCalculator(self.application)
        hash_src = hashCalculator.getHash(self.testPage)

        self.application.config.set(
            HtmlRenderConfig.HTML_SECTION,
            HtmlRenderConfig.FONT_FACE_NAME_PARAM,
            "Бла-бла-бла",
        )

        hash2 = hashCalculator.getHash(self.testPage)
        self.assertNotEqual(hash2, hash_src)

    def testConfigUserStyle(self):
        """
        Test that changing user styles affects caching
        """
        hashCalculator = WikiHashCalculator(self.application)
        hash_src = hashCalculator.getHash(self.testPage)

        self.__htmlconfig.userStyle.value = "p {background-color: maroon; /* Цвет фона под текстом параграфа */ color: white; /* Цвет текста */ }"

        hash2 = hashCalculator.getHash(self.testPage)
        self.assertNotEqual(hash2, hash_src)

    def testInvalidFontSize(self):
        """
        Test correct handling of invalid font size settings
        """
        hashCalculator = WikiHashCalculator(self.application)
        hashCalculator.getHash(self.testPage)

        self.application.config.set(
            HtmlRenderConfig.HTML_SECTION,
            HtmlRenderConfig.FONT_SIZE_PARAM,
            "Бла-бла-бла",
        )

        hashCalculator.getHash(self.testPage)

    def testInvalidFontBold(self):
        """
        Test correct handling of invalid font settings
        """
        hashCalculator = WikiHashCalculator(self.application)
        hashCalculator.getHash(self.testPage)

        self.application.config.set(
            HtmlRenderConfig.HTML_SECTION,
            HtmlRenderConfig.FONT_BOLD_PARAM,
            "Бла-бла-бла",
        )

        hashCalculator.getHash(self.testPage)

    def testInvalidFontItalic(self):
        """
        Test correct handling of invalid font settings
        """
        hashCalculator = WikiHashCalculator(self.application)
        hashCalculator.getHash(self.testPage)

        self.application.config.set(
            HtmlRenderConfig.HTML_SECTION,
            HtmlRenderConfig.FONT_ITALIC_PARAM,
            "Бла-бла-бла",
        )

        hashCalculator.getHash(self.testPage)
