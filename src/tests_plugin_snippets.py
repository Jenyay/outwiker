#!/usr/bin/env python
# -*- coding: utf-8 -*-

from gettext import NullTranslations
import unittest

from test.plugins.snippets.test_loading import SnippetsLoadingTest
from test.plugins.snippets.test_snippetsloader import SnippetsLoaderTest
from test.plugins.snippets.test_snippetparser import SnippetParserTest
from test.plugins.snippets.test_varpanel import SnippetsVarPanelTest
from test.plugins.snippets.test_vardialog import SnippetsVarDialogTest
from test.plugins.snippets.test_vardialogcontroller import SnippetsVarDialogControllerTest
from test.plugins.snippets.test_utils import SnippetsUtilsTest
from test.plugins.snippets.test_wikicommand import SnippetsWikiCommandTest


if __name__ == '__main__':
    NullTranslations().install()
    unittest.main()
