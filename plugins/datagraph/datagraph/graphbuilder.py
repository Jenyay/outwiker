# -*- coding: UTF-8 -*-

from graphelements import Graph


class GraphBuilder (object):
    """Class for creation Graph and fill its properties"""
    def __init__(self, params_dict):
        self._graph = Graph()
        self._build (self._graph, params_dict)


    def _build (self, graph, params_dict):
        pass


    def setProperty (self, param, value):
        pass


    @property
    def graph (self):
        return self._graph
