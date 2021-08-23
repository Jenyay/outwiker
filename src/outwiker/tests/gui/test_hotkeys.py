# -*- coding: utf-8 -*-

from unittest import TestCase

from outwiker.pages.html import htmlpage
from outwiker.pages.wiki import wikipage
from outwiker.tests.basetestcases import BaseOutWikerGUIMixin


class HotKeysTest(TestCase, BaseOutWikerGUIMixin):
    def setUp(self):
        self.initApplication()

    def _find_duplicate(self, actions, item):
        for other_item in actions:
            if (other_item != item and
                    item.hotkey is not None and
                    other_item.hotkey == item.hotkey and
                    other_item.area == item.area):
                return other_item

    def tearDown(self):
        self.destroyApplication()

    def test_duplicate(self):
        import outwiker.gui.actionslist as actionslist
        actions_list = (actionslist.actionsList +
                        wikipage.wiki_actions +
                        htmlpage.html_actions +
                        actionslist.polyactionsList)

        duplicates = []
        for action_info in actions_list:
            if action_info not in duplicates:
                duplicate = self._find_duplicate(actions_list, action_info)
                if duplicate is not None:
                    print(('Hot keys duplicate: {} <---> {} ---> {:<15}'.format(
                        str(action_info),
                        str(duplicate),
                        str(action_info.hotkey))))
                    duplicates.append(duplicate)

        self.assertEqual(len(duplicates), 0, 'Hot keys have duplicates')
