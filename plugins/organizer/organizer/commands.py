# -*- coding: UTF-8 -*-

import re
from datetime import datetime

from outwiker.pages.wiki.parser.command import Command
from outwiker.core.application import Application

from .config import OrganizerConfig
from .defines import (DATE_ORG_PARAM_NANE,
                      HTML_STYLES_COMMENT_START,
                      HTML_STYLES_COMMENT_END,
                      RECORD_TAGS)
from .orgitems import DayDescription, Record
from .orghtmlgenerator import OrgHTMLGenerator
from .localizer import Localizer
from .utils import splitTags


class CommandOrg (Command):
    """
    Org wiki command
    """
    def __init__ (self, parser):
        """
        parser - экземпляр парсера
        """
        super (CommandOrg, self).__init__ (parser)
        config = OrganizerConfig (Application.config)

        self._dateFormat = config.dateTimeFormat.value
        self._htmlGenerator = OrgHTMLGenerator (config, self.parser)


    @property
    def name (self):
        """
        Возвращает имя команды, которую обрабатывает класс
        """
        return u"org"


    def execute (self, params, content):
        """
        Запустить команду на выполнение.
        Метод возвращает текст, который будет вставлен на место команды в вики-нотации
        """
        params_dict = Command.parseParams (params)
        date = None
        if DATE_ORG_PARAM_NANE in params_dict:
            try:
                date = datetime.strptime (params_dict[DATE_ORG_PARAM_NANE], self._dateFormat)
            except ValueError:
                pass

        dayDescription = DayDescription (date)
        self._fillDayDescription (dayDescription, content)

        if HTML_STYLES_COMMENT_START not in self.parser.head:
            self.parser.appendToHead (HTML_STYLES_COMMENT_START)
            self.parser.appendToHead (u'<style>')
            self.parser.appendToHead (self._htmlGenerator.getStyles())
            self.parser.appendToHead (u'</style>')
            self.parser.appendToHead (HTML_STYLES_COMMENT_END)

        self._addTagsToPage (dayDescription)
        return self._htmlGenerator.getHTML (dayDescription)


    def _addTagsToPage (self, dayDescription):
        localizer = Localizer()
        tagsList = []
        for record in dayDescription:
            tagsStr = localizer.getRecordValue (record, RECORD_TAGS)
            if tagsStr:
                tags = splitTags (tagsStr)
                if u'-' in tags:
                    tags.remove (u'-')
                tagsList += tags

        tags = list (set (tagsList + self.parser.page.tags))
        self.parser.page.tags = tags
            


    def _fillDayDescription (self, dayDescription, content):
        content = content.replace ('\r\n', '\n')
        job_list = content.split ('\n\n')
        detail_regex = re.compile (r'\s*(?P<title>.*?):\s*(?P<description>.*)',
                                   re.U | re.M)

        for job in job_list:
            record = None
            for line in job.split ('\n'):
                match = detail_regex.match (line)
                if match is not None:
                    if record is None:
                        record = Record()
                    record.addDetail (match.group ('title'),
                                      match.group ('description'))

            if record is not None:
                dayDescription.addRecord (record)
