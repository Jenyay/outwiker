# -*- coding: UTF-8 -*-

import os.path

from command import Command
from outwiker.core.attachment import Attachment


class SimpleView (object):
    """
    Класс для простого представления списка прикрепленных файлов - каждая страница на отдельной строке
    """
    @staticmethod
    def make (fnames, attachdir):
        """
        fnames - имена файлов, которые нужно вывести (относительный путь)
        attachdir - путь до прикрепленных файлов (полный, а не относительный)
        """
        template = u'<a href="{link}">{title}</a>\n'

        titles = [u"[%s]" % (name) if os.path.isdir (os.path.join (attachdir, name)) else name for name in fnames]

        result = u"".join ([template.format (link = os.path.join (Attachment.attachDir, name).replace ("\\", "/"), title=title)
                            for (name, title) in zip (fnames, titles)]).rstrip()

        return result


class AttachListCommand (Command):
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
    def __init__ (self, parser):
        Command.__init__ (self, parser)

    @property
    def name (self):
        return u"attachlist"


    def execute (self, params, content):
        params_dict = Command.parseParams (params)
        attach = Attachment (self.parser.page)

        attachlist = attach.getAttachRelative ()
        attachpath = attach.getAttachPath()

        (dirs, files) = self.separateDirFiles (attachlist, attachpath)

        self._sortFiles (dirs, params_dict)
        self._sortFiles (files, params_dict)

        return SimpleView.make (dirs + files, attachpath)


    def separateDirFiles (self, attachlist, attachpath):
        """
        Разделить файлы и директории, заодно отбросить директории, начинающиеся с "__"
        """
        dirs = [name for name in attachlist if os.path.isdir (os.path.join (attachpath, name)) and not name.startswith ("__")]
        files = [name for name in attachlist if not os.path.isdir (os.path.join (attachpath, name))]

        return (dirs, files)


    def _sortFiles (self, names, params_dict):
        """
        Отсортировать дочерние страницы, если нужно
        """
        attach = Attachment (self.parser.page)

        if u"sort" not in params_dict:
            names.sort (Attachment.sortByName)
            return

        sort = params_dict["sort"].lower()

        if sort == u"name":
            names.sort (Attachment.sortByName)
        elif sort == u"descendname":
            names.sort (Attachment.sortByName, reverse=True)
        elif sort == u"ext":
            names.sort (Attachment.sortByExt)
        elif sort == u"descendext":
            names.sort (Attachment.sortByExt, reverse=True)
        elif sort == u"size":
            names.sort (attach.sortBySizeRelative)
        elif sort == u"descendsize":
            names.sort (attach.sortBySizeRelative, reverse=True)
        elif sort == u"date":
            names.sort (attach.sortByDateRelative)
        elif sort == u"descenddate":
            names.sort (attach.sortByDateRelative, reverse=True)
        else:
            names.sort (Attachment.sortByName)
