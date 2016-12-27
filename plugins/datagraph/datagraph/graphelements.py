# -*- coding: UTF-8 -*-

import defines

# Values types
TYPE_OBJECT = 0
TYPE_STRING = 1
TYPE_INT = 2
TYPE_FLOAT = 3
TYPE_DATE = 4


class BaseGraphObject(object):
    """ Base class for graph elements
    """
    def __init__(self):
        self._properties = {}
        self._objects = {}

    def getProperty(self, key, default):
        return self._properties.get(key.lower(), default)

    def setProperty(self, key, value):
        self._properties[key.lower()] = value

    def getObject(self, key):
        return self._objects.get(self._prepareObjectKey(key), None)

    def addObject(self, key, obj):
        key = self._prepareObjectKey(key)
        self._objects[key] = obj

    def _prepareObjectKey(self, key):
        if key[-1].isalpha():
            key += u'1'

        key = key.lower()
        return key


class Graph(BaseGraphObject):
    """Class with the properties graph as a whole.
    Contain other parts of the graph."""
    def __init__(self):
        super(Graph, self).__init__()
        self.setProperty(defines.GRAPH_WIDTH_NAME, defines.GRAPH_WIDTH)
        self.setProperty(defines.GRAPH_HEIGHT_NAME, defines.GRAPH_HEIGHT)
        self.addObject(defines.GRAPH_XAXIS_NAME, Axis())
        self.addObject(defines.GRAPH_YAXIS_NAME, Axis())

    def getCurves(self):
        curves = [self._objects[name]
                  for name
                  in sorted(self._objects.keys(), key=self._sortCurves)
                  if name.lower().startswith(u'curve')]

        return curves

    def _sortCurves(self, curvename):
        """
        Sort curves by name: curve1 < curve2 < curve10
        """
        number = curvename.lower().replace(u'curve', u'')
        if len(number) == 0:
            number = '1'

        try:
            return int(number)
        except ValueError:
            return 0


class Curve(BaseGraphObject):
    """Single curve on the graph."""
    def __init__(self):
        super(Curve, self).__init__()
        self.setProperty(defines.CURVE_WIDTH_NAME, defines.GRAPH_WIDTH)
        self.setProperty(defines.CURVE_YCOL_NUMBER_NAME,
                         defines.CURVE_YCOL_NUMBER)
        self.setProperty(defines.CURVE_XCOL_NUMBER_NAME,
                         defines.CURVE_XCOL_NUMBER)
        self.setProperty(defines.CURVE_DATA_NAME, defines.CURVE_DATA)
        self.addObject(defines.CURVE_DATA_OBJECT_NAME, Data())


class Axis(BaseGraphObject):
    """Axis on the graph."""
    def __init__(self):
        super(Axis, self).__init__()


class Legend(BaseGraphObject):
    """Legend for pane."""
    def __init__(self):
        super(Legend, self).__init__()


class Data(BaseGraphObject):
    """Information for data parsing"""
    def __init__(self):
        super(Data, self).__init__()
        self._dataSource = None

    def getRowsIterator(self):
        """Return iterator for rows."""
        assert self._dataSource is not None
        return self._dataSource.getRowsIterator()

    def setSource(self, source):
        """Set source data(StringSource or FileSource)"""
        self._dataSource = source

    def getSource(self):
        return self._dataSource
