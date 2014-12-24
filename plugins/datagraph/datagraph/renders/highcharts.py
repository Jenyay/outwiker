# -*- coding: UTF-8 -*-
""" Module for the graph creation with HighCharts library
"""

import shutil
import os
import os.path
from datagraph.libs.json import dumps

from datagraph import defines
from outwiker.core.attachment import Attachment
from outwiker.core.system import getOS


class HighChartsRender (object):
    """ Class for the graph creation with HighCharts library
    """
    def __init__ (self, wikiparser):
        self._wikiparser = wikiparser

        # Count of the graphs
        self._count = 0

        self._headers = u'''<!--[if lt IE 9]><script language="javascript" type="text/javascript" src="__attach/__thumb/__js/excanvas.js"></script><![endif]-->
\t<script language="javascript" type="text/javascript" src="__attach/__thumb/__js/jquery.min.js"></script>
\t<script language="javascript" type="text/javascript" src="__attach/__thumb/__js/highcharts.js"></script>'''


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

        if self._count == 0:
            self._wikiparser.appendToHead (self._headers)
            try:
                self._setup ()
            except Exception, e:
                return str (e)

        script = self._getGraphScript (graph, name)
        self._wikiparser.appendToHead (script)

        self._count += 1

        return result


    def _getGraphScript (self, graph, graphname):
        properties = self._getJsonResult (graph)

        result = u'''<script>
$(function () {{ $('#{name}').highcharts({prop}); }});
</script>'''.format (name=graphname, prop=properties)

        return result


    def _setup (self):
        """
        Prepare to using the library
        """
        dirname = unicode (os.path.dirname(os.path.abspath(__file__)), getOS().filesEncoding)
        libfiles = [u'excanvas.min.js', u'highcharts.js', u'jquery.min.js']

        libpath = [os.path.join (dirname, u'js', fname) for fname in libfiles]

        jsdir = self._getJsDir ()

        if not os.path.exists(jsdir):
            os.makedirs (jsdir)

        for fname in libpath:
            shutil.copy (fname, jsdir)


    def _getJsDir (self):
        attachdir = Attachment (self._wikiparser.page).getAttachPath (create=True)
        return os.path.join (attachdir, u'__thumb', u'__js')


    def _getJsonResult (self, graph):
        chartDict = self._buildChartDict (graph)
        result = dumps (chartDict)

        return result


    def _buildChartDict (self, graph):
        chartDict = {}

        chartDict[u'credits'] = {u'enabled': False}
        chartDict[u'series'] = self._getSeries (graph)
        chartDict[u'tooltip'] = {u'enabled': False}

        return chartDict


    def _getSeries (self, graph):
        series = []
        for n, curve in enumerate (graph.getCurves()):
            data = self._getData (curve)

            singleSeries = {
                u'data': data,
                u'animation': False,
                u'states': {u'hover': {u'enabled': False}}
            }

            series.append (singleSeries)

        return series


    def _getData (self, curve):
        """
        Return list of the list with points
        """
        result = []

        data = curve.getObject (defines.CURVE_DATA_OBJECT_NAME)

        for n, row in enumerate (data.getRowsIterator()):
            # Calculate columns numbers if they are not assigned
            if n == 0:
                try:
                    xcol = self._getXCol (curve, row)
                    ycol = self._getYcol (curve, row)
                except ValueError:
                    break

            # Create point
            try:
                yval = self._convertValue (curve, ycol, row[ycol - 1])

                if xcol is None:
                    xval = n
                else:
                    xval = self._convertValue (curve, xcol, row[xcol - 1])
            except (IndexError, ValueError):
                break

            result.append ([xval, yval])

        return result


    def _getXCol (self, curve, firstrow):
        xcol = curve.getProperty (defines.CURVE_XCOL_NUMBER_NAME, defines.CURVE_XCOL_NUMBER)

        if xcol is None and len (firstrow) > 1:
            xcol = 1

        if xcol is not None:
            xcol = int (xcol)

        return xcol


    def _getYcol (self, curve, firstrow):
        ycol = curve.getProperty (defines.CURVE_YCOL_NUMBER_NAME, defines.CURVE_YCOL_NUMBER)

        if ycol is None and len (firstrow) > 1:
            ycol = 2
        elif ycol is None:
            ycol = 1

        ycol = int (ycol)

        return ycol



    def _convertValue (self, curve, col, value):
        """ Convert data by column format settings
        """
        return float (value)
