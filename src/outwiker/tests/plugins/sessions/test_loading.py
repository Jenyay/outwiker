"""Loading tests for the Sessions plugin."""

from outwiker.tests.plugins.basepluginloading import BasePluginLoadingTests


class TestSessionsLoading(BasePluginLoadingTests):
    def get_plugin_dir(self) -> str:
        return "plugins/sessions"

    def get_plugin_name(self) -> str:
        return "Sessions"
