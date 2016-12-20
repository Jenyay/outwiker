# -*- coding: UTF-8 -*-

import os

from outwiker.gui.baseaction import BaseAction

from snippets.config import SnippetsConfig
from snippets.defines import EVENT_RUN_SNIPPET
from snippets.events import RunSnippetParams
from snippets.i18n import get_


class RunRecentSnippet (BaseAction):
    stringId = u"snippets_recend_used_snippet"

    def __init__(self, application):
        super(RunRecentSnippet, self).__init__()
        self._application = application
        global _
        _ = get_()

    def run(self, params):
        snippet_fname = SnippetsConfig(self._application.config).recentSnippet
        if snippet_fname and os.path.exists(snippet_fname):
            eventParams = RunSnippetParams(snippet_fname)
            self._application.customEvents(EVENT_RUN_SNIPPET, eventParams)

    @property
    def title(self):
        return _(u"Run recent used snippet...")

    @property
    def description(self):
        return _(u'Snippets. Run recent used snippet.')
