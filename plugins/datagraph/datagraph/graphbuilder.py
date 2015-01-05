# -*- coding: UTF-8 -*-

import re

from outwiker.core.attachment import Attachment

from graphelements import Graph, Curve
from datasources import StringSource, FileSource
import defines


class GraphBuilder (object):
    """Class for creation Graph and fill its properties"""

    def __init__(self, params_dict, content, page):
        """
        params_dict - dictionary with parameters of the (:plot:) command
        content - text between (:plot:) and (:plotend:)
        page - wiki page for that will create graph
        """
        self._graph = Graph()
        self._build (params_dict, page, content)


    def _build (self, params_dict, page, content):
        curvenames = self._createCurves (params_dict)
        self._setUpProperties (params_dict)
        self._setDataSources (curvenames, page, content)


    def _setUpProperties (self, params_dict):
        """Set-up properties of the inner objects"""
        self._sep = u'.'

        for key, val in params_dict.iteritems():
            if key.endswith (self._sep):
                key = key[:-1]

            self._setObjectProperties (self.graph, key, val)


    def _setObjectProperties (self, obj, key, val):
        """ Set properties for single object and them children
        """
        splitted = [subkey.lower() for subkey in key.split (self._sep, 1) if len (subkey) != 0]
        if len (splitted) == 1:
            obj.setProperty (splitted[0], val)
        else:
            subobject = obj.getObject (splitted[0])
            if subobject is not None:
                self._setObjectProperties (subobject, splitted[1], val)


    def _createCurves (self, params_dict):
        """Create curves by parameters.
        Return set of the names of the new curves"""

        curvename = re.compile (r'^(?P<name>curve\d*)\.', re.IGNORECASE)
        names = set([u'curve'])

        for key in params_dict.keys():
            match = curvename.match (key)
            if match is not None:
                names.update (match.groups ('name'))

        for name in names:
            self._graph.addObject (name.lower(), Curve())

        return names


    def _setDataSources (self, curvenames, page, content):
        """
        Set data sources (StringSource or FileSource) for all curves
        """
        for name in curvenames:
            curve = self._graph.getObject (name)
            assert curve is not None

            data = curve.getObject (defines.CURVE_DATA_OBJECT_NAME)
            assert data is not None

            colsep = data.getProperty (defines.DATA_COLUMNS_SEPARATOR_NAME,
                                       defines.DATA_COLUMNS_SEPARATOR_DEFAULT)

            try:
                skiprows = int (data.getProperty (defines.DATA_SKIP_ROWS_NAME, '0'))
            except ValueError:
                skiprows = 0

            attachName = curve.getProperty (defines.CURVE_DATA_NAME, None)
            if attachName is None:
                data.setSource (StringSource (content.strip(), colsep=colsep, skiprows=skiprows))
            else:
                # Remove prefix "Attach:"
                attachPrefix = u'Attach:'
                if attachName.startswith (attachPrefix):
                    attachName = attachName[len (attachPrefix):]

                # Get full path to the attached file
                path = Attachment (page).getFullPath (attachName)
                data.setSource (FileSource (path, colsep=colsep, skiprows=skiprows))


    @property
    def graph (self):
        return self._graph
