# -*- coding: UTF-8 -*-

from .i18n import get_


class Localizer (object):
    """
    The class to localize job's headers.
    With Localizer you can use English and translated header names.
    """
    def __init__ (self):
        global _
        _ = get_()


    def getRecordValue (self, record, header):
        """
        Return value from Record instance for translated or English header name.
        Return None if header not exists.
        """
        if _(header) in record:
            return record[_(header)]
        elif header in record:
            return record[header]

        return None
