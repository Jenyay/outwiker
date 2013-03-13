#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path
import unittest

from outwiker.core.application import Application
from outwiker.core.htmltemplate import HtmlTemplate
from outwiker.core.system import getTemplatesDir
from outwiker.core.htmlimprover import HtmlImprover
from outwiker.gui.guiconfig import HtmlRenderConfig


class HtmlTemplateTest(unittest.TestCase):
    def setUp(self):
        self.config = HtmlRenderConfig (Application.config)
        self.__clearConfig()


    def tearDown (self):
        self.__clearConfig()


    def __clearConfig (self):
        # self.config.userStyle.value = u""
        # self.config.fontFamily.value = u"Verdana"
        # self.config.fontSize.value = 10
        Application.config.remove_section (HtmlRenderConfig.HTML_SECTION)


    def testDefault (self):
        content = u"бла-бла-бла"
        result_right = u"""<!DOCTYPE html>
<HTML>
<HEAD>
	<META HTTP-EQUIV='CONTENT-TYPE' CONTENT='TEXT/HTML; CHARSET=UTF-8'/>

	<STYLE type="text/css">
		body, div, p, table {
			font-size:10pt;
			font-family:Verdana;
		}

		img{border:none}
		
	</STYLE>
	
</HEAD>

<BODY>
<P>бла-бла-бла</P>
</BODY>
</HTML>"""

        templatepath = os.path.join (getTemplatesDir(), "__default", "__style.html")
        tpl = HtmlTemplate (templatepath)
        result = tpl.substitute (content=content)

        self.assertEqual (result, result_right, result)


    def testChangeFontName (self):
        self.config.fontName.value = u"Arial"

        content = u"бла-бла-бла"
        result_right = u"""<!DOCTYPE html>
<HTML>
<HEAD>
	<META HTTP-EQUIV='CONTENT-TYPE' CONTENT='TEXT/HTML; CHARSET=UTF-8'/>

	<STYLE type="text/css">
		body, div, p, table {
			font-size:10pt;
			font-family:Arial;
		}

		img{border:none}
		
	</STYLE>
	
</HEAD>

<BODY>
<P>бла-бла-бла</P>
</BODY>
</HTML>"""

        templatepath = os.path.join (getTemplatesDir(), "__default", "__style.html")
        tpl = HtmlTemplate (templatepath)
        result = tpl.substitute (content=content)

        self.assertEqual (result, result_right, result)


    def testChangeFontSize (self):
        self.config.fontSize.value = 20
        content = u"бла-бла-бла"
        result_right = u"""<!DOCTYPE html>
<HTML>
<HEAD>
	<META HTTP-EQUIV='CONTENT-TYPE' CONTENT='TEXT/HTML; CHARSET=UTF-8'/>

	<STYLE type="text/css">
		body, div, p, table {
			font-size:20pt;
			font-family:Verdana;
		}

		img{border:none}
		
	</STYLE>
	
</HEAD>

<BODY>
<P>бла-бла-бла</P>
</BODY>
</HTML>"""

        templatepath = os.path.join (getTemplatesDir(), "__default", "__style.html")
        tpl = HtmlTemplate (templatepath)
        result = tpl.substitute (content=content)

        self.assertEqual (result, result_right, result)


    def testChangeUserStyle (self):
        style = u"p {background-color: maroon; color: white; }"

        self.config.userStyle.value = style

        content = u"бла-бла-бла"
        
        templatepath = os.path.join (getTemplatesDir(), "__default", "__style.html")
        tpl = HtmlTemplate (templatepath)
        result = tpl.substitute (content=content)

        self.assertTrue (style in result, result)


    def testChangeUserStyleRussian (self):
        style = u"p {background-color: maroon; /* Цвет фона под текстом параграфа */ color: white; /* Цвет текста */ }"

        self.config.userStyle.value = style

        content = u"бла-бла-бла"
        
        templatepath = os.path.join (getTemplatesDir(), "__default", "__style.html")
        tpl = HtmlTemplate (templatepath)
        result = tpl.substitute (content=content)

        self.assertTrue (style in result, result)


    def testImproved1 (self):
        src = u"""<UL><LI>Несортированный список. Элемент 1</LI><LI>Несортированный список. Элемент 2</LI><LI>Несортированный список. Элемент 3</LI><OL><LI>Вложенный сортированный список. Элемент 1</LI><LI>Вложенный сортированный список. Элемент 2</LI><LI>Вложенный сортированный список. Элемент 3</LI><LI>Вложенный сортированный список. Элемент 4</LI><UL><LI>Совсем вложенный сортированный список. Элемент 1</LI><LI>Совсем вложенный сортированный список. Элемент 2</LI></UL><LI>Вложенный сортированный список. Элемент 5</LI></OL><UL><LI>Вложенный несортированный список. Элемент 1</LI></UL></UL>"""

        expectedResult = u"""<!DOCTYPE html>
<HTML>
<HEAD>
	<META HTTP-EQUIV='CONTENT-TYPE' CONTENT='TEXT/HTML; CHARSET=UTF-8'/>

	<STYLE type="text/css">
		body, div, p, table {
			font-size:10pt;
			font-family:Verdana;
		}

		img{border:none}
		
	</STYLE>
	
</HEAD>

<BODY>
<P>
<UL>
<LI>Несортированный список. Элемент 1</LI>
<LI>Несортированный список. Элемент 2</LI>
<LI>Несортированный список. Элемент 3</LI>
<OL>
<LI>Вложенный сортированный список. Элемент 1</LI>
<LI>Вложенный сортированный список. Элемент 2</LI>
<LI>Вложенный сортированный список. Элемент 3</LI>
<LI>Вложенный сортированный список. Элемент 4</LI>
<UL>
<LI>Совсем вложенный сортированный список. Элемент 1</LI>
<LI>Совсем вложенный сортированный список. Элемент 2</LI>
</UL>
<LI>Вложенный сортированный список. Элемент 5</LI>
</OL>
<UL>
<LI>Вложенный несортированный список. Элемент 1</LI>
</UL>
</UL></P>
</BODY>
</HTML>"""

        templatepath = os.path.join (getTemplatesDir(), "__default", "__style.html")
        tpl = HtmlTemplate (templatepath)

        result = tpl.substitute (HtmlImprover.run (src) )
        self.assertEqual (expectedResult, result, result)


    def testImproved2 (self):
        src = ur"""<H2>Attach links</H2><P>Attach:file.odt<BR><A HREF="__attach/file.odt">file.odt</A><BR><A HREF="__attach/file.odt">alternative text</A><BR><A HREF="__attach/file with spaces.pdf">file with spaces.pdf</A><P><H2>Images</H2>"""

        expectedResult = ur"""<!DOCTYPE html>
<HTML>
<HEAD>
	<META HTTP-EQUIV='CONTENT-TYPE' CONTENT='TEXT/HTML; CHARSET=UTF-8'/>

	<STYLE type="text/css">
		body, div, p, table {
			font-size:10pt;
			font-family:Verdana;
		}

		img{border:none}
		
	</STYLE>
	
</HEAD>

<BODY>
<P>
<H2>Attach links</H2></P>

<P>Attach:file.odt
<BR><A HREF="__attach/file.odt">file.odt</A>
<BR><A HREF="__attach/file.odt">alternative text</A>
<BR><A HREF="__attach/file with spaces.pdf">file with spaces.pdf</A></P>

<P>
<H2>Images</H2></P>
</BODY>
</HTML>"""

        templatepath = os.path.join (getTemplatesDir(), "__default", "__style.html")
        tpl = HtmlTemplate (templatepath)

        result = tpl.substitute (HtmlImprover.run (src) )
        self.assertEqual (expectedResult, result, result)


    def testException (self):
        templatepath = os.path.join (getTemplatesDir(), "html_invalid")
        self.assertRaises (IOError, HtmlTemplate, templatepath)
