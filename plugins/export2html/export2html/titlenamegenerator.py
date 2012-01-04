#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os.path


class TitleNameGenerator (object):
    def __init__ (self, outdir):
        self.__outdir = outdir

    
    def getName (self, page):
        name = os.path.join (page.title)

        index = 1
        while os.path.exists (os.path.join (self.__outdir, name + ".html") ):
            name = page.title + " ({0})".format (index)
            index += 1

        return name
