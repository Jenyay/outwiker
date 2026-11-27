"""Loading tests for the HtmlFormatter plugin."""

from outwiker.tests.plugins.basepluginloading import BasePluginLoadingTests


class TestHtmlFormatterLoading(BasePluginLoadingTests):
    def get_plugin_dir(self) -> str:
        return "plugins/htmlformatter"

    def get_plugin_name(self) -> str:
        return "HtmlFormatter"
