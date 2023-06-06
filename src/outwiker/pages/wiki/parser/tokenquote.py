# -*- coding: utf-8 -*-

from .tokenblock import SimpleNestedBlock
from .tokenlinebreak import LineBreakToken

import outwiker.core.cssclasses as css

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
    start_html = '<blockquote class="{css_class}">'.format(css_class=css.CSS_WIKI)
    end_html = '</blockquote>'
    name = 'quote'
    ignore = LineBreakToken().getToken()
