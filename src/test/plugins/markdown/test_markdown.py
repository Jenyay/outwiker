# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.pages.wiki.wikipage import WikiPageFactory
from test.utils import removeDir
from outwiker.core.style import Style


class MarkdownTest(unittest.TestCase):
    """Markdown plug-in tests"""
    def setUp(self):
        self.__createWiki()
        dirlist = [u"../plugins/markdown"]
        self.loader = PluginsLoader(Application)
        self.loader.load(dirlist)

    def tearDown(self):
        removeDir(self.path)
        self.loader.clear()

    def __createWiki(self):
        # Здесь будет создаваться вики
        self.path = u"../test/testwiki"
        removeDir(self.path)

        self.rootwiki = WikiDocument.create(self.path)

        WikiPageFactory().create(self.rootwiki, u"Страница 1", [])
        self.testPage = self.rootwiki[u"Страница 1"]

    def __getHtmlByText(self, text):
        from markdown.markdownhtmlgenerator import MarkdownHtmlGenerator
        self.testPage.content = text

        generator = MarkdownHtmlGenerator(self.testPage)
        result = generator.makeHtml(Style().getPageStyle(self.testPage))
        return result

    def test_plugin_loading(self):
        self.assertEqual(len(self.loader), 1)

    def test_simple_text(self):
        text = u"бла-бла-бла"
        result = self.__getHtmlByText(text)
        self.assertIn(text, result)

    def test_strong_01(self):
        text = u"бла-бла-бла **полужирный шрифт** бла-бла"
        right_result = u"бла-бла-бла <strong>полужирный шрифт</strong> бла-бла"
        result = self.__getHtmlByText(text)
        self.assertIn(right_result, result)

    def test_strong_02(self):
        text = u"бла-бла-бла __полужирный шрифт__ бла-бла"
        right_result = u"бла-бла-бла <strong>полужирный шрифт</strong> бла-бла"
        result = self.__getHtmlByText(text)
        self.assertIn(right_result, result)

    def test_italic_01(self):
        text = u"бла-бла-бла *курсивный шрифт* бла-бла"
        right_result = u"бла-бла-бла <em>курсивный шрифт</em> бла-бла"
        result = self.__getHtmlByText(text)
        self.assertIn(right_result, result)

    def test_italic_02(self):
        text = u"бла-бла-бла _курсивный шрифт_ бла-бла"
        right_result = u"бла-бла-бла <em>курсивный шрифт</em> бла-бла"
        result = self.__getHtmlByText(text)
        self.assertIn(right_result, result)

    def test_strong_italic_01(self):
        text = u"бла-бла-бла ***полужирный курсив*** бла-бла"
        right_result = u"бла-бла-бла <strong><em>полужирный курсив</em></strong> бла-бла"
        result = self.__getHtmlByText(text)
        self.assertIn(right_result, result)

    def test_strong_italic_02(self):
        text = u"бла-бла-бла **_полужирный курсив_** бла-бла"
        right_result = u"бла-бла-бла <strong><em>полужирный курсив</em></strong> бла-бла"
        result = self.__getHtmlByText(text)
        self.assertIn(right_result, result)

    def test_header_01(self):
        text = u'''# Заголовок 1
## Заголовок 2
### Заголовок 3
#### Заголовок 4
##### Заголовок 5
###### Заголовок 6'''
        result = self.__getHtmlByText(text)

        self.assertIn(u'<h1>Заголовок 1</h1>', result)
        self.assertIn(u'<h2>Заголовок 2</h2>', result)
        self.assertIn(u'<h3>Заголовок 3</h3>', result)
        self.assertIn(u'<h4>Заголовок 4</h4>', result)
        self.assertIn(u'<h5>Заголовок 5</h5>', result)
        self.assertIn(u'<h6>Заголовок 6</h6>', result)

    def test_header_02(self):
        text = u'''
Заголовок 1
===========

Заголовок 2
-----------'''
        result = self.__getHtmlByText(text)

        self.assertIn(u'<h1>Заголовок 1</h1>', result)
        self.assertIn(u'<h2>Заголовок 2</h2>', result)

    def test_header_03(self):
        text = u''' # Это не заголовок'''
        result = self.__getHtmlByText(text)

        self.assertIn(u'# Это не заголовок', result)

    def test_header_04(self):
        text = u'''# Заголовок 1 #
## Заголовок 2 ##
### Заголовок 3 ###
#### Заголовок 4 ####
##### Заголовок 5 #####
###### Заголовок 6 ######'''
        result = self.__getHtmlByText(text)

        self.assertIn(u'<h1>Заголовок 1</h1>', result)
        self.assertIn(u'<h2>Заголовок 2</h2>', result)
        self.assertIn(u'<h3>Заголовок 3</h3>', result)
        self.assertIn(u'<h4>Заголовок 4</h4>', result)
        self.assertIn(u'<h5>Заголовок 5</h5>', result)
        self.assertIn(u'<h6>Заголовок 6</h6>', result)

    def test_header_05(self):
        text = u'''# Заголовок 1 #
## Заголовок 2 #
### Заголовок 3 #
#### Заголовок 4 #
##### Заголовок 5 #
###### Заголовок 6 #'''
        result = self.__getHtmlByText(text)

        self.assertIn(u'<h1>Заголовок 1</h1>', result)
        self.assertIn(u'<h2>Заголовок 2</h2>', result)
        self.assertIn(u'<h3>Заголовок 3</h3>', result)
        self.assertIn(u'<h4>Заголовок 4</h4>', result)
        self.assertIn(u'<h5>Заголовок 5</h5>', result)
        self.assertIn(u'<h6>Заголовок 6</h6>', result)

    def test_header_06(self):
        text = u'''# Заголовок 1 ######
## Заголовок 2 ######
### Заголовок 3 ######
#### Заголовок 4 ######
##### Заголовок 5 ######
###### Заголовок 6 ######'''
        result = self.__getHtmlByText(text)

        self.assertIn(u'<h1>Заголовок 1</h1>', result)
        self.assertIn(u'<h2>Заголовок 2</h2>', result)
        self.assertIn(u'<h3>Заголовок 3</h3>', result)
        self.assertIn(u'<h4>Заголовок 4</h4>', result)
        self.assertIn(u'<h5>Заголовок 5</h5>', result)
        self.assertIn(u'<h6>Заголовок 6</h6>', result)

    def test_hr_01(self):
        text = u'''---'''
        result = self.__getHtmlByText(text)
        self.assertIn(u'<hr>', result)

    def test_hr_02(self):
        text = u'''***'''
        result = self.__getHtmlByText(text)
        self.assertIn(u'<hr>', result)

    def test_hr_03(self):
        text = u'''* * *'''
        result = self.__getHtmlByText(text)
        self.assertIn(u'<hr>', result)

    def test_hr_04(self):
        text = u'''- - -'''
        result = self.__getHtmlByText(text)
        self.assertIn(u'<hr>', result)

    def test_quote_01(self):
        text = u'''> Строка 1
> Строка 2
> Строка 3
>
> Строка 4'''

        right_result = u'''<blockquote>
<p>Строка 1
Строка 2
Строка 3</p>
<p>Строка 4</p>
</blockquote>'''
        result = self.__getHtmlByText(text)
        self.assertIn(right_result, result)

    def test_quote_02(self):
        text = u'''> Строка 1
> Строка 2
> Строка 3'''

        right_result = u'''<blockquote>
<p>Строка 1
Строка 2
Строка 3</p>
</blockquote>'''
        result = self.__getHtmlByText(text)
        self.assertIn(right_result, result)

    def test_quote_03(self):
        text = u'''
> Строка 1
Строка 2
Строка 3'''

        right_result = u'''<blockquote>
<p>Строка 1
Строка 2
Строка 3</p>
</blockquote>'''
        result = self.__getHtmlByText(text)
        self.assertIn(right_result, result)

    def test_list_01(self):
        text = u'''
* Строка 1
* Строка 2
* Строка 3'''

        right_result = u'''<ul>
<li>Строка 1</li>
<li>Строка 2</li>
<li>Строка 3</li>
</ul>'''
        result = self.__getHtmlByText(text)
        self.assertIn(right_result, result)

    def test_list_02(self):
        text = u'''
+ Строка 1
+ Строка 2
+ Строка 3'''

        right_result = u'''<ul>
<li>Строка 1</li>
<li>Строка 2</li>
<li>Строка 3</li>
</ul>'''
        result = self.__getHtmlByText(text)
        self.assertIn(right_result, result)

    def test_list_03(self):
        text = u'''
- Строка 1
- Строка 2
- Строка 3'''

        right_result = u'''<ul>
<li>Строка 1</li>
<li>Строка 2</li>
<li>Строка 3</li>
</ul>'''
        result = self.__getHtmlByText(text)
        self.assertIn(right_result, result)

    def test_list_04(self):
        text = u'''
1. Строка 1
1. Строка 2
1. Строка 3'''

        right_result = u'''<ol>
<li>Строка 1</li>
<li>Строка 2</li>
<li>Строка 3</li>
</ol>'''
        result = self.__getHtmlByText(text)
        self.assertIn(right_result, result)

    def test_code_01(self):
        text = u'''
    import os
    import sys'''

        result = self.__getHtmlByText(text)
        self.assertIn(u'<div class="codehilite">', result)

    def test_code_03(self):
        text = u'''Use the `printf()` function.'''

        right_result = u'''Use the <code>printf()</code> function.'''
        result = self.__getHtmlByText(text)
        self.assertIn(right_result, result)

    def test_code_04(self):
        text = u'''Use the ``printf()`` function.'''

        right_result = u'''Use the <code>printf()</code> function.'''
        result = self.__getHtmlByText(text)
        self.assertIn(right_result, result)

    def test_link_01(self):
        text = u'''[Пример ссылки](http://example.com/ "Заголовок")'''

        right_result = u'''<a href="http://example.com/" title="Заголовок">Пример ссылки</a>'''
        result = self.__getHtmlByText(text)
        self.assertIn(right_result, result)

    def test_link_02(self):
        text = u'''[Пример ссылки](http://example.com/)'''

        right_result = u'''<a href="http://example.com/">Пример ссылки</a>'''
        result = self.__getHtmlByText(text)
        self.assertIn(right_result, result)

    def test_link_03(self):
        text = u'''[Пример ссылки][идентификатор]

[идентификатор]: http://example.com/  "Заголовок"
'''

        right_result = u'''<a href="http://example.com/" title="Заголовок">Пример ссылки</a>'''
        result = self.__getHtmlByText(text)
        self.assertIn(right_result, result)

    def test_link_04(self):
        text = u'''[Пример ссылки][идентификатор]

[идентификатор]: http://example.com/
'''

        right_result = u'''<a href="http://example.com/">Пример ссылки</a>'''
        result = self.__getHtmlByText(text)
        self.assertIn(right_result, result)

    def test_link_05(self):
        text = u'''[Google][]

[Google]: http://google.com/
'''

        right_result = u'''<a href="http://google.com/">Google</a>'''
        result = self.__getHtmlByText(text)
        self.assertIn(right_result, result)

    def test_link_06(self):
        text = u'''[идентификатор]

[идентификатор]: http://example.com/  "Заголовок"
'''

        right_result = u'''<a href="http://example.com/" title="Заголовок">идентификатор</a>'''
        result = self.__getHtmlByText(text)
        self.assertIn(right_result, result)

    def test_link_07(self):
        text = u'''[идентификатор]

[идентификатор]: http://example.com/
'''

        right_result = u'''<a href="http://example.com/">идентификатор</a>'''
        result = self.__getHtmlByText(text)
        self.assertIn(right_result, result)

    def test_link_08(self):
        text = u'''<http://example.com/>'''

        right_result = u'''<a href="http://example.com/">http://example.com/</a>'''
        result = self.__getHtmlByText(text)
        self.assertIn(right_result, result)

    def test_image_01(self):
        text = u'''![Текст](__attach/basket.png)'''
        right_result = u'''<img alt="Текст" src="__attach/basket.png">'''
        result = self.__getHtmlByText(text)
        self.assertIn(right_result, result)

    def test_image_02(self):
        text = u'''![Текст](__attach/basket.png "Заголовок")'''
        right_result = u'''<img alt="Текст" src="__attach/basket.png" title="Заголовок">'''
        result = self.__getHtmlByText(text)
        self.assertIn(right_result, result)

    def test_image_03(self):
        text = u'''![Alt text][id]
[id]: __attach/camera.png  "Заголовок"'''

        right_result = u'''<img alt="Alt text" src="__attach/camera.png" title="Заголовок">'''
        result = self.__getHtmlByText(text)
        self.assertIn(right_result, result)
