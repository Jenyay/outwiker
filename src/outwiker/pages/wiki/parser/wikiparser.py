# -*- coding: utf-8 -*-

import traceback

from .tokenfonts import FontsFactory
from .tokennoformat import NoFormatFactory
from .tokenpreformat import PreFormatFactory
from .tokenthumbnail import ThumbnailFactory
from .tokenheading import HeadingFactory
from .tokenadhoc import AdHocFactory
from .tokenhorline import HorLineFactory
from .tokenlink import LinkFactory
from .tokenalign import AlignFactory
from .tokentable import TableFactory
from .tokenurl import UrlFactory
from .tokenurlimage import UrlImageFactory
from .tokenattach import AttachFactory, AttachImagesFactory
from .tokenlist import ListFactory
from .tokenlinebreak import LineBreakFactory
from .tokenlinejoin import LineJoinFactory
from .tokencommand import CommandFactory
from .tokentext import TextFactory
from .tokenquote import QuoteFactory
from .tokenwikistyle import WikiStyleInlineFactory

from ..thumbnails import Thumbnails
from outwiker.libs.pyparsing import NoMatch


class Parser(object):
    def __init__(self, page, config):
        self.page = page
        self.config = config
        self.error_template = u"<b>{error}</b>"

        # Dictionary with nonstandard parameters(for plugins for example)
        self.customProps = {}

        # Массив строк, которые надо добавить в заголовок страницы
        self.__headers = []

        self.__footers = []

        # Команды, которые обрабатывает парсер.
        # Формат команд:(:name params... :) content...(:nameend:)
        # Ключ - имя команды, значение - экземпляр класса команды
        self.commands = {}

        self.italicized = FontsFactory.makeItalic(self)
        self.bolded = FontsFactory.makeBold(self)
        self.boldItalicized = FontsFactory.makeBoldItalic(self)
        self.underlined = FontsFactory.makeUnderline(self)
        self.strike = FontsFactory.makeStrike(self)
        self.subscript = FontsFactory.makeSubscript(self)
        self.superscript = FontsFactory.makeSuperscript(self)
        self.quote = QuoteFactory.make(self)
        self.code = FontsFactory.makeCode(self)
        self.mark = FontsFactory.makeMark(self)
        self.small = FontsFactory.makeSmall(self)
        self.big = FontsFactory.makeBig(self)
        self.headings = HeadingFactory.make(self)
        self.thumb = ThumbnailFactory.make(self)
        self.noformat = NoFormatFactory.make(self)
        self.preformat = PreFormatFactory.make(self)
        self.horline = HorLineFactory.make(self)
        self.link = LinkFactory.make(self)
        self.align = AlignFactory.make(self)
        self.table = TableFactory.make(self)
        self.url = UrlFactory.make(self)
        self.urlImage = UrlImageFactory.make(self)
        self.attaches = AttachFactory.make(self)
        self.attachImages = AttachImagesFactory.make(self)
        self.adhoctokens = AdHocFactory.make(self)
        self.lists = ListFactory.make(self)
        self.lineBreak = LineBreakFactory.make(self)
        self.lineJoin = LineJoinFactory.make(self)
        self.command = CommandFactory.make(self)
        self.text = TextFactory.make(self)
        self.wikistyle_inline = WikiStyleInlineFactory.make(self)

        # Common wiki tokens
        self.wikiTokens = [
            self.attaches,
            self.urlImage,
            self.url,
            self.text,
            self.lineBreak,
            self.lineJoin,
            self.link,
            self.adhoctokens,
            self.subscript,
            self.superscript,
            self.boldItalicized,
            self.bolded,
            self.italicized,
            self.code,
            self.mark,
            self.small,
            self.big,
            self.quote,
            self.preformat,
            self.noformat,
            self.thumb,
            self.underlined,
            self.strike,
            self.horline,
            self.align,
            self.lists,
            self.table,
            self.headings,
            self.wikistyle_inline,
            self.command,
        ]

        # Tokens for using inside links
        self.linkTokens = [
            self.attachImages,
            self.urlImage,
            self.text,
            self.adhoctokens,
            self.subscript,
            self.superscript,
            self.boldItalicized,
            self.bolded,
            self.italicized,
            self.underlined,
            self.small,
            self.big,
            self.mark,
            self.strike,
            self.command,
            self.lineBreak,
            self.lineJoin,
            self.noformat,
            self.wikistyle_inline,
        ]

        # Tokens for using inside headings
        self.headingTokens = [
            self.attaches,
            self.urlImage,
            self.url,
            self.text,
            self.lineBreak,
            self.lineJoin,
            self.link,
            self.adhoctokens,
            self.subscript,
            self.superscript,
            self.boldItalicized,
            self.bolded,
            self.italicized,
            self.small,
            self.big,
            self.mark,
            self.noformat,
            self.thumb,
            self.underlined,
            self.strike,
            self.horline,
            self.align,
            self.wikistyle_inline,
            self.command,
        ]

        # Tokens for using inside text
        self.textLevelTokens = [
            self.attaches,
            self.urlImage,
            self.url,
            self.text,
            self.lineBreak,
            self.lineJoin,
            self.link,
            self.adhoctokens,
            self.subscript,
            self.superscript,
            self.boldItalicized,
            self.bolded,
            self.italicized,
            self.code,
            self.mark,
            self.small,
            self.big,
            self.noformat,
            self.thumb,
            self.underlined,
            self.strike,
            self.horline,
            self.wikistyle_inline,
            self.command,
        ]

        # Tokens for using inside list items(bullets and numeric)
        self.listItemsTokens = [
            self.attaches,
            self.urlImage,
            self.url,
            self.text,
            self.lineBreak,
            self.lineJoin,
            self.link,
            self.boldItalicized,
            self.bolded,
            self.italicized,
            self.code,
            self.mark,
            self.small,
            self.big,
            self.preformat,
            self.noformat,
            self.thumb,
            self.underlined,
            self.strike,
            self.subscript,
            self.superscript,
            self.quote,
            self.attaches,
            self.wikistyle_inline,
            self.command,
        ]

        self._wikiMarkup = None
        self._listItemMarkup = None
        self._linkMarkup = None
        self._headingMarkup = None
        self._textLevelMarkup = None

    def _createMarkup(self, tokens_list):
        return Markup(tokens_list)

    @property
    def head(self):
        """
        Свойство возвращает строку из добавленных заголовочных элементов
        (то, что должно быть внутри тега <head>...</head>)
        """
        return u"".join(self.__headers)

    def appendToHead(self, header):
        """
        Добавить строку в заголовок
        """
        self.__headers.append(header)

    @property
    def headItems(self):
        '''
        Return list of the strings for the <head> HTML tag.

        Added in outwiker.core 1.3
        '''
        return self.__headers

    @property
    def footer(self):
        '''
        Added in outwiker.core 1.3
        '''
        return u''.join(self.__footers)

    @property
    def footerItems(self):
        '''
        Added in outwiker.core 1.3
        '''
        return self.__footers

    def appendToFooter(self, footer):
        """
        Added in outwiker.core 1.3
        """
        self.__footers.append(footer)

    def toHtml(self, text):
        """
        Сгенерить HTML без заголовков типа <HTML> и т.п.
        """
        thumb = Thumbnails(self.page)
        thumb.clearDir()

        return self.parseWikiMarkup(text)

    def parseWikiMarkup(self, text):
        if self._wikiMarkup is None:
            self._wikiMarkup = self._createMarkup(self.wikiTokens)

        try:
            return self._wikiMarkup.transformString(text)
        except Exception:
            error = traceback.format_exc()
            return self.error_template.format(error=error)

    def parseListItemMarkup(self, text):
        if self._listItemMarkup is None:
            self._listItemMarkup = self._createMarkup(self.listItemsTokens)

        try:
            return self._listItemMarkup.transformString(text)
        except Exception:
            error = traceback.format_exc()
            return self.error_template.format(error=error)

    def parseLinkMarkup(self, text):
        if self._linkMarkup is None:
            self._linkMarkup = self._createMarkup(self.linkTokens)

        try:
            return self._linkMarkup.transformString(text)
        except Exception:
            error = traceback.format_exc()
            return self.error_template.format(error=error)

    def parseHeadingMarkup(self, text):
        if self._headingMarkup is None:
            self._headingMarkup = self._createMarkup(self.headingTokens)

        try:
            return self._headingMarkup.transformString(text)
        except Exception:
            error = traceback.format_exc()
            return self.error_template.format(error=error)

    def parseTextLevelMarkup(self, text):
        if self._textLevelMarkup is None:
            self._textLevelMarkup = self._createMarkup(self.textLevelTokens)

        try:
            return self._textLevelMarkup.transformString(text)
        except Exception:
            error = traceback.format_exc()
            return self.error_template.format(error=error)

    def addCommand(self, command):
        self.commands[command.name] = command

    def removeCommand(self, commandName):
        if commandName in self.commands:
            del self.commands[commandName]


class Markup(object):
    def __init__(self, tokens_list):
        self._markup = NoMatch()
        for token in tokens_list:
            self._markup |= token

    def transformString(self, text):
        return self._markup.transformString(text)
