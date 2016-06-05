# -*- coding: UTF-8 -*-
"""
Классы для работы с версией программы
"""

import re


class Status (object):
    def __init__ (self, name, number):
        """
        Класс для нецифровых обозначений версий (альфа, бета и т.д.)
        name - название версии
        weight - "вес" версии. Чем это значение больше, тем более "зрелая" версия
        """
        self.name = name
        self.number = number


    def __eq__ (self, other):
        return self.number == other.number


    def __ne__ (self, other):
        return not self.__eq__ (other)


    def __lt__ (self, other):
        return self.number < other.number


    def __le__ (self, other):
        return self.__lt__ (other) or self.__eq__ (other)


    def __gt__ (self, other):
        return self.number > other.number


    def __ge__ (self, other):
        return self.__gt__ (other) or self.__eq__ (other)


class StatusSet (object):
    """
    Набор стандартных статусов
    """
    DEV = Status ("dev", 0)
    NIGHTLY = Status ("nightly", 1)

    PREALPHA = Status ("prealpha", 100)
    ALPHA = Status ("alpha", 110)
    ALPHA2 = Status ("alpha2", 120)
    ALPHA3 = Status ("alpha3", 130)
    ALPHA4 = Status ("alpha4", 140)
    ALPHA5 = Status ("alpha5", 150)

    PREBETA = Status ("prebeta", 200)
    BETA = Status ("beta", 210)
    BETA2 = Status ("beta2", 220)
    BETA3 = Status ("beta3", 230)
    BETA4 = Status ("beta4", 240)
    BETA5 = Status ("beta5", 250)

    PRERC = Status ("preRC", 300)
    RC = Status ("RC", 310)
    RC2 = Status ("RC2", 320)
    RC3 = Status ("RC3", 330)
    RC4 = Status ("RC4", 340)
    RC5 = Status ("RC5", 350)

    RELEASE = Status ("", 400)

    def __init__ (self):
        pass


class Version (object):
    def __init__ (self, major, *args, **kwargs):
        self.version = [major] + [int (arg) for arg in args]
        self.status = kwargs["status"] if "status" in kwargs else StatusSet.RELEASE


    def __eq__ (self, other):
        return self.status == other.status and self.version == other.version


    def __nq__ (self, other):
        return not self.__eq__ (other)


    def __lt__ (self, other):
        return self.version < other.version or (self.version == other.version and self.status < other.status)


    def __le__ (self, other):
        return self.__lt__ (other) or self.__eq__ (other)


    def __gt__ (self, other):
        return self.version > other.version or (self.version == other.version and self.status > other.status)


    def __ge__ (self, other):
        return self.__gt__ (other) or self.__eq__ (other)


    def __str__ (self):
        result = reduce (lambda x, y: str(x) + "." + str(y), self.version, "")
        result += " " + self.status.name

        # Отбросим первую точку
        return result.strip()[1:]


    def __repr__ (self):
        """
        Added in OutWiker 2.0.0.795
        """
        return self.__str__()


    @staticmethod
    def parseStatus (string):
        result = None
        items = dir (StatusSet)

        for item_name in items:
            item = getattr (StatusSet, item_name)

            if isinstance (item, Status) and item.name.lower() == string.lower():
                result = item
                break

        return result


    @staticmethod
    def parse (string):
        """
        Создать версию по строке
        """
        regex = "^\s*(?P<major>\d+)(?P<minor>(\.\d+)*)(?P<status>.+)?"
        m = re.match (regex, string, re.IGNORECASE)
        if not m:
            raise ValueError

        major = int (m.group ("major"))
        minors = [int(minor) for minor in
                  m.group ("minor").split(".")
                  if len (minor.strip()) > 0] if m.group ("minor") is not None else []

        status = Version.parseStatus (m.group("status").strip()) if m.group("status") is not None else None

        return Version (major, *minors, status=status) if status else Version (major, *minors)
