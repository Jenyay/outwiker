# -*- coding: utf-8 -*-

from outwiker.pages.wiki.parser.command import Command

from .tocwikimaker import TocWikiMaker


class TOCCommand (Command):
    """
    Вставить оглавление
    """

    def __init__(self, parser, application):
        """
        parser - экземпляр парсера
        """
        Command.__init__(self, parser)
        self._application = application
        self._enabled = True

    @property
    def name(self):
        """
        Возвращает имя команды, которую обрабатывает класс
        """
        return u"toc"

    def execute(self, params, content):
        """
        Запустить команду на выполнение.
        Метод возвращает текст, который будет вставлен на место
        команды в вики-нотации
        """
        if self._enabled:
            # To avoid infinite recursion
            self._enabled = False
            toc = TocWikiMaker(self._application.config).make(
                self._application.selectedPage.content)
            result = self.parser.parseWikiMarkup(toc)
            self._enabled = True
        else:
            result = ''

        return result
