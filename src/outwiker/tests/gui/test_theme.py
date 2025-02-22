from outwiker.gui.theme import Theme

class EventHandler:
    def __init__(self):
        self.call_count = 0

    def __call__(self, theme):
        self.call_count += 1


def test_changed_init():
    theme = Theme()
    assert theme.changed == False

def test_changed_set():
    theme = Theme()
    theme.set(Theme.SECTION_GENERAL, Theme.GENERAL_BACKGROUND_COLOR, "#123456")
    assert theme.changed == True

def test_changed_set_none():
    theme = Theme()
    theme.set(Theme.SECTION_GENERAL, Theme.GENERAL_BACKGROUND_COLOR, None)
    assert theme.changed == False

def test_changed_set_default():
    theme = Theme()
    default = theme.getDefaults(Theme.SECTION_GENERAL, Theme.GENERAL_BACKGROUND_COLOR)
    theme.set(Theme.SECTION_GENERAL, Theme.GENERAL_BACKGROUND_COLOR, default)
    assert theme.changed == False

def test_get_defaults_none():
    theme = Theme()
    default = theme.getDefaults(Theme.SECTION_GENERAL, Theme.GENERAL_BACKGROUND_COLOR)
    theme.set(Theme.SECTION_GENERAL, Theme.GENERAL_BACKGROUND_COLOR, None)
    val = theme.get(Theme.SECTION_GENERAL, Theme.GENERAL_BACKGROUND_COLOR)
    assert val == default

def test_get_defaults_none_str():
    theme = Theme()
    default = theme.getDefaults(Theme.SECTION_GENERAL, Theme.GENERAL_BACKGROUND_COLOR)
    theme.set(Theme.SECTION_GENERAL, Theme.GENERAL_BACKGROUND_COLOR, "None")
    val = theme.get(Theme.SECTION_GENERAL, Theme.GENERAL_BACKGROUND_COLOR)
    assert val == default

def test_get_defaults_empty():
    theme = Theme()
    default = theme.getDefaults(Theme.SECTION_GENERAL, Theme.GENERAL_BACKGROUND_COLOR)
    theme.set(Theme.SECTION_GENERAL, Theme.GENERAL_BACKGROUND_COLOR, "")
    val = theme.get(Theme.SECTION_GENERAL, Theme.GENERAL_BACKGROUND_COLOR)
    assert val == default

def test_event_changed():
    theme = Theme()
    handler = EventHandler()
    theme.onThemeChanged += handler
    theme.set(Theme.SECTION_GENERAL, Theme.GENERAL_BACKGROUND_COLOR, "#123456")
    theme.sendEvent()
    assert handler.call_count == 1

def test_event_not_changed():
    theme = Theme()
    handler = EventHandler()
    theme.onThemeChanged += handler
    theme.sendEvent()
    assert handler.call_count == 0

def test_clear():
    theme = Theme()
    theme.set(Theme.SECTION_GENERAL, Theme.GENERAL_BACKGROUND_COLOR, "#123456")
    handler = EventHandler()
    theme.onThemeChanged += handler
    theme.clear()
    theme.sendEvent()
    assert theme.changed == False
    assert handler.call_count == 0
