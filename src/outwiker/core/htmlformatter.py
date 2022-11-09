# -*- coding=utf-8 -*-

from typing import List, Optional

from outwiker.core.cssclasses import CSS_ERROR, CSS_IMAGE


class HtmlFormatter:
    def __init__(self, classes: Optional[List[str]] = None):
        self._error_template = '<div class="{classes}">{content}</div>'
        self._image_template = '<img class="{classes}" src="{content}" />'
        self._block_template = '<div class="{classes}">{content}</div>'

        self._error_classes: List[str] = [CSS_ERROR]
        self._image_classes: List[str] = [CSS_IMAGE]
        self._block_classes: List[str] = []

        self._common_classes = classes if classes is not None else []

    def _format(self,
                content: str,
                template: str,
                main_classes: List[str]) -> str:
        classes = " ".join(self._common_classes + main_classes)
        return template.format(classes=classes, content=content)

    def error(self, content: str) -> str:
        return self._format(content, self._error_template, self._error_classes)

    def image(self, content: str) -> str:
        return self._format(content, self._image_template, self._image_classes)

    def block(self, content: str, other_classes: Optional[List[str]] = None) -> str:
        if other_classes is None:
            other_classes = []

        return self._format(content, self._block_template, self._block_classes + other_classes)
