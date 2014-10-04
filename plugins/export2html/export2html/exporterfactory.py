# -*- coding: UTF-8 -*-

from .exceptions import InvalidPageFormat
from .htmlexporter import HtmlExporter
from .textexporter import TextExporter


class ExporterFactory (object):
    """
    Класс для экспорта страниц в HTML
    """
    @staticmethod
    def getExporter (page):
        exporter = None

        from .i18n import _
        global _

        if page.getTypeString() == "html" or page.getTypeString() == "wiki":
            exporter = HtmlExporter(page)
        elif page.getTypeString() == "text":
            exporter = TextExporter(page)
        else:
            raise InvalidPageFormat (_(u"This page type not support export to HTML"))

        assert exporter is not None
        return exporter
