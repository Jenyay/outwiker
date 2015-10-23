# -*- coding: UTF-8 -*-

from .i18n import get_


class Controller (object):
    """
    Класс отвечает за основную работу интерфейса плагина
    """
    def __init__ (self, plugin, application):
        """
        """
        self._plugin = plugin
        self._application = application


    def initialize (self):
        """
        Инициализация контроллера при активации плагина. Подписка на нужные события
        """
        global _
        _ = get_()
        self._application.onPageDialogPageTypeChanged += self.__onPageDialogPageTypeChanged


    def destroy (self):
        """
        Вызывается при отключении плагина
        """
        self._application.onPageDialogPageTypeChanged -= self.__onPageDialogPageTypeChanged


    def __onPageDialogPageTypeChanged (self, page, params):
        colors = {
            u'wiki': u'#F1F779',
            u'html': u'#9DC0FA',
            u'text': u'#79F7B8',
            u'search': u'#F280E3',
        }

        color = colors.get (params.pageType, 'white')
        params.dialog.generalPanel.titleTextCtrl.SetBackgroundColour (color)
