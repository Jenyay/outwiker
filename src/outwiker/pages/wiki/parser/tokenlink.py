# -*- coding: utf-8 -*-

import html
from typing import Optional, Tuple
from urllib.parse import quote

from pyparsing import QuotedString

from outwiker.core.attachment import Attachment
from outwiker.core.defines import PAGE_ATTACH_DIR
from outwiker.core.htmlformatter import HtmlFormatter
from outwiker.utilites.urls import is_url

from .tokenattach import AttachToken
from .htmlelements import (
    create_link_to_page,
    create_link_to_attached_file,
    create_invalid_attached_file,
    create_invalid_link_to_page,
)
import outwiker.core.cssclasses as css


class LinkFactory:
    @staticmethod
    def make(parser):
        return LinkToken(parser).getToken()


class LinkToken:
    linkStart = "[["
    linkEnd = "]]"
    attachString = "Attach:"

    def __init__(self, parser):
        self.parser = parser
        self.attach_prefix = PAGE_ATTACH_DIR + "/"
        self.page_protocol = "page://"

    def getToken(self):
        return QuotedString(
            LinkToken.linkStart,
            endQuoteChar=LinkToken.linkEnd,
            multiline=False,
            convertWhitespaceEscapes=False,
        ).setParseAction(self._convertToLink)("link")

    def _isHasImage(self, text: str) -> bool:
        return "<img" in text.lower()

    def _convertToLink(self, _s, _l, t):
        """
        Преобразовать ссылку
        """
        if "->" in t[0]:
            url, comment = self._splitArrow(t[0])
        elif "|" in t[0]:
            url, comment = self._splitPipe(t[0])
        else:
            url = t[0]
            comment = None

        if comment is not None:
            comment = self.parser.parseLinkMarkup(comment.strip())

        return self._convertToLinkWithComment(url, comment)

    def _splitArrow(self, text: str) -> Tuple[str, str]:
        """
        Преобразовать ссылки в виде [[comment -> url]]
        """
        comment, url = text.rsplit("->", 1)
        url_result = self._prepareUrl(url)
        comment_result = html.escape(comment, False)

        return url_result, comment_result

    def _splitPipe(self, text: str) -> Tuple[str, str]:
        """
        Преобразовать ссылки в виде [[url | comment]]
        """
        # Т.к. символ | может быть в ссылке и в тексте,
        # считаем, что после ссылки пользователь поставит пробел
        if " |" in text:
            url, comment = text.split(" |", 1)
        else:
            url, comment = text.rsplit("|", 1)

        url_result = self._prepareUrl(url)
        comment_result = html.escape(comment, False)

        return url_result, comment_result

    def _prepareUrl(self, url: str) -> str:
        """
        Подготовить адрес для ссылки.
        Если ссылка - прикрепленный файл, то создать путь до него
        """
        # Prepare URL to attached file
        if url.strip().startswith(AttachToken.attachString):
            url = url.strip()

            # Extract path to attached file
            url = url[len(AttachToken.attachString) :]
            url = self._removeQuotes(url)

            return f"{self.attach_prefix}{url}"

        return url

    def _removeQuotes(self, text):
        if (text.startswith("'") and text.endswith("'")) or (
            text.startswith('"') and text.endswith('"')
        ):
            text = text[1:-1]

        return text

    def _generateLinkToAttach(self, url: str, comment: Optional[str]) -> str:
        # Ссылка на прикрепление
        attach_name = self._removeQuotes(url[len(AttachToken.attachString) :])

        url = f"{self.attach_prefix}{attach_name}"
        comment_result = attach_name if comment is None else comment
        if Attachment(self.parser.page).exists(attach_name):
            return create_link_to_attached_file(url, comment_result)
        else:
            return create_invalid_attached_file(comment_result)

    def _generateAnchor(self, url: str) -> str:
        return HtmlFormatter().anchor(url[1:])

    def _convertToLinkWithComment(self, url: str, comment: Optional[str]) -> str:
        url = url.strip()

        if url.startswith(AttachToken.attachString):
            return self._generateLinkToAttach(
                url, comment.strip() if comment is not None else None
            )

        if (
            comment is None
            and url.startswith("#")
            and self.parser.page is not None
            and self.parser.page[url] is None
        ):
            # Ссылка начинается на #, но вложенoco ых страниц с таким именем нет,
            # значит это якорь
            return self._generateAnchor(url)

        if url.startswith(self.page_protocol):
            return self._generateLinkToPage(url, comment)

        if (
            not is_url(url)
            and not url.startswith(self.attach_prefix)
            and not url.startswith("#")
            and not url.startswith("mailto:")
        ):
            return self._generateLinkToPage(url, comment)

        comment = html.escape(url, False) if comment is None else comment.strip()
        if url.startswith(self.attach_prefix) and not self._isHasImage(comment):
            if Attachment(self.parser.page).exists(url[len(self.attach_prefix) :]):
                return create_link_to_attached_file(url, comment)
            else:
                return create_invalid_attached_file(comment)

        return HtmlFormatter().link(url, comment, [css.CSS_WIKI])

    def _generateLinkToPage(self, href: str, comment: Optional[str] = None) -> str:
        page_uid_src = (
            href[len(self.page_protocol) :]
            if href.startswith(self.page_protocol)
            else href
        )
        params_pos = page_uid_src.rfind("/#") or page_uid_src.rfind("/?")
        page_uid = page_uid_src[:params_pos] if params_pos != -1 else page_uid_src
        params = page_uid_src[params_pos:] if params_pos != -1 else ""

        current_page = self.parser.page

        page = (
            current_page[page_uid_src]
            or current_page.root[page_uid_src]
            or current_page.root.getPageByUid(page_uid)
        )

        url = self.page_protocol + quote(page_uid) + params

        if page is not None:
            if comment is None:
                comment = page.display_title if href.startswith(self.page_protocol) else href

            return create_link_to_page(url, comment)
        else:
            return create_invalid_link_to_page(
                url, href if comment is None else comment
            )
