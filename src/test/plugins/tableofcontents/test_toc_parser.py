# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application


class TOC_ParserTest (unittest.TestCase):
    """Тесты плагина TableOfContents"""
    def setUp (self):
        dirlist = ["../plugins/tableofcontents"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)


    def tearDown (self):
        self.loader.clear()


    def testPluginLoad (self):
        self.assertEqual (len (self.loader), 1)


    def testParser_01 (self):
        from tableofcontents.contentsparser import ContentsParser

        parser = ContentsParser()

        text = ""

        contents = parser.parse (text)

        self.assertEqual (contents, [])


    def testParser_02 (self):
        from tableofcontents.contentsparser import ContentsParser

        parser = ContentsParser()

        text = '''  !! Абырвалг'''

        contents = parser.parse (text)

        self.assertEqual (contents, [])

    def testParser_03 (self):
        from tableofcontents.contentsparser import ContentsParser

        parser = ContentsParser()

        text = '''!! Абырвалг'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 1)
        self.assertEqual (contents[0].title, "Абырвалг")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, "")


    def testParser_04 (self):
        from tableofcontents.contentsparser import ContentsParser

        parser = ContentsParser()

        text = '''!!    Абырвалг    '''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 1)
        self.assertEqual (contents[0].title, "Абырвалг")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, "")


    def testParser_05 (self):
        from tableofcontents.contentsparser import ContentsParser

        parser = ContentsParser()

        text = '''!! Абырвалг 123'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 1)
        self.assertEqual (contents[0].title, "Абырвалг 123")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, "")


    def testParser_06 (self):
        from tableofcontents.contentsparser import ContentsParser

        parser = ContentsParser()

        text = '''!! Абырвалг\\
 123'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 1)
        self.assertEqual (contents[0].title, '''Абырвалг 123''')
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, "")


    def testParser_07 (self):
        from tableofcontents.contentsparser import ContentsParser

        parser = ContentsParser()

        text = '''!! Абырвалг 123
!!! Абырвалг 234'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 2)
        self.assertEqual (contents[0].title, "Абырвалг 123")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, "")

        self.assertEqual (contents[1].title, "Абырвалг 234")
        self.assertEqual (contents[1].level, 2)
        self.assertEqual (contents[1].anchor, "")


    def testParser_08 (self):
        from tableofcontents.contentsparser import ContentsParser

        parser = ContentsParser()

        text = '''!! Абырвалг 123

!!! Абырвалг 234'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 2)
        self.assertEqual (contents[0].title, "Абырвалг 123")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, "")

        self.assertEqual (contents[1].title, "Абырвалг 234")
        self.assertEqual (contents[1].level, 2)
        self.assertEqual (contents[1].anchor, "")


    def testParser_09 (self):
        from tableofcontents.contentsparser import ContentsParser

        parser = ContentsParser()

        text = '''ывп ыфвп ваы

!! Абырвалг 123

ывапыва ывп выап
выапывп ываап ывап

!!! Абырвалг 234'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 2)
        self.assertEqual (contents[0].title, "Абырвалг 123")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, "")

        self.assertEqual (contents[1].title, "Абырвалг 234")
        self.assertEqual (contents[1].level, 2)
        self.assertEqual (contents[1].anchor, "")


    def testParser_10 (self):
        from tableofcontents.contentsparser import ContentsParser

        parser = ContentsParser()

        text = '''ывп ыфвп ваы

!! Абырвалг 123

[=
!! Это не заголовок
=]

ывапыва ывп выап
выапывп ываап ывап

!!! Абырвалг 234'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 2)
        self.assertEqual (contents[0].title, "Абырвалг 123")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, "")

        self.assertEqual (contents[1].title, "Абырвалг 234")
        self.assertEqual (contents[1].level, 2)
        self.assertEqual (contents[1].anchor, "")


    def testParser_11 (self):
        from tableofcontents.contentsparser import ContentsParser

        parser = ContentsParser()

        text = '''ывп ыфвп ваы

!! Абырвалг 123

[=   
dsfasdf
!! Это не заголовок

asdf
=]   

ывапыва ывп выап
выапывп ываап ывап 

!!! Абырвалг 234'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 2)
        self.assertEqual (contents[0].title, "Абырвалг 123")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, "")

        self.assertEqual (contents[1].title, "Абырвалг 234")
        self.assertEqual (contents[1].level, 2)
        self.assertEqual (contents[1].anchor, "")


    def testParser_12 (self):
        from tableofcontents.contentsparser import ContentsParser

        parser = ContentsParser()

        text = '''ывп ыфвп ваы

!! Абырвалг 123

ывапыва ывп выап
выапывп ываап ывап 

!!! Абырвалг 234

фывафыва

!!!! Еще один заголовок

фывафыва
'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 3)


    def testParser_13 (self):
        from tableofcontents.contentsparser import ContentsParser

        parser = ContentsParser()

        text = '''ывп ыфвп ваы

