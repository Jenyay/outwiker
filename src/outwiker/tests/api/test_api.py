def test_old_plugins_imports():
    # Don't used in the last version
    from outwiker.actions.close import CloseAction

    from outwiker.actions.showhideattaches import ShowHideAttachesAction
    from outwiker.actions.showhidetree import ShowHideTreeAction
    from outwiker.core.attachfilters import (getImagesOnlyFilter, getHiddenFilter, getDirOnlyFilter, andFilter, orFilter, notFilter)
    from outwiker.core.attachment import Attachment
    from outwiker.core.commands import MessageBox
    from outwiker.core.commands import copyTextToClipboard
    from outwiker.core.commands import getClipboardText
    from outwiker.core.commands import insertCurrentDate
    from outwiker.core.commands import isImage
    from outwiker.core.commands import openWiki
    from outwiker.core.commands import testPageTitle, renamePage
    from outwiker.core.commands import testreadonly
    from outwiker.core.config import Config
    from outwiker.core.config import StringOption, IntegerOption, ListOption, BooleanOption
    from outwiker.core.defines import PAGE_ATTACH_DIR
    from outwiker.core.defines import PAGE_CONTENT_FILE
    from outwiker.core.defines import PAGE_MODE_TEXT, PAGE_MODE_PREVIEW
    from outwiker.core.defines import PAGE_RESULT_HTML
    from outwiker.core.event import EVENT_PRIORITY_DEFAULT, pagetype
    from outwiker.core.event import Event
    from outwiker.core.events import PAGE_UPDATE_CONTENT
    from outwiker.core.events import PageDialogPageFactoriesNeededParams
    from outwiker.core.events import PageUpdateNeededParams
    from outwiker.core.exceptions import PreferencesException
    from outwiker.core.exceptions import ReadonlyException
    from outwiker.core.factory import PageFactory
    from outwiker.core.factoryselector import FactorySelector
    from outwiker.core.htmlformatter import HtmlFormatter
    from outwiker.core.htmlimprover import HtmlImprover
    from outwiker.core.htmltemplate import HtmlTemplate
    from outwiker.core.htmltemplate import MyTemplate
    from outwiker.core.iconmaker import IconMaker
    from outwiker.core.pagetitletester import WindowsPageTitleTester
    from outwiker.core.pluginbase import Plugin
    from outwiker.core.style import Style
    from outwiker.core.system import getCurrentDir
    from outwiker.core.system import getImagesDir
    from outwiker.core.system import getOS
    from outwiker.core.system import getSpecialDirList
    from outwiker.core.tagslist import TagsList
    from outwiker.core.tree import WikiDocument
    from outwiker.core.tree import WikiPage
    from outwiker.gui.baseaction import BaseAction
    from outwiker.gui.basetextstylingcontroller import BaseTextStylingController
    from outwiker.gui.controls.filestreecombobox import FilesTreeComboBox
    from outwiker.gui.controls.filestreectrl import FilesTreeCtrl
    from outwiker.gui.controls.hyperlink import HyperLinkCtrl
    from outwiker.gui.controls.popupbutton import (PopupButton, EVT_POPUP_BUTTON_MENU_CLICK)
    from outwiker.gui.controls.safeimagelist import SafeImageList
    from outwiker.gui.controls.texteditorbase import TextEditorBase
    from outwiker.gui.defines import MENU_FILE
    from outwiker.gui.defines import MENU_HELP
    from outwiker.gui.defines import MENU_TOOLS
    from outwiker.gui.defines import MENU_VIEW
    from outwiker.gui.defines import TOOLBAR_PLUGINS
    from outwiker.gui.dialogs.baselinkdialogcontroller import BaseLinkDialogController
    from outwiker.gui.guiconfig import GeneralGuiConfig
    from outwiker.gui.guiconfig import MainWindowConfig
    from outwiker.gui.htmltexteditor import HtmlTextEditor
    from outwiker.gui.longprocessrunner import LongProcessRunner
    from outwiker.gui.pagedialogpanels.appearancepanel import (AppearancePanel, AppearanceController)
    from outwiker.gui.preferences.baseprefpanel import BasePrefPanel
    from outwiker.gui.preferences.configelements import IntegerElement
    from outwiker.gui.preferences.preferencepanelinfo import PreferencePanelInfo
    from outwiker.gui.simplespellcontroller import SimpleSpellController
    from outwiker.gui.tabledialog import TableDialog
    from outwiker.gui.tablerowsdialog import TableRowsDialog
    from outwiker.gui.tagsselector import TagsSelector
    from outwiker.gui.testeddialog import TestedDialog
    from outwiker.gui.testeddialog import TestedFileDialog
    from outwiker.gui.texteditorhelper import TextEditorHelper
    from outwiker.pages.html.actions.link import insertLink
    from outwiker.pages.html.actions.switchcoderesult import SwitchCodeResultAction
    from outwiker.pages.html.tabledialogcontroller import ( TableDialogController, TableRowsDialogController)
    from outwiker.pages.wiki.basewikipageview import BaseWikiPageView
    from outwiker.pages.wiki.defines import MENU_WIKI
    from outwiker.pages.wiki.defines import MENU_WIKI_COMMANDS
    from outwiker.pages.wiki.htmlcache import HtmlCache
    from outwiker.pages.wiki.parser.command import Command
    from outwiker.pages.wiki.parser.pagethumbmaker import PageThumbmaker
    from outwiker.pages.wiki.parser.tokenattach import AttachToken
    from outwiker.pages.wiki.parser.wikiparser import Parser
    from outwiker.pages.wiki.parserfactory import ParserFactory
    from outwiker.pages.wiki.thumbnails import Thumbnails
    from outwiker.pages.wiki.wikiconfig import WikiConfig
    from outwiker.pages.wiki.wikieditor import WikiEditor
    from outwiker.pages.wiki.wikipage import WikiWikiPage
    from outwiker.utilites.actionsguicontroller import (ActionsGUIController, ActionGUIInfo, ButtonInfo)
    from outwiker.utilites.text import positionInside
    from outwiker.utilites.textfile import readTextFile, writeTextFile
    import outwiker.actions.polyactionsid
    import outwiker.core.exceptions
