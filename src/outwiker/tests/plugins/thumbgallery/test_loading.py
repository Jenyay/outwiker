"""Loading tests for the ThumbGallery plugin."""

from outwiker.tests.plugins.basepluginloading import BasePluginLoadingTests


class TestThumbGalleryLoading(BasePluginLoadingTests):
    def get_plugin_dir(self) -> str:
        return "plugins/thumbgallery"

    def get_plugin_name(self) -> str:
        return "ThumbGallery"
