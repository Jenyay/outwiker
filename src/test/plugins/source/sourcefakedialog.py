# -*- coding: UTF-8 -*-

from .fakewx.spinctrl import SpinCtrl
from .fakewx.combobox import ComboBox
from .fakewx.dialog import Dialog
from .fakewx.statictext import StaticText
from .fakewx.checkbox import CheckBox
from .fakewx.button import Button


class FakeInsertDialog (Dialog):
    """
    Заглушка вместо реального диалога для вставки команды (:source:)
    """
    def __init__ (self):
        super (FakeInsertDialog, self).__init__ ()

        # Заглушки вместо интерфейса
        self.tabWidthSpin = SpinCtrl ()
        self.languageComboBox = ComboBox ()

        self.fileCheckBox = CheckBox()

        self.attachmentLabel = StaticText ()
        self.attachmentComboBox = ComboBox ()

        self.encodingLabel = StaticText ()
        self.encodingComboBox = ComboBox ()

        self.styleLabel = StaticText ()
        self.styleComboBox = ComboBox ()

        self.attachButton = Button()
        self.parentBgCheckBox = CheckBox ()
        self.lineNumCheckBox = CheckBox ()


    @property
    def language (self):
        return self.languageComboBox.GetValue()


    @property
    def tabWidth (self):
        return self.tabWidthSpin.GetValue()


    @property
    def languageIndex (self):
        return self.languageComboBox.GetCurrentSelection()


    @property
    def attachment (self):
        return self.attachmentComboBox.GetValue()


    @property
    def encoding (self):
        return self.encodingComboBox.GetValue()


    @property
    def insertFromFile (self):
        return self.fileCheckBox.IsChecked()


    @property
    def style (self):
        return self.styleComboBox.GetValue()


    @property
    def parentbg (self):
        return self.parentBgCheckBox.GetValue()


    @property
    def lineNum (self):
        return self.lineNumCheckBox.GetValue()
