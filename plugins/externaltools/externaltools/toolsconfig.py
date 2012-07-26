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
