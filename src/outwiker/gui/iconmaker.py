# -*- coding: utf-8 -*-

from PIL import Image

from outwiker.gui.defines import ICONS_WIDTH, ICONS_HEIGHT


class IconMaker:
    """Class for creation icons by images."""

    def create(self, fname_in, fname_out) -> None:
        """Create icon by file fname_in. Result will have saved as fname_out."""
        img_new = Image.new("RGBA", (ICONS_WIDTH, ICONS_HEIGHT))
        with Image.open(fname_in) as img_src:
            # Resize source image if it is required
            width_src, height_src = img_src.size
            scale = max(
                float(width_src) / float(ICONS_WIDTH),
                float(height_src) / float(ICONS_HEIGHT),
            )
            if scale > 1:
                img_src = img_src.resize(
                    (int(width_src / scale), int(height_src / scale)),
                    Image.Resampling.LANCZOS,
                )

            # Paste source image to result image
            dx = int((ICONS_WIDTH - img_src.size[0]) / 2.0)
            dy = int((ICONS_HEIGHT - img_src.size[1]) / 2.0)

            assert dx >= 0 and dx < ICONS_WIDTH
            assert dy >= 0 and dy < ICONS_HEIGHT

            img_new.paste(img_src, (dx, dy))
            img_new.save(fname_out)
