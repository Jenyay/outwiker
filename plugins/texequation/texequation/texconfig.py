# -*- coding: utf-8 -*-

from outwiker.core.config import IntegerOption, StringOption


class TeXConfig (object):
    SECTION = u"TeXEquationPlugin"

    # Inline equation scale
    SCALE_INLINE_PARAM = 'scale_inline'
    SCALE_INLINE_DEFAULT = 100

    # Block equation scale
    SCALE_BLOCK_PARAM = 'scale_block'
    SCALE_BLOCK_DEFAULT = 100

    TOOLS_WIDTH_SECTION = u'ToolsWidth'
    TOOLS_WIDTH_DEFAULT = 350

    TOOLS_HEIGHT_SECTION = u'ToolsHeight'
    TOOLS_HEIGHT_DEFAULT = 100

    TOOLS_PANE_OPTIONS_SECTION = u'ToolsPane'
    TOOLS_PANE_OPTIONS_DEFAULT = u''

    def __init__(self, config):
        self._config = config

        self.scaleInline = IntegerOption(
            self._config,
            self.SECTION,
            self.SCALE_INLINE_PARAM,
            self.SCALE_INLINE_DEFAULT)

        self.scaleBlock = IntegerOption(
            self._config,
            self.SECTION,
            self.SCALE_BLOCK_PARAM,
            self.SCALE_BLOCK_DEFAULT)

        self.width = IntegerOption(self._config,
                                   self.SECTION,
                                   self.TOOLS_WIDTH_SECTION,
                                   self.TOOLS_WIDTH_DEFAULT)

        self.height = IntegerOption(self._config,
                                    self.SECTION,
                                    self.TOOLS_HEIGHT_SECTION,
                                    self.TOOLS_HEIGHT_DEFAULT)

        self.pane = StringOption(self._config,
                                 self.SECTION,
                                 self.TOOLS_PANE_OPTIONS_SECTION,
                                 self.TOOLS_PANE_OPTIONS_DEFAULT)
