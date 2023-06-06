# -*- coding: utf-8 -*-

from pathlib import Path
from typing import List, Tuple

from outwiker.api.core.attachment import Attachment
from outwiker.api.core.images import isImage
from outwiker.api.pages.wiki.config import WikiConfig
from outwiker.api.pages.wiki.wikiparser import Command

from .thumbstreamgenerator import ThumbStreamGenerator
from .thumbtablegenerator import ThumbTableGenerator


class ThumbListCommand(Command):
    """
    Викикоманда, добавляющая стили к заголовку страницы
    Использование:

    (:thumblist параметры:)
    Список файлов
    (:thumblistend:)
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
        return "thumblist"

    def execute(self, params, content):
        """
        Запустить команду на выполнение.
        Метод возвращает текст, который будет
        вставлен на место команды в вики-нотации
        """
        paramsDict = Command.parseParams(params)
        thumbsize = self._getThumbSize(paramsDict)
        columnsCount = self._getColumnsCount(paramsDict)

        lineItems = self._parseContent(content)

        if columnsCount == 0:
            generator = ThumbStreamGenerator(lineItems, thumbsize, self.parser)
        else:
            generator = ThumbTableGenerator(
                lineItems, thumbsize, self.parser, columnsCount
            )

        return generator.generate()

    def _parseContent(self, content):
        attach = Attachment(self.parser.page)
        root_dir = attach.getAttachPath(create=False)

        filesList = [
            (item[0].replace("\\", "/"), item[1])
            for item in self._getLinesItems(content)
        ]
        allFiles = attach.getAttachRelative()
        allFiles.sort()

        if len(content) == 0:
            files = [(fname, "") for fname in allFiles if isImage(fname)]
        else:
            files = [
                lineitem
                for lineitem in filesList
                if isImage(lineitem[0]) and Path(root_dir, lineitem[0]).exists()
            ]

        return files

    def _getLinesItems(self, content):
        """
        Возвращает список файлов и комментариев к ним,
        перечисленных в теле команды.
        Возвращает список кортежей: (имя файла, комментарий)
        """

        def _removeAttach(line):
            """
            Remove "Attach:" notation
            """
            attachPhrase = "attach:"
            if line.lower().startswith(attachPhrase):
                line = line[len(attachPhrase) :]

            return line

        lines = []
        for line in content.split("\n"):
            if len(line.strip()) != 0:
                items = self._parse_line(_removeAttach(line.strip()))
                lines.extend(items)

        return lines

    def _parse_line(self, line: str) -> List[Tuple[str, str]]:
        """
        Из строки в формате "Имя файла | Комментарий" делает список кортежей
        (Имя файла, Комментарий)
        """
        # Extract comment
        splitItems = line.rsplit("|", 1)
        if len(splitItems) > 1:
            fname = splitItems[0].strip()
            comment = splitItems[1].strip()
        else:
            fname = line
            comment = ""

        fname = fname.replace("\\", "/")

        # Remove quotes
        if fname.startswith('"') and fname.endswith('"'):
            fname = fname[1:-1]

        if fname.startswith("'") and fname.endswith("'"):
            fname = fname[1:-1]

        # Extract files by mask
        files = self._getFilesByMask(fname)
        return [(fname, comment) for fname in files]

    def _getFilesByMask(self, mask: str) -> List[str]:
        attach = Attachment(self.parser.page)
        root_dir = Path(attach.getAttachPath(create=False))
        if not root_dir.exists():
            return []

        glob_result = root_dir.glob(mask)
        glob_images_relative = [
            fname.relative_to(root_dir) for fname in glob_result if isImage(fname)
        ]

        glob_filter = [
            str(fname)
            for fname in glob_images_relative
            if (not str(fname).startswith("__") or str(fname) == fname.name)
        ]

        return glob_filter

    def _getColumnsCount(self, paramsDict):
        """
        Возвращает количество столбцов для таблицы
        """
        paramname = "cols"
        cols = 0

        try:
            cols = int(paramsDict[paramname])
        except KeyError:
            pass
        except ValueError:
            pass

        return cols

    def _getThumbSize(self, paramsDict):
        sizeParamName1 = "px"
        sizeParamName2 = "maxsize"

        if sizeParamName1 in paramsDict:
            thumbsize = paramsDict[sizeParamName1]
        elif sizeParamName2 in paramsDict:
            thumbsize = paramsDict[sizeParamName2]
        else:
            config = WikiConfig(self.parser.config)
            thumbsize = config.thumbSizeOptions.value

        return thumbsize
