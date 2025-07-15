# -*- coding: utf-8 -*-

import os.path
from pathlib import Path
from typing import List, Tuple

from outwiker.core.attachment import Attachment
from outwiker.core.defines import PAGE_ATTACH_DIR
from outwiker.pages.wiki.parser.command import Command
import outwiker.core.cssclasses as css
from outwiker.pages.wiki.parser.wikiparser import Parser


CSS_ID_STYLES = css.CSS_ATTACH_LIST
CSS_STYLES = """ul.ow-attach-list {
		  margin-left: 0px;
		  padding-left: 0px;
		}

		.ow-attach-list ul {
		  margin-left: 15px;
		  padding-left: 10px;
		  border-left: 1px dashed #ddd;
		}

		ul.ow-attach-list li {
		  list-style: none;
		  font-weight: normal;
          background-image: none;
          padding-left: 1.0rem;
		}

		.ow-attach-list a.ow-attach-dir {
		  font-weight: bold;
		  font-style: normal;
		  transition: all 0.2s ease;
		}"""


class SimpleView:
    """
    Класс для простого представления списка прикрепленных файлов - каждая страница на отдельной строке
    """
    def __init__(self):
        self._list_template = '<ul class="ow-attach-list">{title}<ul class="ow-attach-list">{content}</ul></ul>'
        self._item_template = '<li class="{css_class}"><a class="ow-link-attach {css_class}" href="{link}">{title}</a></li>'

    def make(self, parser: Parser, dirnames: List[str], fnames: List[str], subdir: str):
        """
        fnames - имена файлов, которые нужно вывести (относительный путь)
        attach_path - путь до прикрепленных файлов (полный)
        """
        content_items = [self._get_item_dir(subdir, name, name) for name in dirnames]
        content_items += [self._get_item_file(subdir, name, name) for name in fnames]
        content = ''.join(content_items)
        title = self._get_title(subdir)

        parser.addStyle(CSS_ID_STYLES, CSS_STYLES)
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
        return view.make(self.parser, dirs, files, subdir)

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
