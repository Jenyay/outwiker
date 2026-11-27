"""Loading tests for the WebPage plugin."""

from typing import Any

from outwiker.tests.plugins.basepluginloading import BasePluginLoadingTests


class TestWebPageLoading(BasePluginLoadingTests):
    def get_plugin_dir(self) -> str:
        return "plugins/webpage"

    def get_plugin_name(self) -> str:
        return "WebPage"

    def get_application_params(self) -> dict[str, Any]:
        """The plugin uses the tree panel of the main window."""
        return {"createTreePanel": True}
