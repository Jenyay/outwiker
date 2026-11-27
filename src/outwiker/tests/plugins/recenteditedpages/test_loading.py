"""Loading tests for the RecentEditedPages plugin."""

from outwiker.tests.plugins.basepluginloading import BasePluginLoadingTests


class TestRecentEditedPagesLoading(BasePluginLoadingTests):
    def get_plugin_dir(self) -> str:
        return "plugins/recenteditedpages"

    def get_plugin_name(self) -> str:
        return "RecentEditedPages"
