import os
from typing import List
from urllib.parse import urlparse

from fabric.api import cd, put

from outwiker.utilites.textfile import readTextFile
from outwiker.core.changelogfactory import ChangeLogFactory

from buildtools.versions import getPluginChangelogPath
from buildtools.utilites import print_info


class PluginsUploader:
    '''
    Class to upload plug-ins archives to server
    '''

    def __init__(self, build_plugins_dir: str, deploy_home_path: str):
        '''
        build_plugins_dir - path to folder with folders with plug-ins:
            build/version/plugins
        '''
        self.build_plugins_dir = build_plugins_dir
        self.deploy_home_path = deploy_home_path

    def upload(self, plugins: List[str]):
        '''
        Upload plugin to site
        '''
        for pluginname in plugins:
            path_to_plugin_local = os.path.join(
                self.build_plugins_dir, pluginname)

            if not os.path.exists(path_to_plugin_local):
                continue

            path_to_xml_changelog = getPluginChangelogPath(pluginname)
            changelog_xml_content = readTextFile(path_to_xml_changelog)
            changelog = ChangeLogFactory.fromString(changelog_xml_content, '')
            latest_version = changelog.latestVersion
            assert latest_version is not None

            print_info('Uploading...')

            for download in latest_version.downloads:
                url_elements = urlparse(download.href)
                server_src = '{scheme}://{netloc}/'.format(
                    scheme=url_elements.scheme,
                    netloc=url_elements.netloc)

                upload_url = download.href.replace(server_src,
                                                   self.deploy_home_path)

                path_to_upload = os.path.dirname(upload_url)
                archive_name = os.path.basename(upload_url)

                path_to_archive_local = os.path.join(
                    path_to_plugin_local, archive_name)

                with cd(path_to_upload):
                    put(path_to_archive_local, archive_name)
