"""Loading tests for the TableOfContents plugin."""

from outwiker.tests.plugins.basepluginloading import BasePluginLoadingTests


class TestTableOfContentsLoading(BasePluginLoadingTests):
    def get_plugin_dir(self) -> str:
        return "plugins/tableofcontents"

    def get_plugin_name(self) -> str:
        return "TableOfContents"
