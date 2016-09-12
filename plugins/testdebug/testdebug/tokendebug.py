# -*- coding: UTF-8 -*-

from outwiker.libs.pyparsing import QuotedString

from outwiker.pages.wiki.parser.tokenblock import TextBlockToken


class DebugTokenFactory (object):
    @staticmethod
    def makeDebugToken (parser):
        return DebugToken(parser).getToken()



class DebugToken (TextBlockToken):
    start = "{{{{"
    end = "}}}}"

    def getToken (self):
        return QuotedString(DebugToken.start,
                            endQuoteChar=DebugToken.end,
                            multiline=True,
                            convertWhitespaceEscapes=False).setParseAction(self.convertToHTML("<font color='red'>", "</font>"))("debug")
