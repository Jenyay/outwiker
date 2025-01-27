from outwiker.gui.controls.filestreecombobox import FilesTreeComboBox
from outwiker.gui.controls.filestreectrl import FilesTreeCtrl
from outwiker.gui.controls.popupbutton import PopupButton, EVT_POPUP_BUTTON_MENU_CLICK
from outwiker.gui.controls.safeimagelist import SafeImageList
from outwiker.gui.controls.texteditorbase import TextEditorBase
from outwiker.gui.htmltexteditor import HtmlTextEditor
from outwiker.gui.tagsselector import TagsSelector
from outwiker.gui.controls.hyperlink import HyperLinkCtrl
from outwiker.gui.controls.colorcombobox import ColorComboBox
from outwiker.gui.controls.notestreectrl2 import NotesTreeItem

from outwiker.core.system import getOS as _getOS


def getHtmlRender(parent, application):
    return _getOS().getHtmlRender(parent, application)


def getHtmlRenderForPage(parent, application):
    return _getOS().getHtmlRenderForPage(parent, application)
