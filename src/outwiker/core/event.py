# -*- coding: UTF-8 -*-

EVENT_PRIORITY_DEFAULT = 0
EVENT_PRIORITY_MAX_CORE = 100
EVENT_PRIORITY_MIN_CORE = -100


class Event(object):
    """
    Events with priority
    """
    def __init__(self):
        # List of the tuples:(event handler, priority)
        # First item - handler with max priority
        self._handlers = []

    def clear(self):
        del self._handlers[:]

    def bind(self, handler, priority=EVENT_PRIORITY_DEFAULT):
        for item in self._handlers:
            if item[0] == handler:
                return

        # Find last handler with priority less current priority
        index = 0
        for n, item in reversed(list(enumerate(self._handlers))):
            if item[1] >= priority:
                index = n + 1
                break

        self._handlers.insert(index, (handler, priority))

    def unbind(self, handler):
        removed_item = None
        for item in self._handlers:
            if item[0] == handler:
                removed_item = item
                break

        if removed_item is not None:
            self._handlers.remove(removed_item)

    def __iadd__(self, handler):
        self.bind(handler)
        return self

    def __isub__(self, handler):
        self.unbind(handler)
        return self

    def __call__(self, *args, **kwargs):
        for handler in self._handlers:
            handler[0](*args, **kwargs)

    def __len__(self):
        return len(self._handlers)


class CustomEvents(object):
    """Class contains events for access by key"""
    def __init__(self):
        # key - string is event ID
        # value - Event instance
        self._events = {}

    def bind(self, key, handler, priority=EVENT_PRIORITY_DEFAULT):
        """
        Bind handler with event by key
        """
        event = self._events.get(key)
        if event is None:
            event = Event()
            self._events[key] = event
        event.bind(handler, priority)

    def unbind(self, key, handler):
        """
        Unbind handler from event by key
        """
        event = self._events.get(key)
        if event is not None:
            event.unbind(handler)
            if len(event) == 0:
                del self._events[key]

    def clear(self, key):
        """
        Remove all handlers for event by key
        """
        event = self._events.get(key)
        if event is not None:
            event.clear()
            del self._events[key]

    def __call__(self, key, *args, **kwargs):
        """
        Call the event (if it exists)
        """
        event = self._events.get(key)
        if event is not None:
            event(*args, **kwargs)

    def get(self, key):
        if key not in self._events:
            self._events[key] = Event()
        return self._events[key]
