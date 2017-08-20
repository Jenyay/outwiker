# -*- coding: UTF-8 -*-

import logging


logger = logging.getLogger('ExampleEventsPlugin')


class Controller(object):
    def __init__(self, application):
        self._application = application

    def initialize(self):
        logger.info(u'Initialize.')
        self._application.onWikiOpen += self._onWikiOpen
        self._application.onPageSelect += self._onPageSelect
        self._application.onPageUpdate += self._onPageUpdate
        self._application.onEditorPopupMenu += self._onEditorPopupMenu

    def destroy(self):
        logger.info(u'Destroy.')
        self._application.onWikiOpen -= self._onWikiOpen
        self._application.onPageSelect -= self._onPageSelect
        self._application.onPageUpdate -= self._onPageUpdate
        self._application.onEditorPopupMenu -= self._onEditorPopupMenu

    def _onWikiOpen(self, root):
        logger.info(u'onWikiOpen. Path to notes: {}'.format(root.path))

    def _onPageSelect(self, sender):
        if sender is None:
            logger.info(u'onPageSelect. No page selected.')
        else:
            logger.info(u'onPageSelect. Selected page: {}'.format(sender.subpath))

    def _onPageUpdate(self, sender, *args, **kwargs):
        logger.info(u'onPageUpdate. Updated page: {}'.format(sender.subpath))

    def _onEditorPopupMenu(self, page, params):
        logger.info(u'onEditorPopupMenu. Current page: {}'.format(page.subpath))
