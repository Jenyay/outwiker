# -*- coding: UTF-8 -*-

import os
import os.path

from outwiker.core.system import getOS


class DiagramRender (object):
    """
    Класс для создания диаграмм с помощью blockdiag
    """
    def __init__ (self):
        self._fontDefault = u"Ubuntu-R.ttf"


    @staticmethod
    def _initPackage (packagename, modulename):
        """
        Инициализировать пакет с рендерами узлов
        packagename - например, "blockdiag.noderenderer", а modulename - "circle"
        """
        packageFullName = ".".join ([packagename, modulename])

        # Импортируем модуль, чтобы узнать полное имя файла до него
        try:
            rootmodule = __import__ (packageFullName, fromlist=[modulename])
        except (ImportError, ValueError):
            return

        if rootmodule is None:
            return

        path = unicode (os.path.dirname(os.path.abspath(rootmodule.__file__)),
                        getOS().filesEncoding)

        extension = ".py"

        # Перебираем все модули внутри пакета
        for fname in os.listdir (path):
            fullpath = os.path.join (path, fname)

            # Все папки пытаемся открыть как вложенный пакет
            if os.path.isdir (fullpath):
                DiagramRender._initPackage (packageFullName, fname.encode (getOS().filesEncoding))
            else:
                # Проверим, что файл может быть модулем
                if fname.endswith (extension) and fname != "__init__.py":
                    nestedmodulename = fname[: -len (extension)]
                    # Попытаться импортировать функцию setup из модуля
                    try:
                        currentmodulename = packageFullName + "." + nestedmodulename
                        module = __import__ (currentmodulename, fromlist=["setup"])
                    except ImportError:
                        continue

                    try:
                        module.setup(module)
                    except AttributeError:
                        continue


    @staticmethod
    def initialize ():
        """
        Инициализировать blockdiag. Нужно вызывать хотя бы один раз за время работы программы до рендеринга диаграмм.
        """
        DiagramRender._initPackage ("blockdiag", "noderenderer")

        from blockdiag.imagedraw.png import setup
        setup(None)


    def renderToFile (self, content, imagePath):
        """
        content - текст, описывающий диаграмму
        imagePath - полный путь до создаваемого файла
        """
        from blockdiag.parser import parse_string
        from blockdiag.drawer import DiagramDraw
        from blockdiag.builder import ScreenNodeBuilder
        from blockdiag.utils.fontmap import FontMap

        font = os.path.join (unicode (os.path.dirname(os.path.abspath(__file__)),
                                      getOS().filesEncoding),
                             u"fonts", self._fontDefault)

        fontmap = FontMap()
        fontmap.set_default_font (font)

        text = u"blockdiag {{ {content} }}".format (content=content)

        tree = parse_string (text)
        diagram = ScreenNodeBuilder.build (tree)

        draw = DiagramDraw ("png", diagram, imagePath, fontmap=fontmap, antialias=True)
        draw.draw()
        draw.save()
