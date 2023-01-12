# -*- coding: utf-8 -*-

import os
import os.path
import unittest
from pathlib import Path
from tempfile import mkdtemp
from typing import List

from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.core.attachment import Attachment
from outwiker.pages.wiki.parser.commands.attachlist import AttachListCommand
from outwiker.pages.wiki.parserfactory import ParserFactory
from outwiker.pages.wiki.thumbnails import Thumbnails
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.tests.basetestcases import BaseOutWikerMixin
from outwiker.tests.utils import removeDir
import outwiker.core.cssclasses as css


class WikiAttachListCommandTest (BaseOutWikerMixin, unittest.TestCase):
    def setUp(self):
        self.initApplication()
        self.encoding = "utf8"

        self._create_wiki()
        self.testPage = self.wikiroot["Страница 1"]

        factory = ParserFactory()
        self.parser = factory.make(self.testPage, Application.config)

        filesPath = "testdata/samplefiles/"
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

        self.template = '<a class="ow-link-attach {css_class}" href="{link}">{title}</a>'

    def tearDown(self):
        self.destroyApplication()
        removeDir(self.path)

    def _attach_files(self, subdir: str = '.'):
        attach = Attachment(self.testPage)
        attach.attach(self.fullFilesPath, subdir)

    def _create_wiki(self):
        # Здесь будет создаваться вики
        self.path = mkdtemp(prefix='Абырвалг абыр')

        self.wikiroot = WikiDocument.create(self.path)
        WikiPageFactory().create(self.wikiroot, "Страница 1", [])

    def _check_items_order(self, result: str, items: List[str]):
        pos = -1
        for item in items:
            next_pos = result.find(item)
            self.assertNotEqual(-1, next_pos, item)
            self.assertGreater(next_pos, pos, item)
            pos = next_pos

    def _create_link_to_file(self, subdir, fname, title):
        attachdir = Path("__attach")
        link = str(attachdir / subdir / fname).replace("\\", "/")
        return self.template.format(css_class=css.CSS_ATTACH_FILE, link=link, title=title)

    def _create_link_to_dir(self, subdir, dirname, title):
        attachdir = Path("__attach")
        link = str(attachdir / subdir / dirname).replace("\\", "/")
        return self.template.format(css_class=css.CSS_ATTACH_DIR, link=link, title=title)

    def _create_items(self, subdir: str, expected_dirs: List[str], expected_files: List[str]) -> List[str]:
        return (
                [self._create_link_to_dir(subdir, dirname, dirname) for dirname in expected_dirs] + 
                [self._create_link_to_file(subdir, fname, fname) for fname in expected_files]
                )

    def test_сommand(self):
        self._attach_files()
        cmd = AttachListCommand(self.parser)
        result = cmd.execute('', '')

        expected_dirs = ["dir", "for_sort"]
        expected_files = [
                "add.png",
                "anchor.png",
                "image.jpg",
                "файл с пробелами.tmp"
                ]

        items = self._create_items('', expected_dirs, expected_files)
        self._check_items_order(result, items)

    def test_subdir_double_quotes(self):
        subdir = 'test_subdir'
        self._attach_files(subdir)
        cmd = AttachListCommand(self.parser)
        params = 'subdir="{}"'.format(subdir)
        result = cmd.execute(params, '')

        expected_dirs = ["dir", "for_sort"]
        expected_files = [
                "add.png",
                "anchor.png",
                "image.jpg",
                "файл с пробелами.tmp"
                ]

        items = self._create_items(subdir, expected_dirs, expected_files)
        self._check_items_order(result, items)

    def test_subdir_single_quotes(self):
        subdir = 'test_subdir'
        self._attach_files(subdir)
        cmd = AttachListCommand(self.parser)
        params = "subdir='{}'".format(subdir)
        result = cmd.execute(params, '')

        expected_dirs = ["dir", "for_sort"]
        expected_files = [
                "add.png",
                "anchor.png",
                "image.jpg",
                "файл с пробелами.tmp"
                ]

        items = self._create_items(subdir, expected_dirs, expected_files)
        self._check_items_order(result, items)

    def test_subsubdir_forward_slashes(self):
        subdir = 'subdir_1/subdir_2'
        self._attach_files(subdir)
        cmd = AttachListCommand(self.parser)
        params = 'subdir="{}"'.format(subdir)
        result = cmd.execute(params, '')

        expected_dirs = ["dir", "for_sort"]
        expected_files = [
                "add.png",
                "anchor.png",
                "image.jpg",
                "файл с пробелами.tmp"
                ]

        items = self._create_items(subdir, expected_dirs, expected_files)
        self._check_items_order(result, items)

    def test_subsubdir_back_slashes(self):
        subdir = 'subdir_1\\subdir_2'
        self._attach_files(subdir)
        cmd = AttachListCommand(self.parser)
        params = 'subdir="{}"'.format(subdir)
        result = cmd.execute(params, '')

        expected_dirs = ["dir", "for_sort"]
        expected_files = [
                "add.png",
                "anchor.png",
                "image.jpg",
                "файл с пробелами.tmp"
                ]

        items = self._create_items(subdir, expected_dirs, expected_files)
        self._check_items_order(result, items)

    def test_parsing_no_params(self):
        self._attach_files()
        text = "(:attachlist:)"
        result = self.parser.toHtml(text)

        expected_dirs = ["dir", "for_sort"]
        expected_files = [
                "add.png",
                "anchor.png",
                "image.jpg",
                "файл с пробелами.tmp"
                ]

        items = self._create_items('', expected_dirs, expected_files)
        self._check_items_order(result, items)

    def test_parsing_ignore_thumbs(self):
        self._attach_files()
        # Тест на то, что игнорируется директория __thumb
        thumb = Thumbnails(self.testPage)
        thumb.getThumbPath(True)

        text = "(:attachlist:)"
        result = self.parser.toHtml(text)

        self.assertNotIn('__thumb', result)

    def test_command_sort_by_name(self):
        self._attach_files()
        cmd = AttachListCommand(self.parser)
        result = cmd.execute("sort=name", "")

        expected_dirs = ["dir", "for_sort"]
        expected_files = [
                "add.png",
                "anchor.png",
                "image.jpg",
                "файл с пробелами.tmp"
                ]

        items = self._create_items('', expected_dirs, expected_files)
        self._check_items_order(result, items)

    def test_parsing_sort_by_name(self):
        self._attach_files()
        text = "(:attachlist sort=name:)"
        result = self.parser.toHtml(text)

        expected_dirs = ["dir", "for_sort"]
        expected_files = [
                "add.png",
                "anchor.png",
                "image.jpg",
                "файл с пробелами.tmp"
                ]

        items = self._create_items('', expected_dirs, expected_files)
        self._check_items_order(result, items)

    def test_command_sort_descend_name(self):
        self._attach_files()
        cmd = AttachListCommand(self.parser)
        result = cmd.execute("sort=descendname", "")

        expected_dirs = ["for_sort", "dir"]
        expected_files = [
                "файл с пробелами.tmp",
                "image.jpg",
                "anchor.png",
                "add.png",
                ]

        items = self._create_items('', expected_dirs, expected_files)
        self._check_items_order(result, items)

    def test_parsing_sort_descend_name(self):
        self._attach_files()
        text = "(:attachlist sort=descendname:)"
        result = self.parser.toHtml(text)

        expected_dirs = ["for_sort", "dir"]
        expected_files = [
                "файл с пробелами.tmp",
                "image.jpg",
                "anchor.png",
                "add.png",
                ]

        items = self._create_items('', expected_dirs, expected_files)
        self._check_items_order(result, items)

    def test_parsing_sort_by_ext(self):
        self._attach_files()
        text = "(:attachlist sort=ext:)"
        result = self.parser.toHtml(text)

        expected_dirs = ["dir", "for_sort"]
        expected_files = [
                "image.jpg",
                "add.png",
                "anchor.png",
                "файл с пробелами.tmp",
                ]

        items = self._create_items('', expected_dirs, expected_files)
        self._check_items_order(result, items)

    def test_parsing_sort_descend_ext(self):
        self._attach_files()
        text = "(:attachlist sort=descendext:)"
        result = self.parser.toHtml(text)

        expected_dirs = ["for_sort", "dir"]
        expected_files = [
                "файл с пробелами.tmp",
                "anchor.png",
                "add.png",
                "image.jpg",
                ]

        items = self._create_items('', expected_dirs, expected_files)
        self._check_items_order(result, items)

    def test_parsing_sort_by_size(self):
        self._attach_files()
        text = "(:attachlist sort=size:)"
        result = self.parser.toHtml(text)

        expected_dirs = ["dir", "for_sort"]
        expected_files = [
                "файл с пробелами.tmp",
                "anchor.png",
                "add.png",
                "image.jpg",
                ]

        items = self._create_items('', expected_dirs, expected_files)
        self._check_items_order(result, items)

    def test_parsing__sort_descend_size(self):
        self._attach_files()
        text = "(:attachlist sort=descendsize:)"
        result = self.parser.toHtml(text)

        expected_dirs = ["for_sort", "dir"]
        expected_files = [
                "image.jpg",
                "add.png",
                "anchor.png",
                "файл с пробелами.tmp",
                ]

        items = self._create_items('', expected_dirs, expected_files)
        self._check_items_order(result, items)

    def test_parsing_sort_by_date(self):
        files = ["add.png", "Anchor.png",
                 "image2.png", "image.png",
                 "add.png2", "файл с пробелами.tmp",
                 "filename"]

        fullFilesPath = [
                os.path.join(
                    "testdata/samplefiles/for_sort",
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

        expected_dirs = []
        expected_files = [
                files[3],
                files[0],
                files[2],
                files[6],
                files[4],
                files[5],
                files[1],
                ]

        items = self._create_items('', expected_dirs, expected_files)
        self._check_items_order(result, items)

    def test_parsing_sort_descend_date(self):
        files = ["add.png", "Anchor.png",
                 "image2.png", "image.png",
                 "add.png2", "файл с пробелами.tmp",
                 "filename"]

        fullFilesPath = [
                os.path.join(
                    "testdata/samplefiles/for_sort",
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

        expected_dirs = []
        expected_files = [
                files[1],
                files[5],
                files[4],
                files[6],
                files[2],
                files[0],
                files[3]
                ]

        items = self._create_items('', expected_dirs, expected_files)
        self._check_items_order(result, items)
