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


        self.ORG_STYLES_PARAM = u'Organizer_DateTimeFormat'
        self.ORG_STYLES_DEFAULT = u'''.org {
			width: 100%;
			text-align: center;
		}

		.org-date {
			width: 100%;
			text-align: left;
			padding-left: 2em;
			font-weight: bold;
		}

		.org-table {
			width: 98%;
			border-collapse: collapse;
			margin: 0 auto;
			text-align: left;
		}

		.org-table td, th {
			padding: 5px;
			border: 1px solid black;
			text-align: left;
		}
		.org-table th {
			background: #91DAF2;
			text-align: center;
		}'''

        self.orgStyles = StringOption (self._config,
                                       self.ORGANIZER_SECTION,
                                       self.ORG_STYLES_PARAM,
                                       self.ORG_STYLES_DEFAULT)
