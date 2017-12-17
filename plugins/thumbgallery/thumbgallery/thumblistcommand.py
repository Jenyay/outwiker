# -*- coding: UTF-8 -*-

from outwiker.pages.wiki.parser.command import Command
from outwiker.core.attachment import Attachment
from outwiker.pages.wiki.wikiconfig import WikiConfig

from .thumbstreamgenerator import ThumbStreamGenerator
from .thumbtablegenerator import ThumbTableGenerator
from .utilites import isImage


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
        paramsDict = Command.parseParams (params)
        thumbsize = self._getThumbSize(paramsDict)
        columnsCount = self._getColumnsCount(paramsDict)

        lineItems = self._parseContent (content)

        if columnsCount == 0:
            generator = ThumbStreamGenerator (lineItems, thumbsize, self.parser)
        else:
            generator = ThumbTableGenerator (lineItems, thumbsize, self.parser, columnsCount)

        return generator.generate()


    def _parseContent (self, content):
        attach = Attachment (self.parser.page)

        filesList = self._getLinesItems (content)
        allFiles = attach.getAttachRelative()
        allFiles.sort()

        if len (content) == 0:
            files = [(fname, u"") for fname in allFiles if isImage (fname)]
        else:
            files = [lineitem for lineitem
                     in filesList
                     if isImage (lineitem[0]) and lineitem[0] in allFiles]

        return files


    def _getLinesItems (self, content):
        """
        Возвращает список файлов и комментариев к ним, перечисленных в теле команды.
        Возвращает список кортежей: (имя файла, комментарий)
        """
        def _removeAttach (line):
            """
            Удалить фразу "Attach:" в начале строки
            """
            attachPhrase = u"attach:"
            return line[len (attachPhrase):] if line.lower().startswith (attachPhrase) else line

        lines = [self._splitLine (_removeAttach (fname.strip()))
                 for fname in content.split(u"\n")
                 if len (fname.strip()) != 0]

        return lines


    def _splitLine (self, line):
        """
        Из строки в формате "Имя файла | Комментарий" делает кортеж (Имя файла, Комментарий)
        """
        splitItems = line.rsplit ("|", 1)
        if len (splitItems) > 1:
            result = (splitItems[0].strip(), splitItems[1].strip())
        else:
            result = (line, u"")

        return result


    def _getColumnsCount (self, paramsDict):
        """
        Возвращает количество столбцов для таблицы
        """
        paramname = "cols"
        cols = 0

        try:
            cols = int (paramsDict[paramname])
        except KeyError:
            pass
        except ValueError:
            pass

        return cols


    def _getThumbSize (self, paramsDict):
        sizeParamName1 = "px"
        sizeParamName2 = "maxsize"

        if sizeParamName1 in list(paramsDict.keys()):
            thumbsize = paramsDict[sizeParamName1]
        elif sizeParamName2 in list(paramsDict.keys()):
            thumbsize = paramsDict[sizeParamName2]
        else:
            config = WikiConfig (self.parser.config)
            thumbsize = config.thumbSizeOptions.value

        return thumbsize
