# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod
import os.path

from .thumbexception import ThumbException


class ThumbmakerBase (object):
    __metaclass__ = ABCMeta


    @abstractmethod
    def _rescale (self, image, width_new, height_new, fname_out):
        pass


    @abstractmethod
    def _loadImage (self, fname):
        pass


    @abstractmethod
    def _getSize (self, image):
        pass


    def thumbByWidth (self, fname_src, width_new, fname_new):
        """
        Создать превьюшку определенной ширины
        """
        if not os.path.exists (fname_src):
            raise ThumbException (u"Error: %s not found" % os.path.basename (fname_src))

        image_src = self._loadImage (fname_src)
        width_src, height_src = self._getSize (image_src)

        scale = float (width_new) / float (width_src)
        height_new = int (height_src * scale)

        self._rescale (image_src, width_new, height_new, fname_new)


    def thumbByHeight (self, fname_src, height_new, fname_new):
        """
        Создать превьюшку определенной высоты
        """
        if not os.path.exists (fname_src):
            raise ThumbException (u"Error: %s not found" % os.path.basename (fname_src))

        image_src = self._loadImage (fname_src)
        width_src, height_src = self._getSize (image_src)

        scale = float (height_new) / float (height_src)
        width_new = int (width_src * scale)

        self._rescale (image_src, width_new, height_new, fname_new)


    def thumbByMaxSize (self, fname_src, maxsize_res, fname_new):
        """
        Создать превьюшку с заданным максимальным размером
        """
        if not os.path.exists (fname_src):
            raise ThumbException (u"Error: %s not found" % os.path.basename (fname_src))

        image_src = self._loadImage (fname_src)

        width_src, height_src = self._getSize (image_src)

        if width_src > height_src:
            self.thumbByWidth (fname_src, maxsize_res, fname_new)
        else:
            self.thumbByHeight (fname_src, maxsize_res, fname_new)
