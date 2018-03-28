# -*- coding: UTF-8 -*-

import os
import os.path
import unittest
from tempfile import mkdtemp

from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.core.attachment import Attachment
from outwiker.pages.wiki.parser.commands.attachlist import AttachListCommand
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.pages.wiki.thumbnails import Thumbnails
from outwiker.pages.wiki.wikipage import WikiPageFactory

from test.utils import removeDir


class WikiAttachListCommandTest (unittest.TestCase):
    def setUp(self):
        self.encoding = "utf8"

        self.__createWiki()
        self.testPage = self.wikiroot["Страница 1"]

        factory = ParserFactory()
        self.parser = factory.make(self.testPage, Application.config)

        filesPath = "../test/samplefiles/"
        self.files = [
            "image.jpg",
            "add.png",
            "anchor.png",
            "файл с пробелами.tmp",
            "dir",
            "for_sort"]
        self.fullFilesPath = [
            os.path.join(
                filesPath,
                fname) for fname in self.files]

    def _attachFiles(self):
        attach = Attachment(self.testPage)
        attach.attach(self.fullFilesPath)

    def __createWiki(self):
        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix='Абырвалг абыр')

        self.wikiroot = WikiDocument.create(self.path)
        WikiPageFactory().create(self.wikiroot, "Страница 1", [])

    def tearDown(self):
        removeDir(self.path)

    def _compareResult(self, titles, names, result):
        attachdir = "__attach"
        template = '<a href="{path}">{title}</a>\n'

        result_right = "".join([template.format(path=os.path.join(attachdir, name).replace("\\", "/"), title=title)
                                for (name, title) in zip(names, titles)]).rstrip()

        self.assertEqual(result_right, result)

    def testCommand1(self):
        self._attachFiles()
        cmd = AttachListCommand(self.parser)
        result = cmd.execute("", "")

        titles = [
            "[dir]",
            "[for_sort]",
            "add.png",
            "anchor.png",
            "image.jpg",
            "файл с пробелами.tmp"]
        names = [
            "dir",
            "for_sort",
            "add.png",
            "anchor.png",
            "image.jpg",
            "файл с пробелами.tmp"]

        self._compareResult(titles, names, result)

    def testParse1(self):
        self._attachFiles()
        text = "(:attachlist:)"
        result = self.parser.toHtml(text)

        titles = [
            "[dir]",
            "[for_sort]",
            "add.png",
            "anchor.png",
            "image.jpg",
            "файл с пробелами.tmp"]
        names = [
            "dir",
            "for_sort",
            "add.png",
            "anchor.png",
            "image.jpg",
            "файл с пробелами.tmp"]

        self._compareResult(titles, names, result)

    def testParse2(self):
        self._attachFiles()
        # Тест на то, что игнорируется директория __thumb
        thumb = Thumbnails(self.testPage)
        thumb.getThumbPath(True)

        text = "(:attachlist:)"
        result = self.parser.toHtml(text)

        titles = [
            "[dir]",
            "[for_sort]",
            "add.png",
            "anchor.png",
            "image.jpg",
            "файл с пробелами.tmp"]
        names = [
            "dir",
            "for_sort",
            "add.png",
            "anchor.png",
            "image.jpg",
            "файл с пробелами.tmp"]

        self._compareResult(titles, names, result)

    def testCommandSortByName(self):
        self._attachFiles()
        cmd = AttachListCommand(self.parser)
        result = cmd.execute("sort=name", "")

        titles = [
            "[dir]",
            "[for_sort]",
            "add.png",
            "anchor.png",
            "image.jpg",
            "файл с пробелами.tmp"]
        names = [
            "dir",
            "for_sort",
            "add.png",
            "anchor.png",
            "image.jpg",
            "файл с пробелами.tmp"]

        self._compareResult(titles, names, result)

    def testParseSortByName(self):
        self._attachFiles()
        text = "(:attachlist sort=name:)"
        result = self.parser.toHtml(text)

        titles = [
            "[dir]",
            "[for_sort]",
            "add.png",
            "anchor.png",
            "image.jpg",
            "файл с пробелами.tmp"]
        names = [
            "dir",
            "for_sort",
            "add.png",
            "anchor.png",
            "image.jpg",
            "файл с пробелами.tmp"]

        self._compareResult(titles, names, result)

    def testCommandSortDescendName(self):
        self._attachFiles()
        cmd = AttachListCommand(self.parser)
        result = cmd.execute("sort=descendname", "")

        titles = [
            "[for_sort]",
            "[dir]",
            "файл с пробелами.tmp",
            "image.jpg",
            "anchor.png",
            "add.png"]
        names = [
            "for_sort",
            "dir",
            "файл с пробелами.tmp",
            "image.jpg",
            "anchor.png",
            "add.png"]

        self._compareResult(titles, names, result)

    def testParseSortDescendName(self):
        self._attachFiles()
        text = "(:attachlist sort=descendname:)"
        result = self.parser.toHtml(text)

        titles = [
            "[for_sort]",
            "[dir]",
            "файл с пробелами.tmp",
            "image.jpg",
            "anchor.png",
            "add.png"]
        names = [
            "for_sort",
            "dir",
            "файл с пробелами.tmp",
            "image.jpg",
            "anchor.png",
            "add.png"]

        self._compareResult(titles, names, result)

    def testParseSortByExt(self):
        self._attachFiles()
        text = "(:attachlist sort=ext:)"
        result = self.parser.toHtml(text)

        titles = [
            "[dir]",
            "[for_sort]",
            "image.jpg",
            "add.png",
            "anchor.png",
            "файл с пробелами.tmp"]
        names = [
            "dir",
            "for_sort",
            "image.jpg",
            "add.png",
            "anchor.png",
            "файл с пробелами.tmp"]

        self._compareResult(titles, names, result)

    def testParseSortDescendExt(self):
        self._attachFiles()
        text = "(:attachlist sort=descendext:)"
        result = self.parser.toHtml(text)

        titles = [
            "[for_sort]",
            "[dir]",
            "файл с пробелами.tmp",
            "anchor.png",
            "add.png",
            "image.jpg"]
        names = [
            "for_sort",
            "dir",
            "файл с пробелами.tmp",
            "anchor.png",
            "add.png",
            "image.jpg"]

        self._compareResult(titles, names, result)

    def testParseSortBySize(self):
        self._attachFiles()
        text = "(:attachlist sort=size:)"
        result = self.parser.toHtml(text)

        titles = [
            "[dir]",
            "[for_sort]",
            "файл с пробелами.tmp",
            "anchor.png",
            "add.png",
            "image.jpg"]
        names = [
            "dir",
            "for_sort",
            "файл с пробелами.tmp",
            "anchor.png",
            "add.png",
            "image.jpg"]

        self._compareResult(titles, names, result)

    def testParseSortDescendSize(self):
        self._attachFiles()
        text = "(:attachlist sort=descendsize:)"
        result = self.parser.toHtml(text)

        titles = [
            "[for_sort]",
            "[dir]",
            "image.jpg",
            "add.png",
            "anchor.png",
            "файл с пробелами.tmp"]
        names = [
            "for_sort",
            "dir",
            "image.jpg",
            "add.png",
            "anchor.png",
            "файл с пробелами.tmp"]

        self._compareResult(titles, names, result)

    def testParseSortByDate(self):
        files = ["add.png", "Anchor.png",
                 "image2.png", "image.png",
                 "add.png2", "файл с пробелами.tmp",
                 "filename"]

        fullFilesPath = [
            os.path.join(
                "../test/samplefiles/for_sort",
                fname) for fname in files]

        attach = Attachment(self.testPage)
        attach.attach(fullFilesPath)

        os.utime(attach.getFullPath(files[3]), (1000000000, 1000000000))
        os.utime(attach.getFullPath(files[0]), (1000000000, 1100000000))
        os.utime(attach.getFullPath(files[2]), (1000000000, 1200000000))
        os.utime(attach.getFullPath(files[6]), (1000000000, 1300000000))
        os.utime(attach.getFullPath(files[4]), (1000000000, 1400000000))
        os.utime(attach.getFullPath(files[5]), (1000000000, 1500000000))
        os.utime(attach.getFullPath(files[1]), (1000000000, 1600000000))

        text = "(:attachlist sort=date:)"
        result = self.parser.toHtml(text)

        names = [
            files[3],
            files[0],
            files[2],
            files[6],
            files[4],
            files[5],
            files[1]]
        titles = names[:]

        self._compareResult(titles, names, result)

    def testParseSortDescendDate(self):
        files = ["add.png", "Anchor.png",
                 "image2.png", "image.png",
                 "add.png2", "файл с пробелами.tmp",
                 "filename"]

        fullFilesPath = [
            os.path.join(
                "../test/samplefiles/for_sort",
                fname) for fname in files]

        attach = Attachment(self.testPage)
        attach.attach(fullFilesPath)

        os.utime(attach.getFullPath(files[3]), (1000000000, 1000000000))
        os.utime(attach.getFullPath(files[0]), (1000000000, 1100000000))
        os.utime(attach.getFullPath(files[2]), (1000000000, 1200000000))
        os.utime(attach.getFullPath(files[6]), (1000000000, 1300000000))
        os.utime(attach.getFullPath(files[4]), (1000000000, 1400000000))
        os.utime(attach.getFullPath(files[5]), (1000000000, 1500000000))
        os.utime(attach.getFullPath(files[1]), (1000000000, 1600000000))

        text = "(:attachlist sort=descenddate:)"
        result = self.parser.toHtml(text)

        names = [
            files[1],
            files[5],
            files[4],
            files[6],
            files[2],
            files[0],
            files[3]]
        titles = names[:]

        self._compareResult(titles, names, result)
