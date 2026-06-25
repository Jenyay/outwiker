# -*- coding: utf-8 -*-

from .config import IntegerOption


class RecentWiki:
    """
    Class for storing the list of recently opened wikis
    """

    # Default history length
    MAXLEN_DEFAULT = 5

    def __init__(self, config):
        """
        config - instance of core.config class. The list of files is saved there.
        """
        self._config = config
        self._sectionName = "RecentWiki"
        self._paramTemplate = "Path_%d"

        # Parameter name that stores the size of the recently opened wikis history
        self._maxLenParamName = "maxcount"

        self._recentes = self._load()

    def _load(self):
        """
        Load recently opened wikis from the config file
        """
        # Saved paths
        recentes = []

        try:
            for n in range(self.maxlen):
                param = self._paramTemplate % (n + 1)
                path = self._config.get(self._sectionName, param)

                recentes.append(path)
        except Exception:
            pass

        return recentes

    def _save(self):
        """
        Save the list of recently opened wikis
        """
        for n in range(len(self._recentes)):
            param = self._paramTemplate % (n + 1)
            self._config.set(self._sectionName, param, self._recentes[n])

    def add(self, path):
        """
        Add a path to the list of recently opened wikis
        """
        if path in self._recentes:
            self._recentes.remove(path)

        self._recentes.insert(0, path)

        if len(self._recentes) > self.maxlen:
            del self._recentes[self.maxlen :]

        self._save()

    def __len__(self):
        return len(self._recentes)

    def __getitem__(self, index):
        return self._recentes[index]

    def get_all(self):
        return self._recentes

    @property
    def maxlen(self):
        """
        Returns the size of the list of recently opened wikis (value from config)
        """
        return IntegerOption(
            self._config, self._sectionName, self._maxLenParamName, self.MAXLEN_DEFAULT
        ).value
