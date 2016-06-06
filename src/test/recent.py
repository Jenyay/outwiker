# -*- coding: UTF-8 -*-

import unittest
import os

from outwiker.core.config import Config
from outwiker.core.recent import RecentWiki


class RecentWikiTest(unittest.TestCase):
    def setUp(self):
        self.path = u"../test/testconfig.ini"

        if os.path.exists(self.path):
            os.remove(self.path)

    def tearDown(self):
        if os.path.exists(self.path):
            os.remove(self.path)

    def testAdd1(self):
        config = Config(self.path)
        recent = RecentWiki(config)

        self.assertEqual(len(recent), 0)

        recent.add("path1")
        self.assertEqual(len(recent), 1)
        self.assertEqual(recent[0], "path1")

        recent.add("path2")
        self.assertEqual(len(recent), 2)
        self.assertEqual(recent[0], "path2")
        self.assertEqual(recent[1], "path1")

        recent.add("path3")
        self.assertEqual(len(recent), 3)
        self.assertEqual(recent[0], "path3")
        self.assertEqual(recent[1], "path2")
        self.assertEqual(recent[2], "path1")

    def testAdd2(self):
        config = Config(self.path)
        recent = RecentWiki(config)

        self.assertEqual(len(recent), 0)

        recent.add("path1")
        recent.add("path2")
        recent.add("path3")

        recent2 = RecentWiki(config)

        self.assertEqual(len(recent2), 3)
        self.assertEqual(recent2[0], "path3")
        self.assertEqual(recent2[1], "path2")
        self.assertEqual(recent2[2], "path1")

    def testSave(self):
        config = Config(self.path)
        recent = RecentWiki(config)
        recent.add("path1")
        recent.add("path2")
        recent.add("path3")

        config2 = Config(self.path)
        recent2 = RecentWiki(config2)

        self.assertEqual(len(recent2), 3)
        self.assertEqual(recent2[0], "path3")
        self.assertEqual(recent2[1], "path2")
        self.assertEqual(recent2[2], "path1")

    def testRepeat1(self):
        """
        Проверка случая, когда один и тот же файл открывается несолько раз
        """
        config = Config(self.path)
        recent = RecentWiki(config)
        recent.add("path1")
        recent.add("path2")
        recent.add("path3")
        recent.add("path3")

        self.assertEqual(len(recent), 3)
        self.assertEqual(recent[0], "path3")
        self.assertEqual(recent[1], "path2")
        self.assertEqual(recent[2], "path1")

    def testRepeat2(self):
        """
        Проверка случая, когда один и тот же файл открывается несолько раз
        """
        config = Config(self.path)
        recent = RecentWiki(config)
        recent.add("path1")
        recent.add("path2")
        recent.add("path3")
        recent.add("path1")

        self.assertEqual(len(recent), 3)
        self.assertEqual(recent[0], "path1")
        self.assertEqual(recent[1], "path3")
        self.assertEqual(recent[2], "path2")

    def testRepeat3(self):
        """
        Проверка случая, когда один и тот же файл открывается несолько раз
        """
        config = Config(self.path)
        recent = RecentWiki(config)
        recent.add("path1")
        recent.add("path2")
        recent.add("path3")
        recent.add("path2")

        self.assertEqual(len(recent), 3)
        self.assertEqual(recent[0], "path2")
        self.assertEqual(recent[1], "path3")
        self.assertEqual(recent[2], "path1")

    def testLength1(self):
        """
        Тесты, связанные с длиной списка последних открытых вики
        """
        config = Config(self.path)
        recent = RecentWiki(config)

        # Значение по умолчанию
        self.assertEqual(recent.maxlen, 5)

        recent.add("path1")
        recent.add("path2")
        recent.add("path3")
        recent.add("path4")
        recent.add("path5")
        recent.add("path6")

        self.assertEqual(len(recent), recent.maxlen)
        self.assertEqual(recent[0], "path6")
        self.assertEqual(recent[1], "path5")
        self.assertEqual(recent[2], "path4")
        self.assertEqual(recent[3], "path3")
        self.assertEqual(recent[4], "path2")
