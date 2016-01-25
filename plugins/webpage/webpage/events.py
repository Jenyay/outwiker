# -*- coding: UTF-8 -*-

import wx.lib.newevent


UpdateLogEvent, EVT_UPDATE_LOG = wx.lib.newevent.NewEvent()
ErrorDownloadEvent, EVT_DOWNLOAD_ERROR = wx.lib.newevent.NewEvent()
FinishDownloadEvent, EVT_DOWNLOAD_FINISH = wx.lib.newevent.NewEvent()


class PrepareHtmlEventParams (object):
    """Used for 'WebPage_onPrepareHtml' event"""
    def __init__ (self, page, soup):
        """
        page - current page;
        soup - BeaufullSoup instance
        """
        self.page = page
        self.soup = soup
