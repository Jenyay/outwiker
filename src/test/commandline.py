# -*- coding: UTF-8 -*-

import unittest

from outwiker.core.commandline import CommandLine, CommandLineException


class CommandLineTest (unittest.TestCase):
    def testEmpty (self):
        cl = CommandLine ([])
        self.assertEqual (cl.wikipath, None)
        self.assertEqual (cl.help, False)


    def testSingle (self):
        path = u"/tmp/Путь до вики"

        cl = CommandLine ([path])
        self.assertEqual (cl.wikipath, path)


    def testOver (self):
        path = u"/tmp/Путь до вики"

        self.assertRaises (CommandLineException, CommandLine, [path, u"-abyrvalg"])


    def testHelp_01 (self):
        cl = CommandLine (["-h"])
        self.assertTrue (cl.help)


    def testHelp_02 (self):
        cl = CommandLine (["--help"])
        self.assertTrue (cl.help)
