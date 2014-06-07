# -*- coding: UTF-8 -*-

import os.path
import unittest

from outwiker.core.application import Application
from outwiker.core.htmltemplate import HtmlTemplate
from outwiker.core.system import getTemplatesDir, readTextFile
from outwiker.core.htmlimprover import HtmlImprover
from outwiker.gui.guiconfig import HtmlRenderConfig


class HtmlTemplateTest(unittest.TestCase):
    def setUp(self):
        self.config = HtmlRenderConfig (Application.config)
        self.__clearConfig()
        self.maxDiff = None


    def tearDown (self):
        self.__clearConfig()


    def __clearConfig (self):
        Application.config.remove_section (HtmlRenderConfig.HTML_SECTION)


    def testDefault (self):
        content = u"бла-бла-бла"
        result_right = u"""<!DOCTYPE html>
<html>
<head>
	<meta http-equiv='X-UA-Compatible' content='IE=edge' />
	<meta http-equiv='content-type' content='text/html; charset=utf-8'/>

	<style type='text/css'>
		body, div, p, table {
			font-size:10pt;
			font-family:Verdana;
		}

		img{border:none}
		
	</style>
	
</head>

<body>
бла-бла-бла
</body>
</html>"""

        templatepath = os.path.join (getTemplatesDir(), "__default", "__style.html")
        tpl = HtmlTemplate (readTextFile (templatepath).strip() )
        result = tpl.substitute (content=content)

        self.assertEqual (result, result_right, result)


    def testChangeFontName (self):
        self.config.fontName.value = u"Arial"

        content = u"бла-бла-бла"
        result_right = u"""<!DOCTYPE html>
<html>
<head>
	<meta http-equiv='X-UA-Compatible' content='IE=edge' />
	<meta http-equiv='content-type' content='text/html; charset=utf-8'/>

	<style type='text/css'>
		body, div, p, table {
			font-size:10pt;
			font-family:Arial;
		}

		img{border:none}
		
	</style>
	
</head>

<body>
бла-бла-бла
</body>
</html>"""

        templatepath = os.path.join (getTemplatesDir(), "__default", "__style.html")
        tpl = HtmlTemplate (readTextFile (templatepath).strip() )
        result = tpl.substitute (content=content)

        self.assertEqual (result, result_right, result)


    def testChangeFontSize (self):
        self.config.fontSize.value = 20
        content = u"бла-бла-бла"
        result_right = u"""<!DOCTYPE html>
<html>
<head>
	<meta http-equiv='X-UA-Compatible' content='IE=edge' />
	<meta http-equiv='content-type' content='text/html; charset=utf-8'/>

	<style type='text/css'>
		body, div, p, table {
			font-size:20pt;
			font-family:Verdana;
		}

		img{border:none}
		
	</style>
	
</head>

<body>
бла-бла-бла
</body>
</html>"""

        templatepath = os.path.join (getTemplatesDir(), "__default", "__style.html")
        tpl = HtmlTemplate (readTextFile (templatepath).strip() )
        result = tpl.substitute (content=content)

        self.assertEqual (result, result_right, result)


    def testChangeUserStyle (self):
        style = u"p {background-color: maroon; color: white; }"

        self.config.userStyle.value = style

        content = u"бла-бла-бла"
        
        templatepath = os.path.join (getTemplatesDir(), "__default", "__style.html")
        tpl = HtmlTemplate (readTextFile (templatepath).strip() )
        result = tpl.substitute (content=content)

        self.assertTrue (style in result, result)


    def testChangeUserStyleRussian (self):
        style = u"p {background-color: maroon; /* Цвет фона под текстом параграфа */ color: white; /* Цвет текста */ }"

        self.config.userStyle.value = style

        content = u"бла-бла-бла"
        
        templatepath = os.path.join (getTemplatesDir(), "__default", "__style.html")
        tpl = HtmlTemplate (readTextFile (templatepath).strip() )
        result = tpl.substitute (content=content)

        self.assertTrue (style in result, result)


    def testImproved1 (self):
        src = u"""<ul><li>Несортированный список. Элемент 1</li><li>Несортированный список. Элемент 2</li><li>Несортированный список. Элемент 3</li><ol><li>Вложенный сортированный список. Элемент 1</li><li>Вложенный сортированный список. Элемент 2</li><li>Вложенный сортированный список. Элемент 3</li><li>Вложенный сортированный список. Элемент 4</li><ul><li>Совсем вложенный сортированный список. Элемент 1</li><li>Совсем вложенный сортированный список. Элемент 2</li></ul><li>Вложенный сортированный список. Элемент 5</li></ol><ul><li>Вложенный несортированный список. Элемент 1</li></ul></ul>"""

        expectedResult = u"""<!DOCTYPE html>
<html>
<head>
	<meta http-equiv='X-UA-Compatible' content='IE=edge' />
	<meta http-equiv='content-type' content='text/html; charset=utf-8'/>

	<style type='text/css'>
		body, div, p, table {
			font-size:10pt;
			font-family:Verdana;
		}

		img{border:none}
		
	</style>
	
</head>

<body>

<ul>
<li>Несортированный список. Элемент 1</li>
<li>Несортированный список. Элемент 2</li>
<li>Несортированный список. Элемент 3</li>
<ol>
<li>Вложенный сортированный список. Элемент 1</li>
<li>Вложенный сортированный список. Элемент 2</li>
<li>Вложенный сортированный список. Элемент 3</li>
<li>Вложенный сортированный список. Элемент 4</li>
<ul>
<li>Совсем вложенный сортированный список. Элемент 1</li>
<li>Совсем вложенный сортированный список. Элемент 2</li>
</ul>
<li>Вложенный сортированный список. Элемент 5</li>
</ol>
<ul>
<li>Вложенный несортированный список. Элемент 1</li>
</ul>
</ul>

</body>
</html>"""

        templatepath = os.path.join (getTemplatesDir(), "__default", "__style.html")
        tpl = HtmlTemplate (readTextFile (templatepath).strip() )

        result = tpl.substitute (HtmlImprover.run (src) )
        self.assertEqual (expectedResult, result, result)


    def testImproved2 (self):
        src = ur"""<h2>Attach links</h2>Attach:file.odt<br><a href="__attach/file.odt">file.odt</a><br><a href="__attach/file.odt">alternative text</a><br><a href="__attach/file with spaces.pdf">file with spaces.pdf</a><h2>Images</h2>"""

        expectedResult = ur"""<!DOCTYPE html>
<html>
<head>
	<meta http-equiv='X-UA-Compatible' content='IE=edge' />
	<meta http-equiv='content-type' content='text/html; charset=utf-8'/>

	<style type='text/css'>
		body, div, p, table {
			font-size:10pt;
			font-family:Verdana;
		}

		img{border:none}
		
	</style>
	
</head>

<body>

<h2>Attach links</h2>
Attach:file.odt<br>
<a href="__attach/file.odt">file.odt</a><br>
<a href="__attach/file.odt">alternative text</a><br>
<a href="__attach/file with spaces.pdf">file with spaces.pdf</a>
<h2>Images</h2>

</body>
</html>"""

        templatepath = os.path.join (getTemplatesDir(), "__default", "__style.html")
        tpl = HtmlTemplate (readTextFile (templatepath).strip() )

        result = tpl.substitute (HtmlImprover.run (src) )
        self.assertEqual (expectedResult, result)
