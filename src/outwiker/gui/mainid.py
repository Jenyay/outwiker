#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import wx


class MainId (object):
    """
    Коллекция ID для меню и панели главного окна
    С появлением Actions эти константы становятся ненужными. В идеале от них нужно избавиться.
    """
    ID_VIEW_TREE = wx.NewId()
    ID_VIEW_ATTACHES = wx.NewId()
    ID_VIEW_TAGSCLOUD = wx.NewId()
    ID_VIEW_FULLSCREEN = wx.NewId()
    ID_UNDO = wx.ID_UNDO
    ID_REDO = wx.ID_REDO
    ID_CUT = wx.ID_CUT
    ID_COPY = wx.ID_COPY
    ID_PASTE = wx.ID_PASTE
