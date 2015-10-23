# -*- coding: UTF-8 -*-

from outwiker.core.config import StringOption


class PageTypeColorConfig (object):
    '''
    Класс для хранения настроек панели с облагом тегов
    '''
    SECTION = u'PageTypeColor'

    def __init__ (self, config):
        self.config = config

        self.wikiColor = StringOption (self.config,
                                       self.SECTION,
                                       u'wiki',
                                       u'#F1F779')

        self.htmlColor = StringOption (self.config,
                                       self.SECTION,
                                       u'html',
                                       u'#9DC0FA')

        self.textColor = StringOption (self.config,
                                       self.SECTION,
                                       u'text',
                                       u'#79F7B8')

        self.searchColor = StringOption (self.config,
                                         self.SECTION,
                                         u'search',
                                         u'#F280E3')
