# -*- coding: utf-8 -*-
'''
Various names and constants
'''
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

VERSION_FILE_NAME = u'versions.xml'
PLUGIN_VERSION_FILE_NAME = u'plugin.xml'

# Keys for Application.sharedData
# Anchor for transition during the opening other page
APP_DATA_KEY_ANCHOR = u'__anchor'

# Debug mode
APP_DATA_DEBUG = u'__debug'

APP_DATA_DISABLE_MINIMIZING = u'__disableMinimizing'

ICONS_STD_PREFIX = u'__std_'
ICONS_EXTENSIONS = [u'png', u'jpg', u'jpeg', u'gif', u'bmp', u'ico']
ICON_DEFAULT = ICONS_STD_PREFIX + u'_default.png'
RECENT_ICONS_SECTION = u'RecentIcons'
RECENT_ICONS_PARAM_NAME = u'icon'

ICONS_FOLDER_NAME = u'iconset'
IMAGES_FOLDER_NAME = u'images'
STYLES_FOLDER_NAME = u"styles"
PLUGINS_FOLDER_NAME = u"plugins"
SPELL_FOLDER_NAME = u"spell"

PAGE_MODE_TEXT = 0
PAGE_MODE_PREVIEW = 1
PAGE_MODE_HTML = 2

CONFIG_TOOLBARS_SECTION = 'Toolbars'
CONFIG_TOOLBARS_VISIBLE_SUFFIX = '_visible'

REGISTRY_SECTION_PAGES = '__pages'
REGISTRY_PAGE_CURSOR_POSITION = 'cursorposition'

WIKISTYLES_FILE_NAME = 'textstyles.css'


# To translate this words with xgettext
if __name__ == u'__main__':
    _('versions_lang')

    # Folder names for localizations
    _(u"awards")
    _(u"battery")
    _(u"books")
    _(u"computer")
    _(u"emotions")
    _(u"flags")
    _(u"folders")
    _(u"food")
    _(u"internet")
    _(u"money")
    _(u"people")
    _(u"signs")
    _(u"software")
    _(u"tags")
    _(u"weather")
