"""Loading tests for the Livejournal plugin."""

from outwiker.tests.plugins.basepluginloading import BasePluginLoadingTests


class TestLivejournalLoading(BasePluginLoadingTests):
    def get_plugin_dir(self) -> str:
        return "plugins/livejournal"

    def get_plugin_name(self) -> str:
        return "Livejournal"
