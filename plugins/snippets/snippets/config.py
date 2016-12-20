# -*- coding: UTF-8 -*-

from outwiker.core.config import IntegerOption, StringOption


class SnippetsConfig (object):
    def __init__(self, config):
        self._config = config

        self.section = u'SnippetsPlugin'

        # EditDialog size
        self._editDialogWidth = IntegerOption(self._config,
                                              self.section,
                                              u'EditDialogWidth',
                                              800)

        self._editDialogHeight = IntegerOption(self._config,
                                               self.section,
                                               u'EditDialogHeight',
                                               500)

        # VariablesDialog size
        self._variablesDialogWidth = IntegerOption(self._config,
                                                   self.section,
                                                   u'VariablesDialogWidth',
                                                   700)

        self._variablesDialogHeight = IntegerOption(self._config,
                                                    self.section,
                                                    u'VariablesDialogHeight',
                                                    400)

        # Recently used snippet
        self._recentSnippet = StringOption(self._config,
                                           self.section,
                                           u'RecentSnippet',
                                           u'')

    # EditDialog size
    @property
    def editDialogWidth(self):
        return self._editDialogWidth.value

    @editDialogWidth.setter
    def editDialogWidth(self, value):
        self._editDialogWidth.value = value

    @property
    def editDialogHeight(self):
        return self._editDialogHeight.value

    @editDialogHeight.setter
    def editDialogHeight(self, value):
        self._editDialogHeight.value = value

    # VariablesDialog size
    @property
    def variablesDialogWidth(self):
        return self._variablesDialogWidth.value

    @variablesDialogWidth.setter
    def variablesDialogWidth(self, value):
        self._variablesDialogWidth.value = value

    @property
    def variablesDialogHeight(self):
        return self._variablesDialogHeight.value

    @variablesDialogHeight.setter
    def variablesDialogHeight(self, value):
        self._variablesDialogHeight.value = value

    # Recently used snippet
    @property
    def recentSnippet(self):
        return self._recentSnippet.value

    @recentSnippet.setter
    def recentSnippet(self, value):
        self._recentSnippet.value = value
