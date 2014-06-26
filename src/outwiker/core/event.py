# -*- coding: UTF-8 -*-


class Event:
    """
    Класс событий
    """
    def __init__ (self):
        self._handlers = []


    def clear (self):
        del self._handlers[:]


    def _handle (self, handler):
        if handler not in self._handlers:
            self._handlers.append(handler)

        return self


    def _unhandle (self, handler):
        try:
            self._handlers.remove(handler)
        except:
            raise ValueError("Handler is not handling this event, so cannot unhandle it.")
        return self

    def _run (self, *args, **kargs):
        for handler in self._handlers:
            handler(*args, **kargs)


    __iadd__ = _handle
    __isub__ = _unhandle
    __call__ = _run


    def __len__ (self):
        return len (self._handlers)
