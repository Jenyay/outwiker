# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional

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


class LinkClickParams:
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


class HoverLinkParams:
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


class PreprocessingParams:
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


class PostprocessingParams:
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


class PreHtmlImprovingParams:
    """
    Set of parameters for the onPreHtmlImproving event
    """
    def __init__(self, result):
        """
        result - HTML code after wiki parsing.
            This item can be changed by event handlers.
        """
        self.result = result


class EditorPopupMenuParams:
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


class PageDialogInitParams:
    """
    Set of parameters for the onPageDialogInit event
    """
    def __init__(self, dialog):
        self.dialog = dialog


class PageDialogDestroyParams:
    """
    Set of parameters for the onPageDialogDestroy event
    """
    def __init__(self, dialog):
        self.dialog = dialog


class PageDialogPageTypeChangedParams:
    """
    Set of parameters for the onPageDialogPageTypeChanged event
    """
    def __init__(self, dialog, pageType):
        self.dialog = dialog
        self.pageType = pageType


class PageDialogPageTitleChangedParams:
    """
    Set of parameters for the onPageDialogPageTitleChanged event
    """
    def __init__(self, dialog, pageTitle):
        self.dialog = dialog
        self.pageTitle = pageTitle


class PageDialogNewPageOrderChangedParams:
    """
    Set of parameters for the onPageDialogNewPageOrderChanged event
    """
    def __init__(self, dialog, orderCalculator):
        self.dialog = dialog
        self.orderCalculator = orderCalculator


class PageDialogPageStyleChangedParams:
    """
    Set of parameters for the onPageDialogPageStyleChanged event
    """
    def __init__(self, dialog, pageStyle):
        self.dialog = dialog
        self.pageStyle = pageStyle


class PageDialogPageIconChangedParams:
    """
    Set of parameters for the onPageDialogPageIconChanged event
    """
    def __init__(self, dialog, pageIcon):
        self.dialog = dialog
        self.pageIcon = pageIcon


class PageDialogPageTagsChangedParams:
    """
    Set of parameters for the onPageDialogPageTagsChanged event
    """
    def __init__(self, dialog, pageTags):
        self.dialog = dialog
        self.pageTags = pageTags


class PageDialogPageFactoriesNeededParams:
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


class EditorStyleNeededParams:
    """
    Set of parameters for the onEditorStyleNeeded event
    """
    def __init__(self, editor, text, enableSpellChecking):
        self.editor = editor
        self.text = text
        self.enableSpellChecking = enableSpellChecking


class PageUpdateNeededParams:
    """
    Set of parameters for the onPageUpdateNeededParams event
    """
    def __init__(self, allowCache=True):
        self.allowCache = allowCache


class PreWikiOpenParams:
    """
    Set of parameters for the onPreWikiOpen event
    """
    def __init__(self, path, readonly):
        self.path = path
        self.readonly = readonly
        self.abortOpen = False


class PostWikiOpenParams:
    """
    Set of parameters for the onPostWikiOpen event
    """
    def __init__(self, path, readonly, success):
        self.path = path
        self.readonly = readonly
        self.success = success


class PostWikiCloseParams:
    """
    Set of parameters for the onPostWikiClose event
    """
    def __init__(self, path):
        self.path = path


class IconsGroupsListInitParams:
    """
    Set of parameters for the onIconsGroupsListInit event
    """
    def __init__(self, groupsList):
        """
        groupsList - list of the outwiker.gui.iconspanel.IconsGroupInfo.
        """
        self.groupsList = groupsList


class PageModeChangeParams:
    """
    Set of parameters for theon PageModeChange event
    """
    def __init__(self, pagemode):
        """
        pagemode - constant from outwiker.core.defines (or other place):
            PAGE_MODE_TEXT, PAGE_MODE_PREVIEW, PAGE_MODE_HTML
        """
        self.pagemode = pagemode


class AttachListChangedParams:
    """
    Parameters set for the onAttachListChanged event
    """
    def __init__(self):
        pass


class AttachSubdirChangedParams:
    """
    Parameters set for the onAttachSubdirChanged event
    """
    def __init__(self):
        pass


class TextEditorKeyDownParams:
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

    def hasModifiers(self):
        return self.ctrl or self.shift or self.alt or self.cmd or self.meta


class PreWikiCloseParams:
    '''
    Parameters set for onPreWikiClose event
    '''
    def __init__(self, wikiroot: 'outwiker.core.tree.WikiDocument'):
        self.wikiroot = wikiroot
        self.abortClose = False


class PostContentReadingParams:
    '''
    Parameters set for onPostContentReading event
    '''
    def __init__(self, content):
        self.content = content


class PreContentWritingParams:
    '''
    Parameters set for onPreContentWriting event
    '''
    def __init__(self, content):
        self.content = content


class TextEditorCaretMoveParams:
    '''
    Parameters for onTextEditorCaretMove event
    '''
    def __init__(self,
                 editor: 'outwiker.gui.texteditor.TextEditor',
                 startSelection: int,
                 endSelection: int
                 ):
        self.editor = editor
        self.startSelection = startSelection
        self.endSelection = endSelection


@dataclass(frozen=True)
class BeginAttachRenamingParams:
    """
    Parameters for onBeginAttachRenaming
    """
    # Name of renamed attached file or directory.
    # Rename selected item if renamed_item is None.
    renamed_item: Optional[str] = None
