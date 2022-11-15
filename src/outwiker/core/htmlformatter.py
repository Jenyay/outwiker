# -*- coding=utf-8 -*-

from typing import List, Optional

import outwiker.core.cssclasses as css


class HtmlFormatter:
    def __init__(self, classes: Optional[List[str]] = None):
        self._error_template = '<div class="{classes}">{content}</div>'
        self._image_template = '<img class="{classes}" src="{content}" />'
        self._block_template = '<div class="{classes}">{content}</div>'

        self._error_classes: List[str] = [css.CSS_ERROR]
        self._image_classes: List[str] = [css.CSS_IMAGE]
        self._block_classes: List[str] = []

        self._common_classes = classes if classes is not None else []

    def _format(self,
                content: str,
                template: str,
                main_classes: List[str]) -> str:
        classes = ' '.join(self._common_classes + main_classes)
        return template.format(classes=classes, content=content)

    def error(self, content: str) -> str:
        return self._format(content, self._error_template, self._error_classes)

    def image(self, content: str) -> str:
        return self._format(content, self._image_template, self._image_classes)

    def block(self, content: str, other_classes: Optional[List[str]] = None) -> str:
        if other_classes is None:
            other_classes = []

        return self._format(content, self._block_template, self._block_classes + other_classes)

    def link(self, href: str, text: str, css_classes: Optional[List[str]] = None) -> str:
        if css_classes:
            css_class = ' '.join(css_classes)
            return '<a class="{css_class}" href="{href}">{text}</a>'.format(
                    css_class=css_class, href=href, text=text)
        else:
            return '<a href="{href}">{text}</a>'.format(href=href, text=text)

    def anchor(self, anchor: str) -> str:
        return'<a id="{anchor}"></a>'.format(anchor=anchor) 
