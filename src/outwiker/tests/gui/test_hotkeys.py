# -*- coding: utf-8 -*-

from unittest import TestCase

import outwiker.gui.actionslist as actionslist
from outwiker.pages.wiki import wikipage
from outwiker.pages.html import htmlpage


class HotKeysTest(TestCase):
    def _find_duplicate(self, actions, item):
        for other_item in actions:
            if (other_item != item and
                    item[-1] is not None and
                    other_item[-1] == item[-1]):
                return other_item

    def test_duplicate(self):
        actions_list = (actionslist.actionsList +
                        wikipage.wiki_actions +
                        htmlpage.html_actions +
                        actionslist.polyactionsList)

        duplicates = []
        for action in actions_list:
            if action not in duplicates:
                duplicate = self._find_duplicate(actions_list, action)
                if duplicate is not None:
                    print(('Hot keys duplicate: {} <---> {} ---> {:<15}'.format(
                        action[0],
                        duplicate[0],
                        action[-1])))
                    duplicates.append(duplicate)

        self.assertEqual(len(duplicates), 0, 'Hot keys have duplicates')
