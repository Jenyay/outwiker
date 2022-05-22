# -*- coding: utf-8 -*-

import unittest

from outwiker.core.commandline import CommandLine, CommandLineException


class CommandLineTest(unittest.TestCase):
    def test_Empty(self):
        cl = CommandLine()
        cl.parseParams([])
        self.assertEqual(cl.wikipath, None)
        self.assertFalse(cl.help)
        self.assertFalse(cl.readonly)
        self.assertFalse(cl.version)

    def test_Single(self):
        path = '/tmp/wikipath'

        cl = CommandLine()
        cl.parseParams([path])
        self.assertEqual(cl.wikipath, path)

    def test_Over(self):
        path = '/tmp/wikipath'
        cl = CommandLine()

        self.assertRaises(CommandLineException,
                          cl.parseParams,
                          [path, '-abyrvalg'])

    def test_Help_01(self):
        cl = CommandLine()
        cl.parseParams(['-h'])
        self.assertTrue(cl.help)

    def test_Help_02(self):
        cl = CommandLine()
        cl.parseParams(['--help'])
        self.assertTrue(cl.help)

    def test_ReadOnly_01(self):
        cl = CommandLine()
        cl.parseParams(['--readonly'])

        self.assertTrue(cl.readonly)

    def test_ReadOnly_02(self):
        cl = CommandLine()
        cl.parseParams(['-r'])

        self.assertTrue(cl.readonly)

    def test_Version_01(self):
        cl = CommandLine()
        cl.parseParams(['--version'])

        self.assertTrue(cl.version)

    def test_Version_02(self):
        cl = CommandLine()
        cl.parseParams(['-v'])

        self.assertTrue(cl.version)

    def test_PageId_01(self):
        cl = CommandLine()
        cl.parseParams(['--page=Page 1'])

        self.assertEqual(cl.page_id, 'Page 1')

    def test_PageId_02(self):
        cl = CommandLine()
        cl.parseParams(['-p', 'Page 1'])

        self.assertEqual(cl.page_id, 'Page 1')

    def test_PageId_03(self):
        cl = CommandLine()
        cl.parseParams([])

        self.assertIsNone(cl.page_id)
