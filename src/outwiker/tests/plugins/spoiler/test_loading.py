"""Loading tests for the Spoiler plugin."""

from outwiker.tests.plugins.basepluginloading import BasePluginLoadingTests


class TestSpoilerLoading(BasePluginLoadingTests):
    def get_plugin_dir(self) -> str:
        return "plugins/spoiler"

    def get_plugin_name(self) -> str:
        return "Spoiler"
