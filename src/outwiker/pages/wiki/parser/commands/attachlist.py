# -*- coding: utf-8 -*-

import os.path
from pathlib import Path
from string import Template
from typing import List, Tuple

from outwiker.core.attachment import Attachment
from outwiker.core.defines import PAGE_ATTACH_DIR
from outwiker.pages.wiki.parser.command import Command
import outwiker.gui.cssclasses as css
import outwiker.gui.svgimages as svg


class SimpleView:
    """
    Класс для простого представления списка прикрепленных файлов - каждая страница на отдельной строке
    CSS styles taken from https://codemyui.com/directory-list-with-collapsible-nested-folders-and-files/
    """
    def __init__(self):
        self._list_template = '<ul class="ow-attach-list">{title}<ul class="ow-attach-list">{content}</ul></ul>'
        self._item_template = '<li class="{css_class}"><a class="ow-attach {css_class}" href="{link}">{title}</a></li>'    

    def make(self, dirnames, fnames,  subdir):
        """
        fnames - имена файлов, которые нужно вывести (относительный путь)
        attach_path - путь до прикрепленных файлов (полный)
        """
        content_items = [self._get_item_dir(subdir, name, name) for name in dirnames]
        content_items += [self._get_item_file(subdir, name, name) for name in fnames]
        content = ''.join(content_items)
        title = self._get_title(subdir)

        return self._list_template.format(content=content, title=title)

    def _get_title(self, subdir: str) -> str:
        title = subdir if subdir else _('Attachments')
        result = self._get_item_dir(subdir, '', title)
        return result

    def _get_item_dir(self, subdir: str, dirname: str, title: str) -> str:
        link = self._get_attach_path(subdir, dirname)
        return self._item_template.format(link=link, title=title, css_class=css.CSS_ATTACH_DIR)

    def _get_item_file(self, subdir: str, name: str, title: str) -> str:
        link = self._get_attach_path(subdir, name)
        return self._item_template.format(link=link, title=title, css_class=css.CSS_ATTACH_FILE)

    def _get_attach_path(self, subdir: str, fname: str) -> str:
        return os.path.join(PAGE_ATTACH_DIR, subdir, fname).replace("\\", "/")

    def get_css_styles(self) -> str:
        template = '''<style>
.ow-attach-list ul {
  margin-left: 15px;
  padding-left: 10px;
  border-left: 1px dashed #ddd;
}

.ow-attach-list li {
  list-style: none;
  font-style: italic;
  font-weight: normal;
}

.ow-attach-list a {
  border-bottom: 1px solid transparent;
  text-decoration: none;
  transition: all 0.2s ease;
}

.ow-attach-list a:hover {
  border-color: #eee;
  color: #000;
}

.ow-attach-list .$css_attach_dir,
.ow-attach-list .$css_attach_dir > a {
  font-weight: bold;
  font-style: normal;
}

.ow-attach-list a.$css_attach:before {
  margin-right: 5px;
  content: "";
  height: 20px;
  vertical-align: middle;
  width: 20px;
  background-repeat: no-repeat;
  display: inline-block;
  /* file icon by default */
  background-image: url("data:image/svg+xml;base64,$svg_file");
  background-position: center 2px;
  background-size: 60% auto;
}

.ow-attach-list a.$css_attach_dir:before {
  /* folder icon if folder class is specified */
  background-image: url("data:image/svg+xml;base64,$svg_dir");
  background-position: center top;
  background-size: 75% auto;
}
</style>'''
        tpl = Template(template)
        return tpl.safe_substitute(svg_file=svg.SVG_FILE, svg_dir=svg.SVG_DIRECTORY, css_attach_dir=css.CSS_ATTACH_DIR, css_attach=css.CSS_ATTACH)


class AttachListCommand(Command):
    """
    Команда для вставки списка дочерних команд.
    Синтсаксис: (:attachlist [params...]:)
    Параметры:
        subdir="dir_name" - вывести список прикрепленных файлов в поддиректории
        sort=name - сортировка по имени
        sort=descendname - сортировка по имени в обратном направлении
        sort=ext - сортировка по расширению
        sort=descendext - сортировка по расширению в обратном направлении
        sort=size - сортировка по размеру
        sort=descendsize - сортировка по размеру в обратном направлении
    """
    def __init__(self, parser):
        super().__init__(parser)
        self.PARAM_SORT = 'sort'
        self.PARAM_SUBDIR = 'subdir'
        self._append_header = False

    @property
    def name(self):
        return "attachlist"

    def execute(self, params, content):
        params_dict = Command.parseParams(params)
        attach = Attachment(self.parser.page)

        # For empty attach list
        if not attach.getAttachFull():
            return ''

        subdir = params_dict.get(self.PARAM_SUBDIR, '')

        attachlist = attach.getAttachRelative(subdir)
        attachpath = Path(attach.getAttachPath())

        (dirs, files) = self.separateDirFiles(attachlist, attachpath / subdir)

        self._sortFiles(dirs, params_dict)
        self._sortFiles(files, params_dict)

        view = SimpleView()
        if not self._append_header:
            self.parser.appendToHead(view.get_css_styles())
            self._append_header = True

        return view.make(dirs, files, subdir)

    def separateDirFiles(self, attachlist: List[str], attachpath: Path) -> Tuple[List[str], List[str]]:
        """
        Разделить файлы и директории, заодно отбросить директории, начинающиеся с "__"
        """
        dirs = list(filter(lambda name: Path(attachpath, name).is_dir() and not name.startswith('__'), attachlist))
        files = list(filter(lambda name: not Path(attachpath, name).is_dir(), attachlist))

        return (dirs, files)

    def _sortFiles(self, names, params_dict):
        """
        Отсортировать дочерние страницы, если нужно
        """
        attach = Attachment(self.parser.page)

        if self.PARAM_SORT not in params_dict:
            names.sort(key=str.lower)
            return

        sort = params_dict[self.PARAM_SORT].lower()

        if sort == "name":
            names.sort(key=str.lower)
        elif sort == "descendname":
            names.sort(key=str.lower, reverse=True)
        elif sort == "ext":
            names.sort(key=Attachment.sortByExt)
        elif sort == "descendext":
            names.sort(key=Attachment.sortByExt, reverse=True)
        elif sort == "size":
            names.sort(key=attach.sortBySizeRelative)
        elif sort == "descendsize":
            names.sort(key=attach.sortBySizeRelative, reverse=True)
        elif sort == "date":
            names.sort(key=attach.sortByDateRelative)
        elif sort == "descenddate":
            names.sort(key=attach.sortByDateRelative, reverse=True)
        else:
            names.sort(key=str.lower)
