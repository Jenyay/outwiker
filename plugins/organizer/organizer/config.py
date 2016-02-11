# -*- coding: UTF-8 -*-

from outwiker.core.config import StringOption


class OrganizerConfig (object):
    def __init__ (self, config):
        self._config = config

        self.ORGANIZER_SECTION = u'OrganizerPlugin'

        self.DATETIME_FORMAT_PARAM = u'Organizer_DateTimeFormat'
        self.DATETIME_FORMAT_DEFAULT = u'%d.%m.%Y'

        self.dateTimeFormat = StringOption (self._config,
                                            self.ORGANIZER_SECTION,
                                            self.DATETIME_FORMAT_PARAM,
                                            self.DATETIME_FORMAT_DEFAULT)
