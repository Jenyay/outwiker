# -*- coding: UTF-8 -*-
""" Module for the graph creation with HighCharts library
"""

from datetime import datetime
import os
import os.path
import shutil

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

        series = self._getSeries (graph)
        if series:
            chartDict[u'series'] = series

        chartDict[u'tooltip'] = self._getTooltip (graph)
        chartDict[u'chart'] = self._getChart (graph)
        chartDict[u'credits'] = self._getCredits (graph)
        chartDict[u'xAxis'] = self._getXAxis (graph)
        chartDict[u'yAxis'] = self._getYAxis (graph)
        chartDict[u'title'] = self._getTitle (graph)
        chartDict[u'legend'] = self._getLegend (graph)

        return chartDict


    def _getTitle (self, graph):
        title = {
            u'text': None,
        }

        return title


    def _getLegend (self, graph):
        legend = {
            u'enabled': False,
        }

        return legend


    def _getXAxis (self, graph):
        assert graph is not None

        axis = graph.getObject (defines.GRAPH_XAXIS_NAME)
        return self._getAxis (axis)


    def _getYAxis (self, graph):
        assert graph is not None

        axis = graph.getObject (defines.GRAPH_YAXIS_NAME)
        return self._getAxis (axis)


    def _getAxis (self, axis):
        assert axis is not None

        text = axis.getProperty (defines.AXIS_TITLE_NAME, None)

        title = {
            u'text': text,
        }

        result = {
            u'gridLineWidth': 1,
            u'title': title,
        }

        # Min / Max values
        minVal = axis.getProperty (defines.AXIS_MIN_NAME, None)
        maxVal = axis.getProperty (defines.AXIS_MAX_NAME, None)
        if minVal is not None:
            try:
                result[u'min'] = self._convertAxisValue (minVal, axis)
            except ValueError:
                pass

        if maxVal is not None:
            try:
                result[u'max'] = self._convertAxisValue (maxVal, axis)
            except ValueError:
                pass

        # Axis type
        axisType = axis.getProperty (defines.AXIS_TYPE_NAME, None)

        if axisType == defines.AXIS_TYPE_DATE:
            result[u'type'] = u'datetime'
            result[u'labels'] = {u'format': u'{value:%d.%m.%Y}'}

        return result


    def _getTooltip (self, graph):
        tooltip = {
            u'enabled': False,
        }

        return tooltip


    def _getCredits (self, graph):
        credits = {
            u'enabled': False,
        }

        return credits


    def _getChart (self, graph):
        chart = {
            u'plotBorderWidth': 1,
            u'animation': False,
        }

        return chart


    def _getSeries (self, graph):
        series = []
        for n, curve in enumerate (graph.getCurves()):
            data = self._getData (curve)
            if not data:
                continue

            singleSeries = {
                u'data': data,
                u'animation': False,
                u'states': {u'hover': {u'enabled': False}}
            }

            color = curve.getProperty (defines.CURVE_COLOR_NAME, None)
            if color is not None:
                singleSeries[u'color'] = color

            series.append (singleSeries)

        return series


    def _getData (self, curve):
        """
        Return list of the list with points
        """
        result = []

        data = curve.getObject (defines.CURVE_DATA_OBJECT_NAME)
        xColFormat = None
        yColFormat = None

        for n, row in enumerate (data.getRowsIterator()):
            # Calculate columns numbers if they are not assigned
            if n == 0:
                try:
                    xcol = self._getXCol (curve, row)
                    ycol = self._getYcol (curve, row)
                except ValueError:
                    break

                if ((xcol is not None and xcol < 1) or
                        (ycol is not None and ycol < 1)):
                    break

                if xcol is not None:
                    xColFormat = data.getProperty (
                        u'{}{}'.format (defines.DATA_FORMAT_COL, xcol),
                        None
                    )

                if ycol is not None:
                    yColFormat = data.getProperty (
                        u'{}{}'.format (defines.DATA_FORMAT_COL, ycol),
                        None
                    )

            # Create point
            try:
                yval = self._convertValue (yColFormat, row[ycol - 1])

                if xcol is None:
                    xval = n
                else:
                    xval = self._convertValue (xColFormat, row[xcol - 1])
            except (IndexError, ValueError):
                break

            result.append ([xval, yval])

        return result


    def _getXCol (self, curve, firstrow):
        xcol = curve.getProperty (defines.CURVE_XCOL_NUMBER_NAME, defines.CURVE_XCOL_NUMBER)

        if xcol is not None and xcol.strip() == defines.CURVE_XCOL_NUMBER_VALUE:
            xcol = None
        elif xcol is None and len (firstrow) > 1:
            xcol = 1
        elif xcol is not None:
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



    def _convertValue (self, colFormat, value):
        """ Convert data by column format settings
        """
        if colFormat is not None:
            date = datetime.strptime (value, colFormat)
            epoch = datetime.utcfromtimestamp(0)
            delta = (date - epoch).total_seconds() * 1000.0
            return delta
        else:
            return float (value)


    def _convertAxisValue (self, value, axis):
        return float (value)
