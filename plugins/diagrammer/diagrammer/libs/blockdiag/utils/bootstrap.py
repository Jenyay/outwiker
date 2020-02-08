# -*- coding: utf-8 -*-
#  Copyright 2011 Takeshi KOMIYA
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import codecs
import os
import re
import sys
import traceback
from optparse import SUPPRESS_HELP, OptionParser

from blockdiag import imagedraw, plugins
from blockdiag.utils import images
from blockdiag.utils.config import ConfigParser
from blockdiag.utils.fontmap import FontMap, parse_fontpath
from blockdiag.utils.logging import error, warning


class Application(object):
    module = None
    options = None

    def __init__(self):
        self.cleanup_handlers = []

    def __enter__(self):
        self.setup()
        return self

    def __exit__(self, *args):
        self.cleanup()

    def register_cleanup_handler(self, handler):
        self.cleanup_handlers.append(handler)

    def run(self, args):
        try:
            self.parse_options(args)
            self.create_fontmap()
            self.setup()

            parsed = self.parse_diagram()
            return self.build_diagram(parsed)
        except SystemExit as e:
            return e
        except UnicodeEncodeError:
            error("UnicodeEncodeError caught (check your font settings)")
            return -1
        except Exception as e:
            if self.options and self.options.debug:
                traceback.print_exc()
            else:
                error("%s" % e)
            return -1
        finally:
            self.cleanup()

    def parse_options(self, args):
        self.options = Options(self.module).parse(args)

    def create_fontmap(self):
        self.fontmap = create_fontmap(self.options)

    def setup(self):
        images.setup(self)
        plugins.setup(self)

    def parse_diagram(self):
        if self.options.input == '-':
            self.code = sys.stdin.read()
            if self.code.startswith('\ufeff'):  # strip BOM
                self.code = self.code[1:]
        else:
            fp = codecs.open(self.options.input, 'r', 'utf-8-sig')
            self.code = fp.read()

        return self.module.parser.parse_string(self.code)

    def build_diagram(self, tree):
        ScreenNodeBuilder = self.module.builder.ScreenNodeBuilder
        try:
            diagram = ScreenNodeBuilder.build(tree, self.options)
        except Exception:
            diagram = ScreenNodeBuilder.build(tree)  # old interface

        DiagramDraw = self.module.drawer.DiagramDraw
        drawer = DiagramDraw(self.options.type, diagram,
                             self.options.output, fontmap=self.fontmap,
                             code=self.code, antialias=self.options.antialias,
                             nodoctype=self.options.nodoctype,
                             transparency=self.options.transparency)
        drawer.draw()

        if self.options.size:
            drawer.save(size=self.options.size)
        else:
            drawer.save()

        return 0

    def cleanup(self):
        for handler in self.cleanup_handlers[:]:
            try:
                handler()
            except Exception as exc:
                error("%s" % exc)
            finally:
                self.cleanup_handlers.remove(handler)


