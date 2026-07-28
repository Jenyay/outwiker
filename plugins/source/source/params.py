# -*- coding: utf-8 -*-

"""
Constants for (:source:) command
"""

# Source command parameters

# Parameter name for attached file
FILE_PARAM_NAME = "file"

# Parameter name for language
LANGUAGE_PARAM_NAME = "lang"

# Parameter name for encoding of attached file
ENCODING_PARAM_NAME = "encoding"

# Parameter name for tab size
TAB_WIDTH_PARAM_NAME = "tabwidth"

# Parameter name for style
STYLE_PARAM_NAME = "style"

# Parameter name to use page background in code block
PARENT_BACKGROUND_PARAM_NAME = "parentbg"

# Parameter name to add line numbers
LINE_NUM_PARAM_NAME = "linenum"


# Default values

# Default programming language
LANGUAGE_DEFAULT = "text"

# Default encoding
ENCODING_DEFAULT = "utf8"

# Default tab size
TAB_WIDTH_DEFAULT = 4

# Default style name
STYLE_DEFAULT = "default"


# Additional styles

# Style for main div
HIGHLIGHT_STYLE = "{padding: 1em; }"

# Default programming languages list
LANGUAGE_LIST_DEFAULT = [
    "text",
    "c",
    "cpp",
    "csharp",
    "php",
    "python",
    "html",
    "css",
    "ruby",
    "java",
    "javascript",
    "objective-c",
    "perl",
    "vb.net",
]

CSS_SOURCE_PLUGIN = "ow-plugin-source"
CSS_SOURCE_BLOCK = "ow-plugin-source-block"


CUSTOM_STYLES = """
.{name} pre {{padding: 0px; border: none; color: inherit; background-color: inherit; margin:0px; }}
.{name} table {{padding: 0px; border: none;}}
.{name}table td {{border-width:0; vertical-align: baseline; }}
.{name}table tr {{vertical-align: baseline; }}
.{name}table tbody {{vertical-align: baseline; }}
.{name}table td.code {{width:100%; }}
.ow-plugin-source-block pre {{padding: 0px; border: none; color: inherit; background-color: inherit; }}
.linenodiv pre {{padding: 0px; border: none; color: inherit; background-color: inherit; }}
div.ow-plugin-source-block {{border-style: solid; border-color: gray; border-width: 1px; }}"""
