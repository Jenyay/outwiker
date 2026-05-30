# -*- coding: utf-8 -*-


class TagsList:
    """
    Class for storing the list of all tags in the wiki
    """

    def __init__(self, root):
        # Dictionary of tags. Key - tag, value - list of pages with this tag
        self._tags = {}

        self._findTags(root)

    @property
    def tags(self):
        """
        Returns the list of tags
        """
        return list(sorted(self._tags.keys()))

    def _findTags(self, page):
        """
        Search for tags for page and its child pages
        """
        if page.parent is not None:
            for tag in page.tags:
                tag_lower = tag.lower()

                if tag_lower in self._tags:
                    self._tags[tag_lower].append(page)
                else:
                    self._tags[tag_lower] = [page]

        for child in page.children:
            self._findTags(child)

    def __len__(self):
        return len(self._tags)

    def __getitem__(self, tag):
        try:
            pages = self._tags[tag.lower()]
        except KeyError:
            pages = []

        return pages

    def __iter__(self):
        return iter(sorted(self._tags))
