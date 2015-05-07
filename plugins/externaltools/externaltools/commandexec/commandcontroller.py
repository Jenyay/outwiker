# -*- coding: UTF-8 -*-

import urlparse
import subprocess
from StringIO import StringIO

import wx

from outwiker.core.system import getOS
from outwiker.core.commands import MessageBox

from externaltools.commandexec.commandexec import CommandExec
from externaltools.commandexec.commandparams import EXEC_BEGIN, PROTO_COMMAND
from externaltools.commandexec.execinfo import ExecInfo
from externaltools.commandexec.guicreator import GuiCreator
from externaltools.config import ExternalToolsConfig


class CommandController (object):
    def __init__ (self, application):
        self._application = application

        # Enable (:exec:) command only in the "new" OutWiker version.
        # If Application has onLinkClick event
        self._enableExecCommand = u'onLinkClick' in dir (self._application)

        self._guiCreator = None


    def initialize (self):
        if self._enableExecCommand:
            self._application.onWikiParserPrepare += self.__onWikiParserPrepare
            self._application.onHoverLink += self._onHoverLink
            self._application.onLinkClick += self._onLinkClick
            self._application.onPageViewCreate += self.__onPageViewCreate
            self._application.onPageViewDestroy += self.__onPageViewDestroy

            self._guiCreator = GuiCreator (self._application)
            self._guiCreator.initialize()

            if self._isCurrentWikiPage:
                self.__onPageViewCreate (self._application.selectedPage)


    def destroy (self):
        if self._enableExecCommand:
            self._application.onWikiParserPrepare -= self.__onWikiParserPrepare
            self._application.onHoverLink -= self._onHoverLink
            self._application.onLinkClick -= self._onLinkClick
            self._application.onPageViewCreate -= self.__onPageViewCreate
            self._application.onPageViewDestroy -= self.__onPageViewDestroy

            if self._isCurrentWikiPage:
                self._guiCreator.removeTools()

            self._guiCreator.destroy ()


    def __onPageViewCreate(self, page):
        """Обработка события после создания представления страницы"""
        assert self._application.mainWindow is not None

        if page.getTypeString() == u"wiki":
            self._guiCreator.createTools()


    def __onPageViewDestroy (self, page):
        """
        Обработка события перед удалением вида страницы
        """
        assert self._application.mainWindow is not None

        if page.getTypeString() == u"wiki":
            self._guiCreator.removeTools()


    def _getPageView (self):
        """
        Получить указатель на панель представления страницы
        """
        return self._application.mainWindow.pagePanel.pageView


    @property
    def _isCurrentWikiPage (self):
        """
        Возвращает True, если текущая страница - это викистраница, и False в противном случае
        """
        return (self._application.selectedPage is not None and
                self._application.selectedPage.getTypeString() == u"wiki")


    def __onWikiParserPrepare (self, parser):
        """
        Teh event occures before parsing. Add the (:exec:) command
        """
        parser.addCommand (CommandExec (parser))


    def _getParams (self, url):
        """
        Return dictionary with params from url.
        Every value in dictionary is list
        """
        if (url is None or
                not url.startswith (EXEC_BEGIN)):
            return {}

        startpos = url.find (u'?')

        if startpos == -1 or startpos == len (url) - 1:
            return {}

        params = url[startpos + 1:]

        try:
            paramsDict = urlparse.parse_qs (str (params))
        except ValueError:
            return {}

        return paramsDict


    def _onHoverLink (self, page, params):
        if params.link is None:
            return

        urlparams = self._getParams (params.link)
        if not urlparams:
            return

        commands = self.getCommandsList (urlparams)

        if commands:
            params.text = self.getStatusTitle (commands)


    def getStatusTitle (self, commands):
        """
        command - instance of the ExecInfo class
        """
        assert commands

        buf = StringIO()
        buf.write (u'>>> ')
        buf.write (self._getParamText (commands[0].command))

        for param in commands[0].params:
            buf.write (u' ')
            buf.write (self._getParamText (param))

        if len (commands) > 1:
            buf.write (u' ...')

        return buf.getvalue()


    def _getParamText (self, param):
        """
        Quote param if it contain a space
        """
        return u'"{}"'.format (param) if u' ' in param else param


    def _onLinkClick (self, page, params):
        if params.link is None:
            return

        urlparams = self._getParams (params.link)
        if not urlparams:
            return

        params.process = True

        commands = self.getCommandsList (urlparams)

        config = ExternalToolsConfig (self._application.config)

        if len (commands) > 1:
            message = _(u'Run applications by ExternalTools plugin?\nIt may be unsafe.')
        else:
            message = _(u'Run application by ExternalTools plugin?\nIt may be unsafe.')

        if (config.execWarning and
                MessageBox (
                    message,
                    _(u'ExternalTools'),
                    wx.YES_NO | wx.ICON_QUESTION | wx.NO_DEFAULT
                ) != wx.YES):
            return

        for command in commands:
            self._execute (command.command, command.params)


    def getCommandsList (self, urlparams):
        """
        Return list of the ExecInfo. Macros will be replaced in params
        urlparams is dictionary with params from url.
        """
        result = []

        comindex = 1
        comparams = PROTO_COMMAND.format (number = comindex)

        encoding = getOS().filesEncoding

        while comparams in urlparams:
            command = unicode (urlparams[comparams][0], "utf8").encode (encoding)
            params = [unicode (param, "utf8").encode (encoding)
                      for param
                      in urlparams[comparams][1:]]

            result.append (ExecInfo (command, params))

            comindex += 1
            comparams = PROTO_COMMAND.format (number = comindex)

        return result



    def _execute (self, command, params):
        try:
            subprocess.Popen ([command] + params)
        except (OSError, subprocess.CalledProcessError):
            pass
