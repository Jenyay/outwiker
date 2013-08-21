#!/usr/bin/python
# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod, abstractproperty


class BaseAction (object):
    __metaclass__ = ABCMeta
    
    @abstractproperty
    def title (self):
        pass


    @abstractproperty
    def strid (self):
        pass


    @abstractmethod
    def run (self):
        pass
