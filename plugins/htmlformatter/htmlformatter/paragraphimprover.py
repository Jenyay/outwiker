# -*- coding: utf-8 -*-

import re
from io import StringIO

from outwiker.core.htmlimprover import HtmlImprover



class ParagraphHtmlImprover (HtmlImprover):
    """
    Class cover paragraphes by <p> tags
    """
    def _appendLineBreaks (self, text):
        result = self._coverParagraphs (text)
        result = self._addLineBreaks (result)
        result = self._improveRedability (result)

        return result


    def _improveRedability (self, text):
        result = text

        minopentags = r"[uod]l|hr|h\d|tr|td|blockquote"
        opentags = minopentags + r"|table"
        closetags = r"[uod]l|li|d[td]|t[rdh]|caption|table|thead|tfoot|tbody|colgroup|col|h\d|blockquote"

        # Remove <br> tag before some block elements
        remove_br_before = r"<br\s*/?>\s*(?=<(?:" + opentags + r")[ >])"
        result = re.sub(remove_br_before, "", result, flags=re.I | re.M)

        # Remove <br> tag after some block elements
        remove_br_after = r"(<(?:" + opentags + r")(?: [^>]*?)?>|</(?:" + closetags + r")>)\s*<br\s*/?>"
        result = re.sub(remove_br_after, r"\1", result, flags=re.I | re.M)

        # Append </p> before some elements
        append_p_before = r"(?<!</p>)(<(?:h\d|blockquote|[uod]l)[ >])"
        result = re.sub(append_p_before, "</p>\\1", result, flags=re.I | re.M | re.S)

        # Append <p> after some closing elements
        append_p_after = r"(</(?:h\d|blockquote)>)(?!\s*(?:<p[ >]|</t[dh]>))"
        result = re.sub(append_p_after, "\\1<p>", result, flags=re.I | re.M | re.S)

        # Append <p> inside after some elements
        append_p_after_inside = r"(<(?:blockquote)(?: .*?)?>)"
        result = re.sub(append_p_after_inside, "\\1<p>", result, flags=re.I | re.M)

        # Append </p> inside before some closing elements
        append_p_before_inside = r"(</(?:blockquote)>)"
        result = re.sub(append_p_before_inside, "</p>\\1", result, flags=re.I | re.M)

        # Remove <p> tag before some block elements
        remove_p_before = r"<p>\s*(?=<(?:" + minopentags + r")[ >])"
        result = re.sub(remove_p_before, "", result, flags=re.I | re.M)

        # Remove <p> tag before div elements
        # remove_p_before = r"<p>(?=<(?:div.*?>))"
        # result = re.sub(remove_p_before, "", result, flags=re.I)

        # Remove </p> after div element
        # result = result.replace('</div></p>', '</div>\n')

        # Remove </p> tag after some block elements
        remove_p_after = r"(<(?:" + opentags + r")(?: [^>]*?)?>|</(?:" + closetags + r")>)\s*</p>"
        result = re.sub(remove_p_after, r"\1", result, flags=re.I | re.M)

        # Remove empty paragraphs
        empty_par = r"<p></p>"
        result = re.sub (empty_par, "", result, flags=re.I | re.M)

        # Remove <br> on the paragraph end
        final_linebreaks = r"<br\s*/?>\s*(</p>)"
        result = re.sub (final_linebreaks, "\\1", result, flags=re.I | re.M)

        # Append line breaks before some elements (to improve readability)
        append_eol_before = r"\n*(<(?:li|h\d|/?[uo]l|hr|p|script|/?table|/?tr|td)[ >])"
        result = re.sub(append_eol_before, "\n\\1", result, flags=re.I | re.M)

        # Append line breaks after some elements (to improve readability)
        append_eol_after = r"(<(?:hr(?: [^>]*?)?/?|br\s*/?|/\s*(?:h\d|p|script|[uo]l|table))>)\n*"
        result = re.sub(append_eol_after, "\\1\n", result, flags=re.I | re.M)

        # Normalize <p>...</p> inside <div>
        append_p_inside = r"(?P<start><div((?!</div>).)*?>)(?P<content>((?!</div>).)*?</p>.*?)(?P<end></div>)"
        result = re.sub(append_p_inside,
                        "\\g<start><p>\\g<content></p>\\g<end>",
                        result,
                        flags=re.I | re.M | re.S)

        # Remove </p> at the begin
        remove_p_start = r"^</p>"
        result = re.sub(remove_p_start, "", result, flags=re.I)

        # Remove <p> at the end
        remove_p_end = r"<p>$"
        result = re.sub(remove_p_end, "", result, flags=re.I)

        return result


    def _addLineBreaks (self, text):
        return text.replace (u"\n", "<br/>")


    def _coverParagraphs (self, text):
        paragraphs = (par.strip()
                      for par
                      in text.split (u'\n\n')
                      if len (par.strip()) != 0)

        buf = StringIO()
        for par in paragraphs:
            buf.write ("<p>")
            buf.write (par)
            buf.write ("</p>")

        return buf.getvalue()
