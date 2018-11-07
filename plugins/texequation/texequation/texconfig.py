# -*- coding: utf-8 -*-

from outwiker.core.config import IntegerOption


class TeXConfig (object):
    SECTION = u"TeXEquationPlugin"

    # Inline equation scale
    SCALE_INLINE_PARAM = 'scale_inline'
    SCALE_INLINE_DEFAULT = 100

    # Block equation scale
    SCALE_BLOCK_PARAM = 'scale_block'
    SCALE_BLOCK_DEFAULT = 100

    def __init__(self, config):
        self.__config = config

        self.scaleInline = IntegerOption(
            self.__config,
            self.SECTION,
            self.SCALE_INLINE_PARAM,
            self.SCALE_INLINE_DEFAULT)

        self.scaleBlock = IntegerOption(
            self.__config,
            self.SECTION,
            self.SCALE_BLOCK_PARAM,
            self.SCALE_BLOCK_DEFAULT)
