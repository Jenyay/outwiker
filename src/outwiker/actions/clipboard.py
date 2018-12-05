# -*- coding: utf-8 -*-

from outwiker.gui.baseaction import BaseAction
from outwiker.core.commands import (copyTitleToClipboard,
                                    copyLinkToClipboard,
                                    copyPathToClipboard,
                                    copyAttachPathToClipboard)


class CopyPageTitleAction (BaseAction):
    """
    Копировать в буфер обмена заголовок текущей страницы
    """
    stringId = u"CopyPageTitle"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _(u"Copy Page Title")

    @property
    def description(self):
        return _(u"Copy current page title to clipboard")

    def run(self, params):
        assert self._application.selectedPage is not None
        copyTitleToClipboard(self._application.selectedPage)


class CopyPagePathAction (BaseAction):
    """
    Копировать в буфер обмена путь до текущей страницы
    """
    stringId = u"CopyPagePath"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _(u"Copy Page Path")

    @property
    def description(self):
        return _(u"Copy path to current page to clipboard")

    def run(self, params):
        assert self._application.selectedPage is not None
        copyPathToClipboard(self._application.selectedPage)


class CopyAttachPathAction (BaseAction):
    """
    Копировать в буфер обмена путь до прикрепленных файлов
    """
    stringId = u"CopyAttachPath"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _(u"Copy Attachments Path")

    @property
    def description(self):
        return _(u"Copy path to attachments for current page to clipboard")

    def run(self, params):
        assert self._application.selectedPage is not None
        copyAttachPathToClipboard(self._application.selectedPage)


class CopyPageLinkAction (BaseAction):
    """
    Копировать в буфер обмена ссылку на текущую страницу
    """
    stringId = u"CopyPageLink"

    def __init__(self, application):
        self._application = application

    @property
    def title(self):
        return _(u"Copy Page Link")

    @property
    def description(self):
        return _(u"Copy link to current page to clipboard")

    def run(self, params):
        assert self._application.selectedPage is not None
        copyLinkToClipboard(self._application.selectedPage)
