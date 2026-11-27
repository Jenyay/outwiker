"""Loading tests for the Lightbox plugin."""

from outwiker.tests.plugins.basepluginloading import BasePluginLoadingTests


class TestLightboxLoading(BasePluginLoadingTests):
    def get_plugin_dir(self) -> str:
        return "plugins/lightbox"

    def get_plugin_name(self) -> str:
        return "Lightbox"
