# -*- coding: UTF-8 -*-

import unittest

from outwiker.gui.searchreplacecontroller import LocalSearcher


class LocalSearchTest(unittest.TestCase):

    def test1(self):
        text = u"1111 sdf sdf 111 657 111 1111 sdf sdf1243"
        phrase = u"111"

        searcher = LocalSearcher()
        searcher.search(text, phrase)

        self.assertEqual(len(searcher.result), 4)

        self.assertEqual(searcher.result[0].position, 0)
        self.assertEqual(searcher.result[0].phrase, phrase)

        self.assertEqual(searcher.result[1].position, 13)
        self.assertEqual(searcher.result[1].phrase, phrase)

        self.assertEqual(searcher.result[2].position, 21)
        self.assertEqual(searcher.result[2].phrase, phrase)

        self.assertEqual(searcher.result[3].position, 25)
        self.assertEqual(searcher.result[3].phrase, phrase)

    def test2(self):
        text = u"1111 sdf sdf 111 657 111 1111 sdf sdf1243"
        phrase = u"222"

        searcher = LocalSearcher()
        searcher.search(text, phrase)

        self.assertEqual(len(searcher.result), 0)

    def test3(self):
        text = u"бЛабл sdf sdf Бла 657 бла блА sdf sdf1243"
        phrase = u"бЛа"

        searcher = LocalSearcher()
        searcher.search(text, phrase)

        self.assertEqual(len(searcher.result), 4)

        self.assertEqual(searcher.result[0].position, 0)
        self.assertEqual(searcher.result[0].phrase.lower(), phrase.lower())

        self.assertEqual(searcher.result[1].position, 14)
        self.assertEqual(searcher.result[1].phrase.lower(), phrase.lower())

        self.assertEqual(searcher.result[2].position, 22)
        self.assertEqual(searcher.result[2].phrase.lower(), phrase.lower())

        self.assertEqual(searcher.result[3].position, 26)
        self.assertEqual(searcher.result[3].phrase.lower(), phrase.lower())

    def test4(self):
        text = u"111 бла-Бла-блА"
        phrase = u"бЛа-"

        searcher = LocalSearcher()
        searcher.search(text, phrase)

        self.assertEqual(len(searcher.result), 2)

        self.assertEqual(searcher.result[0].position, 4)
        self.assertEqual(searcher.result[0].phrase.lower(), phrase.lower())

        self.assertEqual(searcher.result[1].position, 8)
        self.assertEqual(searcher.result[1].phrase.lower(), phrase.lower())
