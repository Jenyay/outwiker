# -*- coding: utf-8 -*-

import os.path
import shutil
from functools import reduce

import wx

from outwiker.gui.texteditor import TextEditor
from outwiker.gui.guiconfig import HtmlEditorStylesConfig
from outwiker.core.application import Application
from outwiker.core.system import getSpellDirList


class HtmlTextEditor(TextEditor):
    _htmlDictIsCopied = False

    def __init__(self, parent):
        self._htmlStylesSection = "HtmlStyles"
        super().__init__(parent)

    def setDefaultSettings(self):
        super(HtmlTextEditor, self).setDefaultSettings()
        self.setupHtmlStyles(self.textCtrl)

    def setupHtmlStyles(self, textCtrl):
        # Устанавливаемые стили
        styles = self.loadStyles()

        textCtrl.SetLexer(wx.stc.STC_LEX_HTML)
        textCtrl.StyleClearAll()

        for key in styles:
            textCtrl.StyleSetSpec(key, styles[key])
            textCtrl.StyleSetSize(key, self.config.fontSize.value)
            textCtrl.StyleSetFaceName(key, self.config.fontName.value)
            textCtrl.StyleSetBackground(key, self.config.backColor.value)

        tags = u"""a abbr acronym address applet area b base basefont
            bdo big blockquote body br button caption center
            cite code col colgroup dd del dfn dir div dl dt em
            fieldset font form frame frameset h1 h2 h3 h4 h5 h6
            head hr html i iframe img input ins isindex kbd label
            legend li link map menu meta noframes noscript
            object ol optgroup option p param pre q s samp
            script select small span strike strong style sub sup
            table tbody td textarea tfoot th thead title tr tt u ul
            var xml xmlns aside svg section use header main nav time footer
            article bdi details dialog figcaption figure mark menuitem meter
            progress rp rt ruby summary wbr datalist keygen output canvas
            audio embed source track video
            """

        attributes = u"""abbr accept-charset accept accesskey action align alink
            alt archive axis background bgcolor border
            cellpadding cellspacing char charoff charset checked cite
            class classid clear codebase codetype color cols colspan
            compact content coords
            data datafld dataformatas datapagesize datasrc datetime
            declare defer dir disabled enctype event
            face for frame frameborder
            headers height href hreflang hspace http-equiv
            id ismap label lang language leftmargin link longdesc
            marginwidth marginheight maxlength media method multiple
            name nohref noresize noshade nowrap
            object onblur onchange onclick ondblclick onfocus
            onkeydown onkeypress onkeyup onload onmousedown
            onmousemove onmouseover onmouseout onmouseup
            onreset onselect onsubmit onunload
            profile prompt readonly rel rev rows rowspan rules
            scheme scope selected shape size span src standby start style
            summary tabindex target text title topmargin type usemap
            valign value valuetype version vlink vspace width
            text password checkbox radio submit reset
            file hidden image property sizes async role autocomplete itemprop
            datetime data-toggle data-default-title viewbox itemscope pubdate
            """

        textCtrl.SetKeyWords(0, tags + " " + attributes)

    def loadStyles(self):
        """
        Загрузить стили из конфига
        """
        config = HtmlEditorStylesConfig(Application.config)

        styles = {}

        styles[wx.stc.STC_H_TAG] = config.tag.value.tostr()
        styles[wx.stc.STC_H_TAGUNKNOWN] = config.tagUnknown.value.tostr()
        styles[wx.stc.STC_H_ATTRIBUTE] = config.attribute.value.tostr()
        styles[wx.stc.STC_H_ATTRIBUTEUNKNOWN] = config.attributeUnknown.value.tostr()
        styles[wx.stc.STC_H_NUMBER] = config.number.value.tostr()
        styles[wx.stc.STC_H_DOUBLESTRING] = config.string.value.tostr()
        styles[wx.stc.STC_H_SINGLESTRING] = config.string.value.tostr()
        styles[wx.stc.STC_H_COMMENT] = config.comment.value.tostr()

        return styles

    def turnList(self, start, end, itemStart, itemEnd):
        """
        Создать список
        """
        selText = self.textCtrl.GetSelectedText()
        items = [item for item in selText.split("\n") if len(item.strip()) > 0]

        # Собираем все элементы
        if len(items) > 0:
            itemsList = reduce(lambda result, item: result + itemStart + item.strip() + itemEnd + "\n", items, "")
        else:
            itemsList = itemStart + itemEnd + "\n"

        result = start + itemsList + end

        if len(end) == 0:
            # Если нет завершающего тега(как в викинотации),
            # то не нужен перевод строки у последнего элемента
            result = result[: -1]

        self.textCtrl.ReplaceSelection(result)

        if len(items) == 0:
            endText = u"%s\n%s" % (itemEnd, end)

            newPos = self.GetSelectionEnd() - len(endText)
            self.SetSelection(newPos, newPos)

    def getSpellChecker(self):
        checker = super(HtmlTextEditor, self).getSpellChecker()
        htmlDictName = u'html.dic'

        # Copy html.dic dictionary to folder with user's permissions
        if not self._htmlDictIsCopied:
            srcname = os.path.join(getSpellDirList()[0], htmlDictName)
            dstname = os.path.join(getSpellDirList()[-1], htmlDictName)

            if srcname != dstname:
                try:
                    shutil.copyfile(srcname, dstname)
                except IOError:
                    return checker

            self._htmlDictIsCopied = True

        checker.addCustomDict(os.path.join(getSpellDirList()[-1], htmlDictName))
        return checker
