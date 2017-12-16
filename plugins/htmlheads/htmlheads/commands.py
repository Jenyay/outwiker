# -*- coding: UTF-8 -*-

from outwiker.pages.wiki.parser.command import Command


class TitleCommand (Command):
    """
    Команда для вставки тега <title>
    """
    def __init__ (self, parser):
        """
        parser - экземпляр парсера
        """
        Command.__init__ (self, parser)


    @property
    def name (self):
        """
        Возвращает имя команды, которую обрабатывает класс
        """
        return u"title"


    def execute (self, params, content):
        """
        Запустить команду на выполнение.
        Метод возвращает текст, который будет вставлен на место команды в вики-нотации
        """
        title = u"<title>{}</title>".format (params)
        self.parser.appendToHead (title)
        return u""


class DescriptionCommand (Command):
    """
    Команда для вставки тега <meta name="description">
    """
    def __init__ (self, parser):
        """
        parser - экземпляр парсера
        """
        Command.__init__ (self, parser)


    @property
    def name (self):
        """
        Возвращает имя команды, которую обрабатывает класс
        """
        return u"description"


    def execute (self, params, content):
        """
        Запустить команду на выполнение.
        Метод возвращает текст, который будет вставлен на место команды в вики-нотации
        """
        head = u'<meta name="description" content="{}"/>'.format (params)
        self.parser.appendToHead (head)
        return u""


class KeywordsCommand (Command):
    """
    Команда для вставки тега <meta name="keywords">
    """
    def __init__ (self, parser):
        """
        parser - экземпляр парсера
        """
        Command.__init__ (self, parser)


    @property
    def name (self):
        """
        Возвращает имя команды, которую обрабатывает класс
        """
        return u"keywords"


    def execute (self, params, content):
        """
        Запустить команду на выполнение.
        Метод возвращает текст, который будет вставлен на место команды в вики-нотации
        """
        head = u'<meta name="keywords" content="{}"/>'.format (params)
        self.parser.appendToHead (head)
        return u""


class CustomHeadsCommand (Command):
    """
    Команда для вставки любых заголовков в тег <head>...</head>
    """
    def __init__ (self, parser):
        """
        parser - экземпляр парсера
        """
        Command.__init__ (self, parser)


    @property
    def name (self):
        """
        Возвращает имя команды, которую обрабатывает класс
        """
        return u"htmlhead"


    def execute (self, params, content):
        """
        Запустить команду на выполнение.
        Метод возвращает текст, который будет вставлен на место команды в вики-нотации
        """
        list(map (lambda head: self.parser.appendToHead (head.strip()),
             content.split ("\n")))

        return u""
