# -*- coding: UTF-8 -*-

import defines

# Values types
TYPE_OBJECT = 0
TYPE_STRING = 1
TYPE_INT = 2
TYPE_FLOAT = 3
TYPE_DATE = 4


class BaseGraphObject (object):
    """ Base class for graph elements
    """
    def __init__ (self):
        self._properties = {}


    def getValue (self, key):
        return self._properties.get (key.lower(), None)


    def setValue (self, key, value):
        self._properties[key.lower()] = value



class Graph (BaseGraphObject):
    """Class with the properties graph as a whole.
    Contain other parts of the graph."""
    def __init__(self):
        super (Graph, self).__init__()
        self.setValue (defines.GRAPH_WIDTH_NAME, defines.GRAPH_WIDTH)
        self.setValue (defines.GRAPH_HEIGHT_NAME, defines.GRAPH_HEIGHT)



class Pane (BaseGraphObject):
    """Pane with the curves and axes."""
    def __init__ (self):
        super (Pane, self).__init__()



class Curve (BaseGraphObject):
    """Single curve on the graph."""
    def __init__ (self, color):
        super (Curve, self).__init__()
        self.setValue (defines.CURVE_WIDTH_NAME, defines.GRAPH_WIDTH)
        self.setValue (defines.CURVE_COLOR_NAME, color)



class Axis (BaseGraphObject):
    """Axis on the graph."""
    def __init__ (self):
        super (Axis, self).__init__()



class Legend (BaseGraphObject):
    """Legend for pane."""
    def __init__ (self):
        super (Legend, self).__init__()
