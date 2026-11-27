"""Loading tests for the Export2Html plugin."""

from typing import Any

from outwiker.tests.plugins.basepluginloading import BasePluginLoadingTests


class TestExport2HtmlLoading(BasePluginLoadingTests):
    def get_plugin_dir(self) -> str:
        return "plugins/export2html"

    def get_plugin_name(self) -> str:
        return "Export2Html"

    def get_application_params(self) -> dict[str, Any]:
        """The plugin inserts its submenu into the main menu."""
        return {"enableActionsGui": True}
