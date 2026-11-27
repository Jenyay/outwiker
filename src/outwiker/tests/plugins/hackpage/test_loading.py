"""Loading tests for the HackPage plugin."""

from outwiker.tests.plugins.basepluginloading import BasePluginLoadingTests


class TestHackPageLoading(BasePluginLoadingTests):
    def get_plugin_dir(self) -> str:
        return "plugins/hackpage"

    def get_plugin_name(self) -> str:
        return "HackPage"
