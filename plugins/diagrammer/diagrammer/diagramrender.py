# -*- coding: utf-8 -*-

import os
import os.path


class DiagramRender(object):
    """
    Класс для создания диаграмм с помощью blockdiag
    """
    # Список возможных фигур
    shapes = []

    def __init__(self):
        self._fontDefault = "mplus-2p-regular.ttf"

    @classmethod
    def _initPackage(cls, packagename, modulename):
        """
        Инициализировать пакет с рендерами узлов
        packagename - например, "blockdiag.noderenderer",
            а modulename - "circle"
        """
        packageFullName = ".".join([packagename, modulename])

        # Импортируем модуль, чтобы узнать полное имя файла до него
        try:
            rootmodule = __import__(packageFullName, fromlist=[modulename])
        except (ImportError, ValueError):
            return

        if (rootmodule is None or
                not hasattr(rootmodule, '__file__')
                or rootmodule.__file__ is None):
            return

        try:
            path = os.path.dirname(os.path.abspath(rootmodule.__file__))
        except AttributeError:
            return

        extension = ".py"

        # Перебираем все модули внутри пакета
        for fname in os.listdir(path):
            fullpath = os.path.join(path, fname)

            # Все папки пытаемся открыть как вложенный пакет
            if os.path.isdir(fullpath):
                DiagramRender._initPackage(packageFullName, fname)
            else:
                # Проверим, что файл может быть модулем
                if fname.endswith(extension) and fname != "__init__.py":
                    nestedmodulename = fname[: -len(extension)]
                    # Попытаться импортировать функцию setup из модуля
                    try:
                        currentmodulename = packageFullName + "." + nestedmodulename
                        module = __import__(currentmodulename, fromlist=["setup"])
                    except ImportError:
                        continue

                    try:
                        module.setup(module)
                    except AttributeError:
                        continue

                    cls._addShape(packageFullName + "." + nestedmodulename)

    @classmethod
    def _addShape(cls, modulename):
        """
        Добавить фигуру в shapes по имени модуля
        """
        parent = "blockdiag.noderenderer."

        assert parent in modulename

        cls.shapes.append(modulename[len(parent):])

    @classmethod
    def initialize(cls):
        """
        Инициализировать blockdiag. Нужно вызывать хотя бы один раз
            за время работы программы до рендеринга диаграмм.
        """
        cls.shapes = []
        cls._initPackage("blockdiag", "noderenderer")
        cls.shapes.sort()

        from blockdiag.imagedraw.png import setup
        setup(None)

    def renderToFile(self, content, imagePath, fileType="png"):
        """
        content - текст, описывающий диаграмму
        imagePath - полный путь до создаваемого файла
        fileType - filetype of the output file, either png or pdf
        """
        from blockdiag.parser import parse_string
        from blockdiag.drawer import DiagramDraw
        from blockdiag.builder import ScreenNodeBuilder
        from blockdiag.utils.fontmap import FontMap

        font = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "fonts",
                            self._fontDefault)

        fontmap = FontMap()
        fontmap.set_default_font(font)

        text = "blockdiag {{ {content} }}".format(content=content)

        tree = parse_string(text)
        diagram = ScreenNodeBuilder.build(tree)

        draw = DiagramDraw(fileType, diagram, imagePath,
                           fontmap=fontmap, antialias=True)
        draw.draw()
        draw.save()
