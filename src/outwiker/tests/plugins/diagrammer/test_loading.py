"""Loading tests for the Diagrammer plugin."""

from outwiker.tests.plugins.basepluginloading import BasePluginLoadingTests


class TestDiagrammerLoading(BasePluginLoadingTests):
    def get_plugin_dir(self) -> str:
        return "plugins/diagrammer"

    def get_plugin_name(self) -> str:
        return "Diagrammer"
