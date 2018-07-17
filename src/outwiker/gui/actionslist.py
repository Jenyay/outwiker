# -*- coding: UTF-8 -*-

import outwiker.actions as actions
import outwiker.actions.polyactionsid as polyactions
from outwiker.gui.hotkey import HotKey


actionsList = [
    (actions.open.OpenAction, HotKey("O", ctrl=True)),
    (actions.new.NewAction, HotKey("N", ctrl=True)),
    (actions.openreadonly.OpenReadOnlyAction, None),
    (actions.close.CloseAction, HotKey("W", ctrl=True, shift=True)),
    (actions.save.SaveAction, HotKey("S", ctrl=True)),
    (actions.exit.ExitAction, HotKey("F4", alt=True)),

    (actions.showhideattaches.ShowHideAttachesAction, None),
    (actions.showhidetree.ShowHideTreeAction, None),
    (actions.showhidetags.ShowHideTagsAction, None),

    (actions.search.SearchAction, HotKey("F", ctrl=True)),
    (actions.search.SearchNextAction, HotKey("F3")),
    (actions.search.SearchPrevAction, HotKey("F3", shift=True)),
    (actions.search.SearchAndReplaceAction, HotKey("F3", ctrl=True)),

    (actions.addsiblingpage.AddSiblingPageAction, HotKey("Y", ctrl=True, shift=True)),
    (actions.addchildpage.AddChildPageAction, HotKey("P", ctrl=True, shift=True)),
    (actions.movepageup.MovePageUpAction, HotKey("Up", ctrl=True, shift=True)),
    (actions.movepagedown.MovePageDownAction, HotKey("Down", ctrl=True, shift=True)),

    (actions.renamepage.RenamePageAction, HotKey("F2")),
    (actions.removepage.RemovePageAction, HotKey("F8", ctrl=True, shift=True)),

    (actions.sortchildalpha.SortChildAlphabeticalAction, None),
    (actions.sortsiblingsalpha.SortSiblingsAlphabeticalAction, None),

    (actions.tabs.AddTabAction, HotKey("T", ctrl=True)),
    (actions.tabs.CloseTabAction, HotKey("W", ctrl=True)),
    (actions.tabs.PreviousTabAction, HotKey("PageUp", ctrl=True, shift=True)),
    (actions.tabs.NextTabAction, HotKey("PageDown", ctrl=True, shift=True)),

    (actions.globalsearch.GlobalSearchAction, HotKey("F", ctrl=True, shift=True)),
    (actions.attachfiles.AttachFilesAction, HotKey("A", ctrl=True, shift=True)),
    (actions.openattachfolder.OpenAttachFolderAction, None),

    (actions.clipboard.CopyPageTitleAction, None),
    (actions.clipboard.CopyPagePathAction, None),
    (actions.clipboard.CopyAttachPathAction, None),
    (actions.clipboard.CopyPageLinkAction, None),

    (actions.tags.AddTagsToBranchAction, None),
    (actions.tags.RemoveTagsFromBranchAction, None),
    (actions.tags.RenameTagAction, None),

    (actions.history.HistoryBackAction, HotKey("Left", ctrl=True, alt=True)),
    (actions.history.HistoryForwardAction, HotKey("Right", ctrl=True, alt=True)),

    (actions.moving.GoToParentAction, None),
    (actions.moving.GoToFirstChildAction, None),
    (actions.moving.GoToNextSiblingAction, HotKey("Down", ctrl=True)),
    (actions.moving.GoToPrevSiblingAction, HotKey("Up", ctrl=True)),

    (actions.printaction.PrintAction, HotKey("P", ctrl=True)),
    (actions.fullscreen.FullScreenAction, HotKey("F11")),
    (actions.preferences.PreferencesAction, HotKey("F8", ctrl=True)),
    (actions.editpageprop.EditPagePropertiesAction, HotKey("E", ctrl=True)),
    (actions.addbookmark.AddBookmarkAction, HotKey("D", ctrl=True)),
    (actions.reloadwiki.ReloadWikiAction, None),
    (actions.openhelp.OpenHelpAction, HotKey("F1")),
    (actions.about.AboutAction, HotKey("F1", ctrl=True)),
    (actions.applystyle.SetStyleToBranchAction, None),
    (actions.openpluginsfolder.OpenPluginsFolderAction, None),

    (actions.switchto.SwitchToMainPanelAction, None),
    (actions.switchto.SwitchToTreeAction, None),
    (actions.switchto.SwitchToAttachmentsAction, None),
    (actions.switchto.SwitchToTagsCloudAction, None),
]


