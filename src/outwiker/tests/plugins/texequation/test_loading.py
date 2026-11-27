"""Loading tests for the TeXEquation plugin."""

from outwiker.tests.plugins.basepluginloading import BasePluginLoadingTests


class TestTeXEquationLoading(BasePluginLoadingTests):
    def get_plugin_dir(self) -> str:
        return "plugins/texequation"

    def get_plugin_name(self) -> str:
        return "TeXEquation"
