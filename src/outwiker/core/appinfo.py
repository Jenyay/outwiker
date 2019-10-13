# -*- coding: utf-8 -*-

from typing import List, Optional

from .version import Version
from .version_requirements import Requirements


class AppInfo:
    def __init__(self,
                 app_name: str = '',
                 website: str = '',
                 description: str = '',
                 authors: 'Optional[List[AuthorInfo]]' = None,
                 requirements: 'Optional[Requirements]' = None,
                 version: 'Optional[Version]' = None):
        self.app_name = app_name
        self.website = website
        self.description = description

        self.authors = authors if authors is not None else []
        self.requirements = (
            requirements if requirements is not None else Requirements([], []))
        self.version = version


class AuthorInfo:
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
