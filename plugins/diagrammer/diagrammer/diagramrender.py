# -*- coding: UTF-8 -*-

import os.path

from outwiker.core.system import getOS


class DiagramRender (object):
    """
    Класс для создания диаграмм с помощью blockdiag
    """
    def __init__ (self):
        self._fontDefault = u"Ubuntu-R.ttf"


    @staticmethod
    def initialize ():
        import blockdiag.noderenderer.actor
        import blockdiag.noderenderer.beginpoint
        import blockdiag.noderenderer.box
        import blockdiag.noderenderer.circle
        import blockdiag.noderenderer.cloud
        import blockdiag.noderenderer.diamond
        import blockdiag.noderenderer.dots
        import blockdiag.noderenderer.ellipse
        import blockdiag.noderenderer.endpoint
        import blockdiag.noderenderer.mail
        import blockdiag.noderenderer.minidiamond
        import blockdiag.noderenderer.none
        import blockdiag.noderenderer.note
        import blockdiag.noderenderer.roundedbox
        import blockdiag.noderenderer.square
        import blockdiag.noderenderer.textbox
        import blockdiag.noderenderer.flowchart.database
        import blockdiag.noderenderer.flowchart.input
        import blockdiag.noderenderer.flowchart.loopin
        import blockdiag.noderenderer.flowchart.loopout
        import blockdiag.noderenderer.flowchart.terminator

        from blockdiag.imagedraw.png import setup

        setup(None)
        blockdiag.noderenderer.actor.setup(None)
        blockdiag.noderenderer.beginpoint.setup(None)
        blockdiag.noderenderer.box.setup(None)
        blockdiag.noderenderer.circle.setup(None)
        blockdiag.noderenderer.cloud.setup(None)
        blockdiag.noderenderer.diamond.setup(None)
        blockdiag.noderenderer.dots.setup(None)
        blockdiag.noderenderer.ellipse.setup(None)
        blockdiag.noderenderer.endpoint.setup(None)
        blockdiag.noderenderer.mail.setup(None)
        blockdiag.noderenderer.minidiamond.setup(None)
        blockdiag.noderenderer.none.setup(None)
        blockdiag.noderenderer.note.setup(None)
        blockdiag.noderenderer.roundedbox.setup(None)
        blockdiag.noderenderer.square.setup(None)
        blockdiag.noderenderer.textbox.setup(None)

        blockdiag.noderenderer.flowchart.database.setup(None)
        blockdiag.noderenderer.flowchart.input.setup(None)
        blockdiag.noderenderer.flowchart.loopin.setup(None)
        blockdiag.noderenderer.flowchart.loopout.setup(None)
        blockdiag.noderenderer.flowchart.terminator.setup(None)


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
