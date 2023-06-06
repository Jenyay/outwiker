# -*- coding: utf-8 -*-

from outwiker.app.actions.addbookmark import AddBookmarkAction
from outwiker.app.actions.addchildpage import AddChildPageAction
from outwiker.app.actions.addsiblingpage import AddSiblingPageAction
from outwiker.app.actions.applystyle import SetStyleToBranchAction
from outwiker.app.actions.clipboard import (
    CopyAttachPathAction,
    CopyPageLinkAction,
    CopyPagePathAction,
    CopyPageTitleAction,
)
from outwiker.actions.close import CloseAction
from outwiker.app.actions.editpageprop import EditPagePropertiesAction
from outwiker.app.actions.exit import ExitAction
from outwiker.app.actions.fullscreen import FullScreenAction
from outwiker.app.actions.globalsearch import GlobalSearchAction
from outwiker.app.actions.history import HistoryBackAction, HistoryForwardAction
from outwiker.app.actions.movepagedown import MovePageDownAction
from outwiker.app.actions.movepageup import MovePageUpAction
from outwiker.app.actions.moving import (
    GoToFirstChildAction,
    GoToNextSiblingAction,
    GoToParentAction,
    GoToPrevSiblingAction,
)
from outwiker.app.actions.new import NewAction
from outwiker.app.actions.open import OpenAction
from outwiker.app.actions.openhelp import OpenHelpAction
from outwiker.app.actions.openpluginsfolder import OpenPluginsFolderAction
from outwiker.app.actions.openreadonly import OpenReadOnlyAction
from outwiker.app.actions.preferences import PreferencesAction
from outwiker.app.actions.printaction import PrintAction
from outwiker.app.actions.reloadwiki import ReloadWikiAction
from outwiker.app.actions.removepage import RemovePageAction
from outwiker.app.actions.renamepage import RenamePageAction
from outwiker.app.actions.save import SaveAction
from outwiker.app.actions.search import (
    SearchAction,
    SearchAndReplaceAction,
    SearchNextAction,
    SearchPrevAction,
)
from outwiker.app.actions.showhideattaches import ShowHideAttachesAction
from outwiker.app.actions.showhidetags import ShowHideTagsAction
from outwiker.app.actions.showhidetree import ShowHideTreeAction
from outwiker.app.actions.sortchildalpha import SortChildAlphabeticalAction
from outwiker.app.actions.sortsiblingsalpha import SortSiblingsAlphabeticalAction
from outwiker.app.actions.switchto import (
    SwitchToAttachmentsAction,
    SwitchToMainPanelAction,
    SwitchToTagsCloudAction,
    SwitchToTreeAction,
)
from outwiker.app.actions.tabs import (
    AddTabAction,
    CloseTabAction,
    NextTabAction,
    PreviousTabAction,
)
from outwiker.app.actions.tags import (
    AddTagsToBranchAction,
    RemoveTagsFromBranchAction,
    RenameTagAction,
)
import outwiker.actions.polyactionsid as polyactions

from outwiker.app.actions.about import AboutAction
from outwiker.app.actions.attachexecute import AttachExecuteFilesAction
from outwiker.app.actions.attachfiles import (
    AttachFilesAction,
    AttachFilesActionForAttachPanel,
)
from outwiker.app.actions.attachopenfolder import (
    OpenAttachFolderAction,
    OpenAttachFolderActionForAttachPanel,
)
from outwiker.app.actions.attachpastelink import AttachPasteLinkActionForAttachPanel
from outwiker.app.actions.attachremove import RemoveAttachesActionForAttachPanel
from outwiker.app.actions.attachrename import RenameAttachActionForAttachPanel
from outwiker.app.actions.attachselectall import AttachSelectAllAction
from outwiker.app.actions.attachcreatesubdir import (
    AttachCreateSubdirAction,
    AttachCreateSubdirActionForAttachPanel,
)
from outwiker.app.actions.attachfolder import (
    AttachFolderAction,
    AttachFolderActionForAttachPanel,
)

from outwiker.gui.actioninfo import ActionInfo, PolyactionInfo
from outwiker.gui.hotkey import HotKey
from outwiker.gui.defines import ATTACH_ACTIONS_AREA