class Options(object):
    def __init__(self, module):
        self.module = module
        self.build_parser()

    def parse(self, args):
        self.options, self.args = self.parser.parse_args(args)
        self.validate()
        self.read_configfile()

        return self.options

    def build_parser(self):
        version = "%%prog %s" % self.module.__version__
        usage = "usage: %prog [options] infile"
        self.parser = p = OptionParser(usage=usage, version=version)
        p.add_option('-a', '--antialias', action='store_true',
                     help='Pass diagram image to anti-alias filter')
        p.add_option('-c', '--config',
                     help='read configurations from FILE', metavar='FILE')
        p.add_option('--debug', action='store_true',
                     help='Enable debug mode')
        p.add_option('-o', dest='output',
                     help='write diagram to FILE', metavar='FILE')
        p.add_option('-f', '--font', default=[], action='append',
                     help='use FONT to draw diagram', metavar='FONT')
        p.add_option('--fontmap',
                     help='use FONTMAP file to draw diagram', metavar='FONT')
        p.add_option('--ignore-pil', dest='ignore_pil',
                     default=False, action='store_true', help=SUPPRESS_HELP)
        p.add_option('--no-transparency', dest='transparency',
                     default=True, action='store_false',
                     help='do not make transparent background of diagram ' +
                          '(PNG only)')
        p.add_option('--size',
                     help='Size of diagram (ex. 320x240)')
        p.add_option('-T', dest='type', default='PNG',
                     help='Output diagram as TYPE format')
        p.add_option('--nodoctype', action='store_true',
                     help='Do not output doctype definition tags (SVG only)')

        return p

    def validate(self):
        if len(self.args) == 0:
            self.parser.print_help()
            sys.exit(0)

        self.options.input = self.args.pop(0)
        if self.options.output:
            pass
        elif self.options.output == '-':
            self.options.output = 'output.' + self.options.type.lower()
        else:
            basename = os.path.splitext(self.options.input)[0]
            ext = '.%s' % self.options.type.lower()
            self.options.output = basename + ext

        self.options.type = self.options.type.upper()
        try:
            imagedraw.create(self.options.type, None, debug=self.options.debug)
        except Exception:
            msg = "unknown format: %s" % self.options.type
            raise RuntimeError(msg)

        if self.options.size:
            matched = re.match(r'^(\d+)x(\d+)$', self.options.size)
            if matched:
                self.options.size = [int(n) for n in matched.groups()]
            else:
                msg = "--size option must be formatted as WIDTHxHEIGHT."
                raise RuntimeError(msg)

        if self.options.type == 'PDF':
            try:
                import reportlab.pdfgen.canvas
                reportlab.pdfgen.canvas
            except ImportError:
                msg = "could not output PDF format; Install reportlab."
                raise RuntimeError(msg)

        if self.options.ignore_pil:
            warning("--ignore-pil option is deprecated "
                    "(detect automatically).")

        if self.options.nodoctype and self.options.type != 'SVG':
            msg = "--nodoctype option work in SVG images."
            raise RuntimeError(msg)

        if self.options.transparency is False and self.options.type != 'PNG':
            msg = "--no-transparency option work in PNG images."
            raise RuntimeError(msg)

        if self.options.config and not os.path.isfile(self.options.config):
            msg = "config file is not found: %s" % self.options.config
            raise RuntimeError(msg)

        if self.options.fontmap and not os.path.isfile(self.options.fontmap):
            msg = "fontmap file is not found: %s" % self.options.fontmap
            raise RuntimeError(msg)

    def read_configfile(self):
        if self.options.config:
            configpath = self.options.config
        elif os.environ.get('HOME'):
            configpath = '%s/.blockdiagrc' % os.environ.get('HOME')
        elif os.environ.get('USERPROFILE'):
            configpath = '%s/.blockdiagrc' % os.environ.get('USERPROFILE')
        else:
            configpath = ''

        appname = self.module.__name__
        if os.path.isfile(configpath):
            config = ConfigParser()
            config.read(configpath)

            if config.has_option(appname, 'fontpath'):
                fontpath = config.get(appname, 'fontpath')
                self.options.font.append(fontpath)

            if config.has_option(appname, 'fontmap'):
                if self.options.fontmap is None:
                    self.options.fontmap = config.get(appname, 'fontmap')

            if config.has_option(appname, 'antialias'):
                antialias = config.get(appname, 'antialias')
                if antialias.lower() == 'true':
                    self.options.antialias = True

            if self.options.fontmap is None:
                self.options.fontmap = configpath


def detectfont(options):
    import glob
    fontdirs = [
        '/usr/share/fonts',
        '/Library/Fonts',
        '/System/Library/Fonts',
        'c:/windows/fonts',
        '/usr/local/share/font-*',
    ]
    fontfiles = [
        'ipagp.ttf',
        'ipagp.otf',
        'VL-PGothic-Regular.ttf',
        'Hiragino Sans GB W3.otf',
        'AppleGothic.ttf',
        'msgothic.ttf',
        'msgoth04.ttf',
        'msgothic.ttc',
    ]

    fontpath = None
    if options.font:
        for path in options.font:
            _path, _ = parse_fontpath(path)
            if os.path.isfile(_path):
                fontpath = path
                break
        else:
            msg = 'fontfile is not found: %s' % options.font
            raise RuntimeError(msg)

    if fontpath is None:
        globber = (glob.glob(d) for d in fontdirs)
        for fontdir in sum(globber, []):
            for root, _, files in os.walk(fontdir):
                for font in fontfiles:
                    if font in files:
                        fontpath = os.path.join(root, font)
                        break

    return fontpath


def create_fontmap(options):
    fontmap = FontMap(options.fontmap)
    if fontmap.find().path is None or options.font:
        fontpath = detectfont(options)
        fontmap.set_default_font(fontpath)

    return fontmap
