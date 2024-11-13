# -*- coding: utf-8 -*-

import wx

from outwiker.gui.imagelistcache import ImageListCache


def test_empty():
    app = wx.App()
    wx.Log.SetLogLevel(0)

    defaultImage = 'testdata/images/new.png'
    cache = ImageListCache(defaultImage, 16, 16)

    imageList = cache.getImageList()
    assert imageList.GetImageCount() == 1
    assert cache.getDefaultImageId() == 0


def test_single():
    '''
    Add single image to empty ImageList
    '''
    app = wx.App()
    wx.Log.SetLogLevel(0)

    defaultImage = 'testdata/images/new.png'
    cache = ImageListCache(defaultImage, 16, 16)

    index = cache.add('testdata/images/16x16.png')

    imageList = cache.getImageList()
    assert index == 1
    assert imageList.GetImageCount() == 2


def test_error_not_exists():
    '''
    Try add file which not exists
    '''
    app = wx.App()
    wx.Log.SetLogLevel(0)

    defaultImage = 'testdata/images/new.png'
    cache = ImageListCache(defaultImage, 16, 16)

    index = cache.add('testdata/images/not_exists.png')

    imageList = cache.getImageList()
    assert index == 0
    assert imageList.GetImageCount() == 1


def test_error_invalid_file():
    '''
    Try add invalid file (not image)
    '''
    app = wx.App()
    wx.Log.SetLogLevel(0)

    defaultImage = 'testdata/images/new.png'
    cache = ImageListCache(defaultImage, 16, 16)

    index = cache.add('testdata/images/invalid.png')

    imageList = cache.getImageList()
    assert index == 0
    assert imageList.GetImageCount() == 1


def test_duplicate():
    '''
    Add duplicate image to empty ImageList
    '''
    app = wx.App()
    wx.Log.SetLogLevel(0)

    defaultImage = 'testdata/images/new.png'
    cache = ImageListCache(defaultImage, 16, 16)

    cache.add('testdata/images/16x16.png')
    index = cache.add('testdata/images/16x16.png')

    imageList = cache.getImageList()
    assert index == 1
    assert imageList.GetImageCount() == 2
