# -*- coding: utf-8 -*-

import html
import os.path
import re
from pathlib import Path

from outwiker.core.attachment import Attachment
from outwiker.pages.wiki.parser.command import Command
from outwiker.pages.wiki.parser.attachregex import (attach_regex_no_spaces,
                                                    attach_regex_with_spaces)


class IncludeCommand(Command):
    """
    Команда для вставки в текст страницы текста прикрепленного файла
    Синтаксис: (:include Attach:"fname" [params...] :)
    params - необязательные параметры:
        encoding="xxx" - указывает кодировку прикрепленного файла
        htmlescape - заменить символы <, > и т.п. на их HTML-аналоги
            (&lt;, &gt; и т.п.)
        wikiparse - содержимое прикрепленного файла предварительно нужно
            пропустить через википарсер
    """
    def __init__(self, parser):
        """
        parser - экземпляр парсера
        """
        super().__init__(parser)
        self._attach_regex_no_spaces = re.compile('Attach:(?P<fname>{})'.format(attach_regex_no_spaces))
        self._attach_regex_with_spaces = re.compile('Attach:([\'"])(?P<fname>{})\\1'.format(attach_regex_with_spaces))
        self._error_format = '<div class="ow-wiki ow-error ow-wiki-include">{message}</div>'

    @property
    def name(self):
        """
        Возвращает имя команды, которую обрабатывает класс
        """
        return "include"

    def execute(self, params, content):
        """
        Запустить команду на выполнение.
        Метод возвращает текст, который будет вставлен на место команды
            в вики-нотации
        """
        (fname, params_tail) = self._getAttach(params)
        if fname is None:
            return ''

        attach = Attachment(self.parser.page)
        fname_full_path = Path(attach.getAttachPath(create=False), fname)

        params_dict = Command.parseParams(params_tail)
        encoding = self._getEncoding(params_dict)

        try:
            with open(fname_full_path, encoding=encoding) as fp:
                # Почему-то в конце всегда оказывается перевод строки
                text = fp.read().rstrip()
        except IOError:
            error_message = "Can't open file '{}'".format(fname)
            return _(self._error_format.format(message=error_message))
        except Exception:
            error_message = "Encoding error in file '{}'".format(fname)
            return _(self._error_format.format(message=error_message))

        return self._postprocessText(text, params_dict)

    def _postprocessText(self, text, params_dict):
        """
        Выполнить манипуляции согласно настройкам с прочитанным текстом
        """
        result = text

        if "htmlescape" in params_dict:
            result = html.escape(text, False)

        if "wikiparse" in params_dict:
            result = self.parser.parseWikiMarkup(result)

        return result

    def _getEncoding(self, params_dict):
        encoding = "utf8"
        if "encoding" in params_dict:
            encoding = params_dict["encoding"]

        return encoding

    def _getAttach(self, params_str: str):
        """
        Возвращает имя прикрепленного файла, который хотим вставить на
            страницу и хвост параметров после имени файла
        """
        match = self._attach_regex_no_spaces.match(params_str)
        if match is None:
            match = self._attach_regex_with_spaces.match(params_str)

        if match is None:
            return (None, params_str)

        fname = match.group('fname').replace('\\', '/')
        tail = params_str[match.end():]
        return (fname, tail)
