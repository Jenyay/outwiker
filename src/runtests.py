# -*- coding: utf-8 -*-

import cProfile
import sys
import os

import pytest

from test.utils import print_memory

if __name__ == '__main__':
    args = sys.argv[1:]
    args.append('-s')

    profile_dir = '../tmp'
    profile_name = 'test_profile'
    if not os.path.exists(profile_dir):
        os.mkdir(profile_dir)

    profile_fname = os.path.join(profile_dir, profile_name)
    cProfile.run('pytest.main(args)', profile_fname)

    # result = pytest.main(args)
    # print_memory()
    # sys.exit(result)
