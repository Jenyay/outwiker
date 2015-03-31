# -*- coding: UTF-8 -*-


class Event (object):
    """
    Класс событий
    """
    def __init__ (self):
        self._handlers = []


    def clear (self):
        del self._handlers[:]


    def __iadd__ (self, handler):
        if handler not in self._handlers:
            self._handlers.append(handler)

        return self


    def __isub__ (self, handler):
        try:
            self._handlers.remove(handler)
        except:
            raise ValueError("Handler is not handling this event, so cannot unhandle it.")
        return self


    def __call__ (self, *args, **kargs):
        for handler in self._handlers:
            handler(*args, **kargs)


    def __len__ (self):
        return len (self._handlers)
