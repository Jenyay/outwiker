#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from outwiker.core.pluginbase import Plugin


class PluginTestEmpty4(Plugin):
    def __init__(self, application):
        Plugin.__init__(self, application)

    @property
    def name(self):
        return u"TestEmpty4"

    @property
    def description(self):
        return _(u"This plugin is empty")

    def initialize(self):
        pass

    def destroy(self):
        pass
