# -*- coding: utf-8 -*-
'''
Various names and constants
'''

import os.path


# Page icon size
ICON_WIDTH = 16
ICON_HEIGHT = 16


# Files for pages
# Page content
PAGE_CONTENT_FILE = u'__page.text'

# Page options (properties)
PAGE_OPT_FILE = u'__page.opt'

# Registry file (cache)
REGISTRY_FILE = '__cache.tmp'

# Base name for icons
PAGE_ICON_NAME = u'__icon'

# Folder for attached files
PAGE_ATTACH_DIR = u'__attach'

# Final file after wiki parsing or HTML generation
PAGE_RESULT_HTML = u'__content.html'

# This string will be translated to 'en' or 'ru'
VERSIONS_LANG = u'versions_lang'

PLUGIN_INFO_FILE_NAME = u'plugin.xml'

# Keys for Application.sharedData
# Anchor for transition during the opening other page
APP_DATA_KEY_ANCHOR = u'__anchor'

APP_DATA_DEBUG = u'__debug'

APP_DATA_DISABLE_MINIMIZING = u'__disableMinimizing'

APP_DATA_DISABLE_PLUGINS = '__disablePlugins'

ICONS_STD_PREFIX = u'__std_'
ICONS_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'ico']
IMAGES_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp']
ICON_DEFAULT = ICONS_STD_PREFIX + u'_default.png'
RECENT_ICONS_SECTION = u'RecentIcons'
RECENT_ICONS_PARAM_NAME = u'icon'

ICONS_FOLDER_NAME = u'iconset'
IMAGES_FOLDER_NAME = u'images'
STYLES_FOLDER_NAME = u"styles"
PLUGINS_FOLDER_NAME = u"plugins"
SPELL_FOLDER_NAME = u"spell"
STYLES_BLOCK_FOLDER_NAME = os.path.join("textstyles", 'block')
STYLES_INLINE_FOLDER_NAME = os.path.join("textstyles", 'inline')

PAGE_MODE_TEXT = 0
PAGE_MODE_PREVIEW = 1
PAGE_MODE_HTML = 2

CONFIG_GENERAL_SECTION = 'General'
CONFIG_TOOLBARS_SECTION = 'Toolbars'
CONFIG_TOOLBARS_VISIBLE_SUFFIX = '_visible'

REGISTRY_SECTION_PAGES = '__pages'
REGISTRY_PAGE_CURSOR_POSITION = 'cursorposition'
REGISTRY_PAGE_HASH = 'md5_hash'

URL_TRANSLATE = 'https://crowdin.com/project/outwiker'

# Местоположение конфигурационной директории
# По стандарту, если переменная XDG_CONFIG_HOME не задана в окружении,
# то берется значение по умолчанию т.е. ~/.config
# http://standards.freedesktop.org/basedir-spec/basedir-spec-latest.html
DEFAULT_CONFIG_DIR = "outwiker"

# Имя файла настроек по умолчанию
DEFAULT_CONFIG_NAME = "outwiker.ini"


# To translate this words with xgettext
if __name__ == '__main__':
    _ = lambda s: s

    _('versions_lang')

    # Folder names for localizations
    _("awards")
    _("battery")
    _("books")
    _("computer")
    _("emotions")
    _("flags")
    _("folders")
    _("food")
    _("internet")
    _("money")
    _("people")
    _("signs")
    _("software")
    _("tags")
    _("weather")
