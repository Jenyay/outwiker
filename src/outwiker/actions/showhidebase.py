# -*- coding: UTF-8 -*-

from abc import abstractmethod, ABCMeta

from outwiker.gui.baseaction import BaseAction


class ShowHideBaseAction (BaseAction):
    """
    Базовый класс для показа / скрытия панелей главного окна
    """
    __metaclass__ = ABCMeta

    def __init__ (self, application):
        self._application = application


    @abstractmethod
    def getPanel (self):
        pass


    def run (self, params):
        if params:
            self.getPanel().pane.Show ()
        else:
            self.getPanel().pane.Hide ()

        self._application.mainWindow.auiManager.Update()
