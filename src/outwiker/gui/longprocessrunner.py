# -*- coding: utf-8 -*-

import threading
import time

from .controls.progress import ProgressWindow


class LongProcessRunner:
    """Класс для запуска длительных операций в отдельном потоке и показ диалога
    с ожиданием без прогресса на время выполнения.

    Показываемый диалог будет модальным и блокировать текущее окно.
    Диалог нельзя закрыть до завершения функции.
    """

    def __init__(self, threadFunc, parent, dialogTitle="", dialogText=""):
        """
        threadFunc - функцию, которую нужно запустить.
            Функция может возвращать значение
        parent - родитель для диалога
        dialogTitle - заголовок диалога
        dialogText - текст надписи в диалоге
        """
        self._threadFunc = threadFunc
        self._parent = parent
        self._dialogTitle = dialogTitle
        self._dialogText = dialogText

        # Интервал обновления диалога, с
        self.updateInterval = 0.1

    def run(self, *args, **kwargs):
        # progressDlg = ProgressWindow(self._parent, self._dialogTitle, self._dialogText)
        # progressDlg.Show()

        # result = []
        # thread = threading.Thread(
        #     None,
        #     lambda *args, **kwargs: result.append(self._threadFunc(*args, **kwargs)),
        #     args=args,
        #     kwargs=kwargs,
        # )
        # thread.start()

        # while thread.is_alive():
        #     progressDlg.UpdatePulse()
        #     time.sleep(self.updateInterval)

        # progressDlg.Destroy()
        # self._parent.Raise()

        # if result:
        #     return result[0]
        # else:
        #     return None
        return self._threadFunc(*args, **kwargs)
