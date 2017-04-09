# -*- coding: UTF-8 -*-

import wx

from outwiker.core.events import PageDialogPageFactoriesNeededParams

from config import PageTypeColorConfig


class ColorsList(object):
    def __init__(self, application):
        '''
        defaultColor is a string when describes a color.
        '''
        self._application = application
        self._defaultColor = wx.Colour().SetFromString('white')
        self._colors = {}

    def load(self):
        config = PageTypeColorConfig(self._application.config)

        self._colors = {
            u'wiki': config.wikiColor.value,
            u'html': config.htmlColor.value,
            u'text': config.textColor.value,
            u'search': config.searchColor.value,
        }

        eventParams = PageDialogPageFactoriesNeededParams(None, None)
        self._application.onPageDialogPageFactoriesNeeded(None, eventParams)

        for factory in eventParams.pageFactories:
            typeString = factory.getTypeString()

            if typeString not in self._colors:
                color = 'blue'
                self._colors[typeString] = color
                config.config.set(config.SECTION, typeString, color)
                config.config.save()

    def getColor(self, pageTypeString):
        return self._colors.get(pageTypeString, self._defaultColor)
