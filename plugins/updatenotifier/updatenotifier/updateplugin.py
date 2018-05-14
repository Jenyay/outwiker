# -*- coding: utf-8 -*-

import tempfile
from zipfile import ZipFile
import shutil
import os.path
import logging
import urllib.request
import urllib.error

join, dirname = os.path.join, os.path.dirname
logger = logging.getLogger('updatenotifier')


class UpdatePlugin (object):
    """
    Class is responsible to updating plugin.
    """

    def update(self, url, plugin_path):
        """
        Download zip with plugin from url and extract it to plugin_path
        :param url:
            url where latest plugin zip file can be downloaded
        :param plugin_path:
            path to plugin folder on PC
        :return:
            True if plugin was updated, otherwise False
        """
        logger.info('Start update plugin: %s' % (plugin_path))

        # Download the file from `url`, save it in a temporary directory and
        # get the path to it (e.g. '/tmp/tmpb48zma.zip') in
        # the `file_name` variable:
        try:
            zip_name, headers = urllib.request.urlretrieve(url)
        except (urllib.error.HTTPError, urllib.error.URLError, ValueError):
            logger.warning(u"Can't download {}".format(url))
            return False

        # extract plugin to tmp dir
        extracted_path = self._extract_plugin(zip_name)

        # remove plugin directory and copy new data to the plugins folder
        if not self._replacetree(extracted_path, plugin_path):
            return False

        # remove temp files
        if os.path.exists(extracted_path):
            shutil.rmtree(extracted_path)
        os.remove(zip_name)
        return True

    def _replacetree(self, src, dst):
        """
        The function delete dst folder and than copy src to dst
            by shutil.copytree
        """
        if os.path.exists(dst):
            try:
                shutil.rmtree(dst)
            except OSError:
                return False

        if not os.path.exists(dst):
            shutil.copytree(src, dst)

        return True

    def _extract_plugin(self, zip_path):
        """
        Extract plugin.zip into temp folder and return path to extracted folder
        :param zip_path:
            full path to zipped plugin
        :return:
             path to extracted plugin folder (e.g. '/tmp/markdown')
        """
        tempdir = tempfile.gettempdir()

        with ZipFile(zip_path) as myzip:
            myzip.extractall(tempdir)

            if myzip.namelist():
                extracted_path = join(tempdir, dirname(myzip.namelist()[0]))
            else:
                logger.warning(u"Plugin zip file is empty")
                return None

        return extracted_path
