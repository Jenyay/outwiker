from .version_xmlrequirements import XmlRequirements
from .version_requirements import Requirements


class RequirementsFactory:
    @classmethod
    def fromXmlRequirements(cls, requirements: XmlRequirements) -> Requirements:
        if requirements is None:
            return Requirements([], [])

        os_list = requirements.os_list[:]
        api_list = requirements.api_list[:]
        return Requirements(os_list, api_list)
