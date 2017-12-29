# -*- coding: utf-8 -*-

import re

from outwiker.pages.wiki.parser.command import Command

from .renders.highcharts import HighChartsRender
from .graphbuilder import GraphBuilder
from . import defines


class BasePlotCommand(Command):
    def __init__(self, parser):
        """
        parser - экземпляр парсера
        """
        super(BasePlotCommand, self).__init__(parser)
        self._renders = {
            u'highcharts': HighChartsRender(parser),
        }

    @staticmethod
    def parseGraphParams(params):
        """
        Parse params string into parts: key - value. Key may contain a dot.
        Sample params:
            param1
            Параметр2.subparam = 111
            Параметр3 = " bla bla bla"
            param4.sub.param2 = "111"
            param5 =' 222 '
            param7 = " sample 'bla bla bla' example"
            param8 = ' test "bla-bla-bla" test '
        """
        pattern = r"""((?P<name>[\w.]+)
   (\s*=\s*(?P<param>([-_\w.]+)|((?P<quote>["']).*?(?P=quote)) ) )?\s*)"""

        result = {}

        regex = re.compile(
            pattern,
            re.IGNORECASE | re.MULTILINE | re.DOTALL | re.VERBOSE
        )
        matches = regex.finditer(params)

        for match in matches:
            name = match.group("name")
            param = match.group("param")
            if param is None:
                param = u""

            result[name] = Command.removeQuotes(param)

        return result


class PlotCommand(BasePlotCommand):
    """ Create graph by(:plot:) command
    """
    @property
    def name(self):
        """
        Возвращает имя команды, которую обрабатывает класс
        """
        return u"plot"

    def execute(self, params, content):
        """
        Запустить команду на выполнение.
        Метод возвращает текст, который будет вставлен на место
            команды в вики-нотации
        """
        params_dict = self.parseGraphParams(params)
        graph = GraphBuilder(params_dict, content, self.parser.page).graph
        render = self._getRender(graph)

        return render.addGraph(graph)

    def _getRender(self, graph):
        rendername = graph.getProperty(defines.RENDER_NAME,
                                       defines.RENDER_HIGHCHARTS)
        render = self._renders.get(rendername,
                                   self._renders[defines.RENDER_HIGHCHARTS])
        return render
