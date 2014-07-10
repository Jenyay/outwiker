# -*- coding: UTF-8 -*-

import os.path
import re

from .exporterfactory import ExporterFactory
from .indexgenerator import IndexGenerator
from outwiker.core.tree import WikiDocument


class BranchExporter (object):
    def __init__ (self, startpage, nameGenerator, application):
        self.__startpage = startpage
        self.__application = application

        self.__indexfname = u"__index.html"
        self.__contentfname = u"__content.html"

        # Список ошибок, возникших при экспорте
        self.__log = []
        self.__nameGenerator = nameGenerator

        self.__a_tag_regex = re.compile (
            """
            (<\s*a\s+
            (.*?)
            href\s*=['"](.*?)['"]
            (.*?)>)
            """,
            re.IGNORECASE | re.MULTILINE | re.DOTALL | re.VERBOSE)


        # Словарь, который сохраняет, как была названа каждая страница при экспорте
        # Ключ - страница, значение - имя ее директории или файла (без расширения) после экспорта
        self.__renames = {}


    @property
    def log (self):
        return self.__log


    def export (self, outdir, imagesonly, alwaysOverwrite):
        self.__log = []
        self.__renames = {}

        self.__export (self.__startpage,
                       self.__startpage,
                       outdir,
                       imagesonly,
                       alwaysOverwrite)

        self.__replacePageLinks (outdir)
        try:
            self.__createIndex (outdir, alwaysOverwrite)
        except IOError, e:
            str (e)

        return self.log


    def __createIndex (self, outdir, alwaysOverwrite):
        """
        Создать оглавление
        """
        indexpath = os.path.join (outdir, self.__indexfname)
        contentpath = os.path.join (outdir, self.__contentfname)

        indexgenerator = IndexGenerator (self.__startpage, self.__renames)
        indexgenerator.generatefiles (indexpath, contentpath)


    def __replacePageLinks (self, outdir):
        """
        Скорректировать ссылки на страницы
        """
        for page in self.__renames.keys():
            fullname = os.path.join (outdir, self.__renames[page] + u".html")

            try:
                with open (fullname) as fp:
                    text = unicode (fp.read (), "utf8")

                newtext = self.__replacePageLinksInText (text, page, outdir)

                with open (fullname, "wb") as fp:
                    fp.write (newtext.encode ("utf8"))
            except BaseException, error:
                self.__log.append (u"{0}: {1}".format (page.title, unicode (error)))



    def __replacePageLinksInText (self, text, page, outdir):
        matches = self.__a_tag_regex.findall (text)
        hrefMatchIndex = 2
        fullMatchIndex = 0

        result = text

        for match in matches:
            url = match[hrefMatchIndex]

            # Проверить, что это не ссылка на сайт
            if self.__isInternetUrl (url):
                continue

            # Проверить, что это не ссылка на файл
            if self.__isFileLink (url, outdir):
                continue

            linkToPage = None
            anchor = None

            linkToPage, anchor = self.__getPageByProtocol (url)

            # Это ссылка на подстраницу?
            if linkToPage is None:
                linkToPage = page[url]

            if linkToPage is None:
                # Это ссылка на страницу из корня?
                correcturl = url[1:] if url[0] == "/" else url
                linkToPage = page.root[correcturl]

            if linkToPage is None:
                continue

            if linkToPage not in self.__renames.keys():
                continue

            # Эта страница нам подходит
            # Новая ссылка
            newhref = self.__renames[linkToPage] + ".html"
            if anchor is not None:
                newhref += anchor

            newFullLink = match[fullMatchIndex].replace (url, newhref)

            result = result.replace (match[fullMatchIndex], newFullLink)

        return result


    def __getPageByProtocol (self, href):
        """
        Если href - протокол вида page://..., то возвращает страницу, на которую ведет ссылка (если она существует), в противном случае возвращает None.
        """
        # Т.к. поддержка этого протокола появилась только в версии 1.8.0,
        # то нужно проверить, есть ли в self.__application член pageUidDepot
        if "pageUidDepot" not in self.__application.__dict__:
            return (None, None)

        protocol = u"page://"

        if not href.startswith (protocol):
            return (None, None)

        # Отсечем протокол
        uid = href[len (protocol):]

        # Отсечем все, что после /
        slashPos = uid.find ("/")
        uid_clean = uid[: slashPos] if slashPos != -1 else uid

        page = self.__application.pageUidDepot[uid_clean]
        anchor = self.__getAnchor (uid)

        return (page, anchor)


    def __getAnchor (self, href):
        """
        Попытаться найти якорь, если используется ссылка вида page://...
        """
        pos = href.rfind ("/#")
        if pos != -1:
            return href[pos + 1:]

        return None


    def __isInternetUrl (self, url):
        return (url.startswith ("http://") or
                url.startswith ("https://") or
                url.startswith ("ftp://") or
                url.startswith ("mailto:"))


    def __isFileLink (self, url, outdir):
        fname = os.path.join (outdir, url)
        return os.path.exists (fname) and os.path.isfile (fname)


    def __export (self,
                  page,
                  root,
                  outdir,
                  imagesonly,
                  alwaysOverwrite):
        """
        page - страница, начиная с которой надо начать экспортирование
        root - корневая страница, откуда началось общее экспортирование (для определения имени файлов)
        outdir - директория для экспорта
        imagesonly - из вложений оставлять только картинки?
        alwaysOverwrite - перезаписывать существующие файлы?
        """
        if page.getTypeString() != WikiDocument.getTypeString():
            try:
                exporter = ExporterFactory.getExporter (page)
                exportname = self.__nameGenerator.getName (page)
                self.__renames[page] = exportname

                exporter.export (outdir, exportname, imagesonly, alwaysOverwrite)
            except BaseException, error:
                self.__log.append (u"{0}: {1}".format (page.title, unicode (error)))

        for child in page.children:
            self.__export (
                child,
                root,
                outdir,
                imagesonly,
                alwaysOverwrite)
