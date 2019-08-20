# -*- coding: UTF-8 -*-

import wx

from outwiker.gui.basepagepanel import BasePagePanel


class TestPageView (BasePagePanel):
    def __init__ (self, parent, application):
        super (TestPageView, self).__init__ (parent, application)
        self.SetBackgroundColour ('#A190F5')

        self.__createGui()


    def __createGui (self):
        self.text = wx.TextCtrl (self)

        mainSizer = wx.FlexGridSizer (cols=1)
        mainSizer.AddGrowableCol (0)

        mainSizer.Add (self.text,
                       flag = wx.EXPAND | wx.ALL,
                       border = 4)

        self.SetSizer (mainSizer)


    def Print (self):
        """
        Вызов печати страницы
        """
        print (u"Print!")


    def UpdateView (self, page):
        """
        Обновление страницы
        """
        self.text.SetValue (page.content)


    def Save (self):
        """
        Сохранить страницу
        """
        if self.page is not None:
            self.page.content = self.text.GetValue()


    def Clear (self):
        """
        Убрать за собой. Удалить добавленные элементы интерфейса и отписаться от событий
        """
        pass
