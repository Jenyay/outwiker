#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from outwiker.pages.wiki.parser.command import Command

class SpoilerCommand (Command):
    """
    Команда для вставки скрываемого текста. Обрабатывает команды вида (:spoiler params... :) content (:spoilerend:)
    Параметры:
        expandtext - текст вместо надписи "Expand/Развернуть"
        collapsetext - текст вместо надписи "Collapse/Свернуть"
    """
    def __init__ (self, parser, name, lang):
        """
        parser - экземпляр парсера
        """
        Command.__init__ (self, parser)
        global _
        _ = lang

        self.__name = name

        self.__style1 = u"""<STYLE>div.spoiler_style1 {
    padding: 3px; 
    border: 1px solid #d8d8d8; 
    }</STYLE>"""

        self.__style2 = u"""<STYLE>div.spoiler_style2 {
    text-transform: uppercase; 
    border-bottom: 1px solid #CCCCCC; 
    margin-bottom: 3px; 
    font-size: 0.8em; 
    font-weight: bold; 
    display: block;
    }</STYLE>"""

        self.__resultTemplate = ur"""
        <div class="spoiler_style1"><div class="spoiler_style2"><span onClick="if (this.parentNode.parentNode.getElementsByTagName('div')[1].getElementsByTagName('div')[0].style.display != '') {  this.parentNode.parentNode.getElementsByTagName('div')[1].getElementsByTagName('div')[0].style.display = ''; this.innerHTML = '<b></b><a href=\'#\' onClick=\'return false;\'>{collapsetext}</a>'; } else { this.parentNode.parentNode.getElementsByTagName('div')[1].getElementsByTagName('div')[0].style.display = 'none'; this.innerHTML = '<b></b><a href=\'#\' onClick=\'return false;\'>{expandtext}</a>'; }" /><b></b><a href="#" onClick="return false;">{expandtext}</a></span></div><div class="spoiler_quotecontent"><div style="display: none;">{content}</div></div></div>"""
    
        self.__expandParam = u"expandtext"
        self.__collapseParam = u"collapsetext"

        # Надписи по умолчанию
        self.__expandTextDefault = _(u"Expand")
        self.__collapseTextDefault = _(u"Collapse")

        # Добавлены ли стили в заголовок
        self.__styleAppend = False

    
    @property
    def name (self):
        """
        Возвращает имя команды, которую обрабатывает класс
        """
        return self.__name


    def execute (self, params, content):
        """
        Запустить команду на выполнение. 
        Метод возвращает текст, который будет вставлен на место команды в вики-нотации
        """
        params_dict = Command.parseParams (params)

        parsedcontent = self.parser.parseWikiMarkup (content.strip())
        result = self.__resultTemplate.replace (u"{expandtext}", self.__getExpandText (params_dict) )
        result = result.replace (u"{collapsetext}", self.__getCollapseText (params_dict) )
        result = result.replace (u"{content}", parsedcontent)

        self.__appendStyles()

        return result


    def __appendStyles (self):
        if not self.__styleAppend:
            self.parser.appendToHead (self.__style1)
            self.parser.appendToHead (self.__style2)

            self.__styleAppend = True


    def __getExpandText (self, params_dict):
        try:
            return params_dict[self.__expandParam].strip()
        except KeyError:
            return self.__expandTextDefault


    def __getCollapseText (self, params_dict):
        try:
            return params_dict[self.__collapseParam].strip()
        except KeyError:
            return self.__collapseTextDefault
