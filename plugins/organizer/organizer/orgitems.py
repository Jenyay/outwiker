# -*- coding: UTF-8 -*-

from collections import OrderedDict


class Record (object):
    """Record about one job"""
    def __init__ (self):
        self._data = OrderedDict()


    def addDetail (self, header, value):
        """Add new detail about job: title, duration, tags, etc"""
        self._data[header] = value


    def getHeaders (self):
        return self._data.keys()


    def __getitem__ (self, header):
        return self._data.get (header, None)


    def __iter__ (self):
        return iter (self._data)



class DayDescription (object):
    """List of jobs for single day (single command)"""
    def __init__ (self, date):
        self._records = []
        self._date = date

    def addRecord (self, record):
        self._records.append (record)


    @property
    def date (self):
        return self._date


    def __iter__ (self):
        return iter (self._records)
