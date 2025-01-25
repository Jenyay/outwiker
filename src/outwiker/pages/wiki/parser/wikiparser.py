# -*- coding: utf-8 -*-

import traceback

from outwiker.core.htmlformatter import HtmlFormatter
from outwiker.core.thumbnails import Thumbnails
from outwiker.core.application import ApplicationParams
import outwiker.core.cssclasses as css

from .markup import Markup
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
from .tokenwikistyle import WikiStyleInlineFactory, WikiStyleBlockFactory
from .tokencomment import CommentFactory
from .tokenmultilineblock import MultilineBlockFactory


class Parser:
    def __init__(self, page, application: ApplicationParams):
        self.page = page
        self.application = application
        self.config = application.config
        self._html_formatter = HtmlFormatter([css.CSS_WIKI])

        # Dictionary with nonstandard parameters (for plugins for example)
        self.customProps = {}

        # Массив строк, которые надо добавить в заголовок страницы
        self.__headers = []

        self.__footers = []

        # Команды, которые обрабатывает парсер.
        # Формат команд: (:name params... :) content...(:nameend:)
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
        self.wikistyle_block = WikiStyleBlockFactory.make(self)
        self.comment = CommentFactory.make(self)
        self.multiline_block = MultilineBlockFactory.make(self)

        # Common wiki tokens
        self.wikiTokens = [
            self.attachImages,
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
            self.comment,
            self.thumb,
            self.underlined,
            self.strike,
            self.horline,
            self.align,
            self.lists,
            self.table,
            self.headings,
            self.wikistyle_block,
            self.wikistyle_inline,
            self.command,
            self.multiline_block,
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
            self.multiline_block,
        ]

        # Tokens for using inside headings
        self.headingTokens = [
            self.attachImages,
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
            self.comment,
            self.thumb,
            self.underlined,
            self.strike,
            self.horline,
            self.align,
            self.wikistyle_inline,
            self.command,
            self.multiline_block,
        ]

        # Tokens for using inside text
        self.textLevelTokens = [
            self.attachImages,
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
            self.comment,
            self.thumb,
            self.underlined,
            self.strike,
            self.horline,
            self.wikistyle_block,
            self.wikistyle_inline,
            self.command,
            self.multiline_block,
        ]

        # Tokens for using inside list items (bullets and numeric)
        self.listItemsTokens = [
            self.attachImages,
            self.attaches,
            self.urlImage,
            self.url,
            self.text,
            self.multiline_block,
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
            self.comment,
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
        return "".join(self.__headers)

    def appendToHead(self, header):
        """
        Добавить строку в заголовок
        """
        self.__headers.append(header)

    @property
    def headItems(self):
        """
        Return list of the strings for the <head> HTML tag.
        """
        return self.__headers

    @property
    def footer(self):
        return "".join(self.__footers)

    @property
    def footerItems(self):
        return self.__footers

    def appendToFooter(self, footer):
        self.__footers.append(footer)

    def toHtml(self, text):
        """
        Сгенерить HTML без заголовков типа <html> и т.п.
        """
        thumb = Thumbnails(self.page)
        thumb.clearDir()

        return self.parseWikiMarkup(text)

    def _parseMarkup(self, markup, tokens, text) -> str:
        if markup is None:
            markup = self._createMarkup(tokens)

        try:
            return markup.transformString(text)
        except Exception:
            error = traceback.format_exc()
            return self._html_formatter.error(error)

    def parseWikiMarkup(self, text: str) -> str:
        return self._parseMarkup(self._wikiMarkup, self.wikiTokens, text)

    def parseListItemMarkup(self, text: str) -> str:
        return self._parseMarkup(self._listItemMarkup, self.listItemsTokens, text)

    def parseLinkMarkup(self, text: str) -> str:
        return self._parseMarkup(self._linkMarkup, self.linkTokens, text)

    def parseHeadingMarkup(self, text: str) -> str:
        return self._parseMarkup(self._headingMarkup, self.headingTokens, text)

    def parseTextLevelMarkup(self, text):
        return self._parseMarkup(self._textLevelMarkup, self.textLevelTokens, text)

    def addCommand(self, command):
        self.commands[command.name] = command

    def removeCommand(self, commandName):
        if commandName in self.commands:
            del self.commands[commandName]
