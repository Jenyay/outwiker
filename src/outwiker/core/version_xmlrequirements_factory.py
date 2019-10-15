from typing import List, Optional, Iterable
from xml.etree import ElementTree

from .version_xmlrequirements import XmlRequirements


class XmlRequirementsFactory:
    TAG_REQUIREMENTS = 'requirements'
    TAG_REQUIREMENTS_API = 'api'
    TAG_REQUIREMENTS_OS = 'os'

    @classmethod
    def fromXml(cls, tag_parent: ElementTree.Element) -> 'XmlRequirements':
        os_list = []            # type: List[str]
        api_list = []           # type: List[Iterable[int]]

        tag_requirements = tag_parent.find(cls.TAG_REQUIREMENTS)

        if tag_requirements is not None:
            os_list = cls._getTextList(tag_requirements, cls.TAG_REQUIREMENTS_OS)
            api_list_str = cls._getTextList(
                tag_requirements, cls.TAG_REQUIREMENTS_API)
            api_list = []
            for version_str in api_list_str:
                version = cls._parseVersion(version_str)
                if version:
                    api_list.append(version)

        return XmlRequirements(os_list, api_list)

    @classmethod
    def _parseVersion(cls, version_str: str) -> Optional[Iterable[int]]:
        try:
            return tuple((int(item) for item in version_str.split('.')))
        except ValueError:
            return None

    @classmethod
    def _getTextList(cls, root: ElementTree.Element, tag_name: str) -> List[str]:
        """
        Return text list from tags with name tag_name
        """
        result = []

        for tag in root.findall(tag_name):
            text = tag.text if tag.text is not None else ''
            result.append(text)

        return result
