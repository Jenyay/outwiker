import tempfile
import shutil
import os

from outwiker.api.core.plugins import Plugin

from .i18n import set_
from .controller import Controller
from .defines import KATEX_DIR_NAME

class PluginTexEquation(Plugin):
    def __init__(self, application):
        """
        application - экземпляр класса core.application.ApplicationParams
        """
        super().__init__(application)
        self._temp_dir_obj = tempfile.TemporaryDirectory(prefix="outwiker-")
        self.__controller = Controller(self, application)
        self._copy_katex()

    def _copy_katex(self):
        src = os.path.join(self.pluginPath, "tools", KATEX_DIR_NAME)
        dst = os.path.join(self._temp_dir_obj.name, KATEX_DIR_NAME)
        if not os.path.exists(dst):
            shutil.copytree(src, dst)

    @property
    def application(self):
        return self._application

    ###################################################
    # Свойства и методы, которые необходимо определить
    ###################################################

    @property
    def name(self):
        return "TeXEquation"

    @property
    def description(self):
        return _("TeXEquation plug-in allow to insert equations in the TeX format.")

    @property
    def url(self):
        return _("https://jenyay.net/Outwiker/TexEquationEn")

    def initialize(self):
        set_(self.gettext)

        global _
        _ = self.gettext
        self.__controller.initialize()

    def destroy(self):
        """
        Уничтожение(выгрузка) плагина.
        Здесь плагин должен отписаться от всех событий
        """
        self.__controller.destroy()
        self._temp_dir_obj.cleanup()
