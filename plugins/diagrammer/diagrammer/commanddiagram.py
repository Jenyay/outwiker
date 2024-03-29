# -*- coding: utf-8 -*-

import os.path
import hashlib

from outwiker.api.pages.wiki.wikiparser import Command
from outwiker.api.core.attachment import Thumbnails

from .i18n import get_
from .diagramrender import DiagramRender


class CommandDiagram(Command):
    """
    Команда (:diagram:) для википарсера
    """

    def __init__(self, parser):
        """
        parser - экземпляр парсера
        """
        Command.__init__(self, parser)
        self._fileNameFormat = "__diagram_{}.png"

        global _
        _ = get_()

    @property
    def name(self):
        """
        Возвращает имя команды, которую обрабатывает класс
        """
        return "diagram"

    def execute(self, params, content):
        """
        Запустить команду на выполнение.
        Метод возвращает текст, который будет вставлен на место команды в вики-нотации
        """
        from blockdiag.parser import ParseException

        thumb = Thumbnails(self.parser.page)
        thumbPath = thumb.getThumbPath(True)

        md5 = hashlib.md5(content.encode("utf-8")).hexdigest()
        fname = self._fileNameFormat.format(md5)
        imagePath = os.path.join(thumbPath, fname)

        render = DiagramRender()

        if not os.path.exists(imagePath):
            try:
                render.renderToFile(content, imagePath)
            except (ParseException, AttributeError, TypeError):
                return "<b>{}</b>".format(_("Diagram parsing error"))

        return '<img src="{}/{}"/>'.format(thumb.getRelativeThumbDir(), fname)
