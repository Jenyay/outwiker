# -*- coding: UTF-8 -*-


class AppInfo (object):
    """
    Common for OutWiker and plug-ins items.
    """
    def __init__(self,
                 appname,
                 author,
                 versionsList=[],
                 description=u"",
                 appwebsite=u"",
                 updatesUrl=u""):
        """
        appname - application or plug-in name.
        author - author info. It is instance of the AuthorInfo class.
        versionsList - information about every version.
                       It is a instance of the VersionInfo class.
        description - application's or plug-in's description.
        appwebsite - application or plug-in web site.
        updatesUrl - URL to XML file with updates information.
        """
        self.appname = appname
        self.author = author
        self.versionsList = versionsList[:]
        self.description = description
        self.appwebsite = appwebsite
        self.updatesUrl = updatesUrl


class AuthorInfo (object):
    """
    Information about plug-in's author
    """
    def __init__(self, name=u"", email=u"", website=u""):
        self.name = name
        self.email = email
        self.website = website


class VersionInfo (object):
    """
    Information about single version (version, change log, URL to download)
    """
    def __init__(self, version, download=u"", changes=[], hidden=False):
        """
        version - instance of the Version class.
        download - URL to download this version.
        changes - list of the string with changes in current version.
        hidden - hide this version to users?
        """
        self.version = version
        self.download = download
        self.changes = changes[:]
        self.hidden = hidden
