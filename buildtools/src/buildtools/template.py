# -*- coding: utf-8 -*-


def substitute_in_file(filename, **kwargs):
    '''
    Substitute values to {param} string in the filename.
    The file will be owerwrited
    '''
    with open(filename, 'r', encoding='utf8') as fp:
        text = fp.read()

    for param, value in kwargs.items():
        text = text.replace('{' + param + '}', value)

    with open(filename, 'w', encoding='utf8') as fp:
        fp.write(text)
