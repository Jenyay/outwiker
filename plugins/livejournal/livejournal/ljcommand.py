# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractproperty

from outwiker.api.pages.wiki.wikiparser import Command


class LjCommand(Command, metaclass=ABCMeta):
    def __init__(self, parser):
        super().__init__(parser)

    @abstractproperty
    def template(self):
        pass

    def execute(self, params, content):
        name = params
        return self.template.format(name=name, name_correct=name.replace("_", "-"))


class LjUserCommand(LjCommand):
    """
    Команда для вставки ссылки на пользователя ЖЖ
    Синтсаксис: (:ljuser name:)
    """

    def __init__(self, parser):
        super().__init__(parser)

    @property
    def template(self):
        return """<span class='ljuser ljuser-name_{name}' lj:user='{name}' style='white-space:nowrap'><a href='http://{name_correct}.livejournal.com/profile'><img src='http://l-stat.livejournal.com/img/userinfo.gif?v=3' alt='[info]' width='17' height='17' style='vertical-align: bottom; border: 0; padding-right: 1px;'/></a><a href='http://{name_correct}.livejournal.com/'><b>{name}</b></a></span>"""

    @property
    def name(self):
        return "ljuser"


class LjCommunityCommand(LjCommand):
    """
    Команда для вставки ссылки на пользователя ЖЖ
    Синтсаксис: (:ljcomm name:)
    """

    def __init__(self, parser):
        super().__init__(parser)

    @property
    def template(self):
        return """<span class='ljuser ljuser-name_{name}' lj:user='{name}' style='white-space:nowrap'><a href='http://{name_correct}.livejournal.com/profile'><img src='http://l-stat.livejournal.com/img/community.gif?v=3' alt='[info]' width='16' height='16' style='vertical-align: bottom; border: 0; padding-right: 1px;'/></a><a href='http://{name_correct}.livejournal.com/'><b>{name}</b></a></span>"""

    @property
    def name(self):
        return "ljcomm"
