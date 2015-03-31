# -*- coding: UTF-8 -*-

import pprint

from outwiker.core.event import Event


class EventsWatcher (object):
    """
    Class for watching for all events in Application
    """
    def __init__ (self, application):
        self._application = application
        self._printer = pprint.PrettyPrinter(indent=4)

        # List of the tuples: (event name, event handler)
        self._handlers = []


    def startWatch (self):
        for itemname in dir (self._application):
            item = getattr (self._application, itemname)
            if isinstance (item, Event):
                handler = self._getHandler (itemname)
                item += handler
                self._handlers.append ((itemname, handler))


    def stopWatch (self):
        for eventname, handler in self._handlers:
            event = getattr (self._application, eventname)
            event -= handler

        del self._handlers[:]


    def _getHandler (self, eventname):
        def onEvent (*args, **kwargs):
            print u"*** {}".format (eventname)
            # self._printer.pprint (args)
            # self._printer.pprint (kwargs)
            print

        return onEvent
