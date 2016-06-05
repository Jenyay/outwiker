# -*- coding: UTF-8 -*-

from xml.etree import ElementTree

from outwiker.core.appinfo import (AppInfo,
                                   AuthorInfo,
                                   VersionInfo,
                                   RequirementsInfo)
from version import Version


class XmlVersionParser (object):
    """
    Class to read and write application info in XML format.

    Added in OutWiker 2.0.0.795.
    """
    def __init__(self, langlist=[u'en']):
        """
        langlist - list of the languages name ("en", "ru_RU" etc)
        """
        self._langlist = langlist

    def parse(self, text):
        """
        Return AppInfo instance
        """
        try:
            root = ElementTree.fromstring(text.encode('utf8'))
        except ElementTree.ParseError:
            appinfo = AppInfo(u'', None)
            return appinfo

        name = self._getTextValue(root, u'name')
        updatesUrl = self._getTextValue(root, u'updates')
        requirements = self._getRequirements(root)

        # Get data tag for selected language
        data_tag = self._getDataTag (root)
        appwebsite = self._getAppWebsite (data_tag)
        description = self._getDescription (data_tag)
        author = self._getAuthorInfo(data_tag)
        versionsList = self._getVersionsList(data_tag)

        appinfo = AppInfo(name,
                          author=author,
                          versionsList=versionsList,
                          appwebsite=appwebsite,
                          description=description,
                          updatesUrl=updatesUrl,
                          requirements=requirements)
        return appinfo

    def _getRequirements(self, root):
        assert root is not None
        requirements_tag = root.find(u'requirements')
        if requirements_tag is None:
            return None

        outwiker_version=None
        try:
            outwiker_version = Version.parse(self._getTextValue(requirements_tag, u'outwiker'))
        except ValueError:
            pass

        os_str = self._getTextValue(requirements_tag, u'os')
        if os_str is None:
            os_str = u''

        os_list = [current_os.strip()
                   for current_os
                   in os_str.split(u',')
                   if len(current_os.strip()) != 0]
        return RequirementsInfo(outwiker_version, os_list)

    def _getVersionsList(self, data_tag):
        """
        Return list of VersionInfo instance. List sorted by version (last version is first)
        """
        result = []
        if data_tag is None:
            return result

        changelog_tag = data_tag.find(u'changelog')
        if changelog_tag is None:
            return result

        for version_tag in changelog_tag.findall(u'version[@number]'):
            version = self._getVersionInfo(version_tag)
            if version is not None:
                result.append(version)

        result.sort(key=lambda x: x.version, reverse=True)

        return result

    def _getVersionInfo(self, version_tag):
        assert version_tag is not None
        version = self._getVersion(version_tag)
        if version is None:
            return None

        date = version_tag.get(u'date', u'')
        hidden = False
        try:
            hidden = bool(version_tag.get(u'hidden'))
        except ValueError:
            pass
        changes = self._getChanges(version_tag)
        downloads = self._getDownloads(version_tag)

        return VersionInfo(version,
                           date_str=date,
                           downloads=downloads,
                           changes=changes,
                           hidden=hidden)

    def _getDownloads(self, version_tag):
        assert version_tag is not None
        downloads = {}
        for download in version_tag.findall(u'download'):
            os = download.get(u'os', u'all')
            url = download.text
            if url is not None:
                downloads[os] = url
        return downloads

    def _getChanges(self, version_tag):
        assert version_tag is not None
        changes = []
        for change_tag in version_tag.findall(u'change'):
            text = change_tag.text
            if text is None:
                text = u''
            changes.append(text)
        return changes
    
    def _getVersion(self, version_tag):
        """
        Return Version instance or None if version number is not exists.
        """
        assert version_tag is not None
        try:
            number = version_tag.get(u'number')
            status = version_tag.get(u'status')
            if number is None:
                raise ValueError
            full_number = (u' '.join([number, status]) if status is not None
                           else number)
            version = Version.parse(full_number)
        except ValueError:
            return None
        return version

    def _getAuthorInfo(self, data_tag):
        """
        Return information about author or None if 'author' tag not exists
        """
        if data_tag is None:
            return None

        author_tag = data_tag.find(u'author')
        if author_tag is None:
            return None

        name = self._getTextValue(author_tag, u'name')
        email = self._getTextValue(author_tag, u'email')
        website = self._getTextValue(author_tag, u'website')
        return AuthorInfo(name, email, website)

    def _getDataTag(self, root):
        """
        Return data tag for language from _langlist or None
        """
        data_tag = None
        for lang in self._langlist:
            data_tag = root.find('./data[@lang="{}"]'.format(lang))
            if data_tag is not None:
                break
        return data_tag

    def _getAppWebsite(self, root):
        if root is None:
            return u''

        return self._getTextValue(root, u'website')

    def _getDescription(self, root):
        if root is None:
            return u''

        return self._getTextValue(root, u'description')

    def _getTextValue(self, root, tagname):
        """
        Return text inside tag with name tagname or empty string.
        """
        result = None
        result_tag = root.find(tagname)
        if result_tag is not None:
            result = result_tag.text

        if result is None:
            result = u''
        return result
