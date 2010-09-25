#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Класс для более наглядного оформления кода HTML после вики-парсера
"""

class HtmlImprover (object):
	def __init__ (self):
		pass


	#@staticmethod
	#def run (text):
	#	return HtmlImprover.improveHtml (text)

	@staticmethod
	def run (text):
		"""
		Сделать HTML более читаемым
		"""
		result = HtmlImprover.ireplace (text, "<p>", "\n\n<p>")
		result = HtmlImprover.ireplace (result, "<br>", "\n<br>")
		result = HtmlImprover.ireplace (result, "<br/>", "\n<br/>")

		result = HtmlImprover.ireplace (result, "<html>", "<html>\n")
		result = HtmlImprover.ireplace (result, "</html>", "\n</html>")
		
		result = HtmlImprover.ireplace (result, "<head>", "<head>\n")
		result = HtmlImprover.ireplace (result, "</head>", "\n</head>")
		
		result = HtmlImprover.ireplace (result, "<body>", "\n<body>\n")
		result = HtmlImprover.ireplace (result, "</body>", "\n</body>")
		
		result = HtmlImprover.ireplace (result, "<li>", "\n<li>")
		result = HtmlImprover.ireplace (result, "<ul>", "\n<ul>")
		result = HtmlImprover.ireplace (result, "</ul>", "\n</ul>")
		result = HtmlImprover.ireplace (result, "<ol>", "\n<ol>")
		result = HtmlImprover.ireplace (result, "</ol>", "\n</ol>")
		
		result = HtmlImprover.ireplace (result, "<pre>", "\n<pre>")
		#result = HtmlImprover.ireplace (result, "</pre>", "\n</pre>")

		return result


	@staticmethod
	def ireplace (text, old, new):
		"""
		Замена заглавных и прописных строк тегов
		"""
		result = text.replace (old.lower(), new.lower())
		result = result.replace (old.upper(), new.upper())
		return result
