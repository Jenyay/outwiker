# -*- coding: utf-8 -*-

import sys

import pytest

from test.utils import print_memory

if __name__ == '__main__':
    pytest.main((sys.argv[1:]))
    print_memory()
