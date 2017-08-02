# -*- coding: utf-8 -*-

from outwiker.core.pluginbase import Plugin


class PluginFirst(Plugin):
    def __init__(self, application):
        super(PluginFirst, self).__init__(application)

    #########################################
    # Properties and methods to overloading #
    #########################################

    @property
    def name(self):
        return u"FirstPlugin"

    @property
    def description(self):
        return _(u"My first plugin")

    def initialize(self):
        pass

    def destroy(self):
        pass
