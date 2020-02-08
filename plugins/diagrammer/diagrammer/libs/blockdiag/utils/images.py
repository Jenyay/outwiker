# -*- coding: utf-8 -*-
#  Copyright 2011 Takeshi KOMIYA
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from __future__ import division

import io
import os
import re
from tempfile import NamedTemporaryFile

from PIL import Image

from blockdiag.utils import urlutil
from blockdiag.utils.logging import warning

urlopen_cache = {}


def urlopen(url, *args, **kwargs):
    """ auto caching urlopen() (using tempfile) """
    from urllib.request import urlopen as orig_urlopen

    if url not in urlopen_cache:
        with NamedTemporaryFile(delete=False) as tmpfile:
            tmpfile.write(orig_urlopen(url, *args, **kwargs).read())
            tmpfile.flush()
            urlopen_cache[url] = tmpfile.name

    return io.open(urlopen_cache[url], 'rb')


def get_image_size(image):
    if isinstance(image, Image.Image):
        return image.size
    else:
        stream = None
        try:
            stream = open(image)
            return stream.size
        finally:
            if stream and hasattr(stream, 'close'):
                stream.close()


def calc_image_size(size, bounded):
    if bounded[0] < size[0] or bounded[1] < size[1]:
        if (size[0] * 1.0 // bounded[0]) < (size[1] * 1.0 // bounded[1]):
            size = (size[0] * bounded[1] // size[1], bounded[1])
        else:
            size = (bounded[0], size[1] * bounded[0] // size[0])

    return size


def color_to_rgb(color):
    import webcolors
    if color == 'none' or isinstance(color, (list, tuple)):
        rgb = color
    elif re.match('#', color):
        rgb = webcolors.hex_to_rgb(color)
    else:
        rgb = webcolors.name_to_rgb(color)

    return rgb


def wand_open(url, stream):
    try:
        import wand.image
    except Exception:
        warning("unknown image type: %s", url)
        raise IOError

    try:
        png_image = io.BytesIO()
        with wand.image.Image(file=stream) as img:
            img.format = 'PNG'
            img.save(file=png_image)
            png_image.seek(0)
            return png_image
    except Exception as exc:
        warning("Fail to convert %s to PNG: %r", url, exc)
        raise IOError


def pillow_open(url, stream):
    try:
        if isinstance(url, Image.Image):
            return url
        else:
            return Image.open(stream)
    except IOError:
        stream.seek(0)
        png_stream = wand_open(url, stream)

        return Image.open(png_stream)


def open(url, mode='Pillow'):
    if hasattr(url, 'read') or isinstance(url, Image.Image):
        stream = url
    elif not urlutil.isurl(url):
        stream = io.open(url, 'rb')
    else:
        try:
            # wrap BytesIO for rewind stream
            stream = io.BytesIO(urlopen(url).read())
        except Exception:
            warning("Could not retrieve: %s", url)
            raise IOError

    image = pillow_open(url, stream)
    if mode.lower() == 'pillow':
        # stream will be closed by GC
        return image
    else:  # mode == 'png'
        try:
            png_image = io.BytesIO()
            image.save(png_image, 'PNG')
            if hasattr(stream, 'close'):  # close() is implemented on Pillow
                stream.close()
        except Exception:
            warning("Could not convert image: %s", url)
            raise IOError

        png_image.seek(0)
        return png_image


def cleanup():
    for url in list(urlopen_cache.keys()):
        path = urlopen_cache.pop(url)
        try:
            os.remove(path)
        except Exception:
            pass


def setup(app):
    app.register_cleanup_handler(cleanup)
