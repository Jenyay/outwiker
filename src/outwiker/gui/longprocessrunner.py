# -*- coding: UTF-8 -*-

import threading
import time

import wx

from wx.lib.agw.pyprogress import PyProgress


class LongProcessRunner (object):
    """Класс для запуска длительных операций в отдельном потоке и показ диалога с ожиданием без прогресса на время выполнения.

    Показываемый диалог будет модальным и блокировать текущее окно.
    Диалог нельзя закрыть до завершения функции.
    """
    def __init__(self, threadFunc, parent, dialogTitle=u"", dialogText=u""):
        """
        threadFunc - функцию, которую нужно запустить. Функция может возвращать значение
        parent - родитель для диалога
        dialogTitle - заголовок диалога
        dialogText - текст надписи в диалоге
        """
        self._threadFunc = threadFunc
        self._parent = parent
        self._dialogTitle = dialogTitle
        self._dialogText = dialogText

        # Интервал обновления диалога, с
        self.updateGaugeInterval = 0.05

        # Размер бегающей чисти линии прогресса
        self.gaugeProportion = 0.2

        # Количество шагов пробегания линии прогресса
        self.gaugeSteps = 20


    def run (self, *args, **kwargs):
        progressDlg = PyProgress(self._parent, -1, self._dialogTitle,
                                 self._dialogText,
                                 agwStyle = wx.PD_APP_MODAL)

        progressDlg.SetGaugeProportion(self.gaugeProportion)
        progressDlg.SetGaugeSteps(self.gaugeSteps)
        progressDlg.UpdatePulse()

        result = []
        thread = threading.Thread (None,
                                   lambda *args, **kwargs: result.append (self._threadFunc(*args, **kwargs)),
                                   args = args,
                                   kwargs = kwargs)
        thread.start()

        while thread.isAlive ():
            progressDlg.UpdatePulse()
            time.sleep (self.updateGaugeInterval)

        progressDlg.Destroy()
        self._parent.Raise()

        return result[0]
