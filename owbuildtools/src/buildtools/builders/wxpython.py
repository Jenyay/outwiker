import shutil
from pathlib import Path

from invoke import Context

from .base import BuilderBase

from buildtools.defines import WXPYTHON_SRC_DIR, WXPYTHON_BUILD_DIR
from buildtools.utilites import print_info


class BuilderWxPython(BuilderBase):
    def __init__(self, c: Context):
        super().__init__(c, "")
        self.result_dir = Path(self.facts.root_dir, WXPYTHON_BUILD_DIR)

    def _build(self):
        commands = [
                "pip install attrdict3 sip sphinx wheel",
                "python build.py dox",
                "python build.py etg",
                "python build.py sip",
                "python build.py build",
                "python build.py bdist",
                "python build.py bdist_wheel"
                ]

        with self.context.cd(WXPYTHON_SRC_DIR):
            for command in commands:
                print_info(command)
                self.context.run(command)
            
        build_dir = Path(WXPYTHON_SRC_DIR, "dist")
        self.result_dir.mkdir(exist_ok=True)
        for fname in build_dir.glob("*.whl"):
            print_info("{} -> {}".format(fname, self.result_dir))
            shutil.copy(fname, self.result_dir)

    def clear(self):
        super().clear()
        self._remove(self.result_dir)
