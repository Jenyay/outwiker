#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from command import Command

class TestCommand (Command):
    """
    Тестовая команда. Обрабатывает команды вида (:test params... :) content (:testend:)
    В результате выводит текст:
        Command name: test
        params: params
        content: content
    """
    def __init__ (self, parser):
        """
        parser - экземпляр парсера
        """
        Command.__init__ (self, parser)

    
    @property
    def name (self):
        """
        Возвращает имя команды, которую обрабатывает класс
        """
        return u"test"


    def execute (self, params, content):
        """
        Запустить команду на выполнение. 
        Метод возвращает текст, который будет вставлен на место команды в вики-нотации
        """
        params_result = params if params != None else u""
        content_result = content if content != None else u""

        result = u"""Command name: test
params: {params}
content: {content}""".format (params=params_result.strip(), content=content_result.strip())

        return result


class ExceptionCommand (Command):
    """
    Тестовая команда, которая бросает исключение Exception
    """
    def __init__ (self, parser):
        """
        parser - экземпляр парсера
        """
        Command.__init__ (self, parser)

    
    @property
    def name (self):
        """
        Возвращает имя команды, которую обрабатывает класс
        """
        return u"exception"


    def execute (self, params, content):
        raise Exception
