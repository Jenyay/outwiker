# -*- coding: utf-8 -*-

import logging
import os
from typing import Optional

import wx

from outwiker.api.core.tree import testreadonly
from outwiker.api.gui.dialogs.messagebox import MessageBox
from outwiker.api.services.messages import showError
from outwiker.core.application import Application
from outwiker.core.events import PostWikiOpenParams, PreWikiOpenParams
from outwiker.core.exceptions import ReadonlyException, RootFormatError
from outwiker.core.tree import WikiDocument
from outwiker.gui.longprocessrunner import LongProcessRunner
from outwiker.gui.testeddialog import TestedFileDialog


logger = logging.getLogger('outwiker.api.services.tree')


@testreadonly
def removePage(page: 'outwiker.core.tree.WikiPage'):
    assert page is not None

    if page.readonly:
        raise ReadonlyException

    if page.parent is None:
        showError(Application.mainWindow, _(
            "You can't remove the root element"))
        return

    if (MessageBox(_('Remove page "{}" and all subpages?\nAll attached files will also be deleted.').format(page.title),
                   _("Remove page?"),
                   wx.YES_NO | wx.ICON_QUESTION) == wx.YES):
        try:
            page.remove()
        except IOError:
            showError(Application.mainWindow, _("Can't remove page"))


def openWikiWithDialog(parent, readonly=False):
    """
    Показать диалог открытия вики и вернуть открытую wiki
    parent -- родительское окно
    """
    wikiroot = None

    with TestedFileDialog(parent,
                          wildcard="__page.opt|__page.opt",
                          style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as dialog:
        if dialog.ShowModal() == wx.ID_OK:
            fullpath = dialog.GetPath()
            path = os.path.dirname(fullpath)
            wikiroot = openWiki(path, readonly)

    return wikiroot


def openWiki(path: str, readonly: bool = False) -> Optional[WikiDocument]:
    def threadFunc(path, readonly):
        try:
            return WikiDocument.load(path, readonly)
        except Exception as e:
            return e

    logger.debug('Opening notes tree from: {}'.format(path))
    if not os.path.exists(path):
        _canNotLoadWikiMessage(path)
        return None

    preWikiOpenParams = PreWikiOpenParams(path, readonly)
    Application.onPreWikiOpen(Application.selectedPage,
                              preWikiOpenParams)
    if preWikiOpenParams.abortOpen:
        logger.debug('Opening notes tree aborted')
        return None

    # The path may be changed in event handlers
    path = preWikiOpenParams.path
    logger.debug('Notes tree path after onPreWikiOpen: {}'.format(path))

    # Если передан путь до файла настроек (а не до папки с вики),
    # то оставим только папку
    if not os.path.isdir(path):
        path = os.path.split(path)[0]

    runner = LongProcessRunner(threadFunc,
                               Application.mainWindow,
                               _("Loading"),
                               _("Opening notes tree..."))
    result = runner.run(os.path.realpath(path), readonly)

    success = False
    if isinstance(result, RootFormatError):
        _rootFormatErrorHandle(path, readonly)
    elif isinstance(result, Exception):
        logger.error(result)
        _canNotLoadWikiMessage(path)
    else:
        Application.wikiroot = result
        success = True

    postWikiOpenParams = PostWikiOpenParams(path, readonly, success)
    Application.onPostWikiOpen(Application.selectedPage,
                               postWikiOpenParams)

    return Application.wikiroot


def _canNotLoadWikiMessage(path):
    """
    Вывести сообщение о том, что невоможно открыть вики
    """
    logger.warning("Can't load notes tree: {}".format(path))
    text = _("Can't load notes tree:\n") + path
    showError(Application.mainWindow, text)


def _rootFormatErrorHandle(path, readonly):
    """
    Обработчик исключения outwiker.core.exceptions.RootFormatError
    """
    if readonly:
        # Если вики открыт только для чтения, то нельзя изменять файлы
        _canNotLoadWikiMessage(path)
        return

    if (_wantClearWikiOptions(path) != wx.YES):
        return

    # Обнулим файл __page.opt
    WikiDocument.clearConfigFile(path)

    # Попробуем открыть вики еще раз
    try:
        # Загрузить вики
        wikiroot = WikiDocument.load(os.path.realpath(path), readonly)
        Application.wikiroot = wikiroot
    except IOError:
        _canNotLoadWikiMessage(path)

    except outwiker.core.exceptions.RootFormatError:
        _canNotLoadWikiMessage(path)

    finally:
        pass


def _wantClearWikiOptions(path):
    """
    Сообщение о том, хочет ли пользователь сбросить файл __page.opt
    """
    return MessageBox(_("Can't load wiki '%s'\nFile __page.opt is invalid.\nClear this file and load wiki?\nBookmarks will be lost") % path,
                      _("__page.opt error"),
                      wx.ICON_ERROR | wx.YES_NO)
