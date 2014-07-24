# -*- coding: utf-8 -*-

import sys
if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

import os
from blockdiag.utils.compat import u
from blockdiag.tests.utils import capture_stderr, with_pil, TemporaryDirectory

from docutils import nodes
from docutils.core import publish_doctree
from docutils.parsers.rst import directives as docutils
from blockdiag.utils.rst import directives


class TestRstDirectives(unittest.TestCase):
    def setUp(self):
        self._tmpdir = TemporaryDirectory()

    def tearDown(self):
        if 'blockdiag' in docutils._directives:
            del docutils._directives['blockdiag']

        self._tmpdir.clean()

    @property
    def tmpdir(self):
        return self._tmpdir.name

    def test_setup(self):
        directives.setup()
        options = directives.directive_options

        self.assertIn('blockdiag', docutils._directives)
        self.assertEqual(directives.BlockdiagDirective,
                         docutils._directives['blockdiag'])
        self.assertEqual('PNG', options['format'])
        self.assertEqual(False, options['antialias'])
        self.assertEqual(None, options['fontpath'])
        self.assertEqual(False, options['nodoctype'])
        self.assertEqual(False, options['noviewbox'])
        self.assertEqual(False, options['inline_svg'])

    def test_setup_with_args(self):
        directives.setup(format='SVG', antialias=True, fontpath='/dev/null',
                         nodoctype=True, noviewbox=True, inline_svg=True)
        options = directives.directive_options

        self.assertIn('blockdiag', docutils._directives)
        self.assertEqual(directives.BlockdiagDirective,
                         docutils._directives['blockdiag'])
        self.assertEqual('SVG', options['format'])
        self.assertEqual(True, options['antialias'])
        self.assertEqual('/dev/null', options['fontpath'])
        self.assertEqual(True, options['nodoctype'])
        self.assertEqual(True, options['noviewbox'])
        self.assertEqual(True, options['inline_svg'])

    def test_setup_fontpath1(self):
        with self.assertRaises(RuntimeError):
            directives.setup(format='SVG', fontpath=['dummy.ttf'],
                             outputdir=self.tmpdir)
            text = (".. blockdiag::\n"
                    "\n"
                    "   A -> B")
            publish_doctree(text)

    def test_setup_fontpath2(self):
        with self.assertRaises(RuntimeError):
            directives.setup(format='SVG', fontpath='dummy.ttf',
                             outputdir=self.tmpdir)
            text = (".. blockdiag::\n"
                    "\n"
                    "   A -> B")
            publish_doctree(text)

    def test_setup_nodoctype_is_true(self):
        directives.setup(format='SVG', outputdir=self.tmpdir, nodoctype=True)
        text = (".. blockdiag::\n"
                "\n"
                "   A -> B")
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.image, type(doctree[-1]))
        svg = open(doctree[0]['uri']).read()
        self.assertEqual("<svg viewBox=\"0 0 ", svg[:18])

    def test_setup_nodoctype_is_false(self):
        directives.setup(format='SVG', outputdir=self.tmpdir, nodoctype=False)
        text = (".. blockdiag::\n"
                "\n"
                "   A -> B")
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.image, type(doctree[0]))
        svg = open(doctree[0]['uri']).read()
        self.assertEqual("<?xml version='1.0' encoding='UTF-8'?>\n"
                         "<!DOCTYPE ", svg[:49])

    def test_setup_noviewbox_is_true(self):
        directives.setup(format='SVG', outputdir=self.tmpdir, noviewbox=True)
        text = (".. blockdiag::\n"
                "\n"
                "   A -> B")
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.image, type(doctree[0]))
        svg = open(doctree[0]['uri']).read()
        self.assertRegexpMatches(svg, '<svg height="\d+" width="\d+" ')

    def test_setup_noviewbox_is_false(self):
        directives.setup(format='SVG', outputdir=self.tmpdir, noviewbox=False)
        text = (".. blockdiag::\n"
                "\n"
                "   A -> B")
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.image, type(doctree[0]))
        svg = open(doctree[0]['uri']).read()
        self.assertRegexpMatches(svg, '<svg viewBox="0 0 \d+ \d+" ')

    def test_setup_inline_svg_is_true(self):
        directives.setup(format='SVG', outputdir=self.tmpdir, inline_svg=True)
        text = (".. blockdiag::\n"
                "\n"
                "   A -> B")
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.raw, type(doctree[0]))
        self.assertEqual('html', doctree[0]['format'])
        self.assertEqual(nodes.Text, type(doctree[0][0]))
        self.assertEqual("<?xml version='1.0' encoding='UTF-8'?>\n"
                         "<!DOCTYPE ", doctree[0][0][:49])
        self.assertEqual(0, len(os.listdir(self.tmpdir)))

    def test_setup_inline_svg_is_false(self):
        directives.setup(format='SVG', outputdir=self.tmpdir, inline_svg=False)
        text = (".. blockdiag::\n"
                "\n"
                "   A -> B")
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.image, type(doctree[0]))
        self.assertEqual(1, len(os.listdir(self.tmpdir)))

    @with_pil
    def test_setup_inline_svg_is_true_but_format_isnt_svg(self):
        directives.setup(format='PNG', outputdir=self.tmpdir, inline_svg=True)
        text = (".. blockdiag::\n"
                "\n"
                "   A -> B")
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.image, type(doctree[0]))

    def test_setup_inline_svg_is_true_with_multibytes(self):
        directives.setup(format='SVG', outputdir=self.tmpdir)
        text = u(".. blockdiag::\n"
                 "\n"
                 "   あ -> い")
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.image, type(doctree[0]))

    def test_setup_inline_svg_is_true_and_width_option1(self):
        directives.setup(format='SVG', outputdir=self.tmpdir,
                         nodoctype=True, noviewbox=True, inline_svg=True)
        text = (".. blockdiag::\n"
                "   :width: 100\n"
                "\n"
                "   A -> B")
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.raw, type(doctree[0]))
        self.assertEqual(nodes.Text, type(doctree[0][0]))
        self.assertRegexpMatches(doctree[0][0],
                                 '<svg height="\d+" width="100" ')

    def test_setup_inline_svg_is_true_and_width_option2(self):
        directives.setup(format='SVG', outputdir=self.tmpdir,
                         nodoctype=True, noviewbox=True, inline_svg=True)
        text = (".. blockdiag::\n"
                "   :width: 10000\n"
                "\n"
                "   A -> B")
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.raw, type(doctree[0]))
        self.assertEqual(nodes.Text, type(doctree[0][0]))
        self.assertRegexpMatches(doctree[0][0],
                                 '<svg height="\d+" width="10000" ')

    def test_setup_inline_svg_is_true_and_height_option1(self):
        directives.setup(format='SVG', outputdir=self.tmpdir,
                         nodoctype=True, noviewbox=True, inline_svg=True)
        text = (".. blockdiag::\n"
                "   :height: 100\n"
                "\n"
                "   A -> B")
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.raw, type(doctree[0]))
        self.assertEqual(nodes.Text, type(doctree[0][0]))
        self.assertRegexpMatches(doctree[0][0],
                                 '<svg height="100" width="\d+" ')

    def test_setup_inline_svg_is_true_and_height_option2(self):
        directives.setup(format='SVG', outputdir=self.tmpdir,
                         nodoctype=True, noviewbox=True, inline_svg=True)
        text = (".. blockdiag::\n"
                "   :height: 10000\n"
                "\n"
                "   A -> B")
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.raw, type(doctree[0]))
        self.assertEqual(nodes.Text, type(doctree[0][0]))
        self.assertRegexpMatches(doctree[0][0],
                                 '<svg height="10000" width="\d+" ')

    def test_setup_inline_svg_is_true_and_width_and_height_option(self):
        directives.setup(format='SVG', outputdir=self.tmpdir,
                         nodoctype=True, noviewbox=True, inline_svg=True)
        text = (".. blockdiag::\n"
                "   :width: 200\n"
                "   :height: 100\n"
                "\n"
                "   A -> B")
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.raw, type(doctree[0]))
        self.assertEqual(nodes.Text, type(doctree[0][0]))
        self.assertRegexpMatches(doctree[0][0],
                                 '<svg height="100" width="200" ')

    def test_call_with_brace(self):
        directives.setup(format='SVG', outputdir=self.tmpdir)
        text = (".. blockdiag::\n"
                "\n"
                "   {"
                "     A -> B"
                "   }")
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.image, type(doctree[0]))
        self.assertEqual(0, doctree[0]['uri'].index(self.tmpdir))

    def test_call_without_braces(self):
        directives.setup(format='SVG', outputdir=self.tmpdir)
        text = (".. blockdiag::\n"
                "\n"
                "   A -> B")
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.image, type(doctree[0]))
        self.assertEqual(0, doctree[0]['uri'].index(self.tmpdir))

    def test_alt_option(self):
        directives.setup(format='SVG', outputdir=self.tmpdir)
        text = (".. blockdiag::\n"
                "   :alt: hello world\n"
                "\n"
                "   A -> B")
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.image, type(doctree[0]))
        self.assertEqual('hello world', doctree[0]['alt'])
        self.assertEqual(0, doctree[0]['uri'].index(self.tmpdir))

    def test_align_option1(self):
        directives.setup(format='SVG', outputdir=self.tmpdir)
        text = (".. blockdiag::\n"
                "   :align: left\n"
                "\n"
                "   A -> B")
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.image, type(doctree[0]))
        self.assertEqual('left', doctree[0]['align'])
        self.assertEqual(0, doctree[0]['uri'].index(self.tmpdir))

    def test_align_option2(self):
        directives.setup(format='SVG', outputdir=self.tmpdir)
        text = (".. blockdiag::\n"
                "   :align: center\n"
                "\n"
                "   A -> B")
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.image, type(doctree[0]))
        self.assertEqual('center', doctree[0]['align'])
        self.assertEqual(0, doctree[0]['uri'].index(self.tmpdir))

    def test_align_option3(self):
        directives.setup(format='SVG', outputdir=self.tmpdir)
        text = (".. blockdiag::\n"
                "   :align: right\n"
                "\n"
                "   A -> B")
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.image, type(doctree[0]))
        self.assertEqual('right', doctree[0]['align'])
        self.assertEqual(0, doctree[0]['uri'].index(self.tmpdir))

    @capture_stderr
    def test_align_option4(self):
        directives.setup(format='SVG', outputdir=self.tmpdir)
        text = (".. blockdiag::\n"
                "   :align: unknown\n"
                "\n"
                "   A -> B")
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.system_message, type(doctree[0]))

        # clear stderr outputs (ignore ERROR)
        from io import StringIO
        sys.stderr = StringIO()

    def test_caption_option(self):
        directives.setup(format='SVG', outputdir=self.tmpdir)
        text = (".. blockdiag::\n"
                "   :caption: hello world\n"
                "\n"
                "   A -> B")
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.figure, type(doctree[0]))
        self.assertEqual(2, len(doctree[0]))
        self.assertEqual(nodes.image, type(doctree[0][0]))
        self.assertEqual(nodes.caption, type(doctree[0][1]))
        self.assertEqual(1, len(doctree[0][1]))
        self.assertEqual(nodes.Text, type(doctree[0][1][0]))
        self.assertEqual('hello world', doctree[0][1][0])

    def test_caption_option_and_align_option(self):
        directives.setup(format='SVG', outputdir=self.tmpdir)
        text = (".. blockdiag::\n"
                "   :align: left\n"
                "   :caption: hello world\n"
                "\n"
                "   A -> B")
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.figure, type(doctree[0]))
        self.assertEqual('left', doctree[0]['align'])
        self.assertEqual(2, len(doctree[0]))
        self.assertEqual(nodes.image, type(doctree[0][0]))
        self.assertNotIn('align', doctree[0][0])
        self.assertEqual(nodes.caption, type(doctree[0][1]))
        self.assertEqual(1, len(doctree[0][1]))
        self.assertEqual(nodes.Text, type(doctree[0][1][0]))
        self.assertEqual('hello world', doctree[0][1][0])

    @capture_stderr
    def test_maxwidth_option(self):
        directives.setup(format='SVG', outputdir=self.tmpdir)
        text = (".. blockdiag::\n"
                "   :maxwidth: 100\n"
                "\n"
                "   A -> B")
        doctree = publish_doctree(text)
        self.assertEqual(2, len(doctree))
        self.assertEqual(nodes.image, type(doctree[0]))
        self.assertEqual('100', doctree[0]['width'])
        self.assertEqual(0, doctree[0]['uri'].index(self.tmpdir))
        self.assertEqual(nodes.system_message, type(doctree[1]))

    def test_width_option(self):
        directives.setup(format='SVG', outputdir=self.tmpdir)
        text = (".. blockdiag::\n"
                "   :width: 100\n"
                "\n"
                "   A -> B")
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.image, type(doctree[0]))
        self.assertEqual('100', doctree[0]['width'])
        self.assertEqual(0, doctree[0]['uri'].index(self.tmpdir))

    def test_height_option(self):
        directives.setup(format='SVG', outputdir=self.tmpdir)
        text = (".. blockdiag::\n"
                "   :height: 100\n"
                "\n"
                "   A -> B")
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.image, type(doctree[0]))
        self.assertEqual('100', doctree[0]['height'])
        self.assertEqual(0, doctree[0]['uri'].index(self.tmpdir))

    def test_scale_option(self):
        directives.setup(format='SVG', outputdir=self.tmpdir)
        text = (".. blockdiag::\n"
                "   :scale: 50%\n"
                "\n"
                "   A -> B")
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.image, type(doctree[0]))
        self.assertEqual(50, doctree[0]['scale'])
        self.assertEqual(0, doctree[0]['uri'].index(self.tmpdir))

    def test_name_option(self):
        directives.setup(format='SVG', outputdir=self.tmpdir)
        text = (".. blockdiag::\n"
                "   :name: foo%\n"
                "\n"
                "   A -> B")
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.image, type(doctree[0]))
        self.assertEqual(['foo%'], doctree[0]['names'])
        self.assertEqual(0, doctree[0]['uri'].index(self.tmpdir))

    def test_class_option(self):
        directives.setup(format='SVG', outputdir=self.tmpdir)
        text = (".. blockdiag::\n"
                "   :class: bar%\n"
                "\n"
                "   A -> B")
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.image, type(doctree[0]))
        self.assertEqual(['bar'], doctree[0]['classes'])
        self.assertEqual(0, doctree[0]['uri'].index(self.tmpdir))

    def test_figwidth_option1(self):
        directives.setup(format='SVG', outputdir=self.tmpdir)
        text = (".. blockdiag::\n"
                "   :caption: hello world\n"
                "   :figwidth: 100\n"
                "\n"
                "   A -> B")
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.figure, type(doctree[0]))
        self.assertEqual('100px', doctree[0]['width'])

    def test_figwidth_option2(self):
        directives.setup(format='SVG', outputdir=self.tmpdir)
        text = (".. blockdiag::\n"
                "   :caption: hello world\n"
                "   :figwidth: image\n"
                "\n"
                "   A -> B")
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.figure, type(doctree[0]))
        self.assertEqual('448px', doctree[0]['width'])

    def test_figclass_option(self):
        directives.setup(format='SVG', outputdir=self.tmpdir)
        text = (".. blockdiag::\n"
                "   :caption: hello world\n"
                "   :figclass: baz\n"
                "\n"
                "   A -> B")
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.figure, type(doctree[0]))
        self.assertEqual(['baz'], doctree[0]['classes'])

    def test_desctable_option(self):
        directives.setup(format='SVG', outputdir=self.tmpdir)
        text = (".. blockdiag::\n"
                "   :desctable:\n"
                "\n"
                "   A [description = foo]"
                "   B [description = bar]"
                "   group { A }")
        doctree = publish_doctree(text)
        self.assertEqual(2, len(doctree))
        self.assertEqual(nodes.image, type(doctree[0]))
        self.assertEqual(nodes.table, type(doctree[1]))

        # tgroup
        self.assertEqual(4, len(doctree[1][0]))
        self.assertEqual(nodes.colspec, type(doctree[1][0][0]))
        self.assertEqual(nodes.colspec, type(doctree[1][0][1]))
        self.assertEqual(nodes.thead, type(doctree[1][0][2]))
        self.assertEqual(nodes.tbody, type(doctree[1][0][3]))

        # colspec
        self.assertEqual(50, doctree[1][0][0]['colwidth'])
        self.assertEqual(50, doctree[1][0][1]['colwidth'])

        # thead
        thead = doctree[1][0][2]
        self.assertEqual(2, len(thead[0]))
        self.assertEqual('Name', thead[0][0][0][0])
        self.assertEqual('Description', thead[0][1][0][0])

        # tbody
        tbody = doctree[1][0][3]
        self.assertEqual(2, len(tbody))
        self.assertEqual('A', tbody[0][0][0][0])
        self.assertEqual('foo', tbody[0][1][0][0])
        self.assertEqual('B', tbody[1][0][0][0])
        self.assertEqual('bar', tbody[1][1][0][0])

    def test_desctable_option_without_description(self):
        directives.setup(format='SVG', outputdir=self.tmpdir)
        text = (".. blockdiag::\n"
                "   :desctable:\n"
                "\n"
                "   A -> B")
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.image, type(doctree[0]))

    def test_desctable_option_using_node_group(self):
        directives.setup(format='SVG', outputdir=self.tmpdir)
        text = (".. blockdiag::\n"
                "   :desctable:\n"
                "\n"
                "   A [description = foo]"
                "   B [description = bar]"
                "   group { A }")
        doctree = publish_doctree(text)
        self.assertEqual(2, len(doctree))
        self.assertEqual(nodes.image, type(doctree[0]))
        self.assertEqual(nodes.table, type(doctree[1]))

        self.assertEqual(1, len(doctree[1]))
        self.assertEqual(nodes.tgroup, type(doctree[1][0]))

        # tgroup
        self.assertEqual(4, len(doctree[1][0]))
        self.assertEqual(nodes.colspec, type(doctree[1][0][0]))
        self.assertEqual(nodes.colspec, type(doctree[1][0][1]))
        self.assertEqual(nodes.thead, type(doctree[1][0][2]))
        self.assertEqual(nodes.tbody, type(doctree[1][0][3]))

        # colspec
        self.assertEqual(0, len(doctree[1][0][0]))
        self.assertEqual(50, doctree[1][0][0]['colwidth'])

        self.assertEqual(0, len(doctree[1][0][1]))
        self.assertEqual(50, doctree[1][0][1]['colwidth'])

        # thead
        thead = doctree[1][0][2]
        self.assertEqual(1, len(thead))
        self.assertEqual(2, len(thead[0]))

        self.assertEqual(1, len(thead[0][0]))
        self.assertEqual(1, len(thead[0][0][0]))
        self.assertEqual('Name', thead[0][0][0][0])

        self.assertEqual(1, len(thead[0][1]))
        self.assertEqual(1, len(thead[0][1][0]))
        self.assertEqual('Description', thead[0][1][0][0])

        # tbody
        tbody = doctree[1][0][3]
        self.assertEqual(2, len(tbody))

        self.assertEqual(2, len(tbody[0]))
        self.assertEqual(1, len(tbody[0][0]))
        self.assertEqual(1, len(tbody[0][0][0]))
        self.assertEqual('A', tbody[0][0][0][0])
        self.assertEqual(1, len(tbody[0][1]))
        self.assertEqual('foo', tbody[0][1][0][0])

        self.assertEqual(2, len(tbody[1]))
        self.assertEqual(1, len(tbody[1][0]))
        self.assertEqual(1, len(tbody[1][0][0]))
        self.assertEqual('B', tbody[1][0][0][0])
        self.assertEqual(1, len(tbody[1][1]))
        self.assertEqual('bar', tbody[1][1][0][0])

    def test_desctable_option_with_rest_markups(self):
        directives.setup(format='SVG', outputdir=self.tmpdir)
        text = (".. blockdiag::\n"
                "   :desctable:\n"
                "\n"
                "   A [description = \"foo *bar* **baz**\"]"
                "   B [description = \"**foo** *bar* baz\"]")
        doctree = publish_doctree(text)
        self.assertEqual(2, len(doctree))
        self.assertEqual(nodes.image, type(doctree[0]))
        self.assertEqual(nodes.table, type(doctree[1]))

        # tgroup
        self.assertEqual(4, len(doctree[1][0]))
        self.assertEqual(nodes.colspec, type(doctree[1][0][0]))
        self.assertEqual(nodes.colspec, type(doctree[1][0][1]))
        self.assertEqual(nodes.thead, type(doctree[1][0][2]))
        self.assertEqual(nodes.tbody, type(doctree[1][0][3]))

        # colspec
        self.assertEqual(50, doctree[1][0][0]['colwidth'])
        self.assertEqual(50, doctree[1][0][1]['colwidth'])

        # thead
        thead = doctree[1][0][2]
        self.assertEqual(2, len(thead[0]))
        self.assertEqual('Name', thead[0][0][0][0])
        self.assertEqual('Description', thead[0][1][0][0])

        # tbody
        tbody = doctree[1][0][3]
        self.assertEqual(2, len(tbody))
        self.assertEqual('A', tbody[0][0][0][0])
        self.assertEqual(4, len(tbody[0][1][0]))
        self.assertEqual(nodes.Text, type(tbody[0][1][0][0]))
        self.assertEqual('foo ', str(tbody[0][1][0][0]))
        self.assertEqual(nodes.emphasis, type(tbody[0][1][0][1]))
        self.assertEqual(nodes.Text, type(tbody[0][1][0][1][0]))
        self.assertEqual('bar', tbody[0][1][0][1][0])
        self.assertEqual(nodes.Text, type(tbody[0][1][0][2]))
        self.assertEqual(' ', str(tbody[0][1][0][2]))
        self.assertEqual(nodes.strong, type(tbody[0][1][0][3]))
        self.assertEqual(nodes.Text, type(tbody[0][1][0][3][0]))
        self.assertEqual('baz', str(tbody[0][1][0][3][0]))

        self.assertEqual('B', tbody[1][0][0][0])
        self.assertEqual(4, len(tbody[1][1][0]))
        self.assertEqual(nodes.strong, type(tbody[1][1][0][0]))
        self.assertEqual(nodes.Text, type(tbody[1][1][0][0][0]))
        self.assertEqual('foo', str(tbody[1][1][0][0][0]))
        self.assertEqual(nodes.Text, type(tbody[1][1][0][1]))
        self.assertEqual(' ', str(tbody[1][1][0][1]))
        self.assertEqual(nodes.emphasis, type(tbody[1][1][0][2]))
        self.assertEqual(nodes.Text, type(tbody[1][1][0][2][0]))
        self.assertEqual('bar', str(tbody[1][1][0][2][0]))
        self.assertEqual(nodes.Text, type(tbody[1][1][0][3]))
        self.assertEqual(' baz', str(tbody[1][1][0][3]))

    def test_desctable_option_with_numbered(self):
        directives.setup(format='SVG', outputdir=self.tmpdir)
        text = (".. blockdiag::\n"
                "   :desctable:\n"
                "\n"
                "   A [numbered = 2]"
                "   B [numbered = 1]")
        doctree = publish_doctree(text)
        self.assertEqual(2, len(doctree))
        self.assertEqual(nodes.image, type(doctree[0]))
        self.assertEqual(nodes.table, type(doctree[1]))

        # tgroup
        self.assertEqual(4, len(doctree[1][0]))
        self.assertEqual(nodes.colspec, type(doctree[1][0][0]))
        self.assertEqual(nodes.colspec, type(doctree[1][0][1]))
        self.assertEqual(nodes.thead, type(doctree[1][0][2]))
        self.assertEqual(nodes.tbody, type(doctree[1][0][3]))

        # colspec
        self.assertEqual(25, doctree[1][0][0]['colwidth'])
        self.assertEqual(50, doctree[1][0][1]['colwidth'])

        # thead
        thead = doctree[1][0][2]
        self.assertEqual(2, len(thead[0]))
        self.assertEqual('No', thead[0][0][0][0])
        self.assertEqual('Name', thead[0][1][0][0])

        # tbody
        tbody = doctree[1][0][3]
        self.assertEqual(2, len(tbody))
        self.assertEqual('1', tbody[0][0][0][0])
        self.assertEqual('B', tbody[0][1][0][0])
        self.assertEqual('2', tbody[1][0][0][0])
        self.assertEqual('A', tbody[1][1][0][0])

    def test_desctable_option_with_numbered_and_description(self):
        directives.setup(format='SVG', outputdir=self.tmpdir)
        text = (".. blockdiag::\n"
                "   :desctable:\n"
                "\n"
                "   A [description = foo, numbered = 2]"
                "   B [description = bar, numbered = 1]")
        doctree = publish_doctree(text)
        self.assertEqual(2, len(doctree))
        self.assertEqual(nodes.image, type(doctree[0]))
        self.assertEqual(nodes.table, type(doctree[1]))

        # tgroup
        self.assertEqual(5, len(doctree[1][0]))
        self.assertEqual(nodes.colspec, type(doctree[1][0][0]))
        self.assertEqual(nodes.colspec, type(doctree[1][0][1]))
        self.assertEqual(nodes.colspec, type(doctree[1][0][2]))
        self.assertEqual(nodes.thead, type(doctree[1][0][3]))
        self.assertEqual(nodes.tbody, type(doctree[1][0][4]))

        # colspec
        self.assertEqual(25, doctree[1][0][0]['colwidth'])
        self.assertEqual(50, doctree[1][0][1]['colwidth'])
        self.assertEqual(50, doctree[1][0][2]['colwidth'])

        # thead
        thead = doctree[1][0][3]
        self.assertEqual(3, len(thead[0]))
        self.assertEqual('No', thead[0][0][0][0])
        self.assertEqual('Name', thead[0][1][0][0])
        self.assertEqual('Description', thead[0][2][0][0])

        # tbody
        tbody = doctree[1][0][4]
        self.assertEqual(2, len(tbody))
        self.assertEqual('1', tbody[0][0][0][0])
        self.assertEqual('B', tbody[0][1][0][0])
        self.assertEqual(1, len(tbody[0][2]))
        self.assertEqual('bar', tbody[0][2][0][0])
        self.assertEqual('2', tbody[1][0][0][0])
        self.assertEqual('A', tbody[1][1][0][0])
        self.assertEqual('foo', tbody[1][2][0][0])

    def test_desctable_option_for_edges(self):
        directives.setup(format='SVG', outputdir=self.tmpdir)
        text = (".. blockdiag::\n"
                "   :desctable:\n"
                "\n"
                "   A -> B [description = \"foo\"]"
                "   C -> D [description = \"bar\"]"
                "   C [label = \"label_C\"]"
                "   D [label = \"label_D\"]")
        doctree = publish_doctree(text)
        self.assertEqual(2, len(doctree))
        self.assertEqual(nodes.image, type(doctree[0]))
        self.assertEqual(nodes.table, type(doctree[1]))

        # tgroup
        self.assertEqual(4, len(doctree[1][0]))
        self.assertEqual(nodes.colspec, type(doctree[1][0][0]))
        self.assertEqual(nodes.colspec, type(doctree[1][0][1]))
        self.assertEqual(nodes.thead, type(doctree[1][0][2]))
        self.assertEqual(nodes.tbody, type(doctree[1][0][3]))

        # colspec
        self.assertEqual(25, doctree[1][0][0]['colwidth'])
        self.assertEqual(50, doctree[1][0][1]['colwidth'])

        # thead
        thead = doctree[1][0][2]
        self.assertEqual(2, len(thead[0]))
        self.assertEqual('Name', thead[0][0][0][0])
        self.assertEqual('Description', thead[0][1][0][0])

        # tbody
        tbody = doctree[1][0][3]
        self.assertEqual(2, len(tbody))
        self.assertEqual('A -> B', tbody[0][0][0][0])
        self.assertEqual(1, len(tbody[0][1][0]))
        self.assertEqual(nodes.Text, type(tbody[0][1][0][0]))
        self.assertEqual('foo', str(tbody[0][1][0][0]))
        self.assertEqual('label_C -> label_D', tbody[1][0][0][0])
        self.assertEqual(1, len(tbody[1][1][0]))
        self.assertEqual(nodes.Text, type(tbody[1][1][0][0]))
        self.assertEqual('bar', str(tbody[1][1][0][0]))

    def test_desctable_option_for_nodes_and_edges(self):
        directives.setup(format='SVG', outputdir=self.tmpdir)
        text = (".. blockdiag::\n"
                "   :desctable:\n"
                "\n"
                "   A -> B [description = \"foo\"]"
                "   C -> D [description = \"bar\"]"
                "   C [label = \"label_C\", description = foo]"
                "   D [label = \"label_D\"]")
        doctree = publish_doctree(text)
        self.assertEqual(3, len(doctree))
        self.assertEqual(nodes.image, type(doctree[0]))
        self.assertEqual(nodes.table, type(doctree[1]))
        self.assertEqual(nodes.table, type(doctree[2]))

        # tgroup
        self.assertEqual(4, len(doctree[2][0]))
        self.assertEqual(nodes.colspec, type(doctree[2][0][0]))
        self.assertEqual(nodes.colspec, type(doctree[2][0][1]))
        self.assertEqual(nodes.thead, type(doctree[2][0][2]))
        self.assertEqual(nodes.tbody, type(doctree[2][0][3]))

        # colspec
        self.assertEqual(25, doctree[2][0][0]['colwidth'])
        self.assertEqual(50, doctree[2][0][1]['colwidth'])

        # thead
        thead = doctree[2][0][2]
        self.assertEqual(2, len(thead[0]))
        self.assertEqual('Name', thead[0][0][0][0])
        self.assertEqual('Description', thead[0][1][0][0])

        # tbody
        tbody = doctree[2][0][3]
        self.assertEqual(2, len(tbody))
        self.assertEqual('A -> B', tbody[0][0][0][0])
        self.assertEqual(1, len(tbody[0][1][0]))
        self.assertEqual(nodes.Text, type(tbody[0][1][0][0]))
        self.assertEqual('foo', str(tbody[0][1][0][0]))
        self.assertEqual('label_C -> label_D', tbody[1][0][0][0])
        self.assertEqual(1, len(tbody[1][1][0]))
        self.assertEqual(nodes.Text, type(tbody[1][1][0][0]))
        self.assertEqual('bar', str(tbody[1][1][0][0]))

    @capture_stderr
    def test_broken_diagram(self):
        directives.setup(format='SVG', outputdir=self.tmpdir)
        text = (".. blockdiag::\n"
                "\n"
                "     A ->")
        doctree = publish_doctree(text)
        self.assertEqual(1, len(doctree))
        self.assertEqual(nodes.system_message, type(doctree[0]))
