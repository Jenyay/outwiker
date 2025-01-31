from typing import Optional
import outwiker.app.services.clipboard as _clipboard
from outwiker.api.core import Application


def copyTextToClipboard(text: str) -> bool:
    return _clipboard.copyTextToClipboard(text)


def getClipboardText() -> Optional[str]:
    return _clipboard.getClipboardText()


def copyPathToClipboard(page) -> bool:
    """
    Копировать путь до страницы в буфер обмена
    """
    return copyPathToClipboard(page.path)


def copyAttachPathToClipboard(page, is_current_page: bool = False) -> bool:
    """
    Копировать путь до папки с прикрепленными файлами в буфер обмена
    """
    return _clipboard.copyAttachPathToClipboard(page, is_current_page)


def copyLinkToClipboard(page, application: Application) -> bool:
    """
    Копировать ссылку на страницу в буфер обмена
    """
    return _clipboard.copyLinkToClipboard(page, application)


def copyTitleToClipboard(page) -> bool:
    """
    Копировать заголовок страницы в буфер обмена
    """
    return _clipboard.copyTitleToClipboard(page)
