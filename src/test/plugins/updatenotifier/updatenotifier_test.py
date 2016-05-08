# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.pluginsloader import PluginsLoader
from outwiker.core.application import Application
from outwiker.core.version import Version


class UpdateNotifierTest (unittest.TestCase):
    """Тесты плагина UpdateNotifier"""
    def setUp (self):
        self.loader = PluginsLoader(Application)
        self.loader.load ([u"../plugins/updatenotifier"])


    def tearDown (self):
        self.loader.clear()


    def testPluginLoad (self):
        self.assertEqual (len (self.loader), 1)


    def testExtractVersion_1 (self):
        from updatenotifier.versionextractor import extractVersion

        text = u"""Бла-бла-бла 

<!--  #version  stable   1.2.3.456  --> 

Бла-бла-бла"""

        versions = extractVersion (text)

        self.assertEqual (len (versions), 1)
        self.assertEqual (versions[u"stable"], u"1.2.3.456")


    def testExtractVersion_2 (self):
        from updatenotifier.versionextractor import extractVersion

        text = u"""Бла-бла-бла 

<!--#version  unstable   1.2.3.456--> 

Бла-бла-бла"""

        versions = extractVersion (text)

        self.assertEqual (len (versions), 1)
        self.assertEqual (versions[u"unstable"], u"1.2.3.456")


    def testExtractVersion_3 (self):
        from updatenotifier.versionextractor import extractVersion

        text = u"""Бла-бла-бла 

<!--  #version  stable   1.2.3.456  --><!--  #version  unstable   2.3.4.567  --> 

Бла-бла-бла"""

        versions = extractVersion (text)

        self.assertEqual (len (versions), 2)
        self.assertEqual (versions[u"stable"], u"1.2.3.456")
        self.assertEqual (versions[u"unstable"], u"2.3.4.567")


    def testExtractVersion_4 (self):
        from updatenotifier.versionextractor import extractVersion

        text = u"""Бла-бла-бла 

<!--  #version  stable   1.2.3.456  -->

Еще раз бла-бла-бла

<!--  #version  unstable   2.3.4.567  --> 

Бла-бла-бла"""

        versions = extractVersion (text)

        self.assertEqual (len (versions), 2)
        self.assertEqual (versions[u"stable"], u"1.2.3.456")
        self.assertEqual (versions[u"unstable"], u"2.3.4.567")


    def testExtractVersion_5 (self):
        from updatenotifier.versionextractor import extractVersion

        text = u"""Бла-бла-бла 

<!--  #version  stable   1.2.3  --> 

Бла-бла-бла"""

        versions = extractVersion (text)

        self.assertEqual (len (versions), 1)
        self.assertEqual (versions[u"stable"], u"1.2.3")


    def testExtractVersion_6 (self):
        from updatenotifier.versionextractor import extractVersion

        text = u"""Бла-бла-бла 

<!--  #version  stable   1.2  --> 

Бла-бла-бла"""

        versions = extractVersion (text)

        self.assertEqual (len (versions), 1)
        self.assertEqual (versions[u"stable"], u"1.2")


    def testExtractVersion_7 (self):
        from updatenotifier.versionextractor import extractVersion

        text = u"""Бла-бла-бла 

<!--  #version  stable   1  --> 

Бла-бла-бла"""

        versions = extractVersion (text)

        self.assertEqual (len (versions), 1)
        self.assertEqual (versions[u"stable"], u"1")


    def testExtractVersionEmpty_1 (self):
        from updatenotifier.versionextractor import extractVersion

        text = u"""Бла-бла-бла Бла-бла-бла"""

        versions = extractVersion (text)

        self.assertEqual (len (versions), 0)


    def testExtractVersionEmpty_2 (self):
        from updatenotifier.versionextractor import extractVersion

        text = u"""Бла-бла-бла 
        <!--  #version  1.2.3.456  -->
        
        Бла-бла-бла"""

        versions = extractVersion (text)

        self.assertEqual (len (versions), 0)


    def testExtractVersionEmpty_3 (self):
        from updatenotifier.versionextractor import extractVersion

        text = u"""Бла-бла-бла 
        <!--  #version  stable  -->
        
        Бла-бла-бла"""

        versions = extractVersion (text)

        self.assertEqual (len (versions), 0)


    def testExtractVersionEmpty_4 (self):
        from updatenotifier.versionextractor import extractVersion

        text = u"""Бла-бла-бла 
        <!--  #version  -->
        
        Бла-бла-бла"""

        versions = extractVersion (text)

        self.assertEqual (len (versions), 0)


    def testExtractVersionEmpty_5 (self):
        from updatenotifier.versionextractor import extractVersion

        text = u"""Бла-бла-бла 
        <!--  unstable   2.3.4.567  -->
        
        Бла-бла-бла"""

        versions = extractVersion (text)

        self.assertEqual (len (versions), 0)


    def testVersionList_1 (self):
        from updatenotifier.versionlist import VersionList

        self.loader.load ([
            u"../plugins/updatenotifier",
            u"../plugins/testdebug"
        ])

        self.assertEqual ( len (self.loader), 2)

        verlist = VersionList (self.loader)

        # Без обновления все версии равны None
        self.assertTrue (verlist.getPluginVersion (u"Debug Plugin") == None)
        self.assertTrue (verlist.getPluginVersion (u"UpdateNotifier") == None)

        self.assertTrue (verlist.stableVersion == None)
        self.assertTrue (verlist.unstableVersion == None)

        verlist.updateVersions()

        self.assertTrue (verlist.getPluginVersion (u"Debug Plugin") == Version (0, 6))
        self.assertTrue (verlist.stableVersion == Version (1, 9), verlist.stableVersion)


    def testVersionList_2 (self):
        from updatenotifier.versionlist import VersionList

        self.loader.load ([
            u"../plugins/updatenotifier",
            u"../plugins/testdebug"
        ])

        self.assertEqual ( len (self.loader), 2)

        self.loader[u"Debug Plugin"].url = u"http://jenyay.net/invalid"

        verlist = VersionList (self.loader)

        verlist.updateVersions()
        self.assertTrue (verlist.getPluginVersion (u"Debug Plugin") == None)


    def testVersionList_3 (self):
        from updatenotifier.versionlist import VersionList

        self.loader.load ([
            u"../plugins/updatenotifier",
            u"../plugins/testdebug"
        ])

        self.assertEqual ( len (self.loader), 2)

        self.loader[u"Debug Plugin"].url = u"invalid"

        verlist = VersionList (self.loader)

        verlist.updateVersions()
        self.assertTrue (verlist.getPluginVersion (u"Debug Plugin") == None)


    def testVersionListDisconnected (self):
        from updatenotifier.versionlist import VersionList
        import updatenotifier.loaders

        self.loader.load ([
            u"../plugins/updatenotifier",
            u"../plugins/testdebug"
        ])

        self.assertEqual ( len (self.loader), 2)

        self.loader[u"Debug Plugin"].url = u"invalid"

        verlist = VersionList (self.loader)
        verlist.setLoader (updatenotifier.loaders.DisconnectedLoader())

        verlist.updateVersions()
        self.assertEqual (verlist.stableVersion, None)
        self.assertEqual (verlist.unstableVersion, None)
        self.assertEqual (verlist.getPluginVersion (u"Debug Plugin"), None)
