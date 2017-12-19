# -*- coding: UTF-8 -*-

from io import StringIO


class DebChangelogGenerator(object):
    """
    Generator of the debian changelog
    """
    def __init__(self, appinfo, maintainer, maintainer_email):
        """
        appinfo - instance of the AppInfo class
        """
        assert appinfo is not None
        self._appinfo = appinfo
        self._maintainer = maintainer
        self._maintainer_email = maintainer_email

    def make(self, distribname, date_str):
        buf = StringIO()
        self._appendHeading(buf, distribname)
        self._appendChangelog(buf)
        self._appendFooter(buf, date_str)
        return buf.getvalue().strip()

    def _appendFooter(self, buf, date_str):
        footer = u' -- {name} <{email}>  {date}'.format(
            name=self._maintainer,
            email=self._maintainer_email,
            date=date_str
        )
        buf.write(footer)

    def _appendChangelog(self, buf):
        verinfo = self._appinfo.versionsList[0]
        if not verinfo.changes:
            buf.write(u'  * \n\n')
        else:
            for change in verinfo.changes:
                buf.write(u'  * {}\n'.format(change))
            buf.write(u'\n')

    def _appendHeading(self, buf, distribname):
        currentVersion = self._appinfo.currentVersion
        if currentVersion is None:
            raise ValueError('Current version is None')

        version_str = u'{}.{}.{}+{}'.format(currentVersion[0],
                                            currentVersion[1],
                                            currentVersion[2],
                                            currentVersion[3])
        header = u'outwiker ({version}~{distrib}) {distrib}; urgency=medium'.format(
            version=version_str,
            distrib=distribname,
        )
        buf.write(header)
        buf.write(u'\n\n')


class SiteChangelogGenerator(object):
    """
    Content generator for jenyay.net site
    """
    def __init__(self, appinfo):
        """
        appinfo - instance of the AppInfo class
        """
        self._appinfo = appinfo

    def make(self):
        if self._appinfo is None:
            return u''

        versions = self._appinfo.versionsList[:]
        versions.sort(key=lambda v: v.version, reverse=True)

        buf = StringIO()
        for n, verinfo in enumerate(versions):
            if n != 0:
                buf.write(u'\n')
            self._appendHeading(buf, verinfo)
            self._appendChanges(buf, verinfo)
        return buf.getvalue().strip()

    def _appendHeading(self, buf, verinfo):
        if verinfo.date_str:
            buf.write(u'!!!! {} ({})\n\n'.format(verinfo.version,
                                                 verinfo.date_str))
        else:
            buf.write(u'!!!! {}\n\n'.format(verinfo.version))

    def _appendChanges(self, buf, verinfo):
        for change in verinfo.changes:
            buf.write(u'* {}\n'.format(change))

        if verinfo.changes:
            buf.write(u'\n')


class SitePluginsTableGenerator (object):
    def __init__(self, appInfoList):
        self._appInfoList = appInfoList[:]
        self._appInfoList.sort(key=lambda x: x.appname)

    def make(self):
        buf = StringIO()
        for appinfo in self._appInfoList:
            assert appinfo.requirements is not None
            self._appendAppInfo(buf, appinfo)
        return buf.getvalue().strip()

    def _appendAppInfo(self, buf, appinfo):
        # Append plugin name and link
        name_text = u'||[[{name} -> {link}]] '.format(name=appinfo.appname,
                                                      link=appinfo.appwebsite)
        buf.write(name_text)

        # Append description
        description_text = u'||{} '.format(appinfo.description)
        buf.write(description_text)

        # OS
        os_list = appinfo.requirements.os[:]
        os_list.sort(reverse=True)
        os_list_text = u', '.join(os_list)
        os_text = u'|| {} '.format(os_list_text)
        buf.write(os_text)

        # OutWiker version
        version_text = u'|| {}.{}.{} ||'.format(
            appinfo.requirements.outwiker_version[0],
            appinfo.requirements.outwiker_version[1],
            appinfo.requirements.outwiker_version[2],
        )
        buf.write(version_text)
        buf.write(u'\n')
