# -*- coding: UTF-8 -*-
""" Module for the graph creation with HighCharts library
"""

from datagraph import defines


class HighChartsRender (object):
    """ Class for the graph creation with HighCharts library
    """
    def __init__ (self, wikiparser):
        self._wikiparser = wikiparser

        # Count of the graphs
        self._count = 0


    def addGraph (self, graph):
        """
        graph - instance of the Graph class.
        Return string which must be inserted in place of the (:plot:) command
        """
        width = graph.getProperty (defines.GRAPH_WIDTH_NAME, defines.GRAPH_WIDTH)
        height = graph.getProperty (defines.GRAPH_HEIGHT_NAME, defines.GRAPH_HEIGHT)

        if width[-1].isdigit():
            width += u'px'

        if height[-1].isdigit():
            height += u'px'

        name = u'graph-{}'.format (self._count)
        result = u'<div id="{name}" style="width:{width}; height:{height};"></div>'.format (
            name = name, width = width, height = height)

        self._count += 1

        return result
