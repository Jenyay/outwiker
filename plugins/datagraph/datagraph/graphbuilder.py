# -*- coding: UTF-8 -*-

import re

from graphelements import Graph, Curve


class GraphBuilder (object):
    """Class for creation Graph and fill its properties"""

    def __init__(self, params_dict, content, page):
        """
        params_dict - dictionary with parameters of the (:plot:) command
        content - text between (:plot:) and (:plotend:)
        page - wiki page for that will create graph
        """
        self._graph = Graph()
        self._build (params_dict)


    def _build (self, params_dict):
        self._createCurves (params_dict)
        self._setUpProperties (params_dict)


    def _setUpProperties (self, params_dict):
        """Set up properties of the inner objects"""
        self._sep = u'.'

        for key, val in params_dict.iteritems():
            if key.endswith (self._sep):
                key = key[:-1]

            self._setObjectProperty (self.graph, key, val)


    def _setObjectProperty (self, obj, key, val):
        splitted = [subkey.lower() for subkey in key.split (self._sep, 1) if len (subkey) != 0]
        if len (splitted) == 1:
            obj.setProperty (splitted[0], val)
        else:
            subobject = obj.getObject (splitted[0])
            if subobject is not None:
                self._setObjectProperty (subobject, splitted[1], val)


    def _createCurves (self, params_dict):
        """Create curves by parameters"""
        curvename = re.compile (r'^(?P<name>curve\d*)\.', re.IGNORECASE)
        names = set([u'curve'])

        for key in params_dict.keys():
            match = curvename.match (key)
            if match is not None:
                names.update (match.groups ('name'))

        for name in names:
            self._graph.addObject (name.lower(), Curve ())


    @property
    def graph (self):
        return self._graph
