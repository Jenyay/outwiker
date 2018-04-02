# -*- coding: UTF-8 -*-

import tempfile
import zipfile
import shutil
import os.path
import logging

from .loaders import NormalLoader

join, dirname = os.path.join, os.path.dirname

logger = logging.getLogger('updatenotifier')

class UpdatePlugin (object):
    def __init__ (self):
        self.tmp_dir = tempfile.gettempdir()
        self.zip = join(self.tmp_dir,'outwiker_plugin.zip')
        self.unzip = ''

    def update(self, url, plugin_path):

        data = NormalLoader().load(url)

        logger.info('update')
        if data:
            with open(self.zip, 'wb') as f:
                f.write(data)
                self.plugin_updater(plugin_path)
            os.remove(self.zip)

    def plugin_updater(self, plugin_path):

        logger.info('plugin_updater')
        # extract zip
        my_zip = zipfile.ZipFile(self.zip)
        my_zip.extractall(self.tmp_dir)
        if my_zip.namelist():
            self.unzip = join(self.tmp_dir, dirname(my_zip.namelist()[0]))
        my_zip.close()

        pls_path, pl_folder_name = os.path.split(plugin_path)
        pl_path = join(pls_path, pl_folder_name)

        if os.path.exists(pl_path):
            shutil.rmtree(pl_path)
        shutil.copytree(self.unzip, pl_path)

        # remove tmp
        if os.path.exists(self.unzip):
            shutil.rmtree(self.unzip)