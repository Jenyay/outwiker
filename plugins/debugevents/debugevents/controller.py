# -*- coding: UTF-8 -*-

import logging

from outwiker.core.event import Event


logger = logging.getLogger('DebugEventsPlugin')


class Controller(object):
    def __init__(self, application):
        self._application = application
        self._events = []

    def initialize(self):
        logger.info(u'Initialize.')

        for member_name in sorted(dir(self._application)):
            member = getattr(self._application, member_name)
            if isinstance(member, Event):
                logger.info(u'Subscribe to event: {}'.format(member_name))
                handler = self.getHandler(member_name)
                self._events.append((member, handler))
                member += handler

    def getHandler(self, member_name):
        def handler(*args, **kwargs):
            logger.info(member_name)

        return handler

    def destroy(self):
        for event, handler in self._events:
            event -= handler

        self._events = []
        logger.info(u'Destroy.')
