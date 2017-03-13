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

        self._equationTemplate = u'<span class="{classname}" id="{idname}-{index}"></span>'

        self._scriptActionsTemplate = u'''var element = document.getElementById("{idname}-{index}");
katex.render("{code}", element, {{ displayMode: {displayMode}, throwOnError: false }});'''

        self._scriptCommentStart = u'<!-- TeXEquation start -->\n'
        self._scriptCommentEnd = u'\n<!-- TeXEquation end -->\n'

        self._scriptTemplate = self._scriptCommentStart + u'''<script>
{actions}
</script>''' + self._scriptCommentEnd

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

    def _copyKatexLibrary(self):
        thumb = Thumbnails(self.parser.page)
        thumb_path = thumb.getThumbPath(True)
        katex_path = os.path.join(thumb_path, u'katex')

        if os.path.exists(katex_path):
            shutil.rmtree(katex_path)

        shutil.copytree(self._getKaTeXPath(), katex_path)

    def makeTexEquation(self, s, l, t):
        eqn = t[0].strip()
        if len(eqn) == 0:
            return u""

        if self._headers[0] not in self.parser.head:
            map(lambda head: self.parser.appendToHead(head), self._headers)
            try:
                self._copyKatexLibrary()
            except (shutil.Error, IOError):
                return u"<b>{}</b>".format(_(u"Can't copy KaTeX library"))

        eqn = eqn.replace('\\', '\\\\')
        eqn = eqn.replace('"', '\\"')

        result = self._equationTemplate.format(
            index=self._divIndex,
            displayMode=self._getDisplayParam(),
            idname=self._getIdName(),
            classname=self._getClassName()
        )

        scriptAction = self._scriptActionsTemplate.format(
            index=self._divIndex,
            code=eqn,
            displayMode=self._getDisplayParam(),
            idname=self._getIdName()
        )

        script = self._scriptTemplate.format(actions=scriptAction)
        self.parser.appendToFooter(script)

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
