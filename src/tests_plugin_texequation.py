#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Unit-тесты
"""

from gettext import NullTranslations
import unittest

from test.plugins.texequation.test_texequation import TexEquationTest


if __name__ == '__main__':
    NullTranslations().install()
    unittest.main()
