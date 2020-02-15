'''
Test for the outwiker.test.commands.getAlternativeTitle
'''

import pytest

import outwiker.core.tree_commands as tc
from outwiker.pages.text.textpage import TextPageFactory

from tests.utils import create_temp_notes_tree, remove_notes_tree


@pytest.mark.parametrize('title, siblings, expected', [
    ('', [], '(1)'),
    ('         ', [], '(1)'),
    ('', ['(1)'], '(2)'),
    ('Проверка', [], 'Проверка'),
    ('Проверка тест', [], 'Проверка тест'),
    ('    Проверка тест     ', [], 'Проверка тест'),
    ('Проверка', ['Проверка'], 'Проверка (1)'),
    ('Проверка', ['Test', 'Проверка'], 'Проверка (1)'),
    ('Проверка     ', ['Test', 'Проверка'], 'Проверка (1)'),
    ('     Проверка', ['Test', 'Проверка'], 'Проверка (1)'),
    ('     Проверка     ', ['Test', 'Проверка'], 'Проверка (1)'),
    ('Проверка', ['Test', 'Проверка', 'Проверка (1)',
                  'Проверка (2)'], 'Проверка (3)'),
    ('Проверка', ['Test', 'проверка'], 'Проверка (1)'),
    ('проверка', ['Test', 'Проверка'], 'проверка (1)'),
    ('Проверка', ['Test', 'проверка', 'проверка (1)'], 'Проверка (2)'),
    ('проверка', ['Test', 'Проверка', 'Проверка (1)'], 'проверка (2)'),
    ('Проверка:', ['Проверка_'], 'Проверка_ (1)'),
    ('Проверка:', ['Проверка_', 'Проверка_ (1)'], 'Проверка_ (2)'),
    ('Проверка:', [], 'Проверка_'),
    ('Проверка ><|?*:"\\/#%', [], 'Проверка ___________'),
    ('Проверка ><|?*:"\\/#% test', [], 'Проверка ___________ test'),
])
def test_getAlternativeTitle(title, siblings, expected):
    newtitle = tc.getAlternativeTitle(title, siblings)
    assert newtitle == expected


class TestCreatePage:
    def setup(self):
        self.wikiroot = create_temp_notes_tree()

    def teardown(self):
        remove_notes_tree(self.wikiroot)

    def test_createPage_empty(self):
        page_title = 'Страница 1'
        page = tc.createPage(TextPageFactory(), page_title, self.wikiroot, [])

        assert page.title == page_title
        assert page.order == 0
        assert self.wikiroot[page_title] is page

    def test_createPage_alias(self):
        page_title = 'Страница_'
        page_alias = 'Страница/'
        page = tc.createPage(TextPageFactory(), page_alias, self.wikiroot, [])

        assert page.title == page_title
        assert page.alias == page_alias
        assert self.wikiroot[page_title] is page

    def test_createPage_duplicate(self):
        page_alias = 'Страница 1'
        page_title_1 = 'Страница 1'
        page_title_2 = 'Страница 1 (1)'

        page_1 = tc.createPage(
            TextPageFactory(), page_alias, self.wikiroot, [])

        page_2 = tc.createPage(
            TextPageFactory(), page_alias, self.wikiroot, [])

        assert page_1.title == page_title_1
        assert page_1.alias is None
        assert page_1.order == 0

        assert page_2.title == page_title_2
        assert page_2.alias == page_alias
        assert page_2.order == 1

        assert self.wikiroot[page_title_1] is page_1
        assert self.wikiroot[page_title_2] is page_2
