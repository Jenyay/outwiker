# -*- coding: UTF-8 -*-

from outwiker.gui.defines import ID_MOUSE_LEFT

# Constants for the onPageUpdate event

# Changed page content
PAGE_UPDATE_CONTENT = 1

# Changed the icon
PAGE_UPDATE_ICON = 2

# Changed tags
PAGE_UPDATE_TAGS = 4

# Changes in the attach list
PAGE_UPDATE_ATTACHMENT = 8

# Changed page style
PAGE_UPDATE_STYLE = 16


class LinkClickParams (object):
    """
    Parameter set for the onLinkClick event
    """
    def __init__ (self,
                  link = u'',
                  button = ID_MOUSE_LEFT,
                  modifier = 0,
                  linktype = None):
        """
        link - clicked link

        button - mouse button by link was clicked:
            (consts from gui.defines module)

        modifier - pressed keys (consts from gui.defines module)

        linktype - string (or None) which shows type of link:
            "url" - link to Internet site
            "page" - link to page (note)
            "file" - link to file
            "anchor" - link to anchor on current page
            None - unknown

        process - boolean value, which indicates what
            processed this click (True) or not (False).
            This value can be changed by event handlers.
            If click was processed, standard (internal) processing
            is not process.
        """
        self.link = link
        self.button = button
        self.modifier = modifier
        self.linktype = linktype

        self.process = False


class HoverLinkParams (object):
    """
    Parameter set for the onHoverLink event
    """
    def __init__ (self, link = None, text = u''):
        """
        link - link under cursor (or None)
        text - text which will be showed in status bar.
                This member can be changed by event handlers.
        """
        self.link = link
        self.text = text


class PreprocessingParams (object):
    """
    Parameter set for the onPreprocessing event
    """
    def __init__ (self, result):
        """
        result - resulted code (wiki or HTML) for which will be generated final HTML code.
        This item can be changed by event handlers
        """
        self.result = result


class PostprocessingParams (object):
    """
    Parameter set for the onPostprocessing event
    """
    def __init__ (self, result):
        """
        result - resulted HTML code. This item can be changed by event handlers.
            User will see result after all changes.
        """
        self.result = result


class PreHtmlImprovingParams (object):
    """
    Parameter set for the onPreHtmlImproving event
    """
    def __init__ (self, result):
        """
        result - HTML code after wiki parsing. This item can be changed by event handlers.
        """
        self.result = result


class EditorPopupMenuParams (object):
    """
    Parameter set for the onEditorPopupMenu event
    """
    def __init__ (self, editor, menu, point, pos_byte):
        """
        editor - text editor
        menu - popup menu
        point - mouse click position (in pixels)
        pos_byte - nearest editor character position (in bytes, not characters)
        """
        self.editor = editor
        self.menu = menu
        self.point = point
        self.pos_byte = pos_byte


class PageDialogInitParams (object):
    """
    Parameter set for the onPageDialogInit event
    """
    def __init__ (self, dialog):
        self.dialog = dialog


class PageDialogDestroyParams (object):
    """
    Parameter set for the onPageDialogDestroy event
    """
    def __init__ (self, dialog):
        self.dialog = dialog


class PageDialogPageTypeChangedParams (object):
    """
    Parameter set for the onPageDialogPageTypeChanged event
    """
    def __init__ (self, dialog, pageType):
        self.dialog = dialog
        self.pageType = pageType


class PageDialogPageTitleChangedParams (object):
    """
    Parameter set for the onPageDialogPageTitleChanged event
    """
    def __init__ (self, dialog, pageTitle):
        self.dialog = dialog
        self.pageTitle = pageTitle


class PageDialogPageStyleChangedParams (object):
    """
    Parameter set for the onPageDialogPageStyleChanged event
    """
    def __init__ (self, dialog, pageStyle):
        self.dialog = dialog
        self.pageStyle = pageStyle


class PageDialogPageIconChangedParams (object):
    """
    Parameter set for the onPageDialogPageIconChanged event
    """
    def __init__ (self, dialog, pageIcon):
        self.dialog = dialog
        self.pageIcon = pageIcon


class PageDialogPageTagsChangedParams (object):
    """
    Parameter set for the onPageDialogPageTagsChanged event
    """
    def __init__ (self, dialog, pageTags):
        self.dialog = dialog
        self.pageTags = pageTags


class PageDialogPageFactoriesNeededParams (object):
    def __init__ (self, dialog, pageForEdit):
        """
        Parameter set for the onPageDialogPageFactoriesNeeded event
        """
        self.dialog = dialog
        self.pageForEdit = pageForEdit
        self._pageFactories = []


    def addPageFactory (self, factory):
        self._pageFactories.append (factory)


    @property
    def pageFactories (self):
        return self._pageFactories[:]


class EditorStyleNeededParams (object):
    """
    Parameter set for the onEditorStyleNeeded event
    """
    def __init__ (self, editor, text, enableSpellChecking):
        self.editor = editor
        self.text = text
        self.enableSpellChecking = enableSpellChecking


class PageUpdateNeededParams (object):
    """
    Parameter set for the onPageUpdateNeededParams event
    """
    def __init__ (self, data):
        self.data = data


class PreWikiOpenParams (object):
    """
    Parameter set for the onPreWikiOpen event

    Added in OutWiker 2.0.0.795
    """
    def __init__(self, path, readonly):
        self.path = path
        self.readonly = readonly


class PostWikiOpenParams (object):
    """
    Parameter set for the onPostWikiOpen event

    Added in OutWiker 2.0.0.795
    """
    def __init__(self, path, readonly, success):
        self.path = path
        self.readonly = readonly
        self.success = success
