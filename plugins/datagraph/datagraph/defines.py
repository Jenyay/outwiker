# -*- coding: UTF-8 -*-
"""Default values of the parameters"""

GRAPH_WIDTH_NAME = u'width'
GRAPH_WIDTH = u'700'

GRAPH_HEIGHT_NAME = u'height'
GRAPH_HEIGHT = u'300'

GRAPH_XAXIS_NAME = u'x'
GRAPH_YAXIS_NAME = u'y'

# Sequence of the default colors
CURVE_COLOR_NAME = u'color'
CURVE_COLORS = [u'#0051FF', u'#FF0000', u'#19D400', u'#000000',
                u'#FF8214', u'#B700FF', u'#1E9E19', u'#9C571F',
                u'#8C8741']

# Default curve thickness
CURVE_WIDTH_NAME = u'width'
CURVE_WIDTH = u'3'

# Numbers of the columns in data
CURVE_YCOL_NUMBER_NAME = u'ycol'
CURVE_YCOL_NUMBER = None

CURVE_XCOL_NUMBER_NAME = u'xcol'
CURVE_XCOL_NUMBER = None

# X coordinates are the row number
CURVE_XCOL_NUMBER_VALUE = u'number'

# Data source
CURVE_DATA_NAME = u'data'
CURVE_DATA_OBJECT_NAME = u'data'

DATA_FORMAT_COL = u'formatcol'

# If CURVE_DATA is None, data reads from command content
# else CURVE_DATA is name of the Attachment
CURVE_DATA = None


COLUMNS_SEPARATOR_NAME = u'colsep'
COLUMNS_SEPARATOR = r'\s+'

# For selection render engine (at the time is not used)
RENDER_NAME = u'render'
RENDER_HIGHCHARTS = u'highcharts'


# Axis properties
AXIS_TITLE_NAME = u'title'
AXIS_MIN_NAME = u'min'
AXIS_MAX_NAME = u'max'

# Axis types
AXIS_TYPE_NAME = u'type'
AXIS_TYPE_DATE = u'datetime'
