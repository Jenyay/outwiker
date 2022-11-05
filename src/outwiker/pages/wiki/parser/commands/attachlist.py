# -*- coding: utf-8 -*-

import os.path
from pathlib import Path
from typing import List, Tuple

from outwiker.core.attachment import Attachment
from outwiker.core.defines import PAGE_ATTACH_DIR
from outwiker.pages.wiki.parser.command import Command
import outwiker.gui.cssclasses as css


class SimpleView:
    """
    Класс для простого представления списка прикрепленных файлов - каждая страница на отдельной строке
    """
    def __init__(self):
        self._item_file_css_class = '{} {}'.format(css.CSS_ATTACH, css.CSS_ATTACH_FILE)
        self._item_dir_css_class = '{} {}'.format(css.CSS_ATTACH, css.CSS_ATTACH_DIR)

        self._item_template = '<li class="{css_class}"><a href="{link}">{title}</a></li>'    
        self._list_template = '<ul class="{css_class}">{content}</ul>'

    def make(self, dirnames, fnames,  subdir):
        """
        fnames - имена файлов, которые нужно вывести (относительный путь)
        attach_path - путь до прикрепленных файлов (полный)
        """
        content_items = [self._get_item_dir(name, subdir) for name in dirnames]
        content_items += [self._get_item_file(name, subdir) for name in fnames]
        content = ''.join(content_items)

        return self._list_template.format(css_class=css.CSS_ATTACH_LIST, content=content)

    def _get_item_dir(self, name: str, subdir: str) -> str:
        link = self._get_attach_path(subdir, name)
        return self._item_template.format(link=link, title=name, css_class=self._item_dir_css_class)

    def _get_item_file(self, name: str, subdir: str) -> str:
        link = self._get_attach_path(subdir, name)
        return self._item_template.format(link=link, title=name, css_class=self._item_file_css_class)

    def _get_attach_path(self, subdir: str, fname: str) -> str:
        return os.path.join(PAGE_ATTACH_DIR, subdir, fname).replace("\\", "/")

    def get_css_styles(self) -> str:
        return '''<style>
.ow-attach-list ul {
  margin-left: 10px;
  padding-left: 20px;
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

.ow-attach-list .ow-attach-dir,
.ow-attach-list .ow-attach-dir > a {
  font-weight: bold;
  font-style: normal;
}

.ow-attach-list li:before {
  margin-right: 10px;
  content: "";
  height: 20px;
  vertical-align: middle;
  width: 20px;
  background-repeat: no-repeat;
  display: inline-block;
  /* file icon by default */
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><path fill='lightgrey' d='M85.714,42.857V87.5c0,1.487-0.521,2.752-1.562,3.794c-1.042,1.041-2.308,1.562-3.795,1.562H19.643 c-1.488,0-2.753-0.521-3.794-1.562c-1.042-1.042-1.562-2.307-1.562-3.794v-75c0-1.487,0.521-2.752,1.562-3.794 c1.041-1.041,2.306-1.562,3.794-1.562H50V37.5c0,1.488,0.521,2.753,1.562,3.795s2.307,1.562,3.795,1.562H85.714z M85.546,35.714 H57.143V7.311c3.05,0.558,5.505,1.767,7.366,3.627l17.41,17.411C83.78,30.209,84.989,32.665,85.546,35.714z' /></svg>");
  background-position: center 2px;
  background-size: 60% auto;
}

.ow-attach-list li.ow-attach-dir:before {
  /* folder icon if folder class is specified */
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><path fill='lightblue' d='M96.429,37.5v39.286c0,3.423-1.228,6.361-3.684,8.817c-2.455,2.455-5.395,3.683-8.816,3.683H16.071 c-3.423,0-6.362-1.228-8.817-3.683c-2.456-2.456-3.683-5.395-3.683-8.817V23.214c0-3.422,1.228-6.362,3.683-8.817 c2.455-2.456,5.394-3.683,8.817-3.683h17.857c3.422,0,6.362,1.228,8.817,3.683c2.455,2.455,3.683,5.395,3.683,8.817V25h37.5 c3.422,0,6.361,1.228,8.816,3.683C95.201,31.138,96.429,34.078,96.429,37.5z' /></svg>");
  background-position: center top;
  background-size: 75% auto;
}
</style>'''


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
