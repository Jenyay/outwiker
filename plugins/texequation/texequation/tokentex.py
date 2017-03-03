# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod
import os
import os.path
import shutil

from outwiker.core.system import getOS
from outwiker.libs.pyparsing import QuotedString
from outwiker.pages.wiki.thumbnails import Thumbnails


class TexFactory (object):
    @staticmethod
    def makeInlineTexToken(parser):
        return InlineTexToken(parser).getToken()

    @staticmethod
    def makeBigTexToken(parser):
        return BigTexToken(parser).getToken()


class BaseTexToken (object):
    __metaclass__ = ABCMeta

    def __init__(self, parser):
        self.parser = parser
        self._headers = [u'<link rel="stylesheet" href="__attach/__thumb/katex/katex.min.css">',
                         u'<script src="__attach/__thumb/katex/katex.min.js"></script>']
        self._divIndex = 0
        self._divTemplate = u'''<span class="{classname}" id="{idname}-{index}"></span>
<script>
var element = document.getElementById("{idname}-{index}");
katex.render("{code}", element, {{ displayMode: {displayMode}, throwOnError: false }});
</script>'''

    def getToken(self):
        return QuotedString(self.texStart,
                            endQuoteChar=self.texEnd,
                            multiline=True,
                            convertWhitespaceEscapes=False).setParseAction(self.makeTexEquation)("inlinetex")

    @abstractmethod
    def _getDisplayParam(self):
        pass

    @abstractmethod
    def _getClassName(self):
        pass

    @abstractmethod
    def _getIdName(self):
        pass

    def makeTexEquation(self, s, l, t):
        eqn = t[0].strip()
        if len(eqn) == 0:
            return u""

        thumb = Thumbnails(self.parser.page)

        try:
            thumb_path = thumb.getThumbPath(True)
        except IOError:
            return u"<b>{}</b>".format(_(u"Can't create thumbnails directory"))

        if self._headers[0] not in self.parser.head:
            map(lambda head: self.parser.appendToHead(head), self._headers)
            katex_path = os.path.join(thumb_path, u'katex')

            if os.path.exists(katex_path):
                try:
                    shutil.rmtree(katex_path)
                except shutil.Error:
                    return u"<b>{}</b>".format(_(u"Can't remove KaTeX library"))
            try:
                shutil.copytree(self._getKaTeXPath(), katex_path)
            except shutil.Error:
                return u"<b>{}</b>".format(_(u"Can't copy KaTeX library"))

        eqn = eqn.replace('\\', '\\\\')
        eqn = eqn.replace('"', '\\"')

        result = self._divTemplate.format(index=self._divIndex,
                                          code=eqn,
                                          displayMode=self._getDisplayParam(),
                                          classname=self._getClassName(),
                                          idname=self._getIdName())
        self._divIndex += 1
        return result

    def _getKaTeXPath(self):
        """
        Get path to KaTeX library
        """
        katexpath = unicode(os.path.join(os.path.dirname(__file__),
                                         "tools",
                                         "katex"),
                            getOS().filesEncoding)
        return katexpath


class InlineTexToken(BaseTexToken):
    """
    Класс токена для разбора формул
    """
    texStart = "{$"
    texEnd = "$}"

    def _getDisplayParam(self):
        return u'false'

    def _getClassName(self):
        return u'texequation-inline'

    def _getIdName(self):
        return u'texequation-inline'


class BigTexToken(BaseTexToken):
    """
    Класс токена для разбора формул
    """
    texStart = "{$$"
    texEnd = "$$}"

    def _getDisplayParam(self):
        return u'true'

    def _getClassName(self):
        return u'texequation-block'

    def _getIdName(self):
        return u'texequation-block'
