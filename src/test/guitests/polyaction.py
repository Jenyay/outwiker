#!/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest

import wx

from outwiker.gui.polyaction import PolyAction
from outwiker.gui.wxactioncontroller import WxActionController
from outwiker.gui.hotkey import HotKey
from outwiker.core.application import Application
from basemainwnd import BaseMainWndTest


class PolyActionTest (BaseMainWndTest):
    """Тестирование класса PolyAction"""
    def setUp (self):
        BaseMainWndTest.setUp (self)
        self.actionController = WxActionController(self.wnd, Application.config)
        Application.config.remove_section (self.actionController.configSection)

        self._actionVal = 0


    def tearDown (self):
        BaseMainWndTest.tearDown (self)
        Application.config.remove_section (self.actionController.configSection)


    def _addActionVal (self, params):
        self._actionVal += 1


    def _addActionVal2 (self, params):
        self._actionVal += 2


    def _addParams (self, param):
        self._actionVal += param


    def testEmpty (self):
        strid = "test_id"
        title = u"title"
        description = u"description"
        hotkey = HotKey ("F1")

        polyaction = PolyAction (Application, strid, title, description)
        self.actionController.register (polyaction, hotkey)

        self.assertEqual (self.actionController.getAction (strid).title, title)
        self.assertEqual (self.actionController.getAction (strid).description, description)
        
        polyaction.run (None)


    def testPolymorph (self):
        strid = "test_id"
        title = u"title"
        description = u"description"
        polyaction = PolyAction (Application, strid, title, description)

        polyaction.run(None)
        self.assertEqual (self._actionVal, 0)

        polyaction.setFunc (self._addActionVal)
        polyaction.run(None)
        self.assertEqual (self._actionVal, 1)

        polyaction.run(None)
        self.assertEqual (self._actionVal, 2)

        self._actionVal = 0
        polyaction.setFunc (self._addActionVal2)
        polyaction.run (0)
        self.assertEqual (self._actionVal, 2)

        polyaction.setFunc (None)
        polyaction.run (0)
        self.assertEqual (self._actionVal, 2)


    def testPolymorphParam1 (self):
        strid = "test_id"
        title = u"title"
        description = u"description"
        polyaction = PolyAction (Application, strid, title, description)

        polyaction.run(None)
        self.assertEqual (self._actionVal, 0)

        polyaction.setFunc (self._addParams)
        polyaction.run (5)
        self.assertEqual (self._actionVal, 5)


    def testPolymorphParam2 (self):
        strid = "test_id"
        title = u"title"
        description = u"description"
        polyaction = PolyAction (Application, strid, title, description)
        self.actionController.register (polyaction, None)

        self.actionController.getAction(strid).run(None)
        self.assertEqual (self._actionVal, 0)

        self.actionController.getAction(strid).setFunc (self._addParams)
        self.actionController.getAction(strid).run (5)
        self.assertEqual (self._actionVal, 5)
