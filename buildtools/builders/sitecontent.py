# -*- coding: utf-8 -*-

import os.path
from typing import List

from jinja2 import Environment, FileSystemLoader

from buildtools.builders.base import BuilderBase
from buildtools.utilites import print_error

from outwiker.utilites.textfile import readTextFile, writeTextFile
from outwiker.core.appinfofactory import AppInfoFactory
from outwiker.core.changelogfactory import ChangeLogFactory


class SiteContentSource(object):
    def __init__(self, info_xml_file, versions_xml_file, lang, template_file):
        self.info_xml_file = info_xml_file
        self.versions_xml_file = versions_xml_file
        self.lang = lang
        self.template_file = template_file


class SiteContentBuilder(BuilderBase):
    '''
    Class to create content for the site
    '''

    def __init__(self,
                 subdir_name: str,
                 content_sources: List[SiteContentSource],
                 templates_path: str):
        super().__init__(subdir_name)
        self._sources = content_sources
        self._templates_path = templates_path

    def _build(self):
        for source in self._sources:
            self._processSource(source)

    def _processSource(self, source: SiteContentSource) -> None:
        if not os.path.exists(os.path.join(self._templates_path, source.template_file)):
            print_error('Template file not found: {}'.format(
                source.template_file))
            return

        if not os.path.exists(source.info_xml_file):
            print_error('XML file not found: {}'.format(source.info_xml_file))
            return

        if not os.path.exists(source.versions_xml_file):
            print_error('XML file not found: {}'.format(
                source.versions_xml_file))
            return

        info_xml_content = readTextFile(source.info_xml_file)
        app_info = AppInfoFactory.fromString(info_xml_content, source.lang)

        versions_xml_content = readTextFile(source.versions_xml_file)
        versions_info = ChangeLogFactory.fromString(versions_xml_content,
                                                    source.lang)

        template_env = Environment(
            loader=FileSystemLoader(self._templates_path))
        template = template_env.get_template(source.template_file)

        current_version = versions_info.latestVersion
        if current_version is not None:
            version_full_str = str(current_version.version)
            version_main = '.'.join([str(n)
                                     for n
                                     in current_version.version[:-1]]
                                    )
            version_build = current_version.version[-1]
            date_str = (current_version.date.strftime('%d.%m.%Y')
                        if current_version.date is not None
                        else '')
        else:
            print_error('Invalid version for {}'.format(app_info.app_name))
            return

        versions_list = versions_info.versions

        result = template.render(
            version_full=version_full_str,
            version_main=version_main,
            version_build=version_build,
            versions_list=versions_list,
            date=date_str,
        )

        template_name = os.path.basename(source.template_file)
        result_fname = os.path.join(self.build_dir, template_name)
        writeTextFile(result_fname, result)
