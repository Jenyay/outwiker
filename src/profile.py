#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cProfile
import pstats

import wx

from outwiker.core.application import Application
from runoutwiker import OutWiker

def wikiparserProfile ():
    import profiles.pro_parser

    fname = "profiles/test2.wiki"
    profile_fname = "../test/wikiparser.profile"

    global pparser
    pparser = profiles.pro_parser.ParseSample (fname)

    #pparser.run()
    cProfile.run('pparser.run()', profile_fname)

    stats = pstats.Stats(profile_fname)
    stats.strip_dirs().sort_stats('cumulative').print_stats(10)


def outwikerProfile ():
    global outwiker
    outwiker = OutWiker(0)
    profile_fname = "../test/outwiker.profile"

    cProfile.run('outwiker.MainLoop()', profile_fname)

    stats = pstats.Stats(profile_fname)
    #stats.strip_dirs().sort_stats('calls').print_stats(30)
    stats.strip_dirs().sort_stats('time').print_stats(100)


if __name__ == "__main__":
    Application.init ("../test/testconfig.ini")

    class testApp(wx.App):
        def __init__(self, *args, **kwds):
            wx.App.__init__ (self, *args, **kwds)

    app = testApp(redirect=False)

    #wikiparserProfile()
    outwikerProfile ()
