from outwiker.api.core.config import BooleanOption, StringOption


class RecentPagesConfig:
    SECTION = "RecentEditedPagesPlugin"

    # Colorize page
    COLORIZE_PAGE_PARAM = "colorize_page"
    COLORIZE_PAGE_DEFAULT = True

    # Add extra icon
    ADD_EXTRA_ICON_PARAM = "add_extra_icon"
    ADD_EXTRA_ICON_DEFAULT = True

    # Highlight color
    HIGHLIGHT_COLOR_PARAM = "highlight_color"
    HIGHLIGHT_COLOR_DEFAULT = "blue"

    def __init__(self, config):
        self._config = config

        self.colorizePage = BooleanOption(
            self._config,
            self.SECTION,
            self.COLORIZE_PAGE_PARAM,
            self.COLORIZE_PAGE_DEFAULT,
        )

        self.addExtraIcon = BooleanOption(
            self._config,
            self.SECTION,
            self.ADD_EXTRA_ICON_PARAM,
            self.ADD_EXTRA_ICON_DEFAULT,
        )

        self.highlightColor = StringOption(
            self._config,
            self.SECTION,
            self.HIGHLIGHT_COLOR_PARAM,
            self.HIGHLIGHT_COLOR_DEFAULT,
        )
