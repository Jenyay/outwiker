# -*- coding=utf-8 -*-

import os.path

from outwiker.core.config import StringListSection
from outwiker.core.iconcontroller import IconController
from outwiker.core.defines import RECENT_ICONS_SECTION, RECENT_ICONS_PARAM_NAME


class RecentIconsList(object):
    '''
    Class to keep recent used icons in the config file.
    '''
    def __init__(self, maxcount, config, builtin_icons_path):
        self._maxcount = maxcount
        self._config = config
        self._builtin_icons_path = builtin_icons_path

        self._recentIconsConfig = StringListSection(self._config,
                                                    RECENT_ICONS_SECTION,
                                                    RECENT_ICONS_PARAM_NAME)
        self._recentIcons = []

    def getRecentIcons(self):
        return self._recentIcons[:]

    def load(self):
        self._recentIcons = []
        for icon_path in self._recentIconsConfig.value:
            if os.path.exists(icon_path):
                self._recentIcons.append(icon_path)
                continue

            icon_path = os.path.join(self._builtin_icons_path, icon_path)
            if os.path.exists(icon_path):
                self._recentIcons.append(icon_path)

        return self.getRecentIcons()

    def add(self, icon_path):
        icon_path = os.path.abspath(icon_path)

        # Remove duplicate icon
        if icon_path in self._recentIcons:
            self._recentIcons.remove(icon_path)

        self._recentIcons.insert(0, icon_path)
        self._recentIcons = self._recentIcons[0: self._maxcount]
        self._save()

    def _save(self):
        iconController = IconController(self._builtin_icons_path)
        icons_for_config = []

        for icon in self._recentIcons:
            if iconController.is_builtin_icon(icon):
                icon = os.path.relpath(icon, self._builtin_icons_path)

            icons_for_config.append(icon)

        self._recentIconsConfig.value = icons_for_config