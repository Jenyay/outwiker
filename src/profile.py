#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cProfile
import pstats

import wx

from outwiker.core.application import Application
from runoutwiker import OutWiker

def wikiparserProfile ():
    from profiles import pro_parser

    # fname = "../profiles/test2.wiki"
    fname = "../profiles/text_gogol.wiki"
    profile_fname = "../profiles/wikiparser.profile"

    global pparser
    pparser = pro_parser.ParseSample (fname)

    #pparser.run()
    cProfile.run('pparser.run()', profile_fname)

    stats = pstats.Stats(profile_fname)
    stats.strip_dirs().sort_stats('time').print_stats(30)


def outwikerProfile ():
    global outwiker
    outwiker = OutWiker(0)
    profile_fname = "../profiles/outwiker.profile"

    cProfile.run('outwiker.MainLoop()', profile_fname)

    stats = pstats.Stats(profile_fname)
    #stats.strip_dirs().sort_stats('calls').print_stats(30)
    stats.strip_dirs().sort_stats('time').print_stats(100)


if __name__ == "__main__":
    Application.init ("../profiles/testconfig.ini")

    class testApp(wx.App):
        def __init__(self, *args, **kwds):
            wx.App.__init__ (self, *args, **kwds)

    app = testApp(redirect=False)

    # wikiparserProfile()
    outwikerProfile ()
