#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from outwiker.core.pluginbase import Plugin


class PluginTestEmpty1 (Plugin):
    def __init__ (self, application):
        """
        Plugin with an error. No plugin.py modules in the package.
        """
        Plugin.__init__ (self, application)
        self.__enabled = False

    
    @property
    def enabled (self):
        return self.__enabled


    @property
    def application (self):
        return self._application


    ###############################
    # Abstract settings and methods
    ###############################

    @property
    def name (self):
        return u"TestPlugin"

    
    @property
    def description (self):
        return _(u"This plugin is empty")


    @property
    def version (self):
        return u"0.1"

    @version.setter
    def version(self, value):
        self._version = value

    
    def initialize(self):
        self.__enabled = True


    def destroy (self):
        """
        Plugin destroy actions.
        Plugin must unbind for all events here.
        """
        self.__enabled = False

    #############################################
