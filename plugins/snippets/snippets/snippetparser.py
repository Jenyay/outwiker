# -*- coding: UTF-8 -*-

from outwiker.core.attachment import Attachment

from jinja2 import Environment, meta
import snippets.defines as defines


class SnippetParser(object):
    def __init__(self, template, application):
        self._template = template
        self._application = application

    def process(self, selectedText, page, **kwargs):
        assert self._application.selectedPage is not None
        params = self._getGlobalVariables(selectedText, page)
        params.update(kwargs)

        env = Environment()
        tpl = env.from_string(self._template, globals=params)
        result = tpl.render()

        return result

    def getVariables(self):
        env = Environment()
        ast = env.parse(self._template)
        variables = meta.find_undeclared_variables(ast)
        return variables

    def _getGlobalVariables(self, selectedText, page):
        assert page is not None

        globals = {
            defines.VAR_SEL_TEXT: selectedText,
            defines.VAR_TITLE: page.title,
            defines.VAR_SUBPATH: page.subpath,
            defines.VAR_ATTACH: Attachment(page).getAttachPath(True),
            defines.VAR_FOLDER: page.path,
            defines.VAR_PAGE_ID: self._application.pageUidDepot.createUid(page)
        }

        return globals
