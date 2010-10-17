#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import profiles.pro_parser
import cProfile

fname = "profiles/test2.wiki"
pparser = profiles.pro_parser.ParseSample (fname)
#pparser.run()

cProfile.run('pparser.run()')

