"""Loading tests for the Statistics plugin."""

from outwiker.tests.plugins.basepluginloading import BasePluginLoadingTests


class TestStatisticsLoading(BasePluginLoadingTests):
    def get_plugin_dir(self) -> str:
        return "plugins/statistics_ow"

    def get_plugin_name(self) -> str:
        return "Statistics"
