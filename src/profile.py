#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cProfile
import pstats

import wx

from core.application import Application

def wikiparserProfile ():
	import profiles.pro_parser

	fname = "profiles/test2.wiki"
	profile_fname = "../test/wikiparser.profile"

	global pparser
	pparser = profiles.pro_parser.ParseSample (fname)

	#pparser.run()
	cProfile.run('pparser.run()', profile_fname)

	stats = pstats.Stats(profile_fname)
	stats.strip_dirs().sort_stats('cumulative').print_stats()


if __name__ == "__main__":
	Application.init ("../test/testconfig.ini")

	class testApp(wx.App):
		def __init__(self, *args, **kwds):
			wx.App.__init__ (self, *args, **kwds)

	app = testApp(redirect=False)

	wikiparserProfile()
