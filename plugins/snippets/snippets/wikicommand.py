# -*- coding: utf-8 -*-

from outwiker.pages.wiki.parser.command import Command

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
            return self._executeFromFile(params_dict)
        else:
            return self._executeFromContent(params_dict, content)

    def _executeFromFile(self, params_dict):
        return u''

    def _executeFromContent(self, params_dict, content):
        current_dir = self._snippets_dir
        snippet = content

        snippet_parser = SnippetParser(content, current_dir, self._application)
        try:
            result = snippet_parser.process(snippet,
                                            self.parser.page,
                                            **params_dict)
        except SnippetException as e:
            text = _(u'Snippet error: \n') + e.message
            result = u"<div class='__error'>'''{}'''</div>".format(text)
        return self.parser.parseWikiMarkup(result)
