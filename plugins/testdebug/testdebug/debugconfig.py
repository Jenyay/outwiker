# -*- coding: UTF-8 -*-

from outwiker.core.config import BooleanOption


class DebugConfig(object):
    '''
    Класс для хранения настроек панели с облагом тегов
    '''
    SECTION = u'Debug'

    def __init__(self, config):
        self.config = config

        self.enablePreprocessing = BooleanOption(self.config,
                                                 self.SECTION,
                                                 u'EnablePreprocessing',
                                                 False)

        self.enablePostprocessing = BooleanOption(self.config,
                                                  self.SECTION,
                                                  u'EnablePostprocessing',
                                                  False)

        self.enableOnHoverLink = BooleanOption(self.config,
                                               self.SECTION,
                                               u'enableOnHoverLink',
                                               False)

        self.enableOnLinkClick = BooleanOption(self.config,
                                               self.SECTION,
                                               u'enableOnLinkClick',
                                               False)

        self.enableOnEditorPopup = BooleanOption(self.config,
                                                 self.SECTION,
                                                 u'enableOnEditorPopup',
                                                 False)

        self.enableOnSpellChecking = BooleanOption(self.config,
                                                   self.SECTION,
                                                   u'enableOnSpellChecking',
                                                   False)

        self.enableRenderingTimeMeasuring = BooleanOption(
            self.config,
            self.SECTION,
            u'enableRenderingTimeMeasuring',
            False
        )

        self.enableNewPageDialogTab = BooleanOption(self.config,
                                                    self.SECTION,
                                                    u'enableNewPageDialogTab',
                                                    False)

        self.enablePageDialogEvents = BooleanOption(self.config,
                                                    self.SECTION,
                                                    u'enablePageDialogEvents',
                                                    False)

        self.enableOpeningTimeMeasure = BooleanOption(
            self.config,
            self.SECTION,
            u'enableOpeningTimeMeasure',
            False)

        self.enableOnIconsGroupsListInit = BooleanOption(
            self.config,
            self.SECTION,
            u'enableOnIconsGroupsListInit',
            False)

        self.enableOnTextEditorKeyDown = BooleanOption(
            self.config,
            self.SECTION,
            u'enableOnTextEditorKeyDown',
            False)

        self.enableOnPrePostContent = BooleanOption(
            self.config,
            self.SECTION,
            u'enableOnPrePostContent',
            False)

        self.enableOnTextEditorCaretMove = BooleanOption(
            self.config,
            self.SECTION,
            u'enableOnTextEditorCaretMove',
            False)
