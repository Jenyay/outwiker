# -*- coding: utf-8 -*-

"""
Classes for global wiki search
"""
import os.path

from outwiker.core.attachment import Attachment


class AllTagsSearchStrategy(object):
    """
    Tag search strategy when all tags must be found
    """
    @staticmethod
    def testTags(tags, page):
        result = True

        page_tags = [tag.lower() for tag in page.tags]

        for tag in tags:
            if tag not in page_tags:
                result = False
                break

        return result


class AnyTagSearchStrategy(object):
    """
    Tag search strategy when it's enough to find one tag
    """
    @staticmethod
    def testTags(tags, page):
        if len(tags) == 0:
            return True

        result = False

        page_tags = [tag.lower() for tag in page.tags]

        for tag in tags:
            if tag in page_tags:
                result = True
                break

        return result


class Searcher(object):
    def __init__(self, phrase, tags, tagsStrategy):
        """
        phrase - search string (unparsed)
        tags - list of tags to search pages by
        tagsStrategy - tag search strategy
        """
        self.phrase = phrase
        self.tags = [tag.lower() for tag in tags]
        self.tagsStrategy = tagsStrategy

    def find(self, root):
        """
        Find pages matching the search condition
        """
        result = []

        for page in root.children:
            if(self.tagsStrategy.testTags(self.tags, page) and
                    self.__testFullContent(page)):
                result.append(page)

            result += self.find(page)

        return result

    def __testFullContent(self, page):
        """
        Search for the desired text in different parts of the note
        (content, title, tags)
        """
        return (self.__testTitle(page) or
                self.__testContent(page) or
                self.__testTagsContent(page) or
                self.__testAttachment(page))

    def __testTitle(self, page):
        title = page.title.lower()

        if len(self.phrase) == 0 or self.phrase.lower() in title:
            return True

        return False

    def __testContent(self, page):
        """
        Check if the search phrase occurs in the page content.
        Also returns True if the content is empty
        """
        content = page.textContent.lower()
        if len(self.phrase) == 0 or self.phrase.lower() in content:
            return True

        return False

    def __testTagsContent(self, page):
        """
        Check if the search phrase occurs in the tags text
        """
        lowerPhrase = self.phrase.lower()
        tags = [tag for tag in page.tags if lowerPhrase in tag.lower()]
        return len(tags) != 0

    def __testAttachment(self, page):
        attach = Attachment(page)
        if not os.path.exists(attach.getAttachPath()):
            return False

        lowerPhrase = self.phrase.lower()

        for root, subfolders, files in os.walk(attach.getAttachPath()):
            filterfiles = ([fname for fname in files if lowerPhrase in fname.lower()])
            filterdirs = ([dirname for dirname in subfolders if lowerPhrase in dirname.lower()])

            if (len(filterfiles) != 0 or len(filterdirs) != 0):
                return True

        return False
