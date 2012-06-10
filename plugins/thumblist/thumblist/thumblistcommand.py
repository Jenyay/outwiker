#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os.path

from outwiker.pages.wiki.parser.command import Command
from outwiker.core.attachment import Attachment
from outwiker.pages.wiki.wikiconfig import WikiConfig

from .thumbstreamgenerator import ThumbStreamGenerator


class ThumbListCommand (Command):
    """
    Викикоманда, добавляющая стили к заголовку страницы
    Использование:

    (:thumblist параметры:)
    Список файлов
    (:thumblistend:)
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
        return u"thumblist"


    def execute (self, params, content):
        """
        Запустить команду на выполнение. 
        Метод возвращает текст, который будет вставлен на место команды в вики-нотации
        """
        # paramsDict = Command.parseParams (params)
        thumbsize = self._getThumbSize();
        files = self._getFiles (content)

        generator = ThumbStreamGenerator (files, thumbsize, self.parser)
        return generator.generate()


    def _getFiles (self, content):
        attach = Attachment (self.parser.page)

        filesList = self._getFilesList (content)
        allFiles = attach.getAttachRelative()

        if len (content) == 0:
            files = [fname for fname in allFiles if self._isImage (fname)]
        else:
            files = [fname for fname in filesList if self._isImage (fname) and fname in allFiles]

        return files


    def _getFilesList (self, content):
        """
        Возвращает список файлов, перечисленных в теле команды
        """
        def _removeAttach (line):
            """
            Удалить фразу "Attach:" в начале строки
            """
            attachPhrase = u"attach:"
            return line[len (attachPhrase):] if line.lower().startswith (attachPhrase) else line

        files = [_removeAttach (fname) for fname in content.split() if len (fname.strip()) != 0]
        return files


    def _isImage (self, fname):
        """
        Возвращает True, если fname - картинка
        """
        fnameLower = fname.lower()

        return (fnameLower.endswith (".png") or
                fnameLower.endswith (".jpg") or
                fnameLower.endswith (".jpeg") or
                fnameLower.endswith (".bmp") or
                fnameLower.endswith (".gif"))


    def _getThumbSize (self):
        config = WikiConfig (self.parser.config)
        return config.thumbSizeOptions.value
