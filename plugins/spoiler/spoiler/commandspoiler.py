# -*- coding: utf-8 -*-

from outwiker.api.pages.wiki.wikiparser import Command

from .i18n import get_


class SpoilerCommand(Command):
    """
    Команда для вставки скрываемого текста.
    Обрабатывает команды вида (:spoiler params... :) content (:spoilerend:)
    Параметры:
        expandtext - текст вместо надписи "Expand/Развернуть"
        collapsetext - текст вместо надписи "Collapse/Свернуть"
        inline - спойлер вставляется в текст
    """

    def __init__(self, parser, name, lang):
        """
        parser - экземпляр парсера
        """
        super().__init__(parser)
        global _
        _ = get_()

        self.__name = name

        self.__style1 = """<style>div.spoiler_style1 {
    padding: 3px;
    border: 1px solid #d8d8d8;
    }</style>"""

        self.__style2 = """<style>div.spoiler_style2 {
    text-transform: uppercase;
    border-bottom: 1px solid #CCCCCC;
    margin-bottom: 3px;
    font-size: 0.8em;
    font-weight: bold;
    display: block;
    }</style>"""

        self.__blockTemplate = r"""
        <div class="spoiler_style1"><div class="spoiler_style2"><span onClick="if (this.parentNode.parentNode.getElementsByTagName('div')[1].getElementsByTagName('div')[0].style.display != '') {  this.parentNode.parentNode.getElementsByTagName('div')[1].getElementsByTagName('div')[0].style.display = ''; this.innerHTML = '<b></b><a href=\'#\' onClick=\'return false;\'>{collapsetext}</a>'; } else { this.parentNode.parentNode.getElementsByTagName('div')[1].getElementsByTagName('div')[0].style.display = 'none'; this.innerHTML = '<b></b><a href=\'#\' onClick=\'return false;\'>{expandtext}</a>'; }" /><b></b><a href="#" onClick="return false;">{expandtext}</a></span></div><div class="spoiler_quotecontent"><div style="display: none;">{content}</div></div></div>"""

        self.__inlineTemplate = r"""<span><span onClick="this.parentNode.getElementsByTagName('span')[1].style.display = ''; this.style.display = 'none';"><a href="#">{expandtext}</a></span><span style="display: none;" onClick="this.parentNode.getElementsByTagName('span')[0].style.display = ''; this.style.display = 'none';">{content}</span></span>"""

        self.__expandParam = "expandtext"
        self.__collapseParam = "collapsetext"
        self.__inlineParam = "inline"

        # Надписи по умолчанию
        self.__expandTextDefault = _("Expand")
        self.__collapseTextDefault = _("Collapse")

        # Добавлены ли стили в заголовок
        self.__styleAppend = False

    @property
    def name(self):
        """
        Возвращает имя команды, которую обрабатывает класс
        """
        return self.__name

    def execute(self, params, content):
        """
        Запустить команду на выполнение.
        Метод возвращает текст, который будет вставлен на место
        команды в вики-нотации
        """
        params_dict = Command.parseParams(params)
        template = self.__getTemplate(params_dict)

        parsedcontent = self.parser.parseWikiMarkup(content.strip())
        result = template.replace("{expandtext}", self.__getExpandText(params_dict))
        result = result.replace("{collapsetext}", self.__getCollapseText(params_dict))
        result = result.replace("{content}", parsedcontent)

        self.__appendStyles()
        return result

    def __getTemplate(self, params_dict):
        """
        Возвращает шаблон в зависимости от вида спойлера
        """
        if self.__inlineParam in params_dict:
            return self.__inlineTemplate
        else:
            return self.__blockTemplate

    def __appendStyles(self):
        if not self.__styleAppend:
            self.parser.appendToHead(self.__style1)
            self.parser.appendToHead(self.__style2)

            self.__styleAppend = True

    def __getExpandText(self, params_dict):
        try:
            return params_dict[self.__expandParam].strip()
        except KeyError:
            return self.__expandTextDefault

    def __getCollapseText(self, params_dict):
        try:
            return params_dict[self.__collapseParam].strip()
        except KeyError:
            return self.__collapseTextDefault
