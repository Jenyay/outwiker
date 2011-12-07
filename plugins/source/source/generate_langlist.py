#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
Сохранить в файл список поддерживаемых Pygments языков
"""

from pygments.lexers._mapping import LEXERS

if __name__ == "__main__":
    fname = u"languages.txt"

    def getLongestName (namelist):
        """
        Возвращает самое длинное название языка из списка имен одного и того же языка
        """
        maxlen = 0
        bestname = u""

        for name in namelist:
            if len (name) > maxlen:
                maxlen = len (name)
                bestname = name

        return bestname


    names = [getLongestName (lexer[2]).lower() + "\n" for lexer in LEXERS.values()]
    names.sort()
    # names.insert (0, "text\n")

    with open (fname, "w") as fp:
        fp.writelines (names)
