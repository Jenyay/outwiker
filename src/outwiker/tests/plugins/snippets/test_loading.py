"""Loading tests for the Snippets plugin."""

from outwiker.tests.plugins.basepluginloading import BasePluginLoadingTests


class TestSnippetsLoading(BasePluginLoadingTests):
    def get_plugin_dir(self) -> str:
        return "plugins/snippets"

    def get_plugin_name(self) -> str:
        return "Snippets"
