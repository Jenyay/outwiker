#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import re


class HtmlImprover (object):
    """
    Класс, который делает HTML более читаемым (где надо, расставляет переводы строк)
    """
    @staticmethod
    def run (text):
        """
        Сделать HTML более читаемым
        """
        text = HtmlImprover.__improveText (text)
        return text


    @staticmethod
    def __improveText (text):
        result = text.replace ("\r\n", "\n")
        result = HtmlImprover.__replaceEndlines (result)

        return result


    @staticmethod
    def __replaceEndlines (text):
        """
        Заменить переводы строк, но не трогать текст внутри <pre>...</pre>
        """
        text_lower = text.lower()

        starttag = "<pre"
        endtag = "</pre>"

        # Разобьем строку по <pre>
        part1 = text_lower.split (starttag)

        # Подстроки разобьем по </pre>
        parts2 = [item.split (endtag) for item in part1]

        # Склеим части в один массив
        parts = reduce (lambda x, y: x + y, parts2, [])

        # В четных элементах массива заменим переводы строк, а нечетные оставим как есть
        # Строки берем из исходного текста с учетом пропущенных в массиве тегов <pre> и </pre>
        result = u""
        index = 0

        for n in range (len (parts)):
            textitem = text[index: index + len (parts[n]) ]
            if n % 2 == 0:
                textitem = HtmlImprover.__improveTags (textitem)
                index += len (parts[n]) + len (starttag)
            else:
                textitem = "\n<pre" + textitem + "</pre>\n"
                index += len (parts[n]) + len (endtag)

            result += textitem

        return result


    @staticmethod
    def __improveTags (text):
        """
        Улучшения переводов строк до и после некоторых тегов
        """
        result = text
        result = result.replace ("\n", "<br>")

        opentags = r"[uod]l|hr|h\d"
        closetags = r"li|d[td]|t[rdh]|caption|thead|tfoot|tbody|colgroup|col|h\d"

        # Удаление тега <BR> перед некоторыми блочными элементами
        remove_br_before = r"<br\s*/?>[\s\n]*(?=<(?:" + opentags + r")[ >])"
        result = re.sub(remove_br_before, "", result, flags=re.I)

        # Удаление тега <BR> после некоторых блочных элементов
        remove_br_after = r"(<(?:" + opentags + r")[ >]|</(?:" + closetags + r")>)[\s\n]*<br\s*/?>"
        result = re.sub(remove_br_after, r"\1", result, flags=re.I)

        # Добавление переноса строки перед некоторыми элементами
        append_eol_before = r"\n*(<li>|<h\d>|</?[uo]l>|<hr\s*/?>|<p>)"
        result = re.sub(append_eol_before, "\n\\1", result, flags=re.I)

        # Добавление переноса строки после некоторых элементов
        append_eol_after = r"(<hr\s*/?>|<br\s*/?>|</\s*h\d>|</\s*p>|</\s*ul>)\n*"
        result = re.sub(append_eol_after, "\\1\n", result, flags=re.I)

        return result
