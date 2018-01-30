# -*- coding: utf-8 -*-

from outwiker.core.pluginbase import Plugin

from .i18n import set_

from .autorenamer import AutoRenamer


class PluginAutoRenamer(Plugin):
    def __init__(self, application):
        Plugin.__init__(self, application)
        self._autorenamer = AutoRenamer(self, application)

    @property
    def name(self):
        return u"AutoRenamer"

    @property
    def description(self):
        description = _(
            u'''Plugin allows to rename all pages automatically using the first line of the page or automatically rename just those pages where you place (:autorename:) mark''')
        author = _(u'''<b>Author:</b> Vitalii Koshura (delionkur-lestat@mail.ru)''')
        return u"""{description}\n\n{author}""".format(description=description, author=author)

    @property
    def url(self):
        return u"https://github.com/AenBleidd/OutwikerPlugin"

    def initialize(self):
        set_(self.gettext)

        global _
        _ = self.gettext
        self._autorenamer.initialize()

    def destroy(self):
        self._autorenamer.destroy()
