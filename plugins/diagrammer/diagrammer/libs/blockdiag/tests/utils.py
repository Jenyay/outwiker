# -*- coding: utf-8 -*-
from __future__ import print_function

import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

import os
import re
import functools
from shutil import rmtree
from tempfile import mkdtemp, mkstemp
from blockdiag.builder import ScreenNodeBuilder
from blockdiag.parser import parse_file

try:
    # sys.stderr in py2.x allows mixture of str and unicode
    from cStringIO import StringIO
except ImportError:
    # sys.stderr in py3.x allows only str objects (disallow bytes objs)
    from io import StringIO


def supported_pil():
    try:
        from PIL import _imagingft
        _imagingft
        return True
    except:
        return False


def with_pil(fn):
    if not supported_pil():
        fn.__test__ = False

    return fn


def supported_pdf():
    try:
        import reportlab
        reportlab

        return True
    except:
        return False


def with_pdf(fn):
    if not supported_pdf():
        fn.__test__ = False

    return fn


def capture_stderr(func):
    def wrap(*args, **kwargs):
        try:
            stderr = sys.stderr
            sys.stderr = StringIO()

            func(*args, **kwargs)

            if re.search('(ERROR|Traceback)', sys.stderr.getvalue()):
                raise AssertionError('Caught error')
        finally:
            if sys.stderr.getvalue():
                print("---[ stderr ] ---")
                print(sys.stderr.getvalue())

            sys.stderr = stderr

    return functools.wraps(func)(wrap)


stderr_wrapper = capture_stderr   # FIXME: deprecated


class TemporaryDirectory(object):
    def __init__(self, suffix='', prefix='tmp', dir=None):
        self.name = mkdtemp(suffix, prefix, dir)

    def __del__(self):
        self.clean()

    def clean(self):
        if os.path.exists(self.name):
            rmtree(self.name)

    def mkstemp(self, suffix='', prefix='tmp', text=False):
        return mkstemp(suffix, prefix, self.name, text)


class BuilderTestCase(unittest.TestCase):
    def build(self, filename):
        basedir = os.path.dirname(__file__)
        pathname = os.path.join(basedir, 'diagrams', filename)
        return self._build(parse_file(pathname))

    def _build(self, tree):
        return ScreenNodeBuilder.build(tree)

    def __getattr__(self, name):
        if name.startswith('assertNode'):
            def asserter(diagram, attributes):
                attr_name = name.replace('assertNode', '').lower()
                print("[node.%s]" % attr_name)
                for node in (n for n in diagram.nodes if n.drawable):
                    print(node)
                    excepted = attributes[node.id]
                    self.assertEqual(excepted, getattr(node, attr_name))

            return asserter
        elif name.startswith('assertEdge'):
            def asserter(diagram, attributes):
                attr_name = name.replace('assertEdge', '').lower()
                print("[edge.%s]" % attr_name)
                for edge in diagram.edges:
                    print(edge)
                    expected = attributes[(edge.node1.id, edge.node2.id)]
                    self.assertEqual(expected, getattr(edge, attr_name))

            return asserter
        else:
            return getattr(super(BuilderTestCase, self), name)
