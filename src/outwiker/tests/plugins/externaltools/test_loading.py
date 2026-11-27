"""Loading tests for the ExternalTools plugin."""

from outwiker.tests.plugins.basepluginloading import BasePluginLoadingTests


class TestExternalToolsLoading(BasePluginLoadingTests):
    def get_plugin_dir(self) -> str:
        return "plugins/externaltools"

    def get_plugin_name(self) -> str:
        return "ExternalTools"
