from outwiker.core.event import Event


def defaultValue(default_value):
    def decorator(func):
        def wrapper(*args, **kwargs):
            val = func(*args, **kwargs)
            return default_value if val is None or val == "" or val == "None" else val
        return wrapper
    return decorator


class Theme:
    def __init__(self):
        self._colorHyperlink = None

        # Event occurs after theme changing
        # Parameters:
        #    params - instance of the onThemeChangedParams class
        self.onThemeChanged = Event()

    @property
    @defaultValue("#0000FF")
    def colorHyperlink(self):
        return self._colorHyperlink

    def clear(self):
        self.onThemeChanged.clear()

    def loadFromConfig(self, config):
        pass

    def sendEvent(self):
        self.onThemeChanged(self)


class onThemeChangedParams:
    """
    Parameters for onThemeChanged event
    """
    def __init__(self, theme: Theme) -> None:
        self.theme = theme
