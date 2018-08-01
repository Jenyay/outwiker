# -*- coding: utf-8 -*-

from .tokenblock import SimpleNestedBlock
from .tokenlinebreak import LineBreakToken


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
    name = u'quote'
    ignore = LineBreakToken().getToken()
