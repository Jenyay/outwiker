# -*- coding: UTF-8 -*-
'''
Various names and constants
'''
WX_VERSION = "3.0"

# Page icon size
ICON_WIDTH = 16
ICON_HEIGHT = 16


# Files for pages
# Page content
PAGE_CONTENT_FILE = u'__page.text'

# Page options (properties)
PAGE_OPT_FILE = u'__page.opt'

# Base name for icons
PAGE_ICON_NAME = u'__icon'

# Folder for attached files
PAGE_ATTACH_DIR = u'__attach'

# Final file after wiki parsing or HTML generation
PAGE_RESULT_HTML = u'__content.html'

# This string will be translated to 'en' or 'ru'
VERSIONS_LANG = u'versions_lang'

VERSION_FILE_NAME = u'versions.xml'

# Keys for Application.sharedData
# Anchor for transition during the opening other page
APP_DATA_KEY_ANCHOR = u'__anchor'

# Debug mode
APP_DATA_DEBUG = u'__debug'


# To translate this with xgettext
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
