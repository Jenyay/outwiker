#!/usr/bin/python
# -*- coding: UTF-8 -*-

import unittest
import os.path

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application
from test.utils import removeWiki


class UpdateNotifierTest (unittest.TestCase):
    """Тесты плагина PluginName"""
    def setUp (self):
        self.__pluginname = u"UpdateNotifier"

        dirlist = [u"../plugins/updatenotifier"]

        self.loader = PluginsLoader(Application)
        self.loader.load (dirlist)


    def tearDown (self):
        self.loader.clear()


    def testPluginLoad (self):
        self.assertEqual ( len (self.loader), 1)


    def testExtractVersion_1 (self):
        text = u"""Бла-бла-бла 

<!--  #version  stable   1.2.3.456  --> 

Бла-бла-бла"""
        
        extractor = self.loader[self.__pluginname].VersionExtractor ()
        versions = extractor.getVersions (text)

        self.assertEqual (len (versions), 1)
        self.assertEqual (versions[u"stable"], u"1.2.3.456")


    def testExtractVersion_2 (self):
        text = u"""Бла-бла-бла 

<!--#version  unstable   1.2.3.456--> 

Бла-бла-бла"""
        
        extractor = self.loader[self.__pluginname].VersionExtractor ()
        versions = extractor.getVersions (text)

        self.assertEqual (len (versions), 1)
        self.assertEqual (versions[u"unstable"], u"1.2.3.456")


    def testExtractVersion_3 (self):
        text = u"""Бла-бла-бла 

<!--  #version  stable   1.2.3.456  --><!--  #version  unstable   2.3.4.567  --> 

Бла-бла-бла"""
        
        extractor = self.loader[self.__pluginname].VersionExtractor ()
        versions = extractor.getVersions (text)

        self.assertEqual (len (versions), 2)
        self.assertEqual (versions[u"stable"], u"1.2.3.456")
        self.assertEqual (versions[u"unstable"], u"2.3.4.567")


    def testExtractVersion_4 (self):
        text = u"""Бла-бла-бла 

<!--  #version  stable   1.2.3.456  -->

Еще раз бла-бла-бла

<!--  #version  unstable   2.3.4.567  --> 

Бла-бла-бла"""
        
        extractor = self.loader[self.__pluginname].VersionExtractor ()
        versions = extractor.getVersions (text)

        self.assertEqual (len (versions), 2)
        self.assertEqual (versions[u"stable"], u"1.2.3.456")
        self.assertEqual (versions[u"unstable"], u"2.3.4.567")


    def testExtractVersionEmpty_1 (self):
        text = u"""Бла-бла-бла Бла-бла-бла"""
        
        extractor = self.loader[self.__pluginname].VersionExtractor ()
        versions = extractor.getVersions (text)

        self.assertEqual (len (versions), 0)


    def testExtractVersionEmpty_2 (self):
        text = u"""Бла-бла-бла 
        <!--  #version  1.2.3.456  -->
        
        Бла-бла-бла"""
        
        extractor = self.loader[self.__pluginname].VersionExtractor ()
        versions = extractor.getVersions (text)

        self.assertEqual (len (versions), 0)


    def testExtractVersionEmpty_3 (self):
        text = u"""Бла-бла-бла 
        <!--  #version  stable  -->
        
        Бла-бла-бла"""
        
        extractor = self.loader[self.__pluginname].VersionExtractor ()
        versions = extractor.getVersions (text)

        self.assertEqual (len (versions), 0)


    def testExtractVersionEmpty_4 (self):
        text = u"""Бла-бла-бла 
        <!--  #version  -->
        
        Бла-бла-бла"""
        
        extractor = self.loader[self.__pluginname].VersionExtractor ()
        versions = extractor.getVersions (text)

        self.assertEqual (len (versions), 0)


    def testExtractVersionEmpty_5 (self):
        text = u"""Бла-бла-бла 
        <!--  unstable   2.3.4.567  -->
        
        Бла-бла-бла"""
        
        extractor = self.loader[self.__pluginname].VersionExtractor ()
        versions = extractor.getVersions (text)

        self.assertEqual (len (versions), 0)
