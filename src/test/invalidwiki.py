# -*- coding: UTF-8 -*-

"""
Тесты на загрузку вики с ошибками
"""

import datetime
import os.path
import shutil
import unittest

from outwiker.core.attachment import Attachment
from outwiker.core.tree import WikiDocument
from outwiker.pages.text.textpage import TextPageFactory
from test.utils import removeDir
from outwiker.core.exceptions import RootFormatError



class InvalidWikiTest (unittest.TestCase):
    def setUp (self):
        self.defaultdate = datetime.datetime (2020, 1, 1)
        self.path = u"../test/invalidwiki"


    def testInvalidWikiRoot1 (self):
        """
        Тест на обработку ошибки в файле __page.opt корня вики
        """
        def __createInvalidWiki1 ():
            # Здесь будет создаваться вики
            path = u"../test/testwiki"
            removeDir (path)

            rootwiki = WikiDocument.create (path)

            factory = TextPageFactory()
            factory.create (rootwiki, u"Страница 1", [])
            factory.create (rootwiki[u"Страница 1"], u"Страница 2", [])

            # Испортим файл __page.opt
            with open (os.path.join (rootwiki.path, u"__page.opt"), "w") as fp:
                fp.write (u"wsfsdf sdf sdfasdfdsf \nasfasdsadf")

            return path

        path = __createInvalidWiki1 ()
        self.assertRaises (RootFormatError, WikiDocument.load, path)

        # Сбросим файл __page.opt
        WikiDocument.clearConfigFile (path)

        # Теперь ошибок быть не должно
        WikiDocument.load (path)

        removeDir (path)


    def testInvalidWikiRoot2 (self):
        """
        Тест на обработку ошибки в файле __page.opt корня вики
        """
        def __createInvalidWiki2 ():
            # Здесь будет создаваться вики
            path = u"../test/testwiki"
            removeDir (path)

            rootwiki = WikiDocument.create (path)

            factory = TextPageFactory()
            factory.create (rootwiki, u"Страница 1", [])
            factory.create (rootwiki[u"Страница 1"], u"Страница 2", [])

            # Испортим файл __page.opt
            with open (os.path.join (rootwiki.path, u"__page.opt"), "w") as fp:
                fp.write (u"[General]\naaa=xxx\n<<<<<<<<wsfsdf sdf sdfasdfdsf \nasfasdsadf")

            return path

        path = __createInvalidWiki2 ()
        self.assertRaises (RootFormatError, WikiDocument.load, path)

        # Сбросим файл __page.opt
        WikiDocument.clearConfigFile (path)

        # Теперь ошибок быть не должно
        WikiDocument.load (path)

        removeDir (path)


    def testNotPage (self):
        """
        Тест папок, которые не являются страницами
        """
        wiki = WikiDocument.load (self.path)
        page = wiki[u"Просто папка"]
        self.assertEqual (page, None)


    def testEmptyAttaches (self):
        """
        Тест страницы без папки с аттачами
        """
        wiki = WikiDocument.load (self.path)
        page = wiki[u"Страница без аттачей"]
        self.assertEqual (len (Attachment (page).attachmentFull), 0)
        page.datetime = self.defaultdate


    def testEmptyAttaches2 (self):
        """
        Попытка прикрепления файлов к странице без папки __attach
        """
        filesPath = u"../test/samplefiles/"
        files = [u"accept.png", u"add.png", u"anchor.png"]
        attaches = [os.path.join (filesPath, fname) for fname in files]

        wiki = WikiDocument.load (self.path)
        Attachment (wiki[u"Страница без аттачей"]).attach (attaches)

        self.assertEqual (len (Attachment (wiki[u"Страница без аттачей"]).attachmentFull), 3)

        # Удалим прикрепленные файлы
        attachPath = Attachment (wiki[u"Страница без аттачей"]).getAttachPath()
        shutil.rmtree (attachPath)
        wiki[u"Страница без аттачей"].datetime = self.defaultdate


    def testEmptyContent (self):
        """
        Тест страницы без файла контента
        """
        wiki = WikiDocument.load (self.path)
        page = wiki[u"Страница без контента"]
        self.assertEqual (page.content, "")


    def testInvalidPath (self):
        """
        Тест попытки открытия несуществующей вики
        """
        invalidpath = u"../testsss/invalidwiki"
        self.assertRaises (IOError, WikiDocument.load, invalidpath)
