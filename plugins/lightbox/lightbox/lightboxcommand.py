# -*- coding: UTF-8 -*-

import os.path
import shutil

from outwiker.core.system import getOS
from outwiker.pages.wiki.parser.command import Command
from outwiker.pages.wiki.thumbnails import Thumbnails


class LightboxCommand (Command):
    """
    Викикоманда (:lightbox:), при добавлении которой полноразмерные картинки при клике на превьюшки начинают показываться в окне программы с помощью JavaScript
    """
    def __init__ (self, parser):
        """
        parser - экземпляр парсера
        """
        Command.__init__ (self, parser)
        self.__scriptAppend = False


    @property
    def name (self):
        """
        Возвращает имя команды, которую обрабатывает класс
        """
        return u"lightbox"


    def _copyScriptFiles (self):
        """
        Копировать дополнительные файлы, необходимые для работы скрипта (из папки scripts в __attach/__thumb)
        """
        scriptdir = os.path.join (os.path.dirname (__file__), "scripts")
        thumbDir = Thumbnails (self.parser.page).getThumbPath (True)

        files = ["jquery.fancybox.css",
                 "blank.gif",
                 "fancybox_loading.gif",
                 "jquery-1.7.2.min.js",
                 "jquery.fancybox.pack.js",
                 "fancybox_sprite.png"
                 ]

        for fname in files:
            srcPath = os.path.join (scriptdir, fname)
            dstPath = os.path.join (thumbDir, fname)
            shutil.copyfile (srcPath, dstPath)


    def execute (self, params, content):
        """
        Запустить команду на выполнение.
        Метод возвращает текст, который будет вставлен на место команды в вики-нотации
        """

        if not self.__scriptAppend:
            self.__scriptAppend = True

            header = u"""<script type="text/javascript" src="./__attach/__thumb/jquery-1.7.2.min.js"></script>
<link rel="stylesheet" href="./__attach/__thumb/jquery.fancybox.css" type="text/css" media="screen" />
<script type="text/javascript" src="./__attach/__thumb/jquery.fancybox.pack.js"></script>"""

            self.parser.appendToHead (header)

            try:
                self._copyScriptFiles()
            except IOError as e:
                return _(u"<B>Can't copy script files</B>\n{0}").format (e)

        return u"""<script>  $(document).ready(function() {    $("a[href$='.jpg'],a[href$='.jpeg'],a[href$='.JPG'],a[href$='.JPEG'],a[href$='.png'],a[href$='.PNG'],a[href$='.gif'],a[href$='.GIF'],a[href$='.bmp'],a[href$='.BMP'],a[href$='.tif'],a[href$='.TIF'],a[href$='.tiff'],a[href$='.TIFF']").attr('rel', 'gallery').fancybox();  });</script>"""
