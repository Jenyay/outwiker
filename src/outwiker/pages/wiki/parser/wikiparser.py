#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import traceback

from tokenfonts import FontsFactory
from tokennoformat import NoFormatFactory
from tokenpreformat import PreFormatFactory
from tokenthumbnail import ThumbnailFactory
from tokenheading import HeadingFactory
from tokenadhoc import AdHocFactory
from tokenhorline import HorLineFactory
from tokenlink import LinkFactory
from tokenalign import AlignFactory
from tokentable import TableFactory
from tokenurl import UrlFactory
from tokenurlimage import UrlImageFactory
from tokenattach import AttachFactory, AttachImagesFactory
from tokenlist import ListFactory
from tokenlinebreak import LineBreakFactory
from tokentex import TexFactory
from tokencommand import CommandFactory
from tokentext import TextFactory

from ..thumbnails import Thumbnails


class Parser (object):
    def __init__ (self, page, config):
        self.page = page
        self.config = config
        self.error_template = u"<B>{error}</B>"

        # Массив строк, которые надо добавить в заголовок страницы
        self.__headers = []

        # Команды, обрабатывает парсер.
        # Формат команд: (:name params... :) content... (:nameend:)
        # Ключ - имя команды, значение - экземпляр класса команды
        self.commands = {}

        self.italicized = FontsFactory.makeItalic (self)
        self.bolded = FontsFactory.makeBold (self)
        self.boldItalicized = FontsFactory.makeBoldItalic (self)
        self.underlined = FontsFactory.makeUnderline (self)
        self.strike = FontsFactory.makeStrike (self)
        self.subscript = FontsFactory.makeSubscript (self)
        self.superscript = FontsFactory.makeSuperscript (self)
        self.code = FontsFactory.makeCode (self)
        self.headings = HeadingFactory.make(self)
        self.thumb = ThumbnailFactory.make(self)
        self.noformat = NoFormatFactory.make(self)
        self.preformat = PreFormatFactory.make (self)
        self.horline = HorLineFactory.make(self)
        self.link = LinkFactory.make (self)
        self.align = AlignFactory.make(self)
        self.table = TableFactory.make(self)
        self.url = UrlFactory.make (self)
        self.urlImage = UrlImageFactory.make (self)
        self.attaches = AttachFactory.make (self)
        self.attachImages = AttachImagesFactory.make (self)
        self.adhoctokens = AdHocFactory.make(self)
        self.lists = ListFactory.make (self)
        self.lineBreak = LineBreakFactory.make (self)
        self.tex = TexFactory.make (self)
        self.command = CommandFactory.make (self)
        self.text = TextFactory.make(self)

        self.listItemMarkup = (self.attaches |
                self.urlImage |
                self.url |
                self.text | 
                self.lineBreak |
                self.link |
                self.boldItalicized |
                self.bolded |
                self.italicized |
                self.code |
                self.preformat |
                self.noformat |
                self.thumb |
                self.underlined |
                self.strike |
                self.subscript |
                self.superscript |
                self.attaches |
                self.tex |
                self.command
                )


        self.wikiMarkup = (self.attaches |
                self.urlImage |
                self.url |
                self.text | 
                self.lineBreak |
                self.link |
                self.adhoctokens |
                self.subscript |
                self.superscript |
                self.boldItalicized |
                self.bolded |
                self.italicized |
                self.code |
                self.preformat |
                self.noformat |
                self.thumb |
                self.underlined |
                self.strike |
                self.horline |
                self.align |
                self.lists |
                self.table |
                self.headings |
                self.tex |
                self.command
                )

        # Нотация для ссылок
        self.linkMarkup = (self.attachImages |
                self.urlImage |
                self.text | 
                self.adhoctokens |
                self.subscript |
                self.superscript |
                self.boldItalicized |
                self.bolded |
                self.italicized |
                self.underlined |
                self.strike |
                self.tex |
                self.command |
                self.noformat
                )

        # Нотация для заголовков
        self.headingMarkup = (self.text | 
                self.adhoctokens |
                self.subscript |
                self.superscript |
                self.boldItalicized |
                self.bolded |
                self.italicized |
                self.underlined |
                self.strike |
                self.tex |
                self.command |
                self.noformat
                )


    @property
    def head (self):
        """
        Свойство возвращает строку из добавленных заголовочных элементов (то, что должно быть внутри тега <HEAD>...</HEAD>)
        """
        return u"\n".join (self.__headers)


    def appendToHead (self, header):
        """
        Добавить строку в заголовок
        """
        self.__headers.append (header)


    def toHtml (self, text):
        """
        Сгенерить HTML без заголовков типа <HTML> и т.п.
        """
        thumb = Thumbnails (self.page)
        thumb.clearDir()

        text = text.replace ("\\\n", "")
        return self.parseWikiMarkup(text)


    def parseWikiMarkup (self, text):
        try:
            return self.wikiMarkup.transformString (text)
        except Exception, e:
            return self.error_template.format (error = traceback.format_exc())


    def parseListItemMarkup (self, text):
        try:
            return self.listItemMarkup.transformString (text)
        except Exception, e:
            return self.error_template.format (error = traceback.format_exc())


    def parseLinkMarkup (self, text):
        try:
            return self.linkMarkup.transformString (text)
        except Exception, e:
            return self.error_template.format (error = traceback.format_exc())


    def parseHeadingMarkup (self, text):
        try:
            return self.headingMarkup.transformString (text)
        except Exception, e:
            return self.error_template.format (error = traceback.format_exc())


    def addCommand (self, command):
        self.commands[command.name] = command
