# -*- coding: utf-8 -*-

import os
import os.path
import shutil

from outwiker.core.attachment import Attachment
from outwiker.core.defines import PAGE_ATTACH_DIR


class Thumbnails:
    """
    Class for working with attachments directory
    """

    thumbDir = "__thumb"

    def __init__(self, page):
        self.page = page

    @staticmethod
    def getRelativeThumbDir():
        return os.path.join(PAGE_ATTACH_DIR, Thumbnails.thumbDir)

    def getThumbPath(self, create: bool):
        """
        Get the full path to the thumbnails directory
        create - whether to create the directory if it doesn't exist
        """
        path = os.path.join(
            Attachment(self.page).getAttachPath(create=create), Thumbnails.thumbDir
        )

        if create and not os.path.exists(path):
            os.mkdir(path)

        return path

    def clearDir(self):
        """
        Remove all contents of the __thumb directory
        """
        path = self.getThumbPath(create=False)

        if not os.path.exists(path):
            return

        for fname in os.listdir(path):
            fullpath = os.path.join(path, fname)

            if os.path.isfile(fullpath):
                os.remove(fullpath)
            elif os.path.isdir(fullpath):
                shutil.rmtree(fullpath)
