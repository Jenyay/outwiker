# -*- coding: UTF-8 -*-

from PIL import Image

from outwiker.core.defines import ICON_WIDTH, ICON_HEIGHT


class IconMaker (object):
    """ Class for creation icons by images. """
    def create (self, fname_in, fname_out):
        """ Create icon by file fname_in. Result will have saved as fname_out.
        """
        img_new = Image.new ('RGBA', (ICON_WIDTH, ICON_HEIGHT))
        img_src = Image.open (fname_in)

        # Resize source imaga, if it is required
        width_src, height_src = img_src.size
        scale = max (float (width_src) / float (ICON_WIDTH), float (height_src) / float (ICON_HEIGHT))
        if scale > 1:
            img_src = img_src.resize ((int (width_src / scale), int (height_src / scale)), Image.ANTIALIAS)

        # Paste source image to result image
        dx = int ((ICON_WIDTH - img_src.size[0]) / 2.0)
        dy = int ((ICON_HEIGHT - img_src.size[1]) / 2.0)

        assert dx >= 0 and dx < ICON_WIDTH
        assert dy >= 0 and dy < ICON_HEIGHT

        img_new.paste (img_src, (dx, dy))

        img_new.save (fname_out)
