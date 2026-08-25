import wx
from wx.svg import SVGimage

from outwiker.core.exceptions import InvalidImageFormat
from outwiker.core.images import isSVG, isImage


def readSVG(fname: str, width: int, height: int) -> wx.Bitmap:
    with open(fname, "rb") as fp:
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


def resizeBitmap(bitmap: wx.Bitmap, width: int, height: int):
    """
    Convert bitmap to valid size
    """
    size_src = bitmap.GetSize()
    # Create transparent bitmap
    bitmap_new = wx.Bitmap(width, height)
    dc = wx.MemoryDC(bitmap_new)
    dc.SetBackground(wx.Brush("magenta"))
    dc.Clear()
    dc.SelectObject(wx.NullBitmap)
    bitmap_new.SetMaskColour("magenta")

    scale_x = float(size_src[0]) / float(width)
    scale_y = float(size_src[1]) / float(height)

    max_scale = max(scale_x, scale_y)
    image_new = bitmap.ConvertToImage()
    image_new.Rescale(
        int(size_src[0] / max_scale),
        int(size_src[1] / max_scale),
        wx.IMAGE_QUALITY_HIGH,
    )

    size_new = image_new.GetSize()
    result_image = bitmap_new.ConvertToImage()
    paste_x = (width - size_new[0]) // 2
    paste_y = (height - size_new[1]) // 2
    result_image.Paste(image_new, paste_x, paste_y)

    return result_image.ConvertToBitmap()
