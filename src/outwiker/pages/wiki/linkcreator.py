# -*- coding: UTF-8 -*-


class LinkCreator (object):
    def __init__ (self, config):
        """
        config - экземпляр класса WikiConfig
        """
        self.__config = config


    def create (self, link, comment):
        if len (comment.strip()) == 0 or link.strip() == comment.strip():
            return self.__createCompactStyle (link)

        if self.__config.linkStyleOptions.value == 1:
            return self.__createForStyle1 (link, comment)

        return self.__createForStyle0 (link, comment)


    def __createCompactStyle (self, link):
        return u"[[{link}]]".format (link=link)


    def __createForStyle0 (self, link, comment):
        return u"[[{comment} -> {link}]]".format (comment=comment, link=link)


    def __createForStyle1 (self, link, comment):
        return u"[[{link} | {comment}]]".format (comment=comment, link=link)
