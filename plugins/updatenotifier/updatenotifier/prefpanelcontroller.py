# -*- coding: UTF-8 -*-

from .i18n import get_
from .updatesconfig import UpdatesConfig


class PrefPanelController(object):
    """
    Контроллер для панели настроек
    """
    def __init__(self, owner, config):
        self.__owner = owner
        self.__config = UpdatesConfig(config)

        global _
        _ = get_()

        # Список возможных интервалов обновлений
        # Через интерфейс не будем давать возможность задавать
        # произвольный интервал обновлений, хотя это можно сделать
        # через файл настроек. В этом случае появится дополнительный
        # пункт "Custom"
        self.intervalList = {
            0: _(u"Never"),
            1: _(u"Every day"),
            2: _(u"Every two days"),
            3: _(u"Every three days"),
            7: _(u"Every week"),
            14: _(u"Every two weeks"),
            30: _(u"Every month"),
        }

    def loadState(self):
        self.__loadIntervalList()
        self.__owner.ignoreUnstableCheckBox.SetValue(self.__config.ignoreUnstable)

    def __loadIntervalList(self):
        """
        Заполнить комбобокс с интервалами обновлений
        """
        keys = sorted(self.intervalList.keys())

        for key in keys:
            self.__owner.intervalComboBox.Append(self.intervalList[key])

        currentInterval = self.__config.updateInterval

        if currentInterval in keys:
            # Интервал обновлений есть в списке
            self.__owner.intervalComboBox.SetSelection(keys.index(currentInterval))
        else:
            # В списке нет выбранного интервала обновлений
            self.__owner.intervalComboBox.Append(_(u"Custom"))
            self.__owner.intervalComboBox.SetSelection(len(keys))

    def save(self):
        self.__saveInterval()
        self.__config.ignoreUnstable = self.__owner.ignoreUnstableCheckBox.IsChecked()

    def __saveInterval(self):
        """
        Сохранить интервал проверки обновлений
        """
        keys = sorted(self.intervalList.keys())

        selectedInterval = self.__owner.intervalComboBox.GetSelection()
        assert selectedInterval >= 0

        if selectedInterval < len(keys):
            # Выбран пункт не "Custom"
            self.__config.updateInterval = keys[selectedInterval]