!! [[#якорь1]]Абырвалг 123

ывапыва ывп выап
выапывп ываап ывап 

!!! [[#якорь2]] Абырвалг 234

фывафыва

!!!! Еще один заголовок

фывафыва
'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 3)
        self.assertEqual (contents[0].title, "Абырвалг 123")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, "якорь1")

        self.assertEqual (contents[1].title, "Абырвалг 234")
        self.assertEqual (contents[1].level, 2)
        self.assertEqual (contents[1].anchor, "якорь2")


    def testParser_14 (self):
        from tableofcontents.contentsparser import ContentsParser

        parser = ContentsParser()

        text = '''ывп ыфвп ваы

!! [[# якорь1  ]]Абырвалг 123

ывапыва ывп выап
выапывп ываап ывап 

!!! [[#  якорь2   ]] Абырвалг 234

фывафыва

!!!! Еще один заголовок

фывафыва
'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 3)
        self.assertEqual (contents[0].title, "Абырвалг 123")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, "якорь1")

        self.assertEqual (contents[1].title, "Абырвалг 234")
        self.assertEqual (contents[1].level, 2)
        self.assertEqual (contents[1].anchor, "якорь2")


    def testParser_15 (self):
        from tableofcontents.contentsparser import ContentsParser

        parser = ContentsParser()

        text = '''ывп ыфвп ваы

[[#якорь1]]
!! Абырвалг 123

ывапыва ывп выап
выапывп ываап ывап 

[[#якорь2]]
!!! Абырвалг 234

фывафыва

!!!! Еще один заголовок

фывафыва
'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 3)
        self.assertEqual (contents[0].title, "Абырвалг 123")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, "якорь1")

        self.assertEqual (contents[1].title, "Абырвалг 234")
        self.assertEqual (contents[1].level, 2)
        self.assertEqual (contents[1].anchor, "якорь2")


    def testParser_16 (self):
        from tableofcontents.contentsparser import ContentsParser

        parser = ContentsParser()

        text = '''ывп ыфвп ваы

[[#якорь1]]   
!! Абырвалг 123

ывапыва ывп выап
выапывп ываап ывап 

[[#якорь2]]   
!!! Абырвалг 234

фывафыва

!!!! Еще один заголовок

фывафыва
'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 3)
        self.assertEqual (contents[0].title, "Абырвалг 123")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, "якорь1")

        self.assertEqual (contents[1].title, "Абырвалг 234")
        self.assertEqual (contents[1].level, 2)
        self.assertEqual (contents[1].anchor, "якорь2")


    def testParser_17 (self):
        from tableofcontents.contentsparser import ContentsParser

        parser = ContentsParser()

        text = '''ывп ыфвп ваы

!! Абырвалг 123 [[#якорь1]]

ывапыва ывп выап
выапывп ываап ывап 

!!! Абырвалг 234 [[#якорь2]]

фывафыва

!!!! Еще один заголовок

фывафыва
'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 3)
        self.assertEqual (contents[0].title, "Абырвалг 123")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, "якорь1")

        self.assertEqual (contents[1].title, "Абырвалг 234")
        self.assertEqual (contents[1].level, 2)
        self.assertEqual (contents[1].anchor, "якорь2")



    def testParser_18 (self):
        from tableofcontents.contentsparser import ContentsParser

        parser = ContentsParser()

        text = '''ывп ыфвп ваы

!! Абырвалг 123 [[#якорь1]]   

ывапыва ывп выап
выапывп ываап ывап 

!!! Абырвалг 234 [[#якорь2]]   

фывафыва

!!!! Еще один заголовок

фывафыва
'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 3)
        self.assertEqual (contents[0].title, "Абырвалг 123")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, "якорь1")

        self.assertEqual (contents[1].title, "Абырвалг 234")
        self.assertEqual (contents[1].level, 2)
        self.assertEqual (contents[1].anchor, "якорь2")


    def testParser_19 (self):
        from tableofcontents.contentsparser import ContentsParser

        parser = ContentsParser()

        text = '''ывп ыфвп ваы

!! Абырвалг [=123=] [[#якорь1]]

ывапыва ывп выап
выапывп ываап ывап 

!!! Абырвалг 234 [[#якорь2]]

фывафыва

!!!! Еще один заголовок

фывафыва
'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 3)
        self.assertEqual (contents[0].title, "Абырвалг [=123=]")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, "якорь1")

        self.assertEqual (contents[1].title, "Абырвалг 234")
        self.assertEqual (contents[1].level, 2)
        self.assertEqual (contents[1].anchor, "якорь2")


    def testParser_20 (self):
        from tableofcontents.contentsparser import ContentsParser

        parser = ContentsParser()

        text = '''ывп ыфвп ваы

!! Абырвалг 123

   [=   
dsfasdf
!! Это не заголовок

asdf
   =]   

ывапыва ывп выап
выапывп ываап ывап 

!!! Абырвалг 234'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 2)
        self.assertEqual (contents[0].title, "Абырвалг 123")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, "")

        self.assertEqual (contents[1].title, "Абырвалг 234")
        self.assertEqual (contents[1].level, 2)
        self.assertEqual (contents[1].anchor, "")


    def testParser_21 (self):
        from tableofcontents.contentsparser import ContentsParser

        parser = ContentsParser()

        text = '''ывп ыфвп ваы

!! Абырвалг 123

wdsdaf [=   
dsfasdf
!! Это не заголовок

asdf
asdfasdf   =]   

ывапыва ывп выап
выапывп ываап ывап 

!!! Абырвалг 234'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 2)
        self.assertEqual (contents[0].title, "Абырвалг 123")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, "")

        self.assertEqual (contents[1].title, "Абырвалг 234")
        self.assertEqual (contents[1].level, 2)
        self.assertEqual (contents[1].anchor, "")


    def testParser_22 (self):
        from tableofcontents.contentsparser import ContentsParser

        parser = ContentsParser()

        text = '''ывп ыфвп ваы

[= asfsaf fasdg=]

!! Абырвалг 123

wdsdaf [=   
dsfasdf
!! Это не заголовок

asdf
asdfasdf   =]   

ывапыва ывп выап
выапывп ываап ывап 

!!! Абырвалг 234'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 2)
        self.assertEqual (contents[0].title, "Абырвалг 123")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, "")

        self.assertEqual (contents[1].title, "Абырвалг 234")
        self.assertEqual (contents[1].level, 2)
        self.assertEqual (contents[1].anchor, "")


    def testParser_23 (self):
        from tableofcontents.contentsparser import ContentsParser

        parser = ContentsParser()

        text = '''ывп ыфвп ваы

[= asfsaf fasdg

!! Абырвалг 123

ывапыва ывп выап
выапывп ываап ывап 

!!! Абырвалг 234'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 2)
        self.assertEqual (contents[0].title, "Абырвалг 123")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, "")

        self.assertEqual (contents[1].title, "Абырвалг 234")
        self.assertEqual (contents[1].level, 2)
        self.assertEqual (contents[1].anchor, "")


    def testParser_24 (self):
        from tableofcontents.contentsparser import ContentsParser

        parser = ContentsParser()

        text = '''ывп ыфвп ваы

 asfsaf fasdg

!! Абырвалг 123

ывапыва ывп выап
выапывп ываап ывап 

!!! Абырвалг 234

=]'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 2)
        self.assertEqual (contents[0].title, "Абырвалг 123")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, "")

        self.assertEqual (contents[1].title, "Абырвалг 234")
        self.assertEqual (contents[1].level, 2)
        self.assertEqual (contents[1].anchor, "")


    def testParser_25 (self):
        from tableofcontents.contentsparser import ContentsParser

        parser = ContentsParser()

        text = '''ывп ыфвп ваы

=]
 asfsaf fasdg

!! Абырвалг 123

ывапыва ывп выап
выапывп ываап ывап 

!!! Абырвалг 234

=]'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 2)
        self.assertEqual (contents[0].title, "Абырвалг 123")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, "")

        self.assertEqual (contents[1].title, "Абырвалг 234")
        self.assertEqual (contents[1].level, 2)
        self.assertEqual (contents[1].anchor, "")


    def testParser_26 (self):
        from tableofcontents.contentsparser import ContentsParser

        parser = ContentsParser()

        text = '''ывп ыфвп ваы

[[#якорь1_2]]   
!! [[#якорь1_1]] Абырвалг 123

ывапыва ывп выап
выапывп ываап ывап 

[[#якорь2_2]]   
!!! Абырвалг 234 [[#якорь2_3]]

фывафыва

!!!! Еще один заголовок

фывафыва
'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 3)
        self.assertEqual (contents[0].title, "Абырвалг 123")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, "якорь1_1")

        self.assertEqual (contents[1].title, "Абырвалг 234")
        self.assertEqual (contents[1].level, 2)
        self.assertEqual (contents[1].anchor, "якорь2_2")


    def testParser_27 (self):
        from tableofcontents.contentsparser import ContentsParser

        parser = ContentsParser()

        text = '''ывп ыфвп ваы

!! Абырвалг 123

[@
!! Это не заголовок
@]

ывапыва ывп выап
выапывп ываап ывап

!!! Абырвалг 234'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 2)
        self.assertEqual (contents[0].title, "Абырвалг 123")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, "")

        self.assertEqual (contents[1].title, "Абырвалг 234")
        self.assertEqual (contents[1].level, 2)
        self.assertEqual (contents[1].anchor, "")


    def testParser_28 (self):
        from tableofcontents.contentsparser import ContentsParser

        parser = ContentsParser()

        text = '''ывп ыфвп ваы

[=
!! Это не заголовок
=]

!! Абырвалг 123

[=
[@
!! Это не заголовок
@]
=]

ывапыва ывп выап
выапывп ываап ывап

!!! Абырвалг 234'''

        contents = parser.parse (text)

        self.assertEqual (len (contents), 2)
        self.assertEqual (contents[0].title, "Абырвалг 123")
        self.assertEqual (contents[0].level, 1)
        self.assertEqual (contents[0].anchor, "")

        self.assertEqual (contents[1].title, "Абырвалг 234")
        self.assertEqual (contents[1].level, 2)
        self.assertEqual (contents[1].anchor, "")
