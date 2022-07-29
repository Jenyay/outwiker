# -*- coding: utf-8 -*-


class LinkCreator:
    def __init__ (self, config):
        """
        config - экземпляр класса WikiConfig
        """
        self._config = config

    def create (self, link, comment):
        if len (comment.strip()) == 0 or link.strip() == comment.strip():
            return self._createCompactStyle (link)

        if self._config.linkStyleOptions.value == 1:
            return self._createForStyle1 (link, comment)

        return self._createForStyle0 (link, comment)

    def _createCompactStyle (self, link):
        return "[[{link}]]".format (link=link)

    def _createForStyle0 (self, link, comment):
        return "[[{comment} -> {link}]]".format (comment=comment, link=link)

    def _createForStyle1 (self, link, comment):
        return "[[{link} | {comment}]]".format (comment=comment, link=link)
