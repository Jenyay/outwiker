#!/usr/bin/env python
# -*- coding: UTF-8 -*-

class HtmlImprover (object):
    """
    Класс, который делает HTML более читаемым (где надо, расставляет переводы строк)
    """
    @staticmethod
    def run (text):
        """
        Сделать HTML более читаемым
        """
        return HtmlImprover.__improveText (text)


    @staticmethod
    def __improveText (text):
        result = text.replace ("\r\n", "\n")
        result = HtmlImprover.__replaceEndlines (result)

        result = HtmlImprover.ireplace (result, "<p>", "</p>\n\n<p>")
        result = HtmlImprover.ireplace (result, "<br>", "\n<br>")
        result = HtmlImprover.ireplace (result, "<br/>", "\n<br/>")

        result = HtmlImprover.ireplace (result, "<li>", "\n<li>")
        result = HtmlImprover.ireplace (result, "<ul>", "\n<ul>")
        result = HtmlImprover.ireplace (result, "</ul>", "\n</ul>")
        result = HtmlImprover.ireplace (result, "<ol>", "\n<ol>")
        result = HtmlImprover.ireplace (result, "</ol>", "\n</ol>")

        result = HtmlImprover.ireplace (result, "<h1>", "\n<h1>")
        result = HtmlImprover.ireplace (result, "<h2>", "\n<h2>")
        result = HtmlImprover.ireplace (result, "<h3>", "\n<h3>")
        result = HtmlImprover.ireplace (result, "<h4>", "\n<h4>")
        result = HtmlImprover.ireplace (result, "<h5>", "\n<h5>")
        result = HtmlImprover.ireplace (result, "<h6>", "\n<h6>")
        
        result = HtmlImprover.ireplace (result, "<pre>", "\n<pre>")

        return result

    
    @staticmethod
    def __replaceEndlines (text):
        """
        Заменить переводы строк, но не трогать текст внутри <pre>...</pre>
        """
        text_lower = text.lower()

        starttag = "<pre>"
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
                item = "<pre>" + item + "</pre>"
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
