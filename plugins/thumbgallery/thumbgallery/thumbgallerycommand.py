#!/usr/bin/python
# -*- coding: UTF-8 -*-

from .thumblistcommand import ThumbListCommand

class ThumbGalleryCommand (ThumbListCommand):
    """
    Команда (:thumbgallery:) полностью повторяет команду (:thumblist:) и создана для совместимости с командой (:thumbgallery:) из плагина thumblist для omWiki - http://www.pmwiki.org/wiki/Cookbook/ThumbList
    """
    @property
    def name (self):
        """
        Возвращает имя команды, которую обрабатывает класс
        """
        return u"thumbgallery"
