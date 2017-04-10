# -*- coding: UTF-8 -*-

from outwiker.core.events import PageDialogPageFactoriesNeededParams
from outwiker.core.config import StringOption

from config import PageTypeColorConfig


class ColorsList(object):
    def __init__(self, application):
        self._application = application
        self._defaultColor = 'white'
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
                color_param = StringOption(self._application.config,
                                           PageTypeColorConfig.SECTION,
                                           typeString,
                                           None)

                if color_param.value is None:
                    color = self._getNewColor()
                    self._colors[typeString] = color
                    config.config.set(config.SECTION, typeString, color)
                    config.config.save()
                else:
                    self._colors[typeString] = color_param.value

    def _getNewColor(self):
        color = 'white'
        return color

    def getColor(self, pageTypeString):
        return self._colors.get(pageTypeString, self._defaultColor)

    def getPageTypes(self):
        return self._colors.keys()
