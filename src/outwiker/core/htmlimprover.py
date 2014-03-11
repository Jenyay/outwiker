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

        # Компенсация восстановления переносов строк после списков
        ro0 = r"(?<=</[uo]l>)<p><br>(?=<[uo]l>)"
        result = re.sub(ro0, "\n\n", result, flags=re.I)

        # Сохраним исходный регистр тега <p>.
        result = re.sub ("<(p)>", r"</\1>\n\n<\1>", result, flags=re.I)

        blocktags = r"[uod]l|h[1-6]|pre|table|div|blockquote|hr"
        opentags = r"[uod]l|table"
        opentags += r"|" + opentags
        closetags = r"li|d[td]|t[rdh]|caption|thead|tfoot|tbody|colgroup|col"
        closetags += r"|" + closetags

        ro1 = r"<p>((?:<br>)?)(?=<(?:" + blocktags + r")[ >])"
        ro2 = r"(</(?:" + blocktags + r")>|<hr ?/?>)</p>"
        ro3 = r"(<(?:" + opentags + r")[ >]|</(?:" + closetags + r")>)[\s\n]*<br ?/?>"
        ro4 = r"<br ?/?>[\s\n]*(?=<(?:" + opentags + r")[ >]|<hr ?/?>)"
        ro5 = r"<p>(?=</)"
        ro6 = r"(?=<li>|</[uo]l>|<[bh]r ?/?>|<pre>)"

        result = re.sub(ro1, r"\1", result, flags=re.I)  # Удаление тега <P> перед некоторыми блочными элементами
        result = re.sub(ro2, r"\1", result, flags=re.I)  # Удаление тега </P> после некоторых блочных элементов
        result = re.sub(ro3, r"\1", result, flags=re.I)  # Удаление тега <BR> после некоторых блочных элементов
        result = re.sub(ro4, "", result, flags=re.I)     # Удаление тега <BR> перед некоторыми блочными элементами
        result = re.sub(ro5, "", result, flags=re.I)     # Удаление некоторого разного мусора/бесполезного кода
        result = re.sub(ro6, "\n", result, flags=re.I)   # Добавление переноса строки перед некоторыми элементами

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
            item = text[index: index + len (parts[n]) ]
            if n % 2 == 0:
                item = item.replace ("\n\n", "<p>")
                item = item.replace ("\n", "<br>")
                item = item.replace ("<br><li>", "<li>")

                item = item.replace ("<br><h1>", "<h1>")
                item = item.replace ("<br><h2>", "<h2>")
                item = item.replace ("<br><h3>", "<h3>")
                item = item.replace ("<br><h4>", "<h4>")
                item = item.replace ("<br><h5>", "<h5>")
                item = item.replace ("<br><h6>", "<h6>")
                index += len (parts[n]) + len (starttag)
            else:
                item = "<pre" + item + "</pre>"
                index += len (parts[n]) + len (endtag)

            result += item

        return result


    @staticmethod
    def ireplace (text, old, new):
        """
        Замена заглавных и прописных строк тегов
        """
        result = text.replace (old.lower(), new.lower())
        result = result.replace (old.upper(), new.upper())
        return result
