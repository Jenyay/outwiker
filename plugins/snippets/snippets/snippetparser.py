# -*- coding: UTF-8 -*-

import os

from outwiker.core.attachment import Attachment
from outwiker.utilites.textfile import readTextFile

from jinja2 import Environment, meta, FileSystemLoader
import snippets.defines as defines


class SnippetParser(object):
    def __init__(self, template, dirname, application):
        self._template = template
        self._application = application
        self._dirname = dirname
        self._jinja_env = Environment(loader=FileSystemLoader(self._dirname))

    def process(self, selectedText, page, **kwargs):
        assert self._application.selectedPage is not None
        params = self._getGlobalVariables(selectedText, page)
        params.update(kwargs)
        tpl = self._jinja_env.from_string(self._template, globals=params)
        result = tpl.render()
        return result

    def getVariables(self):
        variables = set()
        self._getVariables(self._template, variables)
        return variables

    def _getVariables(self, text, var_set):
        ast = self._jinja_env.parse(text)
        var_set.update(meta.find_undeclared_variables(ast))

        for tpl_fname in meta.find_referenced_templates(ast):
            fname = os.path.join(self._dirname, tpl_fname)
            try:
                text = readTextFile(fname)
                self._getVariables(text, var_set)
            except EnvironmentError:
                pass

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
