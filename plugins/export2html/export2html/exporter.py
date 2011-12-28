#!/usr/bin/python
# -*- coding: UTF-8 -*-

from .exceptions import InvalidPageFormat
from .htmlexporter import HtmlExporter
from .textexporter import TextExporter


class Exporter (object):
    """
    Класс для экспорта страниц в HTML
    """
    @staticmethod
    def exportPage (page,
            outdir,
            imagesonly,
            alwaisOverwrite):
        assert page != None

        exporter = None

        if page.getTypeString() == "html" or page.getTypeString() == "wiki":
            exporter = HtmlExporter()
        elif page.getTypeString() == "text":
            exporter = TextExporter()
        else:
            raise InvalidPageFormat (_(u"Invalid page format"))

        assert exporter != None
        exporter.export (page, outdir, imagesonly, alwaisOverwrite)
