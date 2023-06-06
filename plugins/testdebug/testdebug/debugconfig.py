# -*- coding: utf-8 -*-

from outwiker.api.core.config import BooleanOption


class DebugConfig:
    SECTION = "Debug"

    def __init__(self, config):
        self.config = config

        self.enablePreprocessing = BooleanOption(
            self.config, self.SECTION, "EnablePreprocessing", False
        )

        self.enablePostprocessing = BooleanOption(
            self.config, self.SECTION, "EnablePostprocessing", False
        )

        self.enableOnHoverLink = BooleanOption(
            self.config, self.SECTION, "enableOnHoverLink", False
        )

        self.enableOnLinkClick = BooleanOption(
            self.config, self.SECTION, "enableOnLinkClick", False
        )

        self.enableOnEditorPopup = BooleanOption(
            self.config, self.SECTION, "enableOnEditorPopup", False
        )

        self.enableOnSpellChecking = BooleanOption(
            self.config, self.SECTION, "enableOnSpellChecking", False
        )

        self.enableRenderingTimeMeasuring = BooleanOption(
            self.config, self.SECTION, "enableRenderingTimeMeasuring", False
        )

        self.enableNewPageDialogTab = BooleanOption(
            self.config, self.SECTION, "enableNewPageDialogTab", False
        )

        self.enablePageDialogEvents = BooleanOption(
            self.config, self.SECTION, "enablePageDialogEvents", False
        )

        self.enableOpeningTimeMeasure = BooleanOption(
            self.config, self.SECTION, "enableOpeningTimeMeasure", False
        )

        self.enableOnIconsGroupsListInit = BooleanOption(
            self.config, self.SECTION, "enableOnIconsGroupsListInit", False
        )

        self.enableOnTextEditorKeyDown = BooleanOption(
            self.config, self.SECTION, "enableOnTextEditorKeyDown", False
        )

        self.enableOnPrePostContent = BooleanOption(
            self.config, self.SECTION, "enableOnPrePostContent", False
        )

        self.enableOnTextEditorCaretMove = BooleanOption(
            self.config, self.SECTION, "enableOnTextEditorCaretMove", False
        )
