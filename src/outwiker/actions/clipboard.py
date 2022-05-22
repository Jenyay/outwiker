# -*- coding: utf-8 -*-

from outwiker.gui.baseaction import BaseAction
from outwiker.core.commands import (copyTitleToClipboard,
                                    copyLinkToClipboard,
                                    copyPathToClipboard,
                                    copyAttachPathToClipboard,
                                    showInfo)


class CopyPageTitleAction(BaseAction):
    """
    Копировать в буфер обмена заголовок текущей страницы
    """
    stringId = "CopyPageTitle"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Copy Page Title")

    @property
    def description(self):
        return _("Copy current page title to clipboard")

    def run(self, params):
        assert self._application.selectedPage is not None
        if copyTitleToClipboard(self._application.selectedPage):
            title = _('Copied to clipboard')
            text = _('Page title has been copied to the clipboard')
            showInfo(self._application.mainWindow, title, text)


class CopyPagePathAction(BaseAction):
    """
    Копировать в буфер обмена путь до текущей страницы
    """
    stringId = u"CopyPagePath"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Copy Page Path")

    @property
    def description(self):
        return _("Copy path to current page to clipboard")

    def run(self, params):
        assert self._application.selectedPage is not None
        if copyPathToClipboard(self._application.selectedPage):
            title = _('Copied to clipboard')
            text = _('Path to the page has been copied to the clipboard')
            showInfo(self._application.mainWindow, title, text)


class CopyAttachPathAction(BaseAction):
    """
    Копировать в буфер обмена путь до прикрепленных файлов
    """
    stringId = "CopyAttachPath"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Copy Attachments Path")

    @property
    def description(self):
        return _("Copy path to attachments for current page to clipboard")

    def run(self, params):
        assert self._application.selectedPage is not None
        if copyAttachPathToClipboard(self._application.selectedPage, True):
            title = _('Copied to clipboard')
            text = _('Path to the page attachments has been copied to the clipboard')
            showInfo(self._application.mainWindow, title, text)


class CopyPageLinkAction(BaseAction):
    """
    Копировать в буфер обмена ссылку на текущую страницу
    """
    stringId = u"CopyPageLink"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _("Copy Page Link")

    @property
    def description(self):
        return _("Copy link to current page to clipboard")

    def run(self, params):
        assert self._application.selectedPage is not None
        if copyLinkToClipboard(self._application.selectedPage):
            title = _('Copied to clipboard')
            text = _('Link to the page has been copied to the clipboard')
            showInfo(self._application.mainWindow, title, text)
