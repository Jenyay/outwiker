# -*- coding: UTF-8 -*-

from outwiker.pages.wiki.parser.tokenblock import SimpleNestedBlock


class QuoteFactory(object):
    """
    The fabric to create quote tokens.
    """
    @staticmethod
    def make(parser):
        return QuoteToken(parser).getToken()


class QuoteToken(SimpleNestedBlock):
    start = u'[>'
    end = u'<]'
    start_html = u'<blockquote>'
    end_html = u'</blockquote>'
    name = 'quote'
