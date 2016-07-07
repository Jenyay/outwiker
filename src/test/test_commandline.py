# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.commandline import CommandLine, CommandLineException


class CommandLineTest(unittest.TestCase):
    def testEmpty(self):
        cl = CommandLine()
        cl.parseParams([])
        self.assertEqual(cl.wikipath, None)
        self.assertFalse(cl.help)
        self.assertFalse(cl.readonly)
        self.assertFalse(cl.version)


    def testSingle(self):
        path = "/tmp/wikipath"

        cl = CommandLine()
        cl.parseParams([path])
        self.assertEqual(cl.wikipath, path)


    def testOver(self):
        path = "/tmp/wikipath"
        cl = CommandLine()

        self.assertRaises(CommandLineException,
                          cl.parseParams,
                          [path, u"-abyrvalg"])


    def testHelp_01(self):
        cl = CommandLine()
        cl.parseParams(["-h"])
        self.assertTrue(cl.help)


    def testHelp_02(self):
        cl = CommandLine()
        cl.parseParams(["--help"])
        self.assertTrue(cl.help)


    def testReadOnly_01(self):
        cl = CommandLine()
        cl.parseParams(["--readonly"])

        self.assertTrue(cl.readonly)


    def testReadOnly_02(self):
        cl = CommandLine()
        cl.parseParams(["-r"])

        self.assertTrue(cl.readonly)


    def testVersion_01(self):
        cl = CommandLine()
        cl.parseParams(["--version"])

        self.assertTrue(cl.version)


    def testVersion_02(self):
        cl = CommandLine()
        cl.parseParams(["-v"])

        self.assertTrue(cl.version)
