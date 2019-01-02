# -*- coding: utf-8 -*-

from outwiker.gui.defines import ID_MOUSE_LEFT

# Constants for the onPageUpdate event

# Changed page content
PAGE_UPDATE_CONTENT = 1

# Changed the icon
PAGE_UPDATE_ICON = 2

# Changed tags
PAGE_UPDATE_TAGS = 4

# Changed page style
PAGE_UPDATE_STYLE = 8

# Changed page style
PAGE_UPDATE_TITLE = 16


class LinkClickParams(object):
    """
    Set of parameters for the onLinkClick event
    """
    def __init__(self,
                 link=u'',
                 button=ID_MOUSE_LEFT,
                 modifier=0,
                 linktype=None):
        """
        link - clicked link

        button - mouse button by link was clicked:
            (consts from gui.defines module)

        modifier - pressed keys (consts from gui.defines module)

        linktype - string (or None) which shows type of link:
            "url" - link to Internet site
            "page" - link to page(note)
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


class HoverLinkParams(object):
    """
    Set of parameters for the onHoverLink event
    """
    def __init__(self, link=None, text=u''):
        """
        link - link under cursor (or None)
        text - text which will be showed in status bar.
                This member can be changed by event handlers.
        """
        self.link = link
        self.text = text


class PreprocessingParams(object):
    """
    Set of parameters for the onPreprocessing event
    """
    def __init__(self, result):
        """
        result - resulted code (wiki or HTML) for which will be generated
        final HTML code.
        This item can be changed by event handlers
        """
        self.result = result


class PostprocessingParams(object):
    """
    Set of parameters for the onPostprocessing event
    """
    def __init__(self, result):
        """
        result - resulted HTML code.
            This item can be changed by event handlers.
            User will see result after all changes.
        """
        self.result = result


class PreHtmlImprovingParams(object):
    """
    Set of parameters for the onPreHtmlImproving event
    """
    def __init__(self, result):
        """
        result - HTML code after wiki parsing.
            This item can be changed by event handlers.
        """
        self.result = result


class EditorPopupMenuParams(object):
    """
    Set of parameters for the onEditorPopupMenu event
    """
    def __init__(self, editor, menu, point, pos_byte):
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


class PageDialogInitParams(object):
    """
    Set of parameters for the onPageDialogInit event
    """
    def __init__(self, dialog):
        self.dialog = dialog


class PageDialogDestroyParams(object):
    """
    Set of parameters for the onPageDialogDestroy event
    """
    def __init__(self, dialog):
        self.dialog = dialog


class PageDialogPageTypeChangedParams(object):
    """
    Set of parameters for the onPageDialogPageTypeChanged event
    """
    def __init__(self, dialog, pageType):
        self.dialog = dialog
        self.pageType = pageType


class PageDialogPageTitleChangedParams(object):
    """
    Set of parameters for the onPageDialogPageTitleChanged event
    """
    def __init__(self, dialog, pageTitle):
        self.dialog = dialog
        self.pageTitle = pageTitle


class PageDialogPageStyleChangedParams(object):
    """
    Set of parameters for the onPageDialogPageStyleChanged event
    """
    def __init__(self, dialog, pageStyle):
        self.dialog = dialog
        self.pageStyle = pageStyle


class PageDialogPageIconChangedParams(object):
    """
    Set of parameters for the onPageDialogPageIconChanged event
    """
    def __init__(self, dialog, pageIcon):
        self.dialog = dialog
        self.pageIcon = pageIcon


class PageDialogPageTagsChangedParams(object):
    """
    Set of parameters for the onPageDialogPageTagsChanged event
    """
    def __init__(self, dialog, pageTags):
        self.dialog = dialog
        self.pageTags = pageTags


class PageDialogPageFactoriesNeededParams(object):
    def __init__(self, dialog, pageForEdit):
        """
        Set of parameters for the onPageDialogPageFactoriesNeeded event
        """
        self.dialog = dialog
        self.pageForEdit = pageForEdit
        self._pageFactories = []

    def addPageFactory(self, factory):
        self._pageFactories.append(factory)

    @property
    def pageFactories(self):
        return self._pageFactories[:]


class EditorStyleNeededParams(object):
    """
    Set of parameters for the onEditorStyleNeeded event
    """
    def __init__(self, editor, text, enableSpellChecking):
        self.editor = editor
        self.text = text
        self.enableSpellChecking = enableSpellChecking


class PageUpdateNeededParams(object):
    """
    Set of parameters for the onPageUpdateNeededParams event
    """
    def __init__(self, allowCache=True):
        self.allowCache = allowCache


class PreWikiOpenParams(object):
    """
    Set of parameters for the onPreWikiOpen event
    """
    def __init__(self, path, readonly):
        self.path = path
        self.readonly = readonly
        self.abortOpen = False


class PostWikiOpenParams(object):
    """
    Set of parameters for the onPostWikiOpen event
    """
    def __init__(self, path, readonly, success):
        self.path = path
        self.readonly = readonly
        self.success = success


class PostWikiCloseParams(object):
    """
    Set of parameters for the onPostWikiClose event
    """
    def __init__(self, path):
        self.path = path


class IconsGroupsListInitParams(object):
    """
    Set of parameters for the onIconsGroupsListInit event
    """
    def __init__(self, groupsList):
        """
        groupsList - list of the outwiker.gui.iconspanel.IconsGroupInfo.
        """
        self.groupsList = groupsList


class PageModeChangeParams(object):
    """
    Set of parameters for theon PageModeChange event
    """
    def __init__(self, pagemode):
        """
        pagemode - constant from outwiker.core.defines (or other place):
            PAGE_MODE_TEXT, PAGE_MODE_PREVIEW, PAGE_MODE_HTML
        """
        self.pagemode = pagemode


class AttachListChangedParams(object):
    """
    Parameters set for the onAttachListChanged event
    """
    def __init__(self):
        pass


class TextEditorKeyDownParams(object):
    '''
    Parameters set for onTextEditorKeyDown event
    '''
    def __init__(self,
                 editor: 'outwiker.gui.texteditor.TextEditor',
                 keyCode: int,
                 keyUnicode: int,
                 ctrl: bool,
                 shift: bool,
                 alt: bool,
                 cmd: bool,
                 meta: bool):
        self.editor = editor
        self.keyCode = keyCode
        self.keyUnicode = keyUnicode
        self.ctrl = ctrl
        self.shift = shift
        self.alt = alt
        self.cmd = cmd
        self.meta = meta

        # Set True if the event was processed
        self.processed = False

        # Set True if current character should not be added to editor
        self.disableOutput = False


class PreWikiCloseParams(object):
    '''
    Parameters set for onPreWikiClose event
    '''
    def __init__(self, wikiroot: 'outwiker.core.tree.WikiDocument'):
        self.wikiroot = wikiroot
        self.abortClose = False


class PostContentReadingParams(object):
    '''
    Parameters set for onPostContentReading event
    '''
    def __init__(self, content):
        self.content = content


class PreContentWritingParams(object):
    '''
    Parameters set for onPreContentWriting event
    '''
    def __init__(self, content):
        self.content = content
