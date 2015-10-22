# -*- coding: UTF-8 -*-

from abc import ABCMeta


class BaseController (object):
    __metaclass__ = ABCMeta

    def initialize (self):
        pass


    def clear (self):
        pass
