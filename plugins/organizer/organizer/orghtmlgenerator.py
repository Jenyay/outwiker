# -*- coding: UTF-8 -*-

from StringIO import StringIO

from defines import (HTML_ORG_DIV_DATE_CLASS,
                     HTML_ORG_TABLE_CLASS,
                     HTML_ORG_DIV_CLASS,
                     HTML_EMPTY_CELL_CONTENT)


class OrgHTMLGenerator (object):
    """It is HTML generator for (:org:) command"""
    def __init__ (self, config, parser):
        self._dateConfig = config.dateTimeFormat.value
        self._styles = config.orgStyles.value
        self._parser = parser


    def getHTML (self, dayDescription):
        builder = StringIO()

        builder.write (u'<div class="{}">\n'.format (HTML_ORG_DIV_CLASS))

        if dayDescription.date is not None:
            date_str = dayDescription.date.strftime (self._dateConfig)
            builder.write (self._getDateHTML(date_str))

        builder.write (self._getTableHTML (dayDescription))

        builder.write (u'</div>\n')
        return builder.getvalue()


    def getStyles (self):
        return self._styles


    def _getTableHTML (self, dayDescription):
        headers = self._getHeaders (dayDescription)
        builder = StringIO()
        builder.write (u'<table class="{}">\n'.format (HTML_ORG_TABLE_CLASS))

        if headers:
            # Append headers
            builder.write ('<tr>')
            for header in headers:
                builder.write ('<th>{}</th>'.format (header))
            builder.write ('</tr>\n')

            # Append rows
            for record in dayDescription:
                builder.write (self._getRecordRowHTML (headers, record))

        builder.write (u'</table>\n')
        return builder.getvalue()


    def _getRecordRowHTML (self, headers, record):
        builder = StringIO()
        builder.write ('<tr>')
        for header in headers:
            builder.write ('<td>')
            item = record[header]
            if item is not None:
                builder.write (self._parser.parseWikiMarkup (item))
            else:
                builder.write (HTML_EMPTY_CELL_CONTENT)
            builder.write ('</td>')

        builder.write ('</tr>\n')
        return builder.getvalue()


    def _getDateHTML (self, date_str):
        return u'<div class="{classname}">{content}</div>'.format (
            classname = HTML_ORG_DIV_DATE_CLASS,
            content = date_str
            )


    def _getHeaders (self, dayDescription):
        headers = []
        for record in dayDescription:
            for header in record:
                if header not in headers:
                    headers.append (header)

        return headers
