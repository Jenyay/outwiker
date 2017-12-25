# -*- coding: utf-8 -*-

import os.path
import configparser

import wx

from outwiker.core.config import IntegerOption, BooleanOption

from .toolsinfo import ToolsInfo


class ExternalToolsConfig(object):
    def __init__(self, config):
        self._sectionName = "ExternalTools"
        self._toolsItemTemplate = "tools{index}"

        self._config = config

        # Dialog size for (:exec:) command inserting
        DEFAULT_DIALOG_WIDTH = -1
        DEFAULT_DIALOG_HEIGHT = -1

        DIALOG_WIDTH_OPTION = u"DialogWidth"
        DIALOG_HEIGHT_OPTION = u"DialogHeight"

        # Recent selected format
        DEFAULT_FORMAT = 0
        DIALOG_SELECTED_FORMAT_OPTION = u'ExecFormat'

        # Show warning
        DEFAULT_WARNING = True
        WARNING_OPTION = u'ShowExecWarning'

        self._dialogWidth = IntegerOption(self._config,
                                          self._sectionName,
                                          DIALOG_WIDTH_OPTION,
                                          DEFAULT_DIALOG_WIDTH)

        self._dialogHeight = IntegerOption(self._config,
                                           self._sectionName,
                                           DIALOG_HEIGHT_OPTION,
                                           DEFAULT_DIALOG_HEIGHT)

        self._execFormat = IntegerOption(self._config,
                                         self._sectionName,
                                         DIALOG_SELECTED_FORMAT_OPTION,
                                         DEFAULT_FORMAT)

        self._execWarning = BooleanOption(self._config,
                                          self._sectionName,
                                          WARNING_OPTION,
                                          DEFAULT_WARNING)

    def clearAll(self):
        """
        Remove all options
        """
        self._config.remove_section(self._sectionName)

    @property
    def dialogWidth(self):
        return self._dialogWidth.value

    @dialogWidth.setter
    def dialogWidth(self, value):
        self._dialogWidth.value = value

    @property
    def dialogHeight(self):
        return self._dialogHeight.value

    @dialogHeight.setter
    def dialogHeight(self, value):
        self._dialogHeight.value = value

    @property
    def execFormat(self):
        return self._execFormat.value

    @execFormat.setter
    def execFormat(self, value):
        self._execFormat.value = value

    @property
    def execWarning(self):
        return self._execWarning.value

    @execWarning.setter
    def execWarning(self, value):
        self._execWarning.value = value

    @property
    def tools(self):
        toolsItems = []

        while True:
            paramname = self._toolsItemTemplate.format(index=len(toolsItems) + 1)
            try:
                toolsPath = self._config.get(self._sectionName, paramname)
            except configparser.Error:
                break

            toolsName = os.path.basename(toolsPath)
            toolsItems.append(ToolsInfo(toolsPath, toolsName, wx.NewId()))

        return toolsItems

    @tools.setter
    def tools(self, toolsItems):
        """
        Может бросить исключение ConfigParser.
        Error в случае ошибки сохранения конфига
        """
        self._removeTools(len(toolsItems) + 1)
        self._saveTools(toolsItems)

    def _removeTools(self, minCount):
        """
        удалить все инструменты из настроек
        minCount - минимальное количество элементов,
        которое необходимо проверить на наличие, чтобы удалить
        """
        index = 1
        while True:
            paramname = self._toolsItemTemplate.format(index=index)

            try:
                self._config.get(self._sectionName, paramname)
                self._config.remove_option(self._sectionName, paramname)
            except configparser.Error:
                if index >= minCount:
                    break

            index += 1

    def _saveTools(self, toolsItems):
        index = 1
        for tool in toolsItems:
            paramname = self._toolsItemTemplate.format(index=index)
            self._config.set(self._sectionName, paramname, tool.command)
            index += 1
