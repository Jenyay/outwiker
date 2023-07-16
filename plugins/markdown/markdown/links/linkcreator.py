# -*- coding: utf-8 -*-


class LinkCreator:
    def create(self, link, comment, title):
        """
        Return tuple: (link string, reference string or None)
        """
        link = link.strip()
        reference = None
        if len(title.strip()) == 0:
            link_text = "[{comment}]({link})".format(comment=comment, link=link)
        else:
            link_text = '[{comment}]({link} "{title}")'.format(
                comment=comment, link=link, title=title
            )

        return (link_text, reference)
