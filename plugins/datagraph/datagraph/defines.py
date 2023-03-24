# -*- coding: utf-8 -*-
"""Default values of the parameters"""

GRAPH_WIDTH_NAME = "width"
GRAPH_WIDTH = "700"

GRAPH_HEIGHT_NAME = "height"
GRAPH_HEIGHT = "300"

GRAPH_XAXIS_NAME = "x"
GRAPH_YAXIS_NAME = "y"
GRAPH_TITLE_NAME = "title"
GRAPH_TOOLTIP_NAME = "tooltip"
GRAPH_LEGEND_NAME = "legend"


# Sequence of the default colors
CURVE_COLOR_NAME = "color"
CURVE_COLORS = [
    "#0051FF",
    "#FF0000",
    "#19D400",
    "#000000",
    "#FF8214",
    "#B700FF",
    "#1E9E19",
    "#9C571F",
    "#8C8741",
]

CURVE_SYMBOLS = ["circle", "square", "diamond", "triangle", "triangle-down"]

CURVE_STYLES = [
    "solid",
    "longdash",
    "shortdash",
    "shortdot",
    "shortdashdot",
    "shortdashdotdot",
    "dot",
    "dash",
    "dashdot",
    "longdashdot",
    "longdashdotdot",
]

CURVE_STYLE_NAME = "style"

CURVE_STYLE_AUTO = "auto"

# Default curve thickness
CURVE_WIDTH_NAME = "width"
CURVE_WIDTH = "3"

# Numbers of the columns in data
CURVE_YCOL_NUMBER_NAME = "ycol"
CURVE_YCOL_NUMBER = None

CURVE_XCOL_NUMBER_NAME = "xcol"
CURVE_XCOL_NUMBER = None

# X coordinates are the row number
CURVE_XCOL_NUMBER_VALUE = "number"

# Data source
CURVE_DATA_NAME = "data"
CURVE_DATA_OBJECT_NAME = "data"


# If CURVE_DATA is None, data reads from command content
# else CURVE_DATA is name of the Attachment
CURVE_DATA = None

CURVE_TITLE_NAME = "title"
CURVE_HIDE_NAME = "hide"


DATA_COLUMNS_SEPARATOR_NAME = "colsep"
DATA_COLUMNS_SEPARATOR_DEFAULT = r"\s+"

# For selection render engine (at the time is not used)
RENDER_NAME = "render"
RENDER_HIGHCHARTS = "highcharts"


# Axis properties
AXIS_TITLE_NAME = "title"
AXIS_MIN_NAME = "min"
AXIS_MAX_NAME = "max"

# Axis types
AXIS_TYPE_NAME = "type"
AXIS_TYPE_DATE = "datetime"

# Data properties
DATA_FORMAT_COL = "formatcol"
DATA_SKIP_ROWS_NAME = "skiprows"

AXIS_MAJOR_TICK_INTERVAL_NAME = "tickstep"

TOOLBAR_DATAGRAPH = "Plugin_DataGraph"
MENU_DATAGRAPH = "Plugin_DataGraph"
