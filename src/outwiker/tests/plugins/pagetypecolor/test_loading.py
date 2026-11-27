"""Loading tests for the PageTypeColor plugin."""

from outwiker.tests.plugins.basepluginloading import BasePluginLoadingTests


class TestPageTypeColorLoading(BasePluginLoadingTests):
    def get_plugin_dir(self) -> str:
        return "plugins/pagetypecolor"

    def get_plugin_name(self) -> str:
        return "PageTypeColor"
