#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path
import unittest

from outwiker.core.htmltemplate import HtmlTemplate
from outwiker.core.system import getTemplatesDir
from outwiker.core.htmlimprover import HtmlImprover


class HtmlTemplateTest(unittest.TestCase):
    def setUp(self):
        pass


    def test1(self):
        content = u"бла-бла-бла"
        result_right = u"""<HTML>
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

        templatepath = os.path.join (getTemplatesDir(), "html")
        tpl = HtmlTemplate (templatepath)
        result = tpl.substitute (content=content)

        self.assertEqual (result, result_right, result)


    def testImproved1 (self):
        src = u"""<UL><LI>Несортированный список. Элемент 1</LI><LI>Несортированный список. Элемент 2</LI><LI>Несортированный список. Элемент 3</LI><OL><LI>Вложенный сортированный список. Элемент 1</LI><LI>Вложенный сортированный список. Элемент 2</LI><LI>Вложенный сортированный список. Элемент 3</LI><LI>Вложенный сортированный список. Элемент 4</LI><UL><LI>Совсем вложенный сортированный список. Элемент 1</LI><LI>Совсем вложенный сортированный список. Элемент 2</LI></UL><LI>Вложенный сортированный список. Элемент 5</LI></OL><UL><LI>Вложенный несортированный список. Элемент 1</LI></UL></UL>"""

        expectedResult = u"""<HTML>
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

        templatepath = os.path.join (getTemplatesDir(), "html")
        tpl = HtmlTemplate (templatepath)

        result = tpl.substitute (HtmlImprover.run (src) )
        self.assertEqual (expectedResult, result, result)


    def testImproved2 (self):
        src = ur"""<H2>Attach links</H2><P>Attach:file.odt<BR><A HREF="__attach/file.odt">file.odt</A><BR><A HREF="__attach/file.odt">alternative text</A><BR><A HREF="__attach/file with spaces.pdf">file with spaces.pdf</A><P><H2>Images</H2>"""

        expectedResult = ur"""<HTML>
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
<P><H2>Attach links</H2></P>

<P>Attach:file.odt
<BR><A HREF="__attach/file.odt">file.odt</A>
<BR><A HREF="__attach/file.odt">alternative text</A>
<BR><A HREF="__attach/file with spaces.pdf">file with spaces.pdf</A></P>

<P><H2>Images</H2></P>
</BODY>
</HTML>"""

        templatepath = os.path.join (getTemplatesDir(), "html")
        tpl = HtmlTemplate (templatepath)

        result = tpl.substitute (HtmlImprover.run (src) )
        self.assertEqual (expectedResult, result, result)


    def testException (self):
        templatepath = os.path.join (getTemplatesDir(), "html_invalid")
        self.assertRaises (IOError, HtmlTemplate, templatepath)
