#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os.path
import ConfigParser

import wx

from .toolsinfo import ToolsInfo


class ToolsConfig (object):
    def __init__ (self, config):
        self._sectionName = "ExternalTools"
        self._toolsItemTemplate = "tools{index}"

        self._config = config


    @property
    def tools (self):
        toolsItems = []

        while True:
            paramname = self._toolsItemTemplate.format (index = len (toolsItems) + 1)
            try:
                toolsPath = self._config.get (self._sectionName, paramname)
            except ConfigParser.Error:
                break

            toolsName = os.path.basename (toolsPath)
            toolsItems.append (ToolsInfo (toolsPath, toolsName, wx.NewId()))

        return toolsItems


    @tools.setter
    def tools (self, toolsItems):
        """
        Может бросить исключение ConfigParser.Error в случае ошибки сохранения конфига
        """
        self._removeTools(len (toolsItems) + 1)
        self._saveTools (toolsItems)


    def _removeTools (self, minCount):
        """
        удалить все инструменты из настроек
        minCount - минимальное количество элементов, которое необходимо проверить на наличие, чтобы удалить
        """
        index = 1
        while True:
            paramname = self._toolsItemTemplate.format (index=index)

            try:
                self._config.get (self._sectionName, paramname)
                self._config.remove_option (self._sectionName, paramname)
            except ConfigParser.Error:
                if index >= minCount:
                    break

            index += 1


    def _saveTools (self, toolsItems):
        index = 1
        for tool in toolsItems:
            paramname = self._toolsItemTemplate.format (index=index)
            self._config.set (self._sectionName, paramname, tool.command)
            index += 1