actionsList = [
    ActionInfo(OpenAction, HotKey("O", ctrl=True)),
    ActionInfo(NewAction, HotKey("N", ctrl=True)),
    ActionInfo(OpenReadOnlyAction, None),
    ActionInfo(CloseAction, HotKey("W", ctrl=True, shift=True)),
    ActionInfo(SaveAction, HotKey("S", ctrl=True)),
    ActionInfo(ExitAction, HotKey("F4", alt=True)),
    ActionInfo(ShowHideAttachesAction, None),
    ActionInfo(ShowHideTreeAction, None),
    ActionInfo(ShowHideTagsAction, None),
    ActionInfo(SearchAction, HotKey("F", ctrl=True)),
    ActionInfo(SearchNextAction, HotKey("F3")),
    ActionInfo(SearchPrevAction, HotKey("F3", shift=True)),
    ActionInfo(SearchAndReplaceAction, HotKey("F3", ctrl=True)),
    ActionInfo(AddSiblingPageAction, HotKey("Y", ctrl=True, shift=True)),
    ActionInfo(AddChildPageAction, HotKey("P", ctrl=True, shift=True)),
    ActionInfo(MovePageUpAction, HotKey("Up", ctrl=True, shift=True)),
    ActionInfo(MovePageDownAction, HotKey("Down", ctrl=True, shift=True)),
    ActionInfo(RenamePageAction, HotKey("F2")),
    ActionInfo(RemovePageAction, HotKey("F8", ctrl=True, shift=True)),
    ActionInfo(SortChildAlphabeticalAction, None),
    ActionInfo(SortSiblingsAlphabeticalAction, None),
    ActionInfo(AddTabAction, HotKey("T", ctrl=True)),
    ActionInfo(CloseTabAction, HotKey("W", ctrl=True)),
    ActionInfo(PreviousTabAction, HotKey("PageUp", ctrl=True, shift=True)),
    ActionInfo(NextTabAction, HotKey("PageDown", ctrl=True, shift=True)),
    ActionInfo(GlobalSearchAction, HotKey("F", ctrl=True, shift=True)),
    ActionInfo(AttachFilesAction, HotKey("A", ctrl=True, shift=True)),
    ActionInfo(AttachFolderAction, None),
    ActionInfo(CopyPageTitleAction, None),
    ActionInfo(CopyPagePathAction, None),
    ActionInfo(CopyAttachPathAction, None),
    ActionInfo(CopyPageLinkAction, None),
    ActionInfo(AddTagsToBranchAction, None),
    ActionInfo(RemoveTagsFromBranchAction, None),
    ActionInfo(RenameTagAction, None),
    ActionInfo(HistoryBackAction, HotKey("Left", ctrl=True, alt=True)),
    ActionInfo(HistoryForwardAction, HotKey("Right", ctrl=True, alt=True)),
    ActionInfo(GoToParentAction, None),
    ActionInfo(GoToFirstChildAction, None),
    ActionInfo(GoToNextSiblingAction, HotKey("Down", ctrl=True)),
    ActionInfo(GoToPrevSiblingAction, HotKey("Up", ctrl=True)),
    ActionInfo(PrintAction, HotKey("P", ctrl=True)),
    ActionInfo(FullScreenAction, HotKey("F11")),
    ActionInfo(PreferencesAction, HotKey("F8", ctrl=True)),
    ActionInfo(EditPagePropertiesAction, HotKey("E", ctrl=True)),
    ActionInfo(AddBookmarkAction, HotKey("D", ctrl=True)),
    ActionInfo(ReloadWikiAction, None),
    ActionInfo(OpenHelpAction, HotKey("F1")),
    ActionInfo(AboutAction, HotKey("F1", ctrl=True)),
    ActionInfo(SetStyleToBranchAction, None),
    ActionInfo(OpenPluginsFolderAction, None),
    ActionInfo(SwitchToMainPanelAction, None),
    ActionInfo(SwitchToTreeAction, None),
    ActionInfo(SwitchToAttachmentsAction, None),
    ActionInfo(SwitchToTagsCloudAction, None),
    ActionInfo(OpenAttachFolderAction, None),
    ActionInfo(
        RemoveAttachesActionForAttachPanel,
        hotkey=HotKey("Delete"),
        area=ATTACH_ACTIONS_AREA,
        hidden=False,
    ),
    ActionInfo(
        AttachFilesActionForAttachPanel,
        hotkey=None,
        area=ATTACH_ACTIONS_AREA,
        hidden=True,
    ),
    ActionInfo(
        AttachFolderActionForAttachPanel,
        hotkey=None,
        area=ATTACH_ACTIONS_AREA,
        hidden=True,
    ),
    ActionInfo(
        AttachPasteLinkActionForAttachPanel,
        HotKey("Enter", ctrl=True),
        area=ATTACH_ACTIONS_AREA,
        hidden=False,
    ),
    ActionInfo(AttachExecuteFilesAction, None, area=ATTACH_ACTIONS_AREA, hidden=False),
    ActionInfo(
        OpenAttachFolderActionForAttachPanel,
        None,
        area=ATTACH_ACTIONS_AREA,
        hidden=True,
    ),
    ActionInfo(
        AttachSelectAllAction,
        HotKey("A", ctrl=True),
        area=ATTACH_ACTIONS_AREA,
        hidden=False,
    ),
    ActionInfo(
        RenameAttachActionForAttachPanel,
        HotKey("F2"),
        area=ATTACH_ACTIONS_AREA,
        hidden=False,
    ),
    ActionInfo(AttachCreateSubdirAction, HotKey("Ctrl+F7"), area=None, hidden=False),
    ActionInfo(
        AttachCreateSubdirActionForAttachPanel,
        HotKey("F7"),
        area=ATTACH_ACTIONS_AREA,
        hidden=False,
    ),
]


