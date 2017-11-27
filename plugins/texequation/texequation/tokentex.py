# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import os
import os.path
import shutil

from outwiker.core.system import getOS
from outwiker.libs.pyparsing import QuotedString
from outwiker.pages.wiki.thumbnails import Thumbnails

from defines import KATEX_DIR_NAME


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
        self._headers = [u'<link rel="stylesheet" href="__attach/__thumb/{katex}/katex.min.css">\n'.format(katex=KATEX_DIR_NAME),
                         u'<script src="__attach/__thumb/{katex}/katex.min.js"></script>'.format(katex=KATEX_DIR_NAME)]
        self._divIndex = 0

        self._equationTemplate = u'<span class="{classname}" id="{idname}-{index}"></span>'

        self._scriptActionsTemplate = u'''var element_{index} = document.getElementById("{idname}-{index}");
katex.render("{code}", element_{index}, {{ displayMode: {displayMode}, throwOnError: false }});'''

        self._scriptTemplate = u'''<script>
// {comment_begin}
{actions}
// {comment_end}
</script>
'''
        self._script_code = u''

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

    @abstractmethod
    def _get_script_comment_begin(self):
        pass

    @abstractmethod
    def _get_script_comment_end(self):
        pass

    def _copyKatexLibrary(self):
        thumb = Thumbnails(self.parser.page)
        thumb_path = thumb.getThumbPath(True)
        katex_path = os.path.join(thumb_path, KATEX_DIR_NAME)

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
        eqn = eqn.replace('\n', '\\\n')

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

        self._script_code += u'\n' + scriptAction + u'\n'

        self._addScriptToFooter(self.parser, self._script_code)

        self._divIndex += 1
        return result

    def _addScriptToFooter(self, parser, script_code):
        comment_begin = self._get_script_comment_begin()
        comment_end = self._get_script_comment_end()

        script = self._scriptTemplate.format(actions=script_code,
                                             comment_begin=comment_begin,
                                             comment_end=comment_end)
        index = None
        for n, footer in enumerate(parser.footerItems):
            if comment_begin in footer and comment_end in footer:
                index = n
                break

        if index is not None:
            parser.footerItems.pop(index)

        parser.appendToFooter(script)

    def _getKaTeXPath(self):
        """
        Get path to KaTeX library
        """
        root = unicode(os.path.dirname(__file__), getOS().filesEncoding)
        katexpath = os.path.join(root, u"tools", KATEX_DIR_NAME)
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

    def _get_script_comment_begin(self):
        return u'*** TexEquation inline script begin ***'

    def _get_script_comment_end(self):
        return u'*** TexEquation inline script end ***'


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

    def _get_script_comment_begin(self):
        return u'*** TexEquation block script begin ***'

    def _get_script_comment_end(self):
        return u'*** TexEquation block script end ***'
