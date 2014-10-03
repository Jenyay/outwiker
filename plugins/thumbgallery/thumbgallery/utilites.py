# -*- coding: UTF-8 -*-


def isImage (fname):
    """
    Возвращает True, если fname - картинка
    """
    fnameLower = fname.lower()

    return (fnameLower.endswith (".png") or
            fnameLower.endswith (".jpg") or
            fnameLower.endswith (".jpeg") or
            fnameLower.endswith (".bmp") or
            fnameLower.endswith (".gif"))
