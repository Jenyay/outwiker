# -*- coding: utf-8 -*-

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
