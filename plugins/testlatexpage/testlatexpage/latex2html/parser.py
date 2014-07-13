# -*- coding: UTF-8 -*-

import re
import traceback

from tokens.tokenfonts import FontsFactory
from tokens.tokentext import TextFactory
from tokens.tokentable import TableFactory


class Parser (object):
    def __init__ (self):
        self._transctiption = {
            r"\\textturnv": u"ʌ",
            r"\\textschwa": u"ə",
            r"\\ae": u"æ",
            r"\\textscripta": u"ɑ",
            r"\\textopeno": u"ɔ",
            r"\\textsci": u"ɪ",
            r"\\textrevepsilon": u"ɜ",
            r"\\textesh": u"ʃ",
            r"\\texttheta": u"θ",
            r"\\textteshlig": u"ʧ",
            r"\\textyogh": u"ʒ",
            r"\\textdyoghlig": u"ʤ",
            r"\\dh": u"ð",
            r"\\ng": u"ŋ",
            r"\\textscriptv": u"ʋ",
            r"\\textturnscripta": u"ɒ",
            r"\\symbol\{0}": u"ˈ",
            r"\\textsecstress": u"ˌ",
            r"\\textscriptg": u"ɡ",
            r"\\textlengthmark": u"ː",
        }

        self._symbols = {
            r"<<": u"&laquo;",
            r">>": u"&raquo;",
            r"``": u"&laquo;",
            r"''": u"&raquo;",
            r"~": u" ",
        }

        self._error_template = u"<b>{error}</b>"

        self.italic = FontsFactory.makeItalic (self)
        self.bold = FontsFactory.makeBold (self)
        self.section = FontsFactory.makeSection (self)
        self.table = TableFactory.make(self)
        self.text = TextFactory.make(self)

        self._texMarkup = (
            self.text |
            self.italic |
            self.bold |
            self.section |
            self.table
        )


    def convert (self, text):
        """
        В переданном тексте функция преобразует транскрипции TeX в Unicode и возвращает результат
        """
        result = text


        try:
            result = self._texMarkup.transformString (result)
        except Exception:
            result = self._error_template.format (error = traceback.format_exc())

        result = self._replaceDash (result)
        result = self._replaceSymbols (result)
        result = self._removeTranscriptions (result)
        result = self._clearTex (result)

        return result


    def _replaceSymbols (self, text):
        """
        Функция делает замены некоторых команд TeX
        """
        result = text
        for symbol, html in self._transctiption.items():
            result = re.sub (symbol + r"\s*", html, result, flags=re.I | re.M | re.U)

        for symbol, html in self._symbols.items():
            result = result.replace (symbol, html)

        return result


    def _removeTranscriptions (self, text):
        result = re.sub (ur"\\textipa{\s*(.*?)\s*}", r"\1", text, flags=re.U)
        result = result.replace (ur"\textipa", "")

        return result


    def _replaceDash (self, text):
        result = text.replace (u"---", u"&mdash;")
        result = result.replace (u"--", u"&ndash;")

        return result


    def _clearTex (self, text):
        """
        Удаление остатков TeX, которые не нужно преобразовывать
        """
        # Список регулярных выражений
        commands = [
            ur"\\large\s+",
            ur"\\small\s+",
        ]

        result = text

        for command in commands:
            result = re.sub (command, u"", result, flags=re.U | re.S | re.M)

        return result
