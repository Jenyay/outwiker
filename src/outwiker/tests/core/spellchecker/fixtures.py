import os
import os.path
import shutil
from tempfile import mkdtemp

import pytest

from outwiker.tests.utils import removeDir
from outwiker.core.spellchecker.spellcheckersfactory import SpellCheckersFactory


@pytest.fixture
def spell_factory():
    dst_path_to_dicts = mkdtemp(prefix='tmp spell test')

    if not os.path.exists(dst_path_to_dicts):
        os.mkdir(dst_path_to_dicts)

    src_dict_path = os.path.join('src', 'outwiker', 'data', 'spell')
    _copy_dict_from("ru_RU", src_dict_path, dst_path_to_dicts)
    _copy_dict_from("en_US", src_dict_path, dst_path_to_dicts)

    yield SpellCheckersFactory([dst_path_to_dicts])

    removeDir(dst_path_to_dicts)


def _copy_dict_from(lang, src_dict_path, dst_path_to_dicts):
    fname_dic = os.path.join(src_dict_path, lang + ".dic")
    fname_aff = os.path.join(src_dict_path, lang + ".aff")

    shutil.copy(fname_dic, dst_path_to_dicts)
    shutil.copy(fname_aff, dst_path_to_dicts)
