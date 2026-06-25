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
            Save changes.
            Returns True if save was successful and False otherwise.
        """
        if self.readonly:
            return False

        with open(self.fname, "w", encoding="utf8") as fp:
            self._config.write(fp)

        return True

    def remove_section(self, section):
        """
            Remove section from config file.
            section - name of the section to remove.
        """
        result = self._config.remove_section(section) and self.save()
        return result

    def remove_option(self, section, option):
        """
            Remove option from config file.
            section - name of the section that contains the option.
            option - name of the option to remove.
        """
        result = self._config.remove_option(section, option) and self.save()
        return result

    def getbool(self, section, param):
        """
            Get boolean value from config.
            section - section name in config file.
            param - parameter name.
            Returns string with the read value.
            Can raise exceptions.
        """
        val = self.get(section, param)

        return True if val.strip().lower() == "true" else False


class BaseOption(metaclass=ABCMeta):
    """
    Base class for working with individual config entries
    """

    def __init__(self, config, section, param, defaultValue):
        """
        config - instance of core.Config class
        section - section for config parameter
        param - config parameter name
        defaultValue - default value
        """
        self.config = config
        self.section = section
        self.param = param
        self.defaultValue = defaultValue

        # Pointer to the last exception
        # Generally exceptions are ignored,
        # so this field is used for debugging
        self.error = None

    def remove_option(self):
        """
        Remove the setting
        """
        self.config.remove_option(self.section, self.param)

    @property
    def value(self):
        """
        Returns the parameter value
        """
        return self._loadParam()

    @value.setter
    def value(self, val):
        """
        Sets the parameter value
        """
        self.config.set(self.section, self.param, self._prepareToWrite(val))

    @abstractmethod
    def _loadValue(self):
        """
        Method should read from config the parameter self.param from section
        self.section and return the value.
        Exceptions can be ignored since they are caught above
        in the _loadParam method
        """
        pass

    def _prepareToWrite(self, val) -> str:
        """
        Convert (if needed) the value to the form in which it will be
        written to the config
        """
        return val

    def _loadParam(self):
        """
        Returns the value read from config or the default value
        """
        try:
            val = self._loadValue()
        except Exception as e:
            self.error = e
            val = self.defaultValue

        return val


class StringOption(BaseOption):
    """
    Class for working with string options
    """

    def __init__(self, config, section, param, defaultValue):
        super().__init__(config, section, param, defaultValue)

    def _loadValue(self) -> str:
        """
        Get the value
        """
        return self.config.get(self.section, self.param)


class BooleanOption(BaseOption):
    """
    Boolean option.
    Control element - wx.CheckBox
    """

    def _loadValue(self) -> bool:
        """
        Get the value
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
    Option for storing StcStyledEditor style
    """

    def __init__(self, config, section, param, defaultValue):
        """
        defaultValue - instance of StcStyle class
        """
        super().__init__(config, section, param, defaultValue)

    def _loadValue(self) -> StcStyle:
        """
        Get the value. This method can be overridden in derived classes
        """
        style = StcStyle.parse(self.config.get(self.section, self.param))
        if style is None:
            raise ValueError

        return style

    def _prepareToWrite(self, val: StcStyle) -> str:
        return val.tostr()


class DateTimeOption(BaseOption):
    """
    Option for storing date and time
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
    Class for storing settings as a list.
    By default, elements are separated by the ";" character,
    but the separator can be changed.
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
    Option for integer values.
    Control element - wx.SpinCtrl
    """

    def __init__(self, config, section, param, defaultValue):
        super().__init__(config, section, param, defaultValue)

    def _loadValue(self) -> int:
        """
        Get the value. This method can be overridden in derived classes.
        """
        return self.config.getint(self.section, self.param)


class StringListSection:
    """
    Class for storing a list of strings. The list is stored in a separate section.
    """

    def __init__(self, config, section, paramname):
        """
        config - instance of Config class
        section - name of the section for storing the list
        paramname - beginning of the parameter name that will be stored in the section.
        Sequential numbers will be added to paramname.
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
        Returns the parameter value
        """
        return self._loadValue()

    @value.setter
    def value(self, val: List[str]):
        """
        Sets the parameter value
        """
        self._config.remove_section(self._section)

        for index in range(len(val)):
            option = self._paramname.format(number=index)
            self._config.set(self._section, option, val[index])


class FontOption:
    def __init__(self, faceNameOption, sizeOption, isBoldOption, isItalicOption):
        """
        faceNameOption - instance of StringOption class that stores the font face name
        sizeOption - instance of IntegerOption class that stores the font size
        isBoldOption, isItalicOption - instances of BooleanOption class
        """
        self.faceName = faceNameOption
        self.size = sizeOption
        self.bold = isBoldOption
        self.italic = isItalicOption


class PageConfig(Config):
    """
    Class for storing page settings
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
    pageUidParamName = "uid"

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

        self.pageUidOption = StringOption(
            self, PageConfig.sectionName, PageConfig.pageUidParamName, None
        )
