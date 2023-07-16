# -*- coding: utf-8 -*-

def showError(mainWindow: "outwiker.app.gui.mainwindow.MainWindow", message: str):
    '''
    Show error message with Toaster
    '''
    mainWindow.toaster.showError(message)


def showInfo(mainWindow: "outwiker.app.gui.mainwindow.MainWindow",
             title: str,
             message: str):
    '''
    Show info message with Toaster
    '''
    mainWindow.toaster.showInfo(title, message)
