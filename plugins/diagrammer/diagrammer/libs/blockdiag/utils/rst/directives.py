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

import io
import os
from collections import namedtuple
from functools import wraps
from hashlib import sha1

from docutils import nodes
from docutils.parsers import rst
from docutils.parsers.rst.roles import set_classes
from docutils.statemachine import ViewList

from blockdiag.utils.bootstrap import Application, create_fontmap
from blockdiag.utils.rst.nodes import blockdiag as blockdiag_node

directive_options_default = dict(format='PNG',
                                 antialias=False,
                                 fontpath=None,
                                 outputdir=None,
                                 nodoctype=False,
                                 noviewbox=False,
                                 inline_svg=False)
directive_options = {}


def relfn2path(env, filename):
    if filename.startswith('/') or filename.startswith(os.sep):
        relfn = filename[1:]
    else:
        path = env.doc2path(env.docname, base=None)
        relfn = os.path.join(os.path.dirname(path), filename)

    return relfn, os.path.join(env.srcdir, relfn)


def with_blockdiag(fn):
    @wraps(fn)
    def decorator(*args):
        with Application():
            return fn(*args)

    return decorator


def align(argument):
    align_values = ('left', 'center', 'right')
    return rst.directives.choice(argument, align_values)


def figwidth_value(argument):
    if argument.lower() == 'image':
        return 'image'
    else:
        return rst.directives.length_or_percentage_or_unitless(argument, 'px')


class BlockdiagDirectiveBase(rst.Directive):
    """ Directive to insert arbitrary dot markup. """
    name = "blockdiag"
    node_class = blockdiag_node

    has_content = True
    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = False
    option_spec = {
        'alt': rst.directives.unchanged,
        'height': rst.directives.length_or_unitless,
        'width': rst.directives.length_or_percentage_or_unitless,
        'scale': rst.directives.percentage,
        'align': align,
        'caption': rst.directives.unchanged,
        'desctable': rst.directives.flag,
        'maxwidth': rst.directives.nonnegative_int,  # deprecated
        'name': rst.directives.unchanged,
        'class': rst.directives.class_option,
        'figwidth': figwidth_value,
        'figclass': rst.directives.class_option,
    }

    def run(self):
        if self.arguments:
            document = self.state.document
            if self.content:
                msg = ('%s directive cannot have both content and '
                       'a filename argument' % self.name)
                return [document.reporter.warning(msg, line=self.lineno)]

            try:
                filename = self.source_filename(self.arguments[0])
                fp = io.open(filename, 'r', encoding='utf-8-sig')
                try:
                    dotcode = fp.read()
                finally:
                    fp.close()
            except (IOError, OSError):
                msg = 'External %s file %r not found or reading it failed' % \
                      (self.name, filename)
                return [document.reporter.warning(msg, line=self.lineno)]
        else:
            dotcode = '\n'.join(self.content).strip()
            if not dotcode:
                msg = 'Ignoring "%s" directive without content.' % self.name
                return [self.state_machine.reporter.warning(msg,
                                                            line=self.lineno)]

        set_classes(self.options)
        node = self.node_class()
        results = [node]

        node['code'] = dotcode
        node['caption'] = self.options.pop('caption', None)
        node['options'] = self.options

        # for sphinxcontrib.* module (backward compatibility)
        node['alt'] = self.options.get('alt')

        # replace maxwidth option to width (backward compatibility)
        if 'maxwidth' in node['options']:
            node['options']['width'] = str(node['options']['maxwidth'])

            msg = ':maxwidth: option is deprecated. Use :width: option.'
            warning = self.state_machine.reporter.warning(msg,
                                                          line=self.lineno)
            results.append(warning)

        return results

    def source_filename(self, filename):
        if hasattr(self.state.document.settings, 'env'):
            env = self.state.document.settings.env
            rel_filename, filename = relfn2path(env, self.arguments[0])
            env.note_dependency(rel_filename)

        return filename


