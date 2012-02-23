#!/usr/bin/python
# -*- coding: UTF-8 -*-

from .exporterfactory import ExporterFactory
from .branchexporter import BranchExporter
from .longnamegenerator import LongNameGenerator
from .titlenamegenerator import TitleNameGenerator


class Tester (object):
    @property
    def exporterFactory (self):
        """
        Возвращает класс Exporter, чтобы его можно было легче тестировать при загрузке плагина в реальном времени
        """
        return ExporterFactory


    @property
    def branchExporter (self):
        return BranchExporter


    @property
    def longNameGenerator (self):
        return LongNameGenerator

    @property
    def titleNameGenerator (self):
        return TitleNameGenerator
