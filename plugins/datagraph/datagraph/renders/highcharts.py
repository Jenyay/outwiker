# -*- coding: UTF-8 -*-
""" Module for the graph creation with HighCharts library
"""

from datetime import datetime
import os
import os.path
import shutil

from outwiker.core.attachment import Attachment
from outwiker.core.system import getOS

from datagraph.libs.json import dumps
from datagraph.libs.dateutil.parser import parser
from datagraph import defines
# from datagraph.dateparser import createDateTime


class HighChartsRender (object):
    """ Class for the graph creation with HighCharts library
    """
    def __init__ (self, wikiparser):
        self._wikiparser = wikiparser

        # Count of the graphs
        self._count = 0

        self._headers = [
            (u'excanvas.min.js', u'<!--[if lt IE 9]><script language="javascript" type="text/javascript" src="__attach/__thumb/__js/excanvas.min.js"></script><![endif]-->'),

            (u'jquery.min.js', u'<script language="javascript" type="text/javascript" src="__attach/__thumb/__js/jquery.min.js"></script>'),

            (u'highcharts.js', u'<script language="javascript" type="text/javascript" src="__attach/__thumb/__js/highcharts.js"></script>'),
        ]


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
            # Check what jquery, excanvas or highcharts not append yet
            for libname, header in self._headers:
                if libname not in self._wikiparser.head:
                    self._wikiparser.appendToHead (header)
                    try:
                        self._setup (libname)
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


    def _setup (self, libname):
        """
        Prepare to using the library
        """
        # Get path to JS files inside the plugin
        dirname = unicode (os.path.dirname(os.path.abspath(__file__)), getOS().filesEncoding)
        libpath = os.path.join (dirname, u'js', libname)

        # Get destination path fo JS files
        jsdir = self._getJsDir ()

        if not os.path.exists(jsdir):
            os.makedirs (jsdir)

        shutil.copy (libpath, jsdir)


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
        chartDict[u'plotOptions'] = self._getPlotOptions (graph)

        return chartDict


    def _getPlotOptions (self, graph):
        plotOptions = {}

        return plotOptions


    def _getTitle (self, graph):
        text = graph.getProperty (defines.GRAPH_TITLE_NAME, None)

        title = {
            u'text': text,
        }

        return title


    def _getLegend (self, graph):
        enabled = (graph.getProperty (defines.GRAPH_LEGEND_NAME, '0') != '0')

        legend = {
            u'enabled': enabled,
            u'symbolWidth': 60,
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

        try:
            result[u'min'] = self._convertMinMaxAxisValue (minVal, axis)
        except ValueError:
            pass

        try:
            result[u'max'] = self._convertMinMaxAxisValue (maxVal, axis)
        except ValueError:
            pass

        # Major ticks
        majorTickInterval = axis.getProperty (defines.AXIS_MAJOR_TICK_INTERVAL_NAME, None)
        try:
            interval = self._convertIntervalAxisValue (majorTickInterval, axis)
            if interval > 0:
                result[u'tickInterval'] = interval
        except ValueError:
            pass

        # Axis type
        axisType = axis.getProperty (defines.AXIS_TYPE_NAME, None)

        if axisType == defines.AXIS_TYPE_DATE:
            result[u'type'] = u'datetime'
            result[u'labels'] = {u'format': u'{value:%d.%m.%Y}'}

        return result


    def _getTooltip (self, graph):
        enabled = (graph.getProperty (defines.GRAPH_TOOLTIP_NAME, '0') != '0')

        tooltip = {
            u'enabled': enabled,
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
            hide = curve.getProperty (defines.CURVE_HIDE_NAME, u'0')
            if not data or hide != u'0':
                continue

            singleSeries = {
                u'data': data,
                u'animation': False,
                u'states': {u'hover': {u'enabled': False}},
                u'marker': self._getMarker (curve, n),
                u'dashStyle': self._getCurveStyle (curve, n),
            }

            # Curve's color
            color = curve.getProperty (defines.CURVE_COLOR_NAME, None)
            if color is not None:
                singleSeries[u'color'] = color
            else:
                singleSeries[u'color'] = defines.CURVE_COLORS[n % len (defines.CURVE_COLORS)]

            # Curve's title
            title = curve.getProperty (defines.CURVE_TITLE_NAME, None)
            if title is None:
                title = _(u'Curve-{}').format (n + 1)

            singleSeries[u'name'] = title

            series.append (singleSeries)

        return series


    def _getCurveStyle (self, curve, n):
        style = curve.getProperty (defines.CURVE_STYLE_NAME, defines.CURVE_STYLES[0]).strip().lower()

        # If style is number
        try:
            styleNumber = int (style)
            style = defines.CURVE_STYLES[(styleNumber - 1) % len (defines.CURVE_STYLES)]
        except ValueError:
            pass

        if style == defines.CURVE_STYLE_AUTO:
            style = defines.CURVE_STYLES[n % len (defines.CURVE_STYLES)]

        return style


    def _getMarker (self, curve, n):
        marker = {
            u'symbol': defines.CURVE_SYMBOLS[n % len (defines.CURVE_SYMBOLS)],
            u'enabled': False,
        }

        return marker


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


    def _date2float (self, date):
        epoch = datetime.utcfromtimestamp(0)
        delta = (date - epoch).total_seconds() * 1000.0
        return delta


    def _convertValue (self, colFormat, value):
        """ Convert data by column format settings
        """
        if colFormat is not None:
            return self._date2float (datetime.strptime (value, colFormat))
        else:
            return float (value)


    def _convertMinMaxAxisValue (self, value, axis):
        if value is None:
            raise ValueError

        axisType = axis.getProperty (defines.AXIS_TYPE_NAME, None)
        if axisType == defines.AXIS_TYPE_DATE:
            return self._date2float (self._createDateTime (value))

        return float (value)


    def _convertIntervalAxisValue (self, value, axis):
        if value is None:
            raise ValueError

        return float (value)


    def _createDateTime (self, text):
        if len (text.strip()) == 0:
            raise ValueError

        dateparser = parser()
        date = dateparser.parse (text)

        return date
