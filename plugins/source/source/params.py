# -*- coding: UTF-8 -*-

"""
Константы для команды (:source:)
"""

# Параметры команды source

# Имя параметра для указания прикрепленного файла
FILE_PARAM_NAME = u"file"

# Имя параметра для указания языка
LANGUAGE_PARAM_NAME = u"lang"

# Имя параметра для указания кодировки прикрепленного файла
ENCODING_PARAM_NAME = "encoding"

# Имя параметра для размера табуляции
TAB_WIDTH_PARAM_NAME = u"tabwidth"

# Имя параметра для задания стиля оформления
STYLE_PARAM_NAME = u"style"

# Имя параметра, указывающий, что надо использовать фон страницы в блоке кода
PARENT_BACKGROUND_PARAM_NAME = "parentbg"

# Имя параметра, указывающий, что надо добавить номера строк
LINE_NUM_PARAM_NAME = "linenum"


# Значения по умолчанию

# Язык программирования по умолчанию
LANGUAGE_DEFAULT = u"text"

# Используемая кодировка по умолчанию
ENCODING_DEFAULT = "utf8"

# Размер табуляции по умолчанию
TAB_WIDTH_DEFAULT = 4

# Имя стиля по умолчанию
STYLE_DEFAULT = u"default"


# Дополнительные cтили

# Стиль для общего div
HIGHLIGHT_STYLE = u'{padding: 1em; }'

# Список языков программирования по умолчанию
LANGUAGE_LIST_DEFAULT = [
    u"text",
    u"c",
    u"cpp",
    u"csharp",
    u"php",
    u"python",
    u"html",
    u"css",
    u"ruby",
    u"java",
    u"javascript",
    u"objective-c",
    u"perl",
    u"vb.net"
]


CUSTOM_STYLES = u"""
.{name} pre {{padding: 0px; border: none; color: inherit; background-color: inherit; margin:0px; }}
.{name} table {{padding: 0px; border: none;}}
.{name}table td {{border-width:0; vertical-align: baseline; }}
.{name}table tr {{vertical-align: baseline; }}
.{name}table tbody {{vertical-align: baseline; }}
.{name}table td.code {{width:100%; }}
.source-block pre {{padding: 0px; border: none; color: inherit; background-color: inherit; }}
.linenodiv pre {{padding: 0px; border: none; color: inherit; background-color: inherit; }}
div.source-block {{border-style: solid; border-color: gray; border-width: 1px; }}"""
