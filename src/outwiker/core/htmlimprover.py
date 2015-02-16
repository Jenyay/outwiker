# -*- coding: UTF-8 -*-

from abc import ABCMeta, abstractmethod
import re
from StringIO import StringIO


def getHtmlImprover (improvername):
    """
    Return needed improver (for the time being always return BrHtmlImprover)
    """
    return BrHtmlImprover()


class HtmlImprover (object):
    """
    Class make HTML code more readable and append line breaks.
    """
    __metaclass__ = ABCMeta


    def __init__ (self):
        specialTags = [u'pre', u'script']

        flags = re.I | re.S | re.M

        # List of tuples of the regexp for opening and closing tags
        self._tagsRegexp = [(re.compile (u'\n?<\s*{}.*?>'.format (name), flags),
                             re.compile (u'</\s*{}\s*>\n?'.format (name), flags))
                            for name in specialTags]


    def run (self, text):
        result = text.replace ("\r\n", "\n")
        result = self._replaceEndlines (result)

        return result


    def _replaceEndlines (self, text):
        # Current search position
        start = 0

        # Current index of the special tag (if we inside it)
        currenttag = None

        buf = StringIO()
        while start != -1:
            nexttagstart, nexttagend, currenttag = self._findNextTag (text, start)
            if nexttagstart != -1:
                buf.write (self._appendLineBreaks (text[start: nexttagstart]))
                buf.write (u'\n')
            else:
                buf.write (self._appendLineBreaks (text[start:]))

            if nexttagstart != -1:
                assert currenttag is not None
                assert nexttagend != -1
                closingend = self._findClosingTag (text, nexttagend, currenttag)

                if closingend != -1:
                    buf.write (text[nexttagstart: closingend].strip())
                    buf.write (u'\n')
                else:
                    buf.write (text[nexttagstart:].strip())

                start = closingend
            else:
                start = nexttagstart

        result = buf.getvalue()
        return result


    def _findClosingTag (self, text, pos, tagindex):
        """
        Find closing tag by index tagindex from self._tagsRegexp
        Return the end tag position or -1 if closing tag not found
        """
        assert tagindex is not None
        assert tagindex >= 0

        match = self._tagsRegexp[tagindex][1].search (text, pos)

        return None if match is None else match.end()


    def _findNextTag (self, text, pos):
        """
        Find next opening special tag.
        Return tuple: (start tag position, end tag position, tag index)
        """
        start = -1
        end = -1
        index = None

        for n, tag in enumerate (self._tagsRegexp):
            match = tag[0].search (text, pos)
            if match is None:
                continue

            currentpos = match.start()
            if start == -1 or start > currentpos:
                start = currentpos
                end = match.end()
                index = n

        return (start, end, index)


    @abstractmethod
    def _appendLineBreaks (self, text):
        """
        Replace line breaks to <br> tags
        """



class BrHtmlImprover (HtmlImprover):
    """
    Class replace \\n to <br>
    """
    def _appendLineBreaks (self, text):
        """
        Replace line breaks to <br> tags
        """
        result = text
        result = result.replace ("\n", "<br>")

        opentags = r"[uod]l|hr|h\d|tr|td"
        closetags = r"li|d[td]|t[rdh]|caption|thead|tfoot|tbody|colgroup|col|h\d"

        # Remove <br> tag before some block elements
        remove_br_before = r"<br\s*/?>[\s\n]*(?=<(?:" + opentags + r")[ >])"
        result = re.sub(remove_br_before, "", result, flags=re.I)

        # Remove <br> tag after some block elements
        remove_br_after = r"(<(?:" + opentags + r")[ >]|</(?:" + closetags + r")>)[\s\n]*<br\s*/?>"
        result = re.sub(remove_br_after, r"\1", result, flags=re.I)

        # Append line breaks before some elements (to improve readability)
        append_eol_before = r"\n*(<li>|<h\d>|</?[uo]l>|<hr\s*/?>|<p>|</?table.*?>|</?tr.*?>|<td.*?>)"
        result = re.sub(append_eol_before, "\n\\1", result, flags=re.I)

        # Append line breaks after some elements (to improve readability)
        append_eol_after = r"(<hr\s*/?>|<br\s*/?>|</\s*h\d>|</\s*p>|</\s*ul>)\n*"
        result = re.sub(append_eol_after, "\\1\n", result, flags=re.I)

        return result
