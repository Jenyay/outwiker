from outwiker.gui.dialogs.baselinkdialogcontroller import BaseLinkDialogController
import outwiker.gui.dialogs.messagebox as _messagebox
from outwiker.gui.testeddialog import (TestedDialog, TestedColourDialog,
                                       TestedFileDialog,
                                       TestedSingleChoiceDialog,
                                       TestedDirDialog)
from outwiker.gui.dialogs.buttonsdialog import ButtonsDialog
from outwiker.gui.tabledialog import TableDialog
from outwiker.gui.tablerowsdialog import TableRowsDialog


def MessageBox(*args, **kwargs):
    return _messagebox.MessageBox(*args, **kwargs)
