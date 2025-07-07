# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import configparser
import datetime
import json
import shutil
import logging
import os
from typing import List

from outwiker.gui.stcstyle import StcStyle

logger = logging.getLogger("outwiker.core.config")


class Config:
    """
    Shell for configparser class
    """

    def __init__(self, fname, readonly=False):
        """
        fname: config file name
        readonly: True if config should be in readonly mode
        """
        self.readonly = readonly
        self.fname = fname
        self._config = configparser.ConfigParser(interpolation=None)

        try:
            self._config.read(self.fname, encoding="utf8")
        except (UnicodeDecodeError, IOError, configparser.Error):
            backup_fname = self.fname + ".bak"
            logger.error(
                "Invalid config file: %s. The file will be copied to %s and cleaned.",
                fname,
                os.path.basename(backup_fname),
            )

            self._backup(self.fname, backup_fname)
            with open(self.fname, "w", encoding="utf8") as fp:
                fp.write(self.getDefaultContent())

            self._config.read(self.fname, encoding="utf8")

        # make aliases for the configparser methods
        self.get = self._config.get
        self.getint = self._config.getint
        self.getfloat = self._config.getfloat
        self.has_section = self._config.has_section
        self.has_option = self._config.has_option

    def _backup(self, fname, backup_fname):
        shutil.copyfile(fname, backup_fname)

    def getDefaultContent(self):
        """
        Return default value for config file.
            Returns:
                Empty string.
        """
        return ""

    def set(self, section, param, value):
        """
        Set parameter value. If section is absent in the config it will be added.
            Args:
                :section: section name in configuration file.
                :param: parameter name.
                :value: new value of param. value is converted to str.
            Returns:
                :True: if param was successful added to configuration file
                :False: if config file was opened in readonly mode.
        """
        if self.readonly:
            return False

        if not self._config.has_section(section):
            self._config.add_section(section)

        # no actions if new value is equal to old.
        if self.get(section, param, fallback=None) == str(value):
            return True

        self._config.set(section, param, str(value))
        return self.save()

    def save(self):
        """
        Сохранить изменения
        Возвращает True, если сохранение прошло успешно и False
        в противном случае
        """
        if self.readonly:
            return False

        with open(self.fname, "w", encoding="utf8") as fp:
            self._config.write(fp)

        return True

    def remove_section(self, section):
        """
        Удалить текцию из файла конфига
        section - имя удаляемой секции
        """
        result = self._config.remove_section(section) and self.save()
        return result

    def remove_option(self, section, option):
        """
        Удалить настройку из файла конфига
        section - имя секции, которой принадлежит опция
        option - имя удаляемой опции
        """
        result = self._config.remove_option(section, option) and self.save()
        return result

    def getbool(self, section, param):
        """
        Получить булево значение из конфига
        section - имя секции файла конфига
        param - имя параметра
        Возващает строку с прочитанным значением
        Может бросать исключения
        """
        val = self.get(section, param)

        return True if val.strip().lower() == "true" else False


class BaseOption(metaclass=ABCMeta):
    """
    Базовый класс для работы с отдельными записями конфига
    """

    def __init__(self, config, section, param, defaultValue):
        """
        config - экземпляр класса core.Config
        section - секция для параметра конфига
        param - имя параметра конфига
        defaultValue - значение по умолчанию
        """
        self.config = config
        self.section = section
        self.param = param
        self.defaultValue = defaultValue

        # Указатель на последнее возникшее исключение
        # Как правило исключения игнорируются,
        # поэтому это поле используется для отладки
        self.error = None

    def remove_option(self):
        """
        Удалить настройку
        """
        self.config.remove_option(self.section, self.param)

    @property
    def value(self):
        """
        Возвращает значение парамета
        """
        return self._loadParam()

    @value.setter
    def value(self, val):
        """
        Устанавливает значение параметра
        """
        self.config.set(self.section, self.param, self._prepareToWrite(val))

    @abstractmethod
    def _loadValue(self):
        """
        Метод должен прочитать из конфига параметр self.param из секции
        self.section и вернуть значение.
        Исключения можно игнорировать, поскольку они перехватываются выше
        в методе _loadParam
        """
        pass

    def _prepareToWrite(self, val) -> str:
        """
            Преобразовать (если надо) значение к виду, в котором оно будет
        записано в конфиг
        """
        return val

    def _loadParam(self):
        """
        Возващает прочитанное из конфига значение или значение по умолчанию
        """
        try:
            val = self._loadValue()
        except Exception as e:
            self.error = e
            val = self.defaultValue

        return val


class StringOption(BaseOption):
    """
    Класс для упрощения работы со строковыми опциями
    """

    def __init__(self, config, section, param, defaultValue):
        super().__init__(config, section, param, defaultValue)

    def _loadValue(self) -> str:
        """
        Получить значение
        """
        return self.config.get(self.section, self.param)


class BooleanOption(BaseOption):
    """
    Булевская настройка.
    Элемент управления - wx.CheckBox
    """

    def _loadValue(self) -> bool:
        """
        Получить значение
        """
        return self.config.getbool(self.section, self.param)


class JSONOption(BaseOption):
    """
    Options to store object in JSON format
    """

    def _loadValue(self):
        return json.loads(self.config.get(self.section, self.param))

    def _prepareToWrite(self, val) -> str:
        return json.dumps(val)


