# -*- coding: UTF-8 -*-

from StringIO import StringIO


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
