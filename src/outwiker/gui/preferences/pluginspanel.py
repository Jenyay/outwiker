# -*- coding: utf-8 -*-

import wx
import wx.adv
import logging

from outwiker.core.application import Application
from outwiker.gui.guiconfig import PluginsConfig
from outwiker.core.system import getCurrentDir, getOS
from outwiker.gui.preferences.baseprefpanel import BasePrefPanel


logger = logging.getLogger('pluginspanel')


class PluginsPanel (BasePrefPanel):
    """
    Панель со списком установленных плагинов
    """
    def __init__(self, parent):
        super(PluginsPanel, self).__init__(parent)
        self.__htmlMinWidth = 150

        self.__createGui()
        self.__controller = PluginsController(self)
        self.SetupScrolling()

    def __createGui(self):
        self.pluginsList = wx.CheckListBox(self, -1, style=wx.LB_SORT)
        self.pluginsList.SetMinSize((50, 20))

        self.__downloadLink = wx.adv.HyperlinkCtrl(
            self,
            -1,
            _(u"Download more plugins"),
            _(u"http://jenyay.net/Outwiker/PluginsEn"))

        # Панель, которая потом заменится на HTML-рендер
        self.__blankPanel = wx.Panel(self)
        self.__blankPanel.SetMinSize((self.__htmlMinWidth, -1))

        self.__pluginsInfo = None

        self.__layout()

    @property
    def pluginsInfo(self):
        if self.__pluginsInfo is None:
            # Удалим пустую панель, а вместо нее добавим HTML-рендер
            self.pluginsSizer.Detach(self.__blankPanel)
            self.__blankPanel.Destroy()

            self.__pluginsInfo = getOS().getHtmlRender(self)
            self.__pluginsInfo.SetMinSize((self.__htmlMinWidth, -1))

            self.pluginsSizer.Insert(1, self.__pluginsInfo, flag=wx.EXPAND)
            self.Layout()

        return self.__pluginsInfo

    def __layout(self):
        self.mainSizer = wx.FlexGridSizer(cols=1)
        self.mainSizer.AddGrowableRow(0)
        self.mainSizer.AddGrowableCol(0)

        self.pluginsSizer = wx.FlexGridSizer(cols=2)
        self.pluginsSizer.AddGrowableRow(0)
        self.pluginsSizer.AddGrowableCol(0)
        self.pluginsSizer.AddGrowableCol(1)
        self.pluginsSizer.Add(self.pluginsList, flag=wx.EXPAND)
        self.pluginsSizer.Add(self.__blankPanel, flag=wx.EXPAND)

        self.mainSizer.Add(self.pluginsSizer,
                           flag=wx.ALL | wx.EXPAND,
                           border=2)
        self.mainSizer.Add(self.__downloadLink,
                           flag=wx.ALL | wx.ALIGN_LEFT,
                           border=2)

        self.SetSizer(self.mainSizer)

    def LoadState(self):
        self.__controller.loadState()

    def Save(self):
        self.__controller.save()


class PluginsController (object):
    """
    Контроллер, отвечающий за работу панели со списком плагинов
    """
    def __init__(self, pluginspanel):
        self.__owner = pluginspanel

        # Т.к. под виндой к элементам CheckListBox нельзя
        # прикреплять пользовательские данные,
        # придется их хранить отдельно.
        # Ключ - имя плагина, оно же текст строки
        # Значение - экземпляр плагина
        self.__pluginsItems = {}

        self.__owner.Bind(wx.EVT_LISTBOX,
                          self.__onSelectItem,
                          self.__owner.pluginsList)

    def __onSelectItem(self, event):
        htmlContent = u""
        if event.IsSelection():
            plugin = self.__pluginsItems[event.GetString()]
            assert plugin is not None

            htmlContent = self.__createPluginInfo(plugin)

        self.__owner.pluginsInfo.SetPage(htmlContent, getCurrentDir())

    def __createPluginInfo(self, plugin):
        assert plugin is not None

        infoTemplate = u"""<html>
<head>
    <meta http-equiv='content-type' content='text/html; charset=utf-8'/>
</head>

<body>
{name}<br>
{version}<br>
{url}<br>
{description}<br>
</body>
</html>"""

        plugin_name = u"""<h3>{name}</h3>""".format(name=plugin.name)

        plugin_version = u"""<b>{version_header}:</b> {version}""".format(
            version_header=_(u"Version"),
            version=plugin.version)

        plugin_description = u"""<b>{description_head}:</b> {description}""".format(
            description_head=_(u"Description"),
            description=plugin.description.replace("\n", "<br>"))

        if plugin.url is not None:
            plugin_url = u"""<br><b>{site_head}</b>: <a href="{url}">{url}</a><br>""".format(
                site_head=_("Site"),
                url=plugin.url)
        else:
            plugin_url = u""

        result = infoTemplate.format(
            name=plugin_name,
            version=plugin_version,
            description=plugin_description,
            url=plugin_url)

        return result

    def loadState(self):
        self.__pluginsItems = {}
        self.__owner.pluginsList.Clear()
        self.__appendEnabledPlugins()
        self.__appendDisabledPlugins()
        self.__appendInvalidPlugins()

    def __appendEnabledPlugins(self):
        """
        Добавить загруженные плагины в список
        """
        for plugin in Application.plugins:
            index = self.__owner.pluginsList.Append(plugin.name)

            assert plugin.name not in self.__pluginsItems
            self.__pluginsItems[plugin.name] = plugin

            self.__owner.pluginsList.Check(index, True)

    def __appendDisabledPlugins(self):
        """
        Добавить отключенные плагины в список
        """
        for plugin in Application.plugins.disabledPlugins.values():
            index = self.__owner.pluginsList.Append(plugin.name)

            assert plugin.name not in self.__pluginsItems
            self.__pluginsItems[plugin.name] = plugin

            self.__owner.pluginsList.Check(index, False)

    def __appendInvalidPlugins(self):
        for plugin in Application.plugins.invalidPlugins:
            index = self.__owner.pluginsList.Append(plugin.name)

            self.__pluginsItems[plugin.name] = plugin
            self.__owner.pluginsList.Check(index, False)

    def save(self):
        config = PluginsConfig(Application.config)
        config.disabledPlugins.value = self.__getDisabledPlugins()
        Application.plugins.updateDisableList()

    def __getDisabledPlugins(self):
        disabledList = []

        for itemindex in range(self.__owner.pluginsList.GetCount()):
            if not self.__owner.pluginsList.IsChecked(itemindex):
                disabledList.append(self.__pluginsItems[self.__owner.pluginsList.GetString(itemindex)].name)

        return disabledList
