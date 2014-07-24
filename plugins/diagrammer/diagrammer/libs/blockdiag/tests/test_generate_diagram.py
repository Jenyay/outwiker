# -*- coding: utf-8 -*-

import os
import re
from nose.tools import nottest
from blockdiag.tests.utils import capture_stderr, TemporaryDirectory
from blockdiag.tests.utils import supported_pil, supported_pdf

import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

import blockdiag
import blockdiag.command


def get_fontpath(testdir=None):
    if testdir is None:
        testdir = os.path.dirname(__file__)
    return os.path.join(testdir, 'truetype', 'VL-PGothic-Regular.ttf')


def get_diagram_files(testdir):
    diagramsdir = os.path.join(testdir, 'diagrams')

    skipped = ['README', 'debian-logo-256color-palettealpha.png',
               'errors', 'white.gif']
    for file in os.listdir(diagramsdir):
        if file in skipped:
            pass
        else:
            yield os.path.join(diagramsdir, file)


def test_generate():
    mainfunc = blockdiag.command.main
    basepath = os.path.dirname(__file__)
    files = get_diagram_files(basepath)
    options = []

    for testcase in testcase_generator(basepath, mainfunc, files, options):
        yield testcase


def test_generate_with_separate():
    mainfunc = blockdiag.command.main
    basepath = os.path.dirname(__file__)
    files = get_diagram_files(basepath)
    filtered = (f for f in files if re.search('separate', f))
    options = ['--separate']

    for testcase in testcase_generator(basepath, mainfunc, filtered, options):
        yield testcase


@nottest
def testcase_generator(basepath, mainfunc, files, options):
    fontpath = get_fontpath(basepath)
    if os.path.exists(fontpath):
        options = options + ['-f', fontpath]

    for source in files:
        yield generate, mainfunc, 'svg', source, options

        if supported_pil() and os.path.exists(fontpath):
            yield generate, mainfunc, 'png', source, options
            yield generate, mainfunc, 'png', source, options + ['--antialias']
        else:
            yield unittest.skip("Pillow is not available")(generate)
            yield unittest.skip("Pillow is not available")(generate)

        if supported_pdf() and os.path.exists(fontpath):
            yield generate, mainfunc, 'pdf', source, options
        else:
            yield unittest.skip("reportlab is not available")(generate)


@capture_stderr
def generate(mainfunc, filetype, source, options):
    try:
        tmpdir = TemporaryDirectory()
        fd, tmpfile = tmpdir.mkstemp()
        os.close(fd)

        mainfunc(['--debug', '-T', filetype, '-o', tmpfile, source] +
                 list(options))
    finally:
        tmpdir.clean()


def not_exist_font_config_option_test():
    fontpath = get_fontpath()
    if os.path.exists(fontpath):
        args = ['-f', '/font_is_not_exist', '-f', fontpath, 'input.diag']
        options = blockdiag.command.BlockdiagOptions(blockdiag).parse(args)

        from blockdiag.utils.bootstrap import detectfont
        detectfont(options)


@capture_stderr
def svg_includes_source_code_tag_test():
    from xml.etree import ElementTree

    testdir = os.path.dirname(__file__)
    diagpath = os.path.join(testdir, 'diagrams', 'single_edge.diag')

    try:
        tmpdir = TemporaryDirectory()
        fd, tmpfile = tmpdir.mkstemp()
        os.close(fd)

        args = ['-T', 'SVG', '-o', tmpfile, diagpath]
        blockdiag.command.main(args)

        # compare embeded source code
        source_code = open(diagpath).read()
        tree = ElementTree.parse(tmpfile)
        desc = tree.find('{http://www.w3.org/2000/svg}desc')

        # strip spaces
        source_code = re.sub('\s+', ' ', source_code)
        embeded = re.sub('\s+', ' ', desc.text)
        assert source_code == embeded
    finally:
        tmpdir.clean()
