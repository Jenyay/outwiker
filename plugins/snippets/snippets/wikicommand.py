# -*- coding: utf-8 -*-

import os

from outwiker.pages.wiki.parser.command import Command
from outwiker.utilites.textfile import readTextFile

from snippets.defines import WIKI_COMMAND_PARAM_FILE
from snippets.snippetparser import SnippetParser, SnippetException
from snippets.i18n import get_


class CommandSnip (Command):
    '''
    Command using.

    I. Reading the snippet from command text

    (:snip var1='...' var2='...' ...:)
    template text
    (:snipend:)

    II. Reading the snippet from text file
    (:snip file='subdir/.../snippet' var1='...' var2='...' ...:)
    (:snipend:)

    or

    (:snip file='subdir/.../snippet.tpl' var1='...' var2='...' ...:)
    (:snipend:)
    '''
    def __init__(self, parser, snippets_dir, application):
        super(CommandSnip, self).__init__(parser)
        self._snippets_dir = snippets_dir
        self._application = application

        global _
        _ = get_()

    @property
    def name(self):
        return u"snip"

    def execute(self, params, content):
        params_dict = self.parseParams(params)
        if WIKI_COMMAND_PARAM_FILE in params_dict:
            return self._executeFromFile(params_dict, content)
        else:
            return self._executeFromContent(params_dict, content)

    def _format_error(self, text):
        return u"<div class='__error'><b>{}</b></div>".format(text)

    def _parseSnippet(self,
                      snippet_text,
                      current_dir,
                      params_dict,
                      selected_text=u''):
        snippet_parser = SnippetParser(snippet_text,
                                       current_dir,
                                       self._application)
        try:
            result = snippet_parser.process(selected_text,
                                            self.parser.page,
                                            **params_dict)
        except SnippetException as e:
            text = _(u'Snippet error: \n') + e.message
            return self._format_error(text)
        return self.parser.parseWikiMarkup(result)

    def _executeFromFile(self, params_dict, content):
        snippet_file = params_dict[WIKI_COMMAND_PARAM_FILE]

        snippet_path = os.path.join(self._snippets_dir, snippet_file)
        current_dir = os.path.dirname(snippet_path)

        try:
            snippet_text = readTextFile(snippet_path)
        except EnvironmentError:
            text = (_(u'Snippet error: \n') +
                    _(u"Can't read file '{}'").format(snippet_path))
            return self._format_error(text)

        return self._parseSnippet(snippet_text,
                                  current_dir,
                                  params_dict,
                                  content)

    def _executeFromContent(self, params_dict, content):
        current_dir = self._snippets_dir
        snippet_text = content
        return self._parseSnippet(snippet_text, current_dir, params_dict)
