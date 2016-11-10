# -*- coding: UTF-8 -*-


class HotKey (object):
    """
    Класс для описания горячей клавиши
    """
    def __init__(self, key, ctrl=False, alt=False, shift=False):
        self._key = key
        self._ctrl = ctrl
        self._alt = alt
        self._shift = shift

    @property
    def key(self):
        return self._key

    @property
    def ctrl(self):
        return self._ctrl

    @property
    def alt(self):
        return self._alt

    @property
    def shift(self):
        return self._shift

    def __eq__(self, other):
        return (other is not None and
                self._key == other._key and
                self._ctrl == other._ctrl and
                self._alt == other._alt and
                self._shift == other._shift)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        result = u''
        if self._ctrl:
            result += 'Ctrl+'
        if self._alt:
            result += u'Alt+'
        if self._shift:
            result += u'Shift+'
        result += self._key
        return result
