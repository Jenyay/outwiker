# -*- coding: utf-8 -*-

from outwiker.api.pages.wiki.wikiparser import Command


class TitleCommand(Command):
    """
    Команда для вставки тега <title>
    """

    def __init__(self, parser):
        """
        parser - экземпляр парсера
        """
        super().__init__(parser)

    @property
    def name(self):
        """
        Возвращает имя команды, которую обрабатывает класс
        """
        return "title"

    def execute(self, params, content):
        """
        Запустить команду на выполнение.
        Метод возвращает текст, который будет вставлен на место команды
            в вики-нотации
        """
        title = "<title>{}</title>".format(params)
        self.parser.appendToHead(title)
        return ""


class StyleCommand(Command):
    """
    Команда для вставки тега <style>
    """

    def __init__(self, parser):
        """
        parser - экземпляр парсера
        """
        Command.__init__(self, parser)

    @property
    def name(self):
        """
        Возвращает имя команды, которую обрабатывает класс
        """
        return "style"

    def execute(self, params, content):
        """
        Запустить команду на выполнение.
        Метод возвращает текст, который будет вставлен на место команды
            в вики-нотации
        """
        title = "<style>{}</style>".format(content.strip())
        self.parser.appendToHead(title)
        return ""


class DescriptionCommand(Command):
    """
    Команда для вставки тега <meta name="description">
    """

    def __init__(self, parser):
        """
        parser - экземпляр парсера
        """
        Command.__init__(self, parser)

    @property
    def name(self):
        """
        Возвращает имя команды, которую обрабатывает класс
        """
        return "description"

    def execute(self, params, content):
        """
        Запустить команду на выполнение.
        Метод возвращает текст, который будет вставлен на место
            команды в вики-нотации
        """
        head = '<meta name="description" content="{}"/>'.format(params)
        self.parser.appendToHead(head)
        return ""


class KeywordsCommand(Command):
    """
    Команда для вставки тега <meta name="keywords">
    """

    def __init__(self, parser):
        """
        parser - экземпляр парсера
        """
        Command.__init__(self, parser)

    @property
    def name(self):
        """
        Возвращает имя команды, которую обрабатывает класс
        """
        return "keywords"

    def execute(self, params, content):
        """
        Запустить команду на выполнение.
        Метод возвращает текст, который будет вставлен на место
            команды в вики-нотации
        """
        head = '<meta name="keywords" content="{}"/>'.format(params)
        self.parser.appendToHead(head)
        return ""


class CustomHeadsCommand(Command):
    """
    Команда для вставки любых заголовков в тег <head>...</head>
    """

    def __init__(self, parser):
        """
        parser - экземпляр парсера
        """
        Command.__init__(self, parser)

    @property
    def name(self):
        """
        Возвращает имя команды, которую обрабатывает класс
        """
        return "htmlhead"

    def execute(self, params, content):
        """
        Запустить команду на выполнение.
        Метод возвращает текст, который будет вставлен на место
            команды в вики-нотации
        """
        list(
            map(
                lambda head: self.parser.appendToHead(head.strip()), content.split("\n")
            )
        )

        return ""
