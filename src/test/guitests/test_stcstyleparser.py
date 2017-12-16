# -*- coding: UTF-8 -*-

from unittest import TestCase

from outwiker.gui.stcstyle import StcStyle


class StcStyleParserTest (TestCase):
    def testDefaultStyle (self):
        style = StcStyle()
        self.assertEqual (style.bold, False)
        self.assertEqual (style.italic, False)
        self.assertEqual (style.underline, False)
        self.assertEqual (style.fore, "#000000")
        self.assertEqual (style.back, "#FFFFFF")


    def testCreateStyle_01 (self):
        style = StcStyle(fore="#556677")
        self.assertEqual (style.bold, False)
        self.assertEqual (style.italic, False)
        self.assertEqual (style.underline, False)
        self.assertEqual (style.fore, "#556677")
        self.assertEqual (style.back, "#FFFFFF")


    def testCreateStyle_02 (self):
        style = StcStyle(bold=True)
        self.assertEqual (style.bold, True)
        self.assertEqual (style.italic, False)
        self.assertEqual (style.underline, False)
        self.assertEqual (style.fore, "#000000")
        self.assertEqual (style.back, "#FFFFFF")


    def testToString_01 (self):
        style = StcStyle()
        self.assertEqual (style.tostr(), "fore:#000000,back:#FFFFFF")


    def testToString_02 (self):
        style = StcStyle(bold=True)
        self.assertEqual (style.tostr(), "fore:#000000,back:#FFFFFF,bold")


    def testToString_03 (self):
        style = StcStyle(bold=True, italic=True)
        self.assertEqual (style.tostr(), "fore:#000000,back:#FFFFFF,bold,italic")


    def testToString_04 (self):
        style = StcStyle(bold=True, italic=True, underline=True)
        self.assertEqual (style.tostr(), "fore:#000000,back:#FFFFFF,bold,italic,underline")


    def testToString_05 (self):
        style = StcStyle(fore="#AAAAAA", back="#BBBBBB", bold=True)
        self.assertEqual (style.tostr(), "fore:#AAAAAA,back:#BBBBBB,bold")


    def testToString_06 (self):
        style = StcStyle(fore="", back="", bold=True)
        self.assertEqual (style.tostr(), "bold")


    def testToString_07 (self):
        style = StcStyle(fore="", back="", bold=True, italic=True)
        self.assertEqual (style.tostr(), "bold,italic")


    def testParse_01 (self):
        style = StcStyle.parse ("")

        self.assertEqual (style.bold, False)
        self.assertEqual (style.italic, False)
        self.assertEqual (style.underline, False)
        self.assertEqual (style.fore, "#000000")
        self.assertEqual (style.back, "#FFFFFF")


    def testParse_02 (self):
        style = StcStyle.parse ("fore:#000000")

        self.assertEqual (style.bold, False)
        self.assertEqual (style.italic, False)
        self.assertEqual (style.underline, False)
        self.assertEqual (style.fore, "#000000")
        self.assertEqual (style.back, "#FFFFFF")


    def testParse_03 (self):
        style = StcStyle.parse ("fore:#000000,bold")

        self.assertEqual (style.bold, True)
        self.assertEqual (style.italic, False)
        self.assertEqual (style.underline, False)
        self.assertEqual (style.fore, "#000000")
        self.assertEqual (style.back, "#FFFFFF")


    def testParse_04 (self):
        style = StcStyle.parse ("fore:#AAAAAA")

        self.assertEqual (style.bold, False)
        self.assertEqual (style.italic, False)
        self.assertEqual (style.underline, False)
        self.assertEqual (style.fore, "#AAAAAA")
        self.assertEqual (style.back, "#FFFFFF")


    def testParse_05 (self):
        style = StcStyle.parse ("FORE:#AAAAAA")

        self.assertEqual (style.bold, False)
        self.assertEqual (style.italic, False)
        self.assertEqual (style.underline, False)
        self.assertEqual (style.fore, "#AAAAAA")
        self.assertEqual (style.back, "#FFFFFF")


    def testParse_06 (self):
        style = StcStyle.parse ("fore:#AAAAAA,bold")

        self.assertEqual (style.bold, True)
        self.assertEqual (style.italic, False)
        self.assertEqual (style.underline, False)
        self.assertEqual (style.fore, "#AAAAAA")
        self.assertEqual (style.back, "#FFFFFF")


    def testParse_07 (self):
        style = StcStyle.parse (" fore:#AAAAAA, bold ")

        self.assertEqual (style.bold, True)
        self.assertEqual (style.italic, False)
        self.assertEqual (style.underline, False)
        self.assertEqual (style.fore, "#AAAAAA")
        self.assertEqual (style.back, "#FFFFFF")


    def testParse_08 (self):
        style = StcStyle.parse ("fore:#AAAAAA,back:#222222,bold")

        self.assertEqual (style.bold, True)
        self.assertEqual (style.italic, False)
        self.assertEqual (style.underline, False)
        self.assertEqual (style.fore, "#AAAAAA")
        self.assertEqual (style.back, "#222222")


    def testParse_09 (self):
        style = StcStyle.parse ("fore:#AAAAAA,back:#222222,bold,italic")

        self.assertEqual (style.bold, True)
        self.assertEqual (style.italic, True)
        self.assertEqual (style.underline, False)
        self.assertEqual (style.fore, "#AAAAAA")
        self.assertEqual (style.back, "#222222")


    def testParse_10 (self):
        style = StcStyle.parse ("fore:#AAAAAA,back:#222222,bold,italic,underline")

        self.assertEqual (style.bold, True)
        self.assertEqual (style.italic, True)
        self.assertEqual (style.underline, True)
        self.assertEqual (style.fore, "#AAAAAA")
        self.assertEqual (style.back, "#222222")


    def testParse_11 (self):
        style = StcStyle.parse (" fore:#AAAAAA , back:#222222 , bold,italic , underline ")

        self.assertEqual (style.bold, True)
        self.assertEqual (style.italic, True)
        self.assertEqual (style.underline, True)
        self.assertEqual (style.fore, "#AAAAAA")
        self.assertEqual (style.back, "#222222")


    def testParse_12 (self):
        style = StcStyle.parse ("fore:#AAAAAA,back:#222222,bold,underline")

        self.assertEqual (style.bold, True)
        self.assertEqual (style.italic, False)
        self.assertEqual (style.underline, True)
        self.assertEqual (style.fore, "#AAAAAA")
        self.assertEqual (style.back, "#222222")


    def testParse_13 (self):
        style = StcStyle.parse ("back:#222222,bold,underline")

        self.assertEqual (style.bold, True)
        self.assertEqual (style.italic, False)
        self.assertEqual (style.underline, True)
        self.assertEqual (style.fore, "#000000")
        self.assertEqual (style.back, "#222222")


    def testParse_14 (self):
        style = StcStyle.parse ("back:#222222,bold,,,underline")

        self.assertEqual (style.bold, True)
        self.assertEqual (style.italic, False)
        self.assertEqual (style.underline, True)
        self.assertEqual (style.fore, "#000000")
        self.assertEqual (style.back, "#222222")


    def testParse_invalid (self):
        self.assertEqual (StcStyle.parse ("sdgsgd"), None)
        self.assertEqual (StcStyle.parse ("fore:#AAAAAA,back:#222222,boldasdfa"), None)


    def testCheckColorString (self):
        self.assertTrue (StcStyle.checkColorString ("#000000"))
        self.assertTrue (StcStyle.checkColorString (" #000000 "))
        self.assertTrue (StcStyle.checkColorString ("#AA00FF"))
        self.assertTrue (StcStyle.checkColorString ("#aa00ff"))

        self.assertFalse (StcStyle.checkColorString ("AA00FF"))
        self.assertFalse (StcStyle.checkColorString ("#AA00FF0"))
        self.assertFalse (StcStyle.checkColorString ("#AA00GG"))
        self.assertFalse (StcStyle.checkColorString ("#A0F"))
