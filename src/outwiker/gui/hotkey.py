#!/usr/bin/python
# -*- coding: UTF-8 -*-

class HotKey (object):
    """
    Класс для описания горячей клавиши
    """
    def __init__ (self, key, ctrl=False, alt=False, shift=False):
        self._key = key
        self._ctrl = ctrl
        self._alt = alt
        self._shift = shift


    @property
    def key (self):
        return self._key


    @property
    def ctrl (self):
        return self._ctrl


    @property
    def alt (self):
        return self._alt


    @property
    def shift (self):
        return self._shift
