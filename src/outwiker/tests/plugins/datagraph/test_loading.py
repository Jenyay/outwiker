"""Loading tests for the DataGraph plugin."""

from outwiker.tests.plugins.basepluginloading import BasePluginLoadingTests


class TestDataGraphLoading(BasePluginLoadingTests):
    def get_plugin_dir(self) -> str:
        return "plugins/datagraph"

    def get_plugin_name(self) -> str:
        return "DataGraph"
