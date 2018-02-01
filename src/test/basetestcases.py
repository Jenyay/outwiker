# -*- coding: utf-8 -*-

import unittest

import wx


class BaseWxTestCase(unittest.TestCase):
    def myYield(self, eventsToProcess=wx.EVT_CATEGORY_ALL):
        """
        Since the tests are usually run before MainLoop is called then we
        need to make our own EventLoop for Yield to actually do anything
        useful.

        The method taken from wxPython tests.
        """
        evtLoop = self._wxapp.GetTraits().CreateEventLoop()
        activator = wx.EventLoopActivator(evtLoop)
        evtLoop.YieldFor(eventsToProcess)

    def setUp(self):
        self._wxapp = wx.App()

    def tearDown(self):
        self._wxapp.MainLoop()
        del self._wxapp
