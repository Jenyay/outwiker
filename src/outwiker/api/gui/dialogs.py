from outwiker.gui.dialogs.baselinkdialogcontroller import BaseLinkDialogController
import outwiker.gui.dialogs.messagebox as _messagebox
from outwiker.gui.testeddialog import (TestedDialog, TestedColourDialog,
                                       TestedFileDialog,
                                       TestedSingleChoiceDialog)


def MessageBox(*args, **kwargs):
    return _messagebox.MessageBox(*args, **kwargs)
