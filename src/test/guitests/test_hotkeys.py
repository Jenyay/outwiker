# -*- coding: UTF-8 -*-

from unittest import TestCase

import outwiker.gui.actionslist as actionslist
from outwiker.pages.wiki import wikipage
from outwiker.pages.html import htmlpage


class HotKeysTest(TestCase):
    def _find_duplicate(self, actions, item):
        for other_item in actions:
            if other_item != item and other_item[1] == item[1]:
                return other_item

    def test_duplicate(self):

        actions_list_1 = [(item[0], str(item[-1]))
                          for item
                          in actionslist.actionsList + wikipage.wiki_actions + htmlpage.html_actions
                          if item[-1] is not None]

        actions_list_2 = [(item[0], str(item[-1]))
                          for item
                          in actionslist.polyactionsList
                          if item[-1] is not None]

        actions_list = actions_list_1 + actions_list_2

        duplicates = []
        for action in actions_list:
            if action not in duplicates:
                duplicate = self._find_duplicate(actions_list, action)
                if duplicate is not None:
                    print(u'Hot keys duplicate: {} <---> {} ---> {:<15}'.format(
                        action[0],
                        duplicate[0],
                        action[1]))
                    duplicates.append(duplicate)

        self.assertEqual(len(duplicates), 0, u'Hot keys have duplicates')
