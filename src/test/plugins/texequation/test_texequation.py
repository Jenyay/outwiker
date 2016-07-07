# -*- coding: UTF-8 -*-

import unittest
import os.path

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.tree import WikiDocument
from outwiker.core.application import Application
from outwiker.core.attachment import Attachment
from outwiker.pages.wiki.wikipage import WikiPageFactory
from outwiker.pages.wiki.thumbnails import Thumbnails
from outwiker.pages.wiki.parserfactory import ParserFactory
from test.utils import removeDir


class TexEquationTest (unittest.TestCase):
    def setUp (self):
        self.filesPath = u"../test/samplefiles/"
        self.__createWiki()

        dirlist = [u"../plugins/texequation"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)

        self.testPage = self.wikiroot[u"Страница 1"]
        self.parser = ParserFactory().make (self.testPage, Application.config)


    def tearDown (self):
        removeDir (self.path)
        self.loader.clear()


    def __createWiki (self):
        # Здесь будет создаваться вики
        self.path = u"../test/testwiki"
        removeDir (self.path)

        self.wikiroot = WikiDocument.create (self.path)

        WikiPageFactory().create (self.wikiroot, u"Страница 1", [])
        self.testPage = self.wikiroot[u"Страница 1"]


    def testPluginLoad (self):
        self.assertEqual (len (self.loader), 1)


    def testTex1 (self):
        from texequation.texrender import getTexRender
        thumb = Thumbnails (self.parser.page)
        texrender = getTexRender(thumb.getThumbPath (True))

        eqn = u"y = f(x)"
        text = u"{$ %s $}" % (eqn)

        fname = texrender.getImageName (eqn)
        path = os.path.join (Thumbnails.getRelativeThumbDir(), fname)

        result_right = u'<img src="{0}"/>'.format (path.replace ("\\", "/"))

        result = self.parser.toHtml (text)

        self.assertEqual (result_right, result, result)

        full_path = os.path.join (self.parser.page.path, path)
        self.assertTrue (os.path.exists (full_path), full_path)


    def testTex2 (self):
        from texequation.texrender import getTexRender
        thumb = Thumbnails (self.parser.page)
        texrender = getTexRender(thumb.getThumbPath (True))

        eqn1 = u"y = f(x)"
        eqn2 = u"y = e^x"
        eqn3 = u"y = \sum_{i=0}\pi"

        text = u"""бла-бла-бла
* бла-бла-бла {$ %s $} 1111
* бла-бла-бла {$ %s $} 222
* бла-бла-бла {$ %s $} 333""" % (eqn1, eqn2, eqn3)

        fname1 = texrender.getImageName (eqn1)
        fname2 = texrender.getImageName (eqn2)
        fname3 = texrender.getImageName (eqn3)

        path1 = os.path.join (Thumbnails.getRelativeThumbDir(), fname1)
        path2 = os.path.join (Thumbnails.getRelativeThumbDir(), fname2)
        path3 = os.path.join (Thumbnails.getRelativeThumbDir(), fname3)

        result_right = u'''бла-бла-бла
<ul><li>бла-бла-бла <img src="{path1}"/> 1111</li><li>бла-бла-бла <img src="{path2}"/> 222</li><li>бла-бла-бла <img src="{path3}"/> 333</li></ul>'''.format (path1=path1.replace ("\\", "/"),
                                                                                                                                                                                        path2=path2.replace ("\\", "/"),
                                                                                                                                                                                        path3=path3.replace ("\\", "/"))

        result = self.parser.toHtml (text)

        self.assertEqual (result_right, result, result)

        full_path1 = os.path.join (self.parser.page.path, path1)
        full_path2 = os.path.join (self.parser.page.path, path2)
        full_path3 = os.path.join (self.parser.page.path, path3)

        self.assertTrue (os.path.exists (full_path1), full_path1)
        self.assertTrue (os.path.exists (full_path2), full_path2)
        self.assertTrue (os.path.exists (full_path3), full_path3)


    def testTex3 (self):
        from texequation.texrender import getTexRender
        thumb = Thumbnails (self.parser.page)
        texrender = getTexRender(thumb.getThumbPath (True))

        eqn = u"y = f(x)"
        text = u"[[{$ %s $} -> http://jenyay.net]]" % (eqn)

        fname = texrender.getImageName (eqn)
        path = os.path.join (Thumbnails.getRelativeThumbDir(), fname)

        result_right = u'<a href="http://jenyay.net"><img src="{0}"/></a>'.format (path.replace ("\\", "/"))

        result = self.parser.toHtml (text)

        self.assertEqual (result_right, result, result)

        full_path = os.path.join (self.parser.page.path, path)
        self.assertTrue (os.path.exists (full_path), full_path)


    def testTex4 (self):
        from texequation.texrender import getTexRender
        thumb = Thumbnails (self.parser.page)
        texrender = getTexRender(thumb.getThumbPath (True))

        eqn = u"y = f(x)"
        text = u"[[http://jenyay.net | {$ %s $}]]" % (eqn)

        fname = texrender.getImageName (eqn)
        path = os.path.join (Thumbnails.getRelativeThumbDir(), fname)

        result_right = u'<a href="http://jenyay.net"><img src="{0}"/></a>'.format (path.replace ("\\", "/"))

        result = self.parser.toHtml (text)

        self.assertEqual (result_right, result, result)

        full_path = os.path.join (self.parser.page.path, path)
        self.assertTrue (os.path.exists (full_path), full_path)


    def testTex5 (self):
        text = u"{$ $}"
        result_right = u''

        result = self.parser.toHtml (text)

        self.assertEqual (result_right, result, result)


    def testTexRussian (self):
        from texequation.texrender import getTexRender
        thumb = Thumbnails (self.parser.page)
        texrender = getTexRender(thumb.getThumbPath (True))

        eqn = u"y = бла-бла-бла"
        text = u"{$ %s $}" % (eqn)

        fname = texrender.getImageName (eqn)
        path = os.path.join (Thumbnails.getRelativeThumbDir(), fname)

        result_right = u'<img src="{0}"/>'.format (path.replace ("\\", "/"))

        result = self.parser.toHtml (text)

        self.assertEqual (result_right, result, result)

        full_path = os.path.join (self.parser.page.path, path)
        self.assertTrue (os.path.exists (full_path), full_path)


    def testHeaderTex (self):
        text = u"бла-бла-бла \n!!! Заголовок {$e^x$}\nбла-бла-бла"
        result_parse = self.parser.toHtml (text)

        self.assertTrue (result_parse.startswith (u'бла-бла-бла \n<h2>Заголовок <img src="__attach/__thumb/eqn_'))


    def testTexLinks1 (self):
        pagelinks = [u"Страница 1", u"/Страница 1", u"/Страница 2/Страница 3"]
        for link in pagelinks:
            text = u"бла-бла-бла \n[[%s | {$e^x$} ]] бла-бла-бла\nбла-бла-бла" % (link)
            result_begin = u'бла-бла-бла \n<a href="%s"><img src="__attach/__thumb/eqn_' % (link)

            self.assertTrue (self.parser.toHtml (text).startswith (result_begin))


    def testTexLinks2 (self):
        pagelinks = [u"Страница 1", u"/Страница 1", u"/Страница 2/Страница 3"]
        for link in pagelinks:
            text = u"бла-бла-бла \n[[{$e^x$} -> %s]] бла-бла-бла\nбла-бла-бла" % (link)
            result_begin = u'бла-бла-бла \n<a href="%s"><img src="__attach/__thumb/eqn_' % (link)

            self.assertTrue (self.parser.toHtml (text).startswith (result_begin))


    def testThumbnailsClear2_attach (self):
        fname = u"accept.png"
        attachPath = os.path.join (self.filesPath, fname)
        Attachment (self.parser.page).attach ([attachPath])

        thumb = Thumbnails (self.parser.page)

        eqn = "y = f(x)"

        text = "{$ %s $}" % (eqn)
        self.parser.toHtml (text)

        self.assertFalse (len (os.listdir (thumb.getThumbPath (False))) == 0)

        thumb.clearDir()

        self.assertEqual (len (os.listdir (thumb.getThumbPath (False))), 0)


    def testThumbnailsClear3_attach (self):
        fname = u"accept.png"
        attachPath = os.path.join (self.filesPath, fname)
        Attachment (self.parser.page).attach ([attachPath])

        thumb = Thumbnails (self.parser.page)

        eqn1 = "y = f(x)"
        eqn2 = "y = f_2(x)"

        self.parser.toHtml ("{$ %s $}" % (eqn1))
        self.assertEqual (len (os.listdir (thumb.getThumbPath (False))), 2)

        self.parser.toHtml ("{$ %s $}" % (eqn2))
        self.assertEqual (len (os.listdir (thumb.getThumbPath (False))), 2)


    def testThumbnailsClear2 (self):
        thumb = Thumbnails (self.parser.page)

        eqn = "y = f(x)"

        text = "{$ %s $}" % (eqn)
        self.parser.toHtml (text)

        self.assertFalse (len (os.listdir (thumb.getThumbPath (False))) == 0)

        thumb.clearDir()

        self.assertEqual (len (os.listdir (thumb.getThumbPath (False))), 0)


    def testThumbnailsClear3 (self):
        thumb = Thumbnails (self.parser.page)

        eqn1 = "y = f(x)"
        eqn2 = "y = f_2(x)"

        self.parser.toHtml ("{$ %s $}" % (eqn1))
        self.assertEqual (len (os.listdir (thumb.getThumbPath (False))), 2)

        self.parser.toHtml ("{$ %s $}" % (eqn2))
        self.assertEqual (len (os.listdir (thumb.getThumbPath (False))), 2)
