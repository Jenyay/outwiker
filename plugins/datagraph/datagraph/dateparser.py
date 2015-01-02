# -*- coding: UTF-8 -*-

import re

from datetime import datetime, timedelta

"""
Functions for creation datetime and timedelta from string "2015y 12mon 31d 23h 59min 59s"
"""


class DateTimeStruct (object):
    def __init__ (self):
        self.years = 0
        self.months = 0
        self.days = 0
        self.hours = 0
        self.minutes = 0
        self.seconds = 0


def createDateTime (text):
    date = createDateTimeStruct (text)
    return datetime (date.years,
                     date.months,
                     date.days,
                     date.hours,
                     date.minutes,
                     date.seconds)


def createDateTimeStruct (text):
    if len (text.strip()) == 0:
        raise ValueError

    result = DateTimeStruct()

    regexp = re.compile (r'(?P<val>\d+)(?P<element>y|mon|d|h|min|s)$', re.I)
    elements = text.split()

    ok = False

    for element in elements:
        match = regexp.match (element)
        if match is not None:
            ok = True
            val = int (match.group ('val'))

            if match.group ('element') == u'y':
                result.years = val
            elif match.group ('element') == u'mon':
                result.months = val
            elif match.group ('element') == u'd':
                result.days = val
            elif match.group ('element') == u'h':
                result.hours = val
            elif match.group ('element') == u'min':
                result.minutes = val
            elif match.group ('element') == u's':
                result.seconds = val

    if not ok:
        raise ValueError

    return result
