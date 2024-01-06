import wx
from wx.svg import SVGimage

from outwiker.core.exceptions import InvalidImageFormat
from outwiker.core.images import isSVG, isImage

def readSVG(fname: str, width: int, height: int) -> wx.Bitmap:
    with open(fname, 'rb') as fp:
        data = fp.read()
        svg = SVGimage.CreateFromBytes(data)
    return svg.ConvertToScaledBitmap((width, height))


def readImage(fname: str, width: int, height: int) -> wx.Bitmap:
    if isImage(fname):
        bitmap = wx.Bitmap(fname)
    elif isSVG(fname):
        bitmap = readSVG(fname, width, height)
    else:
        raise InvalidImageFormat(fname)

    return bitmap

