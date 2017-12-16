# -*- coding: UTF-8 -*-

import unittest
import os
import os.path

from outwiker.gui.hotkeyoption import HotKeyOption
from outwiker.gui.hotkey import HotKey
from outwiker.core.config import Config


class HotKeyConfigTest(unittest.TestCase):
    """Тесты, связанные с сохранением горячих клавиш в настройках"""

    def setUp(self):
        self.path = "../test/testconfig.ini"

        if os.path.exists(self.path):
            os.remove(self.path)


    def tearDown(self):
        if os.path.exists(self.path):
            os.remove(self.path)


    def testHotKeyOptionEmptyConfig(self):
        config = Config(self.path)
        hotKeyDefault = HotKey("F11", ctrl=True)
        section = "TestHotKey"
        paramName = "MyHotKey"

        option = HotKeyOption(config, section, paramName, hotKeyDefault)
        self.assertEqual(option.value, hotKeyDefault)


    def testReadOption1(self):
        with open(self.path, "w") as fp:
            fp.write("""[TestHotKey]
MyHotKey=Ctrl+T""")

        config = Config(self.path)
        section = "TestHotKey"
        paramName = "MyHotKey"

        option = HotKeyOption(config, section, paramName, None)
        result = option.value

        self.assertNotEqual(result, None)
        self.assertEqual(result.key, "T")
        self.assertTrue(result.ctrl)
        self.assertFalse(result.alt)
        self.assertFalse(result.shift)


    def testReadOption2(self):
        with open(self.path, "w") as fp:
            fp.write("""[TestHotKey]
MyHotKey = Ctrl + F11

""")

        config = Config(self.path)
        section = "TestHotKey"
        paramName = "MyHotKey"

        option = HotKeyOption(config, section, paramName, None)
        result = option.value

        self.assertNotEqual(result, None)
        self.assertEqual(result.key, "F11")
        self.assertTrue(result.ctrl)
        self.assertFalse(result.alt)
        self.assertFalse(result.shift)


    def testReadOption3(self):
        with open(self.path, "w") as fp:
            fp.write("""[TestHotKey]
MyHotKey=Ctrl+""")

        config = Config(self.path)
        section = "TestHotKey"
        paramName = "MyHotKey"

        option = HotKeyOption(config, section, paramName, None)
        result = option.value

        self.assertEqual(result, None)


    def testReadOption4(self):
        with open(self.path, "w") as fp:
            fp.write("""[TestHotKey]
MyHotKey=Ctrl+DEL""")

        config = Config(self.path)
        section = "TestHotKey"
        paramName = "MyHotKey2"
        hotKeyDefault = HotKey("F11", ctrl=True)

        option = HotKeyOption(config, section, paramName, hotKeyDefault)
        result = option.value

        self.assertEqual(result, hotKeyDefault)


    def testHotKeyWrite1(self):
        config = Config(self.path)
        hotkey = HotKey("F11", ctrl=True)
        section = "TestHotKey"
        paramName = "MyHotKey"

        option = HotKeyOption(config, section, paramName, None)
        option.value = hotkey

        with open(self.path) as fp:
            resultFile = fp.read()

        self.assertTrue("[TestHotKey]" in resultFile)
        self.assertTrue("myhotkey = Ctrl+F11" in resultFile)


    def testHotKeyWrite2(self):
        config = Config(self.path)
        section = "TestHotKey"
        paramName = "MyHotKey"

        option = HotKeyOption(config, section, paramName, None)
        option.value = None

        with open(self.path) as fp:
            resultFile = fp.read()

        self.assertTrue("[TestHotKey]" in resultFile)
        self.assertTrue("myhotkey =" in resultFile)
