#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from command import Command


class LjUserCommand (Command):
	"""
	Команда для вставки ссылки на пользователя ЖЖ
	Синтсаксис: (:ljuser name:)
	"""
	def __init__ (self, parser):
		Command.__init__ (self, parser)
		self.template = u"""<span class='ljuser ljuser-name_{username}' lj:user='{username}' style='white-space:nowrap'><a href='http://{username_corrent}.livejournal.com/profile'><img src='http://l-stat.livejournal.com/img/userinfo.gif?v=2' alt='[info]' width='17' height='17' style='vertical-align: bottom; border: 0; padding-right: 1px;'/></a><a href='http://{username_corrent}.livejournal.com/'><b>{username}</b></a></span>"""

	@property
	def name (self):
		return u"ljuser"


	def execute (self, params, content):
		username = params
		username_corrent = params.replace ("_", "-")
		return self.template.format (username=username, username_corrent=username_corrent)


class LjCommunityCommand (Command):
	"""
	Команда для вставки ссылки на пользователя ЖЖ
	Синтсаксис: (:ljuser name:)
	"""
	def __init__ (self, parser):
		Command.__init__ (self, parser)
		self.template = u"""<span class='ljuser ljuser-name_{community}' lj:user='{community}' style='white-space:nowrap'><a href='http://community.livejournal.com/{community}/profile'><img src='http://l-stat.livejournal.com/img/community.gif?v=2' alt='[info]' width='16' height='16' style='vertical-align: bottom; border: 0; padding-right: 1px;'/></a><a href='http://community.livejournal.com/{community}/'><b>{community}</b></a></span>"""

	@property
	def name (self):
		return u"ljcomm"


	def execute (self, params, content):
		community = params
		return self.template.format (community=community)
