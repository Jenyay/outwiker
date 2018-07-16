# -*- coding: utf-8 -*-

import unittest

import wx

from outwiker.pages.wiki.gui.styledialog import StyleDialog
from test.basetestcases import BaseOutWikerGUIMixin


class WikiStyleDialogTest(unittest.TestCase, BaseOutWikerGUIMixin):
    def setUp(self):
        self.initApplication()

    def tearDown(self):
        self.destroyApplication()

    def test_default(self):
        parent = self.application.mainWindow
        title = ''
        styles = {}
        example_html = '<div class="{css_class}">...</div>'
        tag = 'div'

        dlg = StyleDialog(parent, title, styles, example_html, tag)
        html = dlg.getHTML()

        self.assertIsNone(dlg.getTextColor())
        self.assertIsNone(dlg.getBackgroundColor())
        self.assertIsNone(dlg.getCustomStyleName())
        self.assertIsNone(dlg.getCustomCSS())

        self.assertIn('<div class="__outwiker_preview">', html)
        self.assertIn('div.__outwiker_preview', html)

    def test_color(self):
        parent = self.application.mainWindow
        title = ''
        styles = {}
        example_html = '<div class="{css_class}">...</div>'
        tag = 'div'
        dlg = StyleDialog(parent, title, styles, example_html, tag)

        color = wx.Colour(10, 20, 30)
        dlg.setTextColor(color)

        html = dlg.getHTML()
        self.assertIn('color: {};'.format(color.GetAsString(wx.C2S_HTML_SYNTAX)),
                      html)
        self.assertEqual(dlg.getTextColor(), color)

    def test_color_disable(self):
        parent = self.application.mainWindow
        title = ''
        styles = {}
        example_html = '<div class="{css_class}">...</div>'
        tag = 'div'
        dlg = StyleDialog(parent, title, styles, example_html, tag)

        color = wx.Colour(10, 20, 30)
        dlg.setTextColor(color)
        dlg.enableTextColor(False)

        html = dlg.getHTML()
        self.assertNotIn('color: ', html)

    def test_background_color(self):
        parent = self.application.mainWindow
        title = ''
        styles = {}
        example_html = '<div class="{css_class}">...</div>'
        tag = 'div'
        dlg = StyleDialog(parent, title, styles, example_html, tag)

        color = wx.Colour(10, 20, 30)
        dlg.setBackgroundColor(color)

        html = dlg.getHTML()
        self.assertIn('background-color: {};'.format(color.GetAsString(wx.C2S_HTML_SYNTAX)),
                      html)
        self.assertEqual(dlg.getBackgroundColor(), color)

    def test_background_color_disable(self):
        parent = self.application.mainWindow
        title = ''
        styles = {}
        example_html = '<div class="{css_class}">...</div>'
        tag = 'div'
        dlg = StyleDialog(parent, title, styles, example_html, tag)

        color = wx.Colour(10, 20, 30)
        dlg.setBackgroundColor(color)
        dlg.enableBackgroundColor(False)

        html = dlg.getHTML()
        self.assertNotIn('background-color:', html)

    def test_custom_css(self):
        parent = self.application.mainWindow
        title = ''
        styles = {}
        example_html = '<div class="{css_class}">...</div>'
        tag = 'div'
        dlg = StyleDialog(parent, title, styles, example_html, tag)

        css = 'font-weight: bold;'
        dlg.setCustomCSS(css)

        html = dlg.getHTML()
        self.assertIn(css, html)
        self.assertEqual(dlg.getCustomCSS(), css)

    def test_custom_css_disable(self):
        parent = self.application.mainWindow
        title = ''
        styles = {}
        example_html = '<div class="{css_class}">...</div>'
        tag = 'div'
        dlg = StyleDialog(parent, title, styles, example_html, tag)

        css = 'font-weight: bold;'
        dlg.setCustomCSS(css)
        dlg.enableCustomCSS(False)

        html = dlg.getHTML()
        self.assertNotIn(css, html)

    def test_custom_style_name(self):
        parent = self.application.mainWindow
        title = ''
        styles = {'test': 'div.test {}'}
        example_html = '<div class="{css_class}">...</div>'
        tag = 'div'
        dlg = StyleDialog(parent, title, styles, example_html, tag)

        dlg.setCustomStyleName('test')

        html = dlg.getHTML()
        self.assertIn(styles['test'], html)
        self.assertEqual(dlg.getCustomStyleName(), 'test')

    def test_custom_style_name_disable(self):
        parent = self.application.mainWindow
        title = ''
        styles = {'test': 'div.test {}'}
        example_html = '<div class="{css_class}">...</div>'
        tag = 'div'
        dlg = StyleDialog(parent, title, styles, example_html, tag)

        dlg.setCustomStyleName('test')
        dlg.disableCustomStyleName()

        html = dlg.getHTML()
        self.assertNotIn(styles['test'], html)
