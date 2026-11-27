"""Loading tests for the Counter plugin."""

from outwiker.tests.plugins.basepluginloading import BasePluginLoadingTests


class TestCounterLoading(BasePluginLoadingTests):
    def get_plugin_dir(self) -> str:
        return "plugins/counter"

    def get_plugin_name(self) -> str:
        return "Counter"
