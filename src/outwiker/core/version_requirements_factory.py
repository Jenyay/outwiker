from typing import Optional

from .version_xmlrequirements import XmlRequirements
from .version_requirements import Requirements


class RequirementsFactory:
    @classmethod
    def fromXmlRequirements(cls, requirements: Optional[XmlRequirements]) -> Requirements:
        if requirements is None:
            return Requirements([], [])

        os_list = requirements.os_list[:]
        api_list = requirements.api_list[:]
        return Requirements(os_list, api_list)
