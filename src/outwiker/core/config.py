#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import datetime


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
        """
        Установить значение параметра.
        section - имя секции в файле конфига
        param - имя параметра
        value - устанавливаемое значение
        """
        if self.readonly:
            return False

        section_encoded = section.encode ("utf8")
        if not self.__config.has_section (section_encoded):
            self.__config.add_section (section_encoded)

        self.__config.set (section_encoded, 
                param.encode ("utf8"), 
                unicode (value).encode ("utf8"))

        return self.save()


    def save (self):
        """
        Сохранить изменения
        Возвращает True, если сохранение прошло успешно и False в противном случае
        """
        if self.readonly:
            return False

        with open (self.fname, "wb") as fp:
            self.__config.write (fp)

        return True


    def get (self, section, param):
        """
        Получить значение из конфига
        section - имя секции файла конфига
        param - имя параметра
        Возващает строку с прочитанным значением
        Может бросать исключения
        """
        val = self.__config.get (section.encode ("utf8"), 
                param.encode ("utf8"))
        return unicode (val, "utf8", "replace")

    
    def getint (self, section, param):
        """
        Получить целочисленное значение из конфига
        section - имя секции файла конфига
        param - имя параметра
        Возващает строку с прочитанным значением
        Может бросать исключения
        """
        return int (self.get (section, param))


    def getbool (self, section, param):
        """
        Получить булево значение из конфига
        section - имя секции файла конфига
        param - имя параметра
        Возващает строку с прочитанным значением
        Может бросать исключения
        """
        val = self.get (section, param)

        return True if val.strip().lower() == "true" else False


    def remove_section (self, section):
        """
        Удалить текцию из файла конфига
        section - имя удаляемой секции
        """
        section_encoded = section.encode ("utf8")
        result1 = self.__config.remove_section (section_encoded)
        result2 = self.save()

        return result1 and result2


    def remove_option (self, section, option):
        """
        Удалить настройку из файла конфига
        section - имя секции, которой принадлежит опция
        option - имя удаляемой опции
        """
        section_encoded = section.encode ("utf8")
        option_encoded = option.encode ("utf8")

        result1 = self.__config.remove_option (section_encoded, 
                option_encoded)

        result2 = self.save()

        return result1 and result2


    def has_section (self, section):
        """
        Возврщает True, если векция с именем section существует или False в противном случае
        """
        section_encoded = section.encode ("utf8")
        return self.__config.has_section (section_encoded)


class StringOption (object):
    """
    Класс для упрощения работы со строковыми опциями
    """
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
        # Как правило исключения игнорируются, 
        # поэтому это поле используется для отладки
        self.error = None


    def _loadParam (self):
        """
        Возващает прочитанное из конфига значение или значение по умолчанию
        """
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
        """
        Возвращает знвчение парамета
        """
        return self._loadParam ()


    @value.setter
    def value (self, val):
        """
        Устанавливает значение параметра
        """
        self.config.set (self.section, self.param, self._prepareToWrite (val) )


    def _prepareToWrite (self, val):
        """
        Преобразовать (если надо) значение к виду, в котором оно будет записано в конфиг
        """
        return val


    def remove_option (self):
        """
        Удалить настройку
        """
        self.config.remove_option (self.section, self.param)


class BooleanOption (StringOption):
    """
    Булевская настройка.
    Элемент управления - wx.CheckBox
    """
    def __init__ (self, config, section, param, defaultValue):
        super (BooleanOption, self).__init__ (config, section, param, defaultValue)


    def _loadValue (self):
        """
        Получить значение. В производных классах этот метод переопределяется
        """
        return self.config.getbool (self.section, self.param)


class DateTimeOption (StringOption):
    """
    Настройка для хранения даты и времени
    """
    formatDate = "%Y-%m-%d %H:%M:%S.%f"

    def __init__ (self, config, section, param, defaultValue):
        super (DateTimeOption, self).__init__ (config, section, param, defaultValue)


    def _loadValue (self):
        strdate = self.config.get (self.section, self.param)

        try:
            date = datetime.datetime.strptime (strdate, self.formatDate)
        except ValueError:
            return self.defaultValue

        return date


    @property
    def value (self):
        return self._loadParam ()


    @value.setter
    def value (self, date):
        val = datetime.datetime.strftime (date, self.formatDate)
        self.config.set (self.section, self.param, val)


class ListOption (StringOption):
    """
    Класс для хранения настроек в виде списка. По умолчанию элементы разделяются символом ";", но разделитель можно изменять
    """
    def __init__ (self, config, section, param, defaultValue, separator=";"):
        super (ListOption, self).__init__ (config, section, param, defaultValue)
        self.__separator = separator


    def _loadValue (self):
        line = self.config.get (self.section, self.param)
        items = line.split (self.__separator)
        return items


    def _prepareToWrite (self, value):
        return self.__separator.join (value)


class IntegerOption (StringOption):
    """
    Настройка для целых чисел.
    Элемент управления - wx.SpinCtrl
    """
    def __init__ (self, config, section, param, defaultValue):
        super (IntegerOption, self).__init__ (config, section, param, defaultValue)


    def _loadValue (self):
        """
        Получить значение. В производных классах этот метод переопределяется
        """
        return self.config.getint (self.section, self.param)


class StringListSection (object):
    """
    Класс для хранения списка строк. Список хранится в отдельной секции
    """
    def __init__ (self, config, section, paramname):
        """
        config - экземпляр класса Config
        section - имя секции для хранения списка
        paramname - начало имени параметров, которые будут храниться в секции. К paramname будут добавляться порядковые числа.
        """
        self._config = config
        self._section = section
        self._paramname = u"%s{number}" % paramname


    def _loadValue (self):
        if not self._config.has_section (self._section):
            return []

        result = []
        index = 0
        try:
            while (1):
                option = self._paramname.format (number=index)
                subpath = self._config.get (self._section, option)
                result.append (subpath)
                index += 1
        except ConfigParser.NoOptionError:
            pass

        return result


    @property
    def value (self):
        """
        Возвращает знвчение парамета
        """
        return self._loadValue ()


    @value.setter
    def value (self, val):
        """
        Устанавливает значение параметра
        """
        self._config.remove_section (self._section)

        for index in range (len (val)):
            option = self._paramname.format (number=index)
            self._config.set (self._section, option, val[index])


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
    datetimeParamName = u"datetime"

    def __init__ (self, fname, readonly=False):
        Config.__init__ (self, fname, readonly)

        self.typeOption = StringOption (self, 
                PageConfig.sectionName, 
                u"type", u"")

        self.orderOption = IntegerOption (self, 
                PageConfig.sectionName, 
                PageConfig.orderParamName, -1)

        self.lastViewedPageOption = StringOption (self, 
                u"History", 
                u"LastViewedPage", 
                u"")

        self.datetimeOption = DateTimeOption (self, 
                PageConfig.sectionName, 
                PageConfig.datetimeParamName, 
                None)

