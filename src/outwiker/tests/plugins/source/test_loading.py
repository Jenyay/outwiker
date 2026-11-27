"""Loading tests for the Source plugin."""

from outwiker.tests.plugins.basepluginloading import BasePluginLoadingTests


class TestSourceLoading(BasePluginLoadingTests):
    def get_plugin_dir(self) -> str:
        return "plugins/source"

    def get_plugin_name(self) -> str:
        return "Source"