class StcStyleOption(BaseOption):
    """
    Настрока для хранения стиля редактора StcStyledEditor
    """

    def __init__(self, config, section, param, defaultValue):
        """
        defaultValue - экземпляр класса StcStyle
        """
        super().__init__(config, section, param, defaultValue)

    def _loadValue(self) -> StcStyle:
        """
        Получить значение. В производных классах этот метод переопределяется
        """
        style = StcStyle.parse(self.config.get(self.section, self.param))
        if style is None:
            raise ValueError

        return style

    def _prepareToWrite(self, val: StcStyle) -> str:
        return val.tostr()


class DateTimeOption(BaseOption):
    """
    Настройка для хранения даты и времени
    """

    formatDate = "%Y-%m-%d %H:%M:%S.%f"

    def __init__(self, config, section, param, defaultValue):
        super(DateTimeOption, self).__init__(config, section, param, defaultValue)

    def _loadValue(self) -> datetime.datetime:
        strdate = self.config.get(self.section, self.param)
        return datetime.datetime.strptime(strdate, self.formatDate)

    def _prepareToWrite(self, value: datetime.datetime) -> str:
        return datetime.datetime.strftime(value, self.formatDate)


class ListOption(BaseOption):
    """
    Класс для хранения настроек в виде списка.
    По умолчанию элементы разделяются символом ";",
    но разделитель можно изменять
    """

    def __init__(
        self, config, section, param, defaultValue, separator=";", strip=False
    ):
        super().__init__(config, section, param, defaultValue)
        self._separator = separator
        self._strip = strip

    def _loadValue(self) -> List[str]:
        line = self.config.get(self.section, self.param)
        items = line.split(self._separator)
        if self._strip:
            items = [item.strip() for item in items]
        return items

    def _prepareToWrite(self, value: List[str]) -> str:
        if self._strip:
            new_value = [item.strip() for item in value]
        else:
            new_value = value
        return self._separator.join(new_value)


class IntegerOption(BaseOption):
    """
    Настройка для целых чисел.
    Элемент управления - wx.SpinCtrl
    """

    def __init__(self, config, section, param, defaultValue):
        super().__init__(config, section, param, defaultValue)

    def _loadValue(self) -> int:
        """
        Получить значение. В производных классах этот метод переопределяется
        """
        return self.config.getint(self.section, self.param)


class StringListSection:
    """
    Класс для хранения списка строк. Список хранится в отдельной секции
    """

    def __init__(self, config, section, paramname):
        """
        config - экземпляр класса Config
        section - имя секции для хранения списка
        paramname - начало имени параметров, которые будут храниться в секции.
        К paramname будут добавляться порядковые числа.
        """
        self._config = config
        self._section = section
        self._paramname = "%s{number}" % paramname

    def _loadValue(self) -> List[str]:
        if not self._config.has_section(self._section):
            return []

        result = []
        index = 0
        try:
            while 1:
                option = self._paramname.format(number=index)
                subpath = self._config.get(self._section, option)
                result.append(subpath)
                index += 1
        except configparser.NoOptionError:
            pass

        return result

    @property
    def value(self) -> List[str]:
        """
        Возвращает знвчение парамета
        """
        return self._loadValue()

    @value.setter
    def value(self, val: List[str]):
        """
        Устанавливает значение параметра
        """
        self._config.remove_section(self._section)

        for index in range(len(val)):
            option = self._paramname.format(number=index)
            self._config.set(self._section, option, val[index])


class FontOption:
    def __init__(self, faceNameOption, sizeOption, isBoldOption, isItalicOption):
        """
        faceNameOption - экземепляр класса StringOption, где хранится
        значение начертания шрифта
        sizeOption - экземпляр класса IntegerOption, где хранится размер шрифта
        isBoldOption, isItalicOption - экземпляры класса BooleanOption
        """
        self.faceName = faceNameOption
        self.size = sizeOption
        self.bold = isBoldOption
        self.italic = isItalicOption


class PageConfig(Config):
    """
    Класс для хранения настроек страниц
    """

    sectionName = "General"
    orderParamName = "order"
    datetimeParamName = "datetime"
    creationDatetimeParamName = "creationdatetime"
    aliasParamName = "alias"
    iconParamName = "icon"
    typeParamName = "type"
    tagsParamName = "tags"
    titleColorParamName = "titlecolor"

    def __init__(self, fname, readonly=False):
        super().__init__(fname, readonly)

        self.typeOption = StringOption(
            self, PageConfig.sectionName, PageConfig.typeParamName, ""
        )

        self.orderOption = IntegerOption(
            self, PageConfig.sectionName, PageConfig.orderParamName, -1
        )

        self.lastViewedPageOption = StringOption(self, "History", "LastViewedPage", "")

        self.datetimeOption = DateTimeOption(
            self, PageConfig.sectionName, PageConfig.datetimeParamName, None
        )

        self.creationDatetimeOption = DateTimeOption(
            self, PageConfig.sectionName, PageConfig.creationDatetimeParamName, None
        )

        self.aliasOption = StringOption(
            self, PageConfig.sectionName, PageConfig.aliasParamName, ""
        )

        self.iconOption = StringOption(
            self, PageConfig.sectionName, PageConfig.iconParamName, ""
        )

        self.tagsOption = ListOption(
            self,
            PageConfig.sectionName,
            PageConfig.tagsParamName,
            defaultValue=[],
            separator=",",
            strip=True,
        )

        self.titleColorOption = StringOption(
            self, PageConfig.sectionName, PageConfig.titleColorParamName, ""
        )
