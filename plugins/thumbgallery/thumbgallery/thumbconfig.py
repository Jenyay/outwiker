# -*- coding: UTF-8 -*-

from outwiker.core.config import IntegerOption


class ThumbConfig (object):
    CONFIG_SECTION = u"Thumbgallery"

    COLUMNS_COUNT_PARAMNAME = u"ColumnsCount"
    COLUMNS_COUNT_DEFAULT = 3
    COLUMNS_COUNT_MAX = 100

    THUMB_SIZE_PARAMNAME = u"ThumbSize"
    THUMB_SIZE_DEFAULT = 150
    THUMB_SIZE_MAX = 10000


    def __init__ (self, config):
        self.config = config

        self.columnsCount = IntegerOption (self.config,
                                           ThumbConfig.CONFIG_SECTION,
                                           ThumbConfig.COLUMNS_COUNT_PARAMNAME,
                                           ThumbConfig.COLUMNS_COUNT_DEFAULT)

        self.thumbSize = IntegerOption (self.config,
                                        ThumbConfig.CONFIG_SECTION,
                                        ThumbConfig.THUMB_SIZE_PARAMNAME,
                                        ThumbConfig.THUMB_SIZE_DEFAULT)