polyactionsList = [
    PolyactionInfo(
        polyactions.BOLD_STR_ID, _("Bold"), _("Bold"), HotKey("B", ctrl=True)
    ),
    PolyactionInfo(
        polyactions.ITALIC_STR_ID, _("Italic"), _("Italic"), HotKey("I", ctrl=True)
    ),
    PolyactionInfo(
        polyactions.BOLD_ITALIC_STR_ID,
        _("Bold italic"),
        _("Bold italic"),
        HotKey("I", ctrl=True, shift=True),
    ),
    PolyactionInfo(
        polyactions.UNDERLINE_STR_ID,
        _("Underline"),
        _("Underline"),
        HotKey("U", ctrl=True),
    ),
    PolyactionInfo(
        polyactions.STRIKE_STR_ID,
        _("Strikethrough"),
        _("Strikethrough"),
        HotKey("K", ctrl=True),
    ),
    PolyactionInfo(
        polyactions.SUBSCRIPT_STR_ID,
        _("Subscript"),
        _("Subscript"),
        HotKey("=", ctrl=True),
    ),
    PolyactionInfo(
        polyactions.SUPERSCRIPT_STR_ID,
        _("Superscript"),
        _("Superscript"),
        HotKey("+", ctrl=True),
    ),
    PolyactionInfo(
        polyactions.PREFORMAT_STR_ID,
        _("Preformatted text"),
        _("Preformatted text"),
        HotKey("B", ctrl=True, shift=True),
    ),
    PolyactionInfo(
        polyactions.CODE_STR_ID,
        _("Insert code"),
        _("Insert code(monospaced font)"),
        None,
    ),
    PolyactionInfo(
        polyactions.ALIGN_LEFT_STR_ID,
        _("Align text left"),
        _("Align text left"),
        HotKey("L", ctrl=True, shift=True),
    ),
    PolyactionInfo(
        polyactions.ALIGN_CENTER_STR_ID,
        _("Align text center"),
        _("Center"),
        HotKey("C", ctrl=True, shift=True),
    ),
    PolyactionInfo(
        polyactions.ALIGN_RIGHT_STR_ID,
        _("Align text right"),
        _("Align text right"),
        HotKey("R", ctrl=True, shift=True),
    ),
    PolyactionInfo(
        polyactions.ALIGN_JUSTIFY_STR_ID,
        _("Justify"),
        _("Justify"),
        HotKey("J", ctrl=True, shift=True),
    ),
    PolyactionInfo(
        polyactions.HEADING_1_STR_ID,
        _("First-level heading"),
        _("First-level heading"),
        HotKey("1", ctrl=True),
    ),
    PolyactionInfo(
        polyactions.HEADING_2_STR_ID,
        _("Second-level heading"),
        _("Second-level heading"),
        HotKey("2", ctrl=True),
    ),
    PolyactionInfo(
        polyactions.HEADING_3_STR_ID,
        _("Subtitle three"),
        _("Subtitle three"),
        HotKey("3", ctrl=True),
    ),
    PolyactionInfo(
        polyactions.HEADING_4_STR_ID,
        _("Subtitle four"),
        _("Subtitle four"),
        HotKey("4", ctrl=True),
    ),
    PolyactionInfo(
        polyactions.HEADING_5_STR_ID,
        _("Subtitle five"),
        _("Subtitle five"),
        HotKey("5", ctrl=True),
    ),
    PolyactionInfo(
        polyactions.HEADING_6_STR_ID,
        _("Subtitle six"),
        _("Subtitle six"),
        HotKey("6", ctrl=True),
    ),
    PolyactionInfo(polyactions.ANCHOR_STR_ID, _("Anchor"), _("Anchor"), None),
    PolyactionInfo(
        polyactions.HORLINE_STR_ID,
        _("Horizontal rule"),
        _("Horizontal rule"),
        HotKey("H", ctrl=True, shift=True),
    ),
    PolyactionInfo(
        polyactions.LINK_STR_ID, _("Link"), _("Insert Link"), HotKey("L", ctrl=True)
    ),
    PolyactionInfo(
        polyactions.QUOTE_STR_ID,
        _("Quote"),
        _("Insert a quote block"),
        HotKey("Q", ctrl=True),
    ),
    PolyactionInfo(
        polyactions.IMAGE_STR_ID,
        _("Image"),
        _("Insert image"),
        HotKey("M", ctrl=True, shift=True),
    ),
    PolyactionInfo(polyactions.MARK_STR_ID, _("Mark"), _("Mark text"), None),
    PolyactionInfo(
        polyactions.LIST_BULLETS_STR_ID,
        _("Bullets list"),
        _("Insert a bullets list"),
        HotKey("G", ctrl=True),
    ),
    PolyactionInfo(
        polyactions.LIST_NUMBERS_STR_ID,
        _("Numbers list"),
        _("Insert a numbers list"),
        HotKey("J", ctrl=True),
    ),
    PolyactionInfo(
        polyactions.LIST_DECREASE_LEVEL_STR_ID,
        _("Decrease nesting level"),
        _("Decrease the nesting level of the selected list items"),
        None,
    ),
    PolyactionInfo(
        polyactions.LINE_BREAK_STR_ID,
        _("Line break"),
        _("Insert a line break"),
        HotKey("Return", ctrl=True),
    ),
    PolyactionInfo(
        polyactions.HTML_ESCAPE_STR_ID,
        _("Convert HTML Symbols"),
        _("Convert HTML Symbols"),
        None,
    ),
    PolyactionInfo(
        polyactions.TABLE_STR_ID,
        _("Table"),
        _("Insert a table"),
        HotKey("T", ctrl=True, shift=True),
    ),
    PolyactionInfo(
        polyactions.TABLE_ROW_STR_ID,
        _("Table rows"),
        _("Insert table rows"),
        HotKey("G", ctrl=True, shift=True),
    ),
    PolyactionInfo(
        polyactions.TABLE_CELL_STR_ID,
        _("Table cell"),
        _("Insert a table cell"),
        HotKey("U", ctrl=True, shift=True),
    ),
    PolyactionInfo(
        polyactions.CURRENT_DATE, _("Current date"), _("Insert the current date"), None
    ),
    PolyactionInfo(
        polyactions.SPELL_ON_OFF_ID,
        _("Spell checking"),
        _("Enable / disable spell checking"),
        HotKey("F7"),
    ),
    PolyactionInfo(
        polyactions.LINE_DUPLICATE_ID,
        _("Duplicate line"),
        _("Duplicate current line"),
        HotKey("D", ctrl=True, shift=True),
    ),
    PolyactionInfo(
        polyactions.MOVE_SELECTED_LINES_UP_ID,
        _("Move selected lines up"),
        _("Move the selected lines up one line"),
        None,
    ),
    PolyactionInfo(
        polyactions.MOVE_SELECTED_LINES_DOWN_ID,
        _("Move selected lines down"),
        _("Move the selected lines down one line"),
        None,
    ),
    PolyactionInfo(
        polyactions.DELETE_CURRENT_LINE,
        _("Delete line"),
        _("Delete the current line"),
        None,
    ),
    PolyactionInfo(polyactions.JOIN_LINES, _("Join lines"), _("Join lines"), None),
    PolyactionInfo(
        polyactions.DELETE_WORD_LEFT,
        _("Delete word to the left"),
        _("Delete text to beginning of the word"),
        HotKey("Back", ctrl=True),
    ),
    PolyactionInfo(
        polyactions.DELETE_WORD_RIGHT,
        _("Delete word to the right"),
        _("Delete text to ending of the word"),
        HotKey("Delete", ctrl=True),
    ),
    PolyactionInfo(
        polyactions.DELETE_LINE_LEFT,
        _("Delete to start of the line"),
        _("Delete text back from the current position to the start of the line"),
        HotKey("Back", ctrl=True, shift=True),
    ),
    PolyactionInfo(
        polyactions.DELETE_LINE_RIGHT,
        _("Delete to end of the line"),
        _("Delete text forwards from the current position to the end of the line"),
        HotKey("Delete", ctrl=True, shift=True),
    ),
    PolyactionInfo(
        polyactions.GOTO_PREV_WORD,
        _("Go to previous word"),
        _("Move cursor to previous word"),
        HotKey("Left", ctrl=True),
    ),
    PolyactionInfo(
        polyactions.GOTO_NEXT_WORD,
        _("Go to next word"),
        _("Move cursor to next word"),
        HotKey("Right", ctrl=True),
    ),
    PolyactionInfo(
        polyactions.GOTO_PREV_WORD_SELECT,
        _("Go to previous word and select"),
        _("Move cursor to previous word and select text"),
        HotKey("Left", ctrl=True, shift=True),
    ),
    PolyactionInfo(
        polyactions.GOTO_NEXT_WORD_SELECT,
        _("Go to next word and select"),
        _("Move cursor to next word and select text"),
        HotKey("Right", ctrl=True, shift=True),
    ),
    PolyactionInfo(
        polyactions.GOTO_WORD_START,
        _("Go to start of the word"),
        _("Move cursor to start of the current word"),
        None,
    ),
    PolyactionInfo(
        polyactions.GOTO_WORD_END,
        _("Go to end of the word"),
        _("Move cursor to end of the current word"),
        None,
    ),
    PolyactionInfo(
        polyactions.CLIPBOARD_COPY_LINE,
        _("Copy line"),
        _("Copy the current line to clipboard"),
        None,
    ),
    PolyactionInfo(
        polyactions.CLIPBOARD_CUT_LINE,
        _("Cut line"),
        _("Cut the current line to clipboard"),
        None,
    ),
    PolyactionInfo(
        polyactions.CLIPBOARD_COPY_WORD,
        _("Copy word"),
        _("Copy the current word to clipboard"),
        None,
    ),
    PolyactionInfo(
        polyactions.CLIPBOARD_CUT_WORD,
        _("Cut word"),
        _("Cut the current word to clipboard"),
        None,
    ),
    PolyactionInfo(
        polyactions.TEXT_COLOR_STR_ID,
        _("Text color..."),
        _("Set text color"),
        HotKey("K", ctrl=True, shift=True),
    ),
    PolyactionInfo(
        polyactions.TEXT_BACKGROUND_COLOR_STR_ID,
        _("Text background color..."),
        _("Set text background color"),
        HotKey("N", ctrl=True, shift=True),
    ),
    PolyactionInfo(
        polyactions.COMMENT_STR_ID, _("Comment"), _("Mark text as comment"), None
    ),
    PolyactionInfo(
        polyactions.SWITCH_TO_CODE_TAB_ID,
        _("Switch to code tab"),
        _("Switch to code tab for some page types"),
        None,
    ),
    PolyactionInfo(
        polyactions.SWITCH_TO_PREVIEW_TAB_ID,
        _("Switch to preview tab"),
        _("Switch to preview tab for some page types"),
        None,
    ),
]
