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

		result = HtmlImprover.ireplace (result, "<P>", "</P>\n\n<P>")
		result = HtmlImprover.ireplace (result, "<BR>", "\n<BR>")
		result = HtmlImprover.ireplace (result, "<BR/>", "\n<BR/>")

		result = HtmlImprover.ireplace (result, "<LI>", "\n<LI>")
		result = HtmlImprover.ireplace (result, "<UL>", "\n<UL>")
		result = HtmlImprover.ireplace (result, "</UL>", "\n</UL>")
		result = HtmlImprover.ireplace (result, "<OL>", "\n<OL>")
		result = HtmlImprover.ireplace (result, "</OL>", "\n</OL>")
		
		result = HtmlImprover.ireplace (result, "<PRE>", "\n<PRE>")

		return result

	
	@staticmethod
	def __replaceEndlines (text):
		"""
		Заменить переводы строк, но не трогать текст внутри <PRE>...</PRE>
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
				item = item.replace ("\n\n", "<P>")
				item = item.replace ("\n", "<BR>")
				item = item.replace ("<BR><LI>", "<LI>")
				index += len (parts[n]) + len (starttag)
			else:
				item = "<PRE>" + item + "</PRE>"
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
