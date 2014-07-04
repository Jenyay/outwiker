# -*- coding: UTF-8 -*-

import re


class Parser (object):
    def __init__ (self):
        self._symbols = {
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
            r"<<": u"&laquo;",
            r">>": u"&raquo;",
            r"~": u" ",
        }


    def convert (self, text):
        """
        В переданном тексте функция преобразует транскрипции TeX в Unicode и возвращает результат
        """
        result = self._replaceSymbols (text)
        result = self._removeTranscriptions (result)
        result = self._replaceDash (result)

        return result


    def _replaceSymbols (self, text):
        """
        Функция делает замены команды TeX в Unicode
        """
        result = text
        for symbol, html in self._symbols.items():
            result = re.sub (symbol + r"\s*", html, result, flags=re.I | re.M | re.U)

        return result


    def _removeTranscriptions (self, text):
        result = re.sub (ur"\\textipa{\s*(.*?)\s*}", r"\1", text, flags=re.U)
        result = result.replace (ur"\textipa", "")

        return result


    def _replaceDash (self, text):
        result = text.replace (u"---", u"&mdash;")
        result = result.replace (u"--", u"&ndash;")

        return result