polyactionsList = [
    (polyactions.BOLD_STR_ID, _(u"Bold"), _(u"Bold"), HotKey("B", ctrl=True)),
    (polyactions.ITALIC_STR_ID, _(u"Italic"), _(u"Italic"), HotKey("I", ctrl=True)),
    (polyactions.BOLD_ITALIC_STR_ID, _(u"Bold italic"), _(u"Bold italic"), HotKey("I", ctrl=True, shift=True)),
    (polyactions.UNDERLINE_STR_ID, _(u"Underline"), _(u"Underline"), HotKey("U", ctrl=True)),
    (polyactions.STRIKE_STR_ID, _(u"Strikethrough"), _(u"Strikethrough"), HotKey("K", ctrl=True)),
    (polyactions.SUBSCRIPT_STR_ID, _(u"Subscript"), _(u"Subscript"), HotKey("=", ctrl=True)),
    (polyactions.SUPERSCRIPT_STR_ID, _(u"Superscript"), _(u"Superscript"), HotKey("+", ctrl=True)),
    (polyactions.PREFORMAT_STR_ID, _(u"Preformatted text"), _(u"Preformatted text"), HotKey("B", ctrl=True, shift=True)),
    (polyactions.CODE_STR_ID, _(u"Insert code"), _(u"Insert code(monospaced font)"), None),

    (polyactions.ALIGN_LEFT_STR_ID, _(u"Align text left"), _(u"Align text left"), HotKey("L", ctrl=True, shift=True)),
    (polyactions.ALIGN_CENTER_STR_ID, _(u"Align text center"), _(u"Center"), HotKey("C", ctrl=True, shift=True)),
    (polyactions.ALIGN_RIGHT_STR_ID, _(u"Align text right"), _(u"Align text right"), HotKey("R", ctrl=True, shift=True)),
    (polyactions.ALIGN_JUSTIFY_STR_ID, _(u"Justify"), _(u"Justify"), HotKey("J", ctrl=True, shift=True)),

    (polyactions.HEADING_1_STR_ID, _(u"First-level heading"), _(u"First-level heading"), HotKey("1", ctrl=True)),
    (polyactions.HEADING_2_STR_ID, _(u"Second-level heading"), _(u"Second-level heading"), HotKey("2", ctrl=True)),
    (polyactions.HEADING_3_STR_ID, _(u"Subtitle three"), _(u"Subtitle three"), HotKey("3", ctrl=True)),
    (polyactions.HEADING_4_STR_ID, _(u"Subtitle four"), _(u"Subtitle four"), HotKey("4", ctrl=True)),
    (polyactions.HEADING_5_STR_ID, _(u"Subtitle five"), _(u"Subtitle five"), HotKey("5", ctrl=True)),
    (polyactions.HEADING_6_STR_ID, _(u"Subtitle six"), _(u"Subtitle six"), HotKey("6", ctrl=True)),

    (polyactions.ANCHOR_STR_ID, _(u"Anchor"), _(u"Anchor"), None),
    (polyactions.HORLINE_STR_ID, _(u"Horizontal rule"), _(u"Horizontal rule"), HotKey("H", ctrl=True, shift=True)),
    (polyactions.LINK_STR_ID, _(u"Link"), _(u"Insert Link"), HotKey("L", ctrl=True)),
    (polyactions.QUOTE_STR_ID, _(u"Quote"), _(u"Insert a quote block"), HotKey("Q", ctrl=True)),
    (polyactions.IMAGE_STR_ID, _(u"Image"), _(u"Insert image"), HotKey("M", ctrl=True, shift=True)),
    (polyactions.MARK_STR_ID, _(u"Mark"), _(u"Mark text"), None),

    (polyactions.LIST_BULLETS_STR_ID, _(u"Bullets list"), _(u"Insert a bullets list"), HotKey("G", ctrl=True)),
    (polyactions.LIST_NUMBERS_STR_ID, _(u"Numbers list"), _(u"Insert a numbers list"), HotKey("J", ctrl=True)),

    (polyactions.LIST_DECREASE_LEVEL_STR_ID, _(u"Decrease nesting level"), _(u"Decrease the nesting level of the selected list items"), None),
    (polyactions.LINE_BREAK_STR_ID, _(u"Line break"), _(u"Insert a line break"), HotKey("Return", ctrl=True)),
    (polyactions.HTML_ESCAPE_STR_ID, _(u"Convert HTML Symbols"), _(u"Convert HTML Symbols"), None),

    (polyactions.TABLE_STR_ID, _(u"Table"), _(u"Insert a table"), HotKey("T", ctrl=True, shift=True)),
    (polyactions.TABLE_ROW_STR_ID, _(u"Table rows"), _(u"Insert table rows"), HotKey("G", ctrl=True, shift=True)),
    (polyactions.TABLE_CELL_STR_ID, _(u"Table cell"), _(u"Insert a table cell"), HotKey("U", ctrl=True, shift=True)),

    (polyactions.CURRENT_DATE, _(u"Current date"), _(u"Insert the current date"), None),
    (polyactions.SPELL_ON_OFF_ID, _(u"Spell checking"), _(u"Enable / disable spell checking"), HotKey("F7")),

    (polyactions.LINE_DUPLICATE_ID, _(u"Duplicate line"), _(u"Duplicate current line"), HotKey("D", ctrl=True, shift=True)),
    (polyactions.MOVE_SELECTED_LINES_UP_ID, _(u"Move selected lines up"), _(u"Move the selected lines up one line"), None),
    (polyactions.MOVE_SELECTED_LINES_DOWN_ID, _(u"Move selected lines down"), _(u"Move the selected lines down one line"), None),
    (polyactions.DELETE_CURRENT_LINE, _(u"Delete line"), _(u"Delete the current line"), None),
    (polyactions.JOIN_LINES, _(u"Join lines"), _(u"Join lines"), None),

    (polyactions.DELETE_WORD_LEFT, _(u"Delete word to the left"), _(u"Delete text to beginning of the word"), HotKey("Back", ctrl=True)),
    (polyactions.DELETE_WORD_RIGHT, _(u"Delete word to the right"), _(u"Delete text to ending of the word"), HotKey("Delete", ctrl=True)),
    (polyactions.DELETE_LINE_LEFT, _(u"Delete to start of the line"), _(u"Delete text back from the current position to the start of the line"), HotKey("Back", ctrl=True, shift=True)),
    (polyactions.DELETE_LINE_RIGHT, _(u"Delete to end of the line"), _(u"Delete text forwards from the current position to the end of the line"), HotKey("Delete", ctrl=True, shift=True)),

    (polyactions.GOTO_PREV_WORD, _(u"Go to previous word"), _(u"Move cursor to previous word"), HotKey("Left", ctrl=True)),
    (polyactions.GOTO_NEXT_WORD, _(u"Go to next word"), _(u"Move cursor to next word"), HotKey("Right", ctrl=True)),
    (polyactions.GOTO_PREV_WORD_SELECT, _(u"Go to previous word and select"), _(u"Move cursor to previous word and select text"), HotKey("Left", ctrl=True, shift=True)),
    (polyactions.GOTO_NEXT_WORD_SELECT, _(u"Go to next word and select"), _(u"Move cursor to next word and select text"), HotKey("Right", ctrl=True, shift=True)),
    (polyactions.GOTO_WORD_START, _(u"Go to start of the word"), _(u"Move cursor to start of the current word"), None),
    (polyactions.GOTO_WORD_END, _(u"Go to end of the word"), _(u"Move cursor to end of the current word"), None),

    (polyactions.CLIPBOARD_COPY_LINE, _(u"Copy line"), _(u"Copy the current line to clipboard"), None),
    (polyactions.CLIPBOARD_CUT_LINE, _(u"Cut line"), _(u"Cut the current line to clipboard"), None),
    (polyactions.CLIPBOARD_COPY_WORD, _(u"Copy word"), _(u"Copy the current word to clipboard"), None),
    (polyactions.CLIPBOARD_CUT_WORD, _(u"Cut word"), _(u"Cut the current word to clipboard"), None),
    (polyactions.TEXT_COLOR_STR_ID, _(u"Text color..."), _(u"Set text color"), HotKey("K", ctrl=True, shift=True)),
    (polyactions.TEXT_BACKGROUND_COLOR_STR_ID, _(u"Text background color..."), _(u"Set text background color"), HotKey("N", ctrl=True, shift=True)),
]
