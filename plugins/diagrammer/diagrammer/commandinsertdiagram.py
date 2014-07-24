# -*- coding: UTF-8 -*-

import os.path
import hashlib

from outwiker.pages.wiki.parser.command import Command
from outwiker.pages.wiki.thumbnails import Thumbnails


class CommandInsertDiagram (Command):
    """
    Команда (:diagram:) для википарсера
    """
    def __init__ (self, parser):
        """
        parser - экземпляр парсера
        """
        Command.__init__ (self, parser)
        self._diagramNumber = 0
        self._fileNameFormat = u"__diagram_{}"


    @property
    def name (self):
        """
        Возвращает имя команды, которую обрабатывает класс
        """
        return u"diagram"


    def execute (self, params, content):
        """
        Запустить команду на выполнение.
        Метод возвращает текст, который будет вставлен на место команды в вики-нотации
        """
        # params_dict = Command.parseParams (params)
        thumb = Thumbnails(self.parser.page)
        thumbPath = thumb.getThumbPath(True)

        md5 = hashlib.md5 (content).hexdigest()
        fname = self._fileNameFormat.format (md5)
        imagePath = os.path.join (thumbPath, fname)

        self._diagramNumber += 1

        self._createDiagram (content, imagePath)

        return u'<img src="{}/{}"/>'.format (thumb.getRelativeThumbDir(), fname)


    def _createDiagram (self, content, imagePath):
        """
        content - текст, описывающий диаграмму
        imagePath - полный путь до создаваемого файла
        """
        from blockdiag.parser import parse_string
        from blockdiag.drawer import DiagramDraw
        from blockdiag.builder import ScreenNodeBuilder

        tree = parse_string (content)
        diagram = ScreenNodeBuilder.build (tree)

        draw = DiagramDraw ("png", diagram, imagePath)
        draw.draw()
        draw.save()