class BlockdiagDirective(BlockdiagDirectiveBase):
    processor = None  # backward compatibility for 1.4.0

    @with_blockdiag
    def run(self):
        figwidth = self.options.pop('figwidth', None)
        figclasses = self.options.pop('figclass', None)
        if self.options.get('caption'):
            align = self.options.pop('align', None)
        else:
            align = None

        results = super(BlockdiagDirective, self).run()

        node = results[0]
        if not isinstance(node, self.node_class):
            return results

        try:
            diagram = self.node2diagram(node)
        except Exception as e:
            raise self.warning(str(e))

        if 'desctable' in node['options']:
            results += self.description_tables(diagram)

        results[0] = self.node2image(node, diagram)
        self.add_name(results[0])

        if node.get('caption'):
            elem = nodes.Element()
            self.state.nested_parse(ViewList([node['caption']], source=''),
                                    self.content_offset, elem)
            caption_node = nodes.caption(elem[0].rawsource, '',
                                         *elem[0].children)
            caption_node.source = elem[0].source
            caption_node.line = elem[0].line

            fig = nodes.figure()
            fig += results[0]
            fig += caption_node

            if figwidth == 'image':
                width = self.get_actual_width(node, diagram)
                fig['width'] = str(width) + 'px'
            elif figwidth is not None:
                fig['width'] = figwidth
            if figclasses:
                fig['classes'] += figclasses
            if align:
                fig['align'] = align

            results[0] = fig

        return results

    @property
    def global_options(self):
        return directive_options

    def node2diagram(self, node):
        if hasattr(node, 'to_diagram'):
            return node.to_diagram()
        else:
            try:
                tree = self.processor.parser.parse_string(node['code'])
            except Exception:
                code = '%s { %s }' % (self.name, node['code'])
                tree = self.processor.parser.parse_string(code)
                node['code'] = code  # replace if succeeded

            return self.processor.builder.ScreenNodeBuilder.build(tree)

    def get_actual_width(self, node, diagram):
        fontmap = self.create_fontmap()
        if hasattr(node, 'to_drawer'):
            drawer = node.to_drawer('SVG', None, fontmap,
                                    **self.global_options)
        else:
            drawer = self.processor.drawer.DiagramDraw('SVG', diagram,
                                                       None, fontmap=fontmap)

        return drawer.pagesize()[0]

    def node2image(self, node, diagram):
        _format = self.global_options['format'].lower()
        if _format == 'svg' and self.global_options['inline_svg'] is True:
            return self.node2image_inline_svg(node, diagram)

        filename = self.image_filename(node)
        fontmap = self.create_fontmap()
        if hasattr(node, 'to_drawer'):
            drawer = node.to_drawer(_format, filename, fontmap,
                                    **self.global_options)
        else:
            drawer = self.processor.drawer.DiagramDraw(_format, diagram,
                                                       filename,
                                                       fontmap=fontmap,
                                                       **self.global_options)

        if not os.path.isfile(filename):
            drawer.draw()
            drawer.save()

        return nodes.image(uri=filename, **node['options'])

    def node2image_inline_svg(self, node, diagram):
        fontmap = self.create_fontmap()
        if hasattr(node, 'to_drawer'):
            drawer = node.to_drawer('SVG', None, fontmap,
                                    **self.global_options)
        else:
            drawer = self.processor.drawer.DiagramDraw('svg', diagram,
                                                       None, fontmap=fontmap,
                                                       **self.global_options)
        drawer.draw()

        size = drawer.pagesize().resize(**node['options']).to_integer_point()
        content = drawer.save(size)

        return nodes.raw('', content, format='html')

    def create_fontmap(self):
        Options = namedtuple('Options', 'font fontmap')
        fontpath = self.global_options['fontpath']
        if isinstance(fontpath, (list, tuple)):
            options = Options(fontpath, None)
        elif isinstance(fontpath, str):
            options = Options([fontpath], None)
        else:
            options = Options([], None)

        return create_fontmap(options)

    def image_filename(self, node, prefix='', ext='png'):
        if hasattr(node, 'get_path'):
            return node.get_path(**self.global_options)
        else:
            options = dict(node['options'])
            options.update(font=self.global_options['fontpath'],
                           antialias=self.global_options['antialias'])
            hashseed = (node['code'] + str(options)).encode('utf-8')
            hashed = sha1(hashseed).hexdigest()

            _format = self.global_options['format'].lower()
            outputdir = self.global_options['outputdir']
            filename = "%s%s-%s.%s" % (self.name, prefix, hashed, _format)
            if outputdir:
                filename = os.path.join(outputdir, filename)

            return filename

    def description_tables(self, diagram):
        tables = []
        desctable = self.node_description_table(diagram)
        if desctable:
            tables.append(desctable)

        desctable = self.edge_description_table(diagram)
        if desctable:
            tables.append(desctable)

        return tables

    def node_description_table(self, diagram):
        nodes = diagram.traverse_nodes()
        klass = diagram._DiagramNode

        widths = [25] + [50] * (len(klass.desctable) - 1)
        headers = [klass.attrname[n] for n in klass.desctable]

        def node_number(node):
            try:
                return int(node[0])
            except (TypeError, ValueError):
                return 65535

        descriptions = [n.to_desctable() for n in nodes if n.drawable]
        descriptions.sort(key=node_number)

        for i in reversed(range(len(headers))):
            if any(desc[i] for desc in descriptions):
                pass
            else:
                widths.pop(i)
                headers.pop(i)
                for desc in descriptions:
                    desc.pop(i)

        if len(headers) == 1:
            return None
        else:
            return self._description_table(descriptions, widths, headers)

    def edge_description_table(self, diagram):
        edges = diagram.traverse_edges()

        widths = [25, 50]
        headers = ['Name', 'Description']
        descriptions = [e.to_desctable() for e in edges if e.style != 'none']

        if any(desc[1] for desc in descriptions):
            return self._description_table(descriptions, widths, headers)
        else:
            return None

    def _description_table(self, descriptions, widths, headers):
        # generate table-root
        tgroup = nodes.tgroup(cols=len(widths))
        for width in widths:
            tgroup += nodes.colspec(colwidth=width)
        table = nodes.table()
        table += tgroup

        # generate table-header
        thead = nodes.thead()
        row = nodes.row()
        for header in headers:
            entry = nodes.entry()
            entry += nodes.paragraph(text=header)
            row += entry
        thead += row
        tgroup += thead

        # generate table-body
        tbody = nodes.tbody()
        for desc in descriptions:
            row = nodes.row()
            for attr in desc:
                entry = nodes.entry()
                if not isinstance(attr, str):
                    attr = str(attr)
                self.state.nested_parse(ViewList([attr], source=attr),
                                        0, entry)
                row += entry
            tbody += row
        tgroup += tbody

        return table


def setup(**kwargs):
    global directive_options, directive_options_default

    for key, value in directive_options_default.items():
        directive_options[key] = kwargs.get(key, value)

    rst.directives.register_directive("blockdiag", BlockdiagDirective)
