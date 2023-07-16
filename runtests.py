# -*- coding: utf-8 -*-

import cProfile
import sys
import os

import pytest

from outwiker.tests.utils import print_memory

if __name__ == '__main__':
    args = sys.argv[1:]
    args.append('-s')

    profile_dir = 'tmp'
    profile_name = 'test_profile'
    if not os.path.exists(profile_dir):
        os.mkdir(profile_dir)

    profile_path = os.path.join(profile_dir, profile_name)

    profile = cProfile.Profile()
    profile.enable()
    result = pytest.main(args)
    profile.create_stats()
    profile.dump_stats(profile_path)

    # print_memory()
    sys.exit(result)
