# -*- coding: utf-8 -*-

from datetime import datetime
import os

from outwiker.core.attachment import Attachment
from outwiker.utilites.textfile import readTextFile

from jinja2 import (Environment, meta, FileSystemLoader,
                    TemplateSyntaxError, TemplateNotFound)
import snippets.defines as defines
from snippets.i18n import get_


class SnippetException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


def _convertExceptions(func):
    '''
    Decorator to convert Jinja's errors and other errors to SnippetException.
    '''
    def _process(self, *args, **kwargs):
        global _
        _ = get_()

        try:
            return func(self, *args, **kwargs)
        except TemplateNotFound as e:
            text = _(u'Snippet "{name}" not found').format(
                name=e.name
            )
            raise SnippetException(text)
        except TemplateSyntaxError as e:
            text = _(u'Snippet error at line {line}:\n{text}').format(
                line=e.lineno,
                text=e.message
            )
            raise SnippetException(text)
        except EnvironmentError as e:
            text = _(u'Snippet reading error:\n{text}').format(
                text=str(e)
            )
            raise SnippetException(text)
        except BaseException as e:
            text = _(u'Snippet processing error:\n{text}').format(
                text=str(e)
            )
            raise SnippetException(text)

    return _process


class SnippetParser(object):
    def __init__(self, template, dirname, application):
        self._template = template
        self._application = application
        self._dirname = dirname
        self._jinja_env = Environment(loader=FileSystemLoader(self._dirname))

    @_convertExceptions
    def process(self, selectedText, page, **kwargs):
        params = self._getGlobalVariables(selectedText, page)
        params.update(kwargs)
        tpl = self._jinja_env.from_string(self._template, globals=params)
        result = tpl.render()
        return result

    @_convertExceptions
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
        globals = {
            defines.VAR_DATE: datetime.now(),
        }

        if page is not None:
            attach = Attachment(page)
            attachList = VarList([fname
                                  for fname
                                  in sorted(attach.getAttachRelative())
                                  if not fname.startswith(u'__')])

            globals_page = {
                defines.VAR_SEL_TEXT: selectedText,
                defines.VAR_TITLE: page.display_title,
                defines.VAR_SUBPATH: page.subpath,
                defines.VAR_ATTACH: attach.getAttachPath(True),
                defines.VAR_FOLDER: page.path,
                defines.VAR_PAGE_ID: self._application.pageUidDepot.createUid(page),
                defines.VAR_DATE_CREATING: page.creationdatetime,
                defines.VAR_DATE_EDITIND: page.datetime,
                defines.VAR_TAGS: VarList(sorted(page.tags)),
                defines.VAR_PAGE_TYPE: page.getTypeString(),
                defines.VAR_CHILDLIST: VarList([subpage.title
                                                for subpage
                                                in page.children]),
                defines.VAR_ATTACHLIST: attachList,
            }
            globals.update(globals_page)

        return globals


class VarList(object):
    def __init__(self, data):
        self._data = tuple(data)

    def __len__(self):
        return len(self._data)

    def __getitem__(self, i):
        return self._data[i]

    def __str__(self):
        return ', '.join(self._data)

    def __iter__(self):
        return iter(self._data)
