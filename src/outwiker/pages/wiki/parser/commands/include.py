# -*- coding: utf-8 -*-

import html
import re
from pathlib import Path

from outwiker.core.images import isImage
from outwiker.core.attachment import Attachment
from outwiker.core.defines import PAGE_ATTACH_DIR
from outwiker.core.htmlformatter import HtmlFormatter
from outwiker.core.cssclasses import CSS_WIKI, CSS_WIKI_INCLUDE
from outwiker.pages.wiki.parser.command import Command
from outwiker.pages.wiki.parser.attachregex import (
    attach_regex_no_spaces,
    attach_regex_with_spaces,
)


class IncludeCommand(Command):
    """
    Command to insert the text of an attached file into the page text.
    Syntax: (:include Attach:"fname" [params...] :)
    params - optional parameters:
        encoding="xxx" - specifies the encoding of the attached file
        htmlescape - replace characters <, > etc. with their HTML equivalents (&lt;, &gt; etc.)
        wikiparse - the content of the attached file should first be processed through the wiki parser
    """

    def __init__(self, parser):
        """
        parser - parser instance
        """
        super().__init__(parser)
        self._attach_regex_no_spaces = re.compile(
            "Attach:(?P<fname>{})".format(attach_regex_no_spaces)
        )
        self._attach_regex_with_spaces = re.compile(
            "Attach:(['\"])(?P<fname>{})\\1".format(attach_regex_with_spaces)
        )
        self._html_formatter = HtmlFormatter(classes=[CSS_WIKI, CSS_WIKI_INCLUDE])

    @property
    def name(self):
        """
        Returns the name of the command handled by the class
        """
        return "include"

    def execute(self, params, content):
        """
        Execute the command.
        Method returns the text that will be inserted at the command's place in wiki notation
        """
        (fname_relative, params_tail) = self._getAttach(params)
        if fname_relative is None:
            return ""

        self.parser.addWatchAttachments([fname_relative])
        if isImage(fname_relative):
            return self._execute_image(fname_relative)
        else:
            return self._execute_not_image(fname_relative, params_tail)

    def _execute_image(self, fname_relative):
        fname = str(Path(PAGE_ATTACH_DIR, fname_relative)).replace("\\", "/")
        return self._html_formatter.image(fname)

    def _execute_not_image(self, fname, params_tail):
        attach = Attachment(self.parser.page)
        fname_full_path = Path(attach.getAttachPath(create=False), fname)

        params_dict = Command.parseParams(params_tail)
        encoding = self._getEncoding(params_dict)

        try:
            with open(fname_full_path, encoding=encoding) as fp:
                # There's always a newline at the end for some reason
                text = fp.read().rstrip()
        except IOError:
            error_message = _("Can't open file '{}'").format(fname)
            return self._html_formatter.error(error_message)
        except Exception:
            error_message = _("Encoding error in file '{}'").format(fname)
            return self._html_formatter.error(error_message)

        return self._postprocessText(text, params_dict)

    def _postprocessText(self, text, params_dict):
        """
        Perform manipulations with the read text according to settings
        """
        result = text

        if "htmlescape" in params_dict:
            result = html.escape(text, False)

        if "wikiparse" in params_dict:
            result = self.parser.parseWikiMarkup(result)

        return result

    def _getEncoding(self, params_dict):
        encoding = "utf8"
        if "encoding" in params_dict:
            encoding = params_dict["encoding"]

        return encoding

    def _getAttach(self, params_str: str):
        """
        Returns the name of the attached file to be inserted into the
            page and the tail of parameters after the filename
        """
        match = self._attach_regex_no_spaces.match(params_str)
        if match is None:
            match = self._attach_regex_with_spaces.match(params_str)

        if match is None:
            return (None, params_str)

        fname = match.group("fname").replace("\\", "/")
        tail = params_str[match.end() :]
        return (fname, tail)
