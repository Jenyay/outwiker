# -*- coding: utf-8 -*-

from .thumblistcommand import ThumbListCommand


class ThumbGalleryCommand(ThumbListCommand):
    """
    The (:thumbgallery:) command fully replicates the (:thumblist:) command and
    is created for compatibility with the (:thumbgallery:) command from the
    thumblist plugin for pmWiki - http://www.pmwiki.org/wiki/Cookbook/ThumbList
    """

    @property
    def name(self):
        """
        Returns the name of the command processed by the class
        """
        return "thumbgallery"
