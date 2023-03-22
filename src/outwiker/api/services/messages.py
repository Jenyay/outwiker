import outwiker.app.services.messages as _messages


def showError(mainWindow: "outwiker.app.gui.mainwindow.MainWindow", message: str):
    '''
    Show error message with Toaster
    '''
    return _messages.showError(mainWindow, message)


def showInfo(mainWindow: "outwiker.app.gui.mainwindow.MainWindow",
             title: str,
             message: str):
    '''
    Show info message with Toaster
    '''
    return _messages.showInfo(mainWindow, title, message)
