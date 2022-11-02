# -*- coding: utf-8 -*-

import os.path

from outwiker.core.attachment import Attachment
from outwiker.core.defines import PAGE_ATTACH_DIR
from outwiker.pages.wiki.parser.command import Command
from outwiker.gui.cssclasses import CSS_ATTACH, CSS_ATTACH_LIST


class SimpleView:
    """
    Класс для простого представления списка прикрепленных файлов - каждая страница на отдельной строке
    """
    def __init__(self):
        self._item_template = '<a class="{css_class}" href="{link}">{title}</a>\n'    
        self._list_template = '<div class="{css_class}">{content}</div>'

    def make(self, fnames, attach_dir):
        """
        fnames - имена файлов, которые нужно вывести (относительный путь)
        attach_dir - путь до прикрепленных файлов (полный)
        """
        content = ''.join([self._get_link(fname, attach_dir) for fname in fnames]).rstrip()
        return self._list_template.format(css_class=CSS_ATTACH_LIST, content=content)

    def _get_link(self, fname: str, attach_dir: str) -> str:
        if os.path.isdir(os.path.join(attach_dir, fname)):
            title = self._get_dir_item(fname)
        else:
            title = self._get_file_item(fname) 

        return self._item_template.format(link=self._get_attach_path(fname), title=title, css_class=CSS_ATTACH)

    def _get_dir_item(self, dirname: str) -> str:
        return "[{}]".format(dirname)

    def _get_file_item(self, fname: str) -> str:
        return fname

    def _get_attach_path(self, fname: str) -> str:
        return os.path.join(PAGE_ATTACH_DIR, fname).replace("\\", "/")


class AttachListCommand(Command):
    """
    Команда для вставки списка дочерних команд.
    Синтсаксис: (:attachlist [params...]:)
    Параметры:
        sort=name - сортировка по имени
        sort=descendname - сортировка по имени в обратном направлении
        sort=ext - сортировка по расширению
        sort=descendext - сортировка по расширению в обратном направлении
        sort=size - сортировка по размеру
        sort=descendsize - сортировка по размеру в обратном направлении
    """
    @property
    def name(self):
        return "attachlist"

    def execute(self, params, content):
        params_dict = Command.parseParams(params)
        attach = Attachment(self.parser.page)

        attachlist = attach.getAttachRelative()
        attachpath = attach.getAttachPath()

        (dirs, files) = self.separateDirFiles(attachlist, attachpath)

        self._sortFiles(dirs, params_dict)
        self._sortFiles(files, params_dict)

        view = SimpleView()
        return view.make(dirs + files, attachpath)

    def separateDirFiles(self, attachlist, attachpath):
        """
        Разделить файлы и директории, заодно отбросить директории, начинающиеся с "__"
        """
        dirs = [name for name in attachlist if os.path.isdir(
            os.path.join(attachpath, name)) and not name.startswith("__")]
        files = [name for name in attachlist if not os.path.isdir(
            os.path.join(attachpath, name))]

        return (dirs, files)

    def _sortFiles(self, names, params_dict):
        """
        Отсортировать дочерние страницы, если нужно
        """
        attach = Attachment(self.parser.page)

        if "sort" not in params_dict:
            names.sort(key=str.lower)
            return

        sort = params_dict["sort"].lower()

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
