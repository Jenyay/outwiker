# -*- coding: utf-8 -*-
"""
Various names and constants
"""

import os.path


# Files for pages
# Page content
PAGE_CONTENT_FILE = "__page.text"

# Page options (properties)
PAGE_OPT_FILE = "__page.opt"

# Registry file (cache)
REGISTRY_FILE = "__cache.tmp"

# Base name for icons
PAGE_ICON_NAME = "__icon"

# Folder for attachments
PAGE_ATTACH_DIR = "__attach"

# Final file after wiki parsing or HTML generation
PAGE_RESULT_HTML = "__content.html"

# This string will be translated to 'en' or 'ru'
VERSIONS_LANG = "versions_lang"

PLUGIN_INFO_FILE_NAME = "plugin.xml"

# Keys for Application.sharedData
# Anchor for transition during the opening other page
APP_DATA_KEY_ANCHOR = "__anchor"

APP_DATA_DEBUG = "__debug"

APP_DATA_DISABLE_MINIMIZING = "__disableMinimizing"

APP_DATA_DISABLE_PLUGINS = "__disablePlugins"

APP_DATA_CREATE_TREE_PANEL = "__createTreePanel"
APP_DATA_CREATE_ATTACH_PANEL = "__createAttachPanel"
APP_DATA_CREATE_TAGS_PANEL = "__createTagsPanel"

ICONS_STD_PREFIX = "__std_"
ICONS_EXTENSIONS = ["png", "jpg", "jpeg", "gif", "bmp", "ico", "svg"]
IMAGES_EXTENSIONS = ["png", "jpg", "jpeg", "gif", "bmp", "webp"]
ICON_DEFAULT = ICONS_STD_PREFIX + "_default.svg"
RECENT_ICONS_SECTION = "RecentIcons"
RECENT_ICONS_PARAM_NAME = "icon"

DATA_FOLDER_NAME = "data"
ICONS_FOLDER_NAME = "iconset"
IMAGES_FOLDER_NAME = "images"
STYLES_FOLDER_NAME = "styles"
PLUGINS_FOLDER_NAME = "plugins"
SPELL_FOLDER_NAME = "spell"
STYLES_BLOCK_FOLDER_NAME = os.path.join("textstyles", "block")
STYLES_INLINE_FOLDER_NAME = os.path.join("textstyles", "inline")

PAGE_MODE_TEXT = 0
PAGE_MODE_PREVIEW = 1
PAGE_MODE_HTML = 2

CONFIG_GENERAL_SECTION = "General"
CONFIG_TOOLBARS_SECTION = "Toolbars"
CONFIG_TOOLBARS_VISIBLE_SUFFIX = "_visible"

REGISTRY_SECTION_PAGES = "__pages"
REGISTRY_PAGE_CURSOR_POSITION = "cursorposition"
REGISTRY_PAGE_PREVIEW_SCROLL_POSITION = "preview_scroll"
REGISTRY_PAGE_HASH = "md5_hash"

URL_TRANSLATE = "https://crowdin.com/project/outwiker"

# Location of the configuration directory
# According to the standard, if the XDG_CONFIG_HOME environment variable is not set,
# the default value is used, i.e. ~/.config
# http://standards.freedesktop.org/basedir-spec/basedir-spec-latest.html
DEFAULT_CONFIG_DIR = "outwiker"

# Default configuration file name
DEFAULT_CONFIG_NAME = "outwiker.ini"

OUTWIKER_PATH_ENV_VAR = "OUTWIKER_PATH"

URL_PROTOCOL = "outwiker"
URL_MESSAGE_SCROLLED = "scroll-position-changed"


# To translate this words with xgettext
if __name__ == "__main__":
    _ = lambda s: s

    _("versions_lang")

    # Folder names for localizations
    _("awards")
    _("battery")
    _("bookmarks")
    _("books")
    _("charts")
    _("computer")
    _("emotions")
    _("flags")
    _("folders")
    _("food")
    _("images")
    _("internet")
    _("list")
    _("money")
    _("office")
    _("pages")
    _("people")
    _("plants")
    _("signs")
    _("software")
    _("sport")
    _("tags")
    _("text")
    _("weather")
