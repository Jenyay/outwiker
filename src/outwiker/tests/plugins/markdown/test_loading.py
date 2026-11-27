"""Loading tests for the Markdown plugin."""

from outwiker.tests.plugins.basepluginloading import BasePluginLoadingTests


class TestMarkdownLoading(BasePluginLoadingTests):
    def get_plugin_dir(self) -> str:
        return "plugins/markdown"

    def get_plugin_name(self) -> str:
        return "Markdown"
