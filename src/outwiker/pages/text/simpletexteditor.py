# -*- coding: UTF-8 -*-

from outwiker.gui.texteditor import TextEditor


class SimpleTextEditor (TextEditor):
    def __init__ (self, parent):
        super (SimpleTextEditor, self).__init__ (parent)


    def getIndcatorsStyleBytes (self, text):
        """
        Функция должна возвращать список байт, описывающих раскраску (стили) для текста text
        Этот метод выполняется в отдельном потоке
        """
        textlength = self.calcByteLen (text)
        stylelist = [0] * textlength

        self.runSpellChecking (stylelist, 0, len (text))

        stylebytes = "".join ([chr(byte) for byte in stylelist])
        return stylebytes


    def getStyleBytes (self, text):
        return None
