from typing import List, Optional

from .dataforlanguage import DataForLanguage
from .version_xmlrequirements import XmlRequirements


class XmlAppInfo:
    def __init__(self):
        # Key - language, value - apllication name
        self.app_name = DataForLanguage()       # type: DataForLanguage[str]

        # Key - language, value - URL
        self.website = DataForLanguage()        # type: DataForLanguage[str]

        # Key - language, value - description
        self.description = DataForLanguage()    # type: DataForLanguage[str]

        # Key - language, value - list of authors information
        self.authors = DataForLanguage()        # type: DataForLanguage[List[XmlAuthorInfo]]

        self.requirements = XmlRequirements([], [])

        self.version = None                     # type: Optional[XmlVersionInfo]


class XmlAuthorInfo:
    """
    Information about plug-in's author
    """

    def __init__(self,
                 name: str = '',
                 email: str = '',
                 website: str = ''):
        self.name = name
        self.email = email
        self.website = website


class XmlVersionInfo:
    def __init__(self, number: str, status: str = ''):
        self.number = number                # type: str
        self.status = status                # type: str
