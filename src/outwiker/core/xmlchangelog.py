from datetime import datetime
from typing import List, Optional

from .dataforlanguage import DataForLanguage
from .version_xmlrequirements import XmlRequirements


class XmlChangeItem:
    def __init__(self, description: str):
        self.description = description


class XmlDownload:
    def __init__(self,
                 href: str,
                 requirements: Optional[XmlRequirements] = None):
        self.href = href
        self.requirements = requirements


class XmlChangeLog:
    def __init__(self):
        self.versions = []                      # type: List[XmlChangeLogVersionInfo]


class XmlChangeLogVersionInfo:
    def __init__(self,
                 number: str,
                 status: str = '',
                 date: Optional[datetime] = None):
        self.number = number                # type: str
        self.status = status                # type: str
        self.date = date                    # type: Optional[datetime]
        self.downloads = []                 # type: List[XmlDownload]

        # Key - language, value - list of XmlChangeItem
        self.changes = DataForLanguage()    # type: DataForLanguage[List[XmlChangeItem]]
