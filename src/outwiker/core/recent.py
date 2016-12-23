# -*- coding: UTF-8 -*-

from .config import IntegerOption


class RecentWiki(object):
    """
    Класс для хранения списка последних открытых вики
    """
    # Длина истории по умолчанию
    MAXLEN_DEFAULT = 5

    def __init__(self, config):
        """
        config - эксемпляр класса core.config. Туда сохраняем список файлов
        """
        self._config = config
        self._sectionName = u"RecentWiki"
        self._paramTemplate = u"Path_%d"

        # Имя параметра, в котором хранится размер истории
        # последних открытых вики
        self._maxLenParamName = u"maxcount"

        self._recentes = self._load()

    def onWikiOpen(self, wikiroot):
        """
        Обработчик события на открытие вики
        """
        if wikiroot is not None and not wikiroot.readonly:
            self.add(wikiroot.path)

    def _load(self):
        """
        Загрузка последних открытых вики из файла конфига
        """
        # Сохраненные пути
        recentes = []

        try:
            for n in range(self.maxlen):
                param = self._paramTemplate % (n + 1)
                path = self._config.get(self._sectionName, param)

                recentes.append(path)
        except:
            pass

        return recentes

    def _save(self):
        """
        Сохранение списка последних открытых вики
        """
        for n in range(len(self._recentes)):
            param = self._paramTemplate % (n + 1)
            self._config.set(self._sectionName, param, self._recentes[n])

    def add(self, path):
        """
        Добавить путь к списку последних открытых вики
        """
        if path in self._recentes:
            self._recentes.remove(path)

        self._recentes.insert(0, path)

        if len(self._recentes) > self.maxlen:
            del self._recentes[self.maxlen:]

        self._save()

    def __len__(self):
        return len(self._recentes)

    def __getitem__(self, index):
        return self._recentes[index]

    @property
    def maxlen(self):
        """
        Возвращает размер списка последних открытых вики (значение из конфига)
        """
        return IntegerOption(self._config,
                             self._sectionName,
                             self._maxLenParamName,
                             self.MAXLEN_DEFAULT).value
