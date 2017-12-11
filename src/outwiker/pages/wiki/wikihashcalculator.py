# -*- coding: UTF-8 -*-

import os.path
import hashlib
from StringIO import StringIO
from functools import cmp_to_key

from outwiker.core.attachment import Attachment
from outwiker.core.style import Style
from outwiker.gui.guiconfig import HtmlRenderConfig

from .wikiconfig import WikiConfig
from .emptycontent import EmptyContent


class WikiHashCalculator (object):
    """
    Класс для расчета контрольной суммы викистраницы
    """
    def __init__ (self, application):
        self._unicodeEncoding = "unicode_escape"

        self._application = application
        self._mainConfig = self._application.config
        self._wikiConfig = WikiConfig (self._mainConfig)
        self._htmlConfig = HtmlRenderConfig (self._mainConfig)


    def getHash (self, page):
        return hashlib.md5(self.__getFullContent (page)).hexdigest()


    def __getFullContent (self, page):
        """
        Получить контент для расчета контрольной суммы, по которой определяется, нужно ли обновлять страницу
        """
        # Здесь накапливаем список интересующих строк (по которым определяем изменилась страница или нет)
        content = StringIO()

        # Заголовок страницы
        content.write (page.title.encode (self._unicodeEncoding))

        # Содержимое
        pagecontent = page.content.encode (self._unicodeEncoding)
        content.write (pagecontent)

        self.__getDirContent (page, content)
        content.write (self.__getPluginsList())
        content.write (self.__getStyleContent (page))

        # Настройки, касающиеся вида вики-страницы
        content.write (str (self._wikiConfig.showAttachInsteadBlankOptions.value))
        content.write (str (self._wikiConfig.thumbSizeOptions.value))

        # Настройки отображения HTML-страницы
        content.write (str (self._htmlConfig.fontSize.value))
        content.write (self._htmlConfig.fontName.value.encode(self._unicodeEncoding))
        content.write (self._htmlConfig.userStyle.value.encode(self._unicodeEncoding))
        content.write (self._htmlConfig.HTMLImprover.value.encode(self._unicodeEncoding))

        # Список подстраниц
        for child in page.children:
            content.write (child.title.encode (self._unicodeEncoding) + "\n")

        if len (page.content) == 0:
            # Если страница пустая, то проверим настройку, отвечающую за шаблон пустой страницы
            emptycontent = EmptyContent (self._mainConfig)
            content.write (emptycontent.content.encode (self._unicodeEncoding))

        result = content.getvalue()
        content.close()

        return result


    def __getStyleContent (self, page):
        """
        Возвращает содержимое шаблона
        """
        style = Style ()

        try:
            with open (style.getPageStyle (page)) as fp:
                stylecontent = unicode (fp.read(), "utf8")
        except IOError:
            stylecontent = u""
        except UnicodeDecodeError:
            stylecontent = u""

        return stylecontent.encode (self._unicodeEncoding)


    def __getPluginsList (self):
        """
        Создать список плагинов с учетом номеров версий
        Возвращает строку
        """
        if len (self._application.plugins) == 0:
            return u""

        plugins = [plugin.name + unicode(plugin.version) for plugin in self._application.plugins]
        plugins.sort()
        result = reduce (lambda x, y: x + y, plugins)
        return result


    def __getDirContent (self, page, filescontent, dirname="."):
        """
        Сформировать строку для расчета хеша по данным вложенной поддиректории dirname (путь относительно __attach)
        page - страница, для которой собираем список вложений
        filescontent - список, содержащий строки, описывающие вложенные файлы
        """
        attach = Attachment (page)
        attachroot = attach.getAttachPath()

        attachlist = attach.getAttachRelative (dirname)
        attachlist.sort (key=cmp_to_key(Attachment.sortByName))

        for fname in attachlist:
            fullpath = os.path.join (attachroot, dirname, fname)

            # Пропустим директории, которые начинаются с __
            if not os.path.isdir (fname) or not fname.startswith ("__"):
                try:
                    filescontent.write (fname.encode (self._unicodeEncoding))
                    filescontent.write (unicode (os.stat (fullpath).st_mtime))

                    if os.path.isdir (fullpath):
                        self.__getDirContent (page, filescontent, os.path.join (dirname, fname))
                except OSError:
                    # Если есть проблемы с доступом к файлу, то здесь на это не будем обращать внимания
                    pass
