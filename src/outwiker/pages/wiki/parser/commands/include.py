# -*- coding: utf-8 -*-

import os.path
import html

from outwiker.pages.wiki.parser.command import Command
from outwiker.core.attachment import Attachment


class IncludeCommand(Command):
    """
    Команда для вставки в текст страницы текста прикрепленного файла
    Синтаксис:(:include Attach:fname [params...] :)
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
        Command.__init__(self, parser)

    @property
    def name(self):
        """
        Возвращает имя команды, которую обрабатывает класс
        """
        return u"include"

    def execute(self, params, content):
        """
        Запустить команду на выполнение.
        Метод возвращает текст, который будет вставлен на место команды
            в вики-нотации
        """
        (path, params_tail) = self._getAttach(params)
        if path is None:
            return u""

        params_dict = Command.parseParams(params_tail)
        encoding = self._getEncoding(params_dict)

        try:
            with open(path, encoding=encoding) as fp:
                # Почему-то в конце всегда оказывается перевод строки
                text = fp.read().rstrip()
        except IOError:
            return _(u"<b>Can't open file %s</b>" % path)
        except Exception:
            return _(u"<b>Encoding error in file %s</b>" % os.path.basename(path))

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
        encoding = u"utf8"
        if "encoding" in params_dict:
            encoding = params_dict["encoding"]

        return encoding

    def _getAttach(self, params):
        """
        Возвращает имя прикрепленного файла, который хотим вставить на
            страницу и хвост параметров после имени файла
        """
        attach_begin = "Attach:"
        params_end = None
        params_tail = params

        # Выделим конец строки после Attach:
        if params.startswith(attach_begin):
            params_end = params[len(attach_begin):]
        else:
            return (None, params_tail)

        attaches = Attachment(self.parser.page).attachmentFull
        attaches.sort(key=len, reverse=True)

        path = None

        for fname in attaches:
            if params_end.startswith(os.path.basename(fname)):
                path = fname
                params_tail = params_end[len(os.path.basename(fname)):]
                break

        return (path, params_tail)
