#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser


class Config (object):
    """
    Оболочка над ConfigParser
    """
    def __init__ (self, fname, readonly=False):
        """
        fname -- имя файла конфига
        """
        self.readonly = readonly
        self.fname = fname
        self.__config = ConfigParser.ConfigParser()

        self.__config.read (self.fname)
    

    def set (self, section, param, value):
        if self.readonly:
            return False

        section_encoded = section.encode ("utf8")
        if not self.__config.has_section (section_encoded):
            self.__config.add_section (section_encoded)

        self.__config.set (section_encoded, param.encode ("utf8"), unicode (value).encode ("utf8"))

        return self.save()


    def save (self):
        if self.readonly:
            return False

        with open (self.fname, "wb") as fp:
            self.__config.write (fp)

        return True
    
    
    def get (self, section, param):
        val = self.__config.get (section.encode ("utf8"), param.encode ("utf8"))
        return unicode (val, "utf8", "replace")

    
    def getint (self, section, param):
        return int (self.__config.get (section.encode ("utf8"), param.encode ("utf8")))

    def getbool (self, section, param):
        val = self.__config.get (section.encode ("utf8"), param.encode ("utf8"))

        return True if val.strip().lower() == "true" else False


    def remove_section (self, section):
        section_encoded = section.encode ("utf8")
        result1 = self.__config.remove_section (section_encoded)
        result2 = self.save()

        return result1 and result2


    def remove_option (self, section, option):
        section_encoded = section.encode ("utf8")
        option_encoded = option.encode ("utf8")

        result1 = self.__config.remove_option (section_encoded, option_encoded)
        result2 = self.save()

        return result1 and result2


    def has_section (self, section):
        section_encoded = section.encode ("utf8")
        return self.__config.has_section (section_encoded)


class StringOption (object):
    def __init__ (self, config, section, param, defaultValue):
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
        # Т.к. как правило исключения игнорируются, то это поле используется для отладкиы
        self.error = None


    def _loadParam (self):
        try:
            val = self._loadValue()
        except Exception as e:
            self.error = e
            val = self.defaultValue

        return val


    def _loadValue (self):
        """
        Получить значение. В производных классах этот метод переопределяется
        """
        return self.config.get (self.section, self.param)


    @property
    def value (self):
        return self._loadParam ()


    @value.setter
    def value (self, val):
        self.config.set (self.section, self.param, val)


    def remove_option (self):
        self.config.remove_option (self.section, self.param)


class BooleanOption (StringOption):
    """
    Булевская настройка.
    Элемент управления - wx.CheckBox
    """
    def __init__ (self, config, section, param, defaultValue):
        StringOption.__init__ (self, config, section, param, defaultValue)


    def _loadValue (self):
        """
        Получить значение. В производных классах этот метод переопределяется
        """
        return self.config.getbool (self.section, self.param)


class ListOption (StringOption):
    """
    Класс для хранения настроек в виде списка. По умолчанию элементы разделяются символом ";", но разделитель можно изменять
    """
    def __init__ (self, config, section, param, defaultValue, separator=";"):
        StringOption.__init__ (self, config, section, param, defaultValue)
        self.__separator = separator


    def _loadValue (self):
        line = self.config.get (self.section, self.param)
        items = line.split (self.__separator)
        return items


    @property
    def value (self):
        return self._loadParam ()


    @value.setter
    def value (self, val):
        line = self.__separator.join (val)
        self.config.set (self.section, self.param, line)


class IntegerOption (StringOption):
    """
    Настройка для целых чисел.
    Элемент управления - wx.SpinCtrl
    """
    def __init__ (self, config, section, param, defaultValue):
        StringOption.__init__ (self, config, section, param, defaultValue)


    def _loadValue (self):
        """
        Получить значение. В производных классах этот метод переопределяется
        """
        return self.config.getint (self.section, self.param)


class FontOption (object):
    def __init__ (self, 
            faceNameOption, 
            sizeOption,
            isBoldOption,
            isItalicOption):
        """
        faceNameOption - экземепляр класса StringOption, где хранится значение начертания шрифта
        sizeOption - экземпляр класса IntegerOption, где хранится размер шрифта
        isBoldOption, isItalicOption - экземпляры класса BooleanOption
        """
        self.faceName = faceNameOption
        self.size = sizeOption
        self.bold = isBoldOption
        self.italic = isItalicOption


class PageConfig (Config):
    """
    Класс для хранения настроек страниц
    """
    sectionName = u"General"
    orderParamName = u"order"

    def __init__ (self, fname, readonly=False):
        Config.__init__ (self, fname, readonly)

        self.typeOption = StringOption (self, PageConfig.sectionName, u"type", u"")
        self.orderOption = IntegerOption (self, PageConfig.sectionName, PageConfig.orderParamName, -1)
        self.lastViewedPageOption = StringOption (self,u"History", u"LastViewedPage", u"")

