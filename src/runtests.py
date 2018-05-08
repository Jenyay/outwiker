# -*- coding: utf-8 -*-

import sys

import pytest

from test.utils import print_memory

if __name__ == '__main__':
    args = sys.argv[1:]
    args.append('-s')

    pytest.main(args)
    # print_memory()
