# -*- coding: utf-8 -*-


def find_all(text: str, sub: str, start=0, end=None):
    if end is None:
        end = len(text)

    pos = text.find(sub, start, end)
    while pos != -1:
        yield pos
        pos = text.find(sub, pos + len(sub), end)


def positionInside(text: str,
                   position: int,
                   open_str: str,
                   close_str: str) -> bool:
    '''
    Return true if position located between open_str and close_str strings
    '''
    left_open_count = len(list(find_all(text, open_str, 0, position)))
    left_close_count = len(list(find_all(text, close_str, 0, position)))
    right_open_count = len(list(find_all(text, open_str, position)))
    right_close_count = len(list(find_all(text, close_str, position)))

    return (left_open_count > left_close_count and
            right_close_count > right_open_count)
