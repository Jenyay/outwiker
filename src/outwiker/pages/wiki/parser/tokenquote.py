# -*- coding: utf-8 -*-

from .tokenblock import SimpleNestedBlock
from .tokenlinebreak import LineBreakToken


class QuoteFactory:
    """
    The fabric to create quote tokens.
    """
    @staticmethod
    def make(parser):
        return QuoteToken(parser).getToken()


class QuoteToken(SimpleNestedBlock):
    start = '[>'
    end = '<]'
    start_html = '<blockquote>'
    end_html = '</blockquote>'
    name = 'quote'
    ignore = LineBreakToken().getToken()
