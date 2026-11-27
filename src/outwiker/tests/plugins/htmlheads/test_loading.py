"""Loading tests for the HtmlHeads plugin."""

from outwiker.tests.plugins.basepluginloading import BasePluginLoadingTests


class TestHtmlHeadsLoading(BasePluginLoadingTests):
    def get_plugin_dir(self) -> str:
        return "plugins/htmlheads"

    def get_plugin_name(self) -> str:
        return "HtmlHeads"
