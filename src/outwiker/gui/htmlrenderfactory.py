# -*- coding: UTF-8 -*-

from outwiker.core.system import getOS


def getHtmlRender (parent):
    """
    ! This function is deprecated. It used by Statistics plugin.
    Function return HTML render for current system
    """
    return getOS().getHtmlRender(parent)
