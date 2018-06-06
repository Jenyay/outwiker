# -*- coding: utf-8 -*-

from collections import MutableMapping


class Registry(object):
    '''
    The class for easy work with tree parameters (like Windows registry)
    '''
    def __init__(self, items_dict):
        '''
        items_dict - dictionary with initial values.
        '''
        self._items = items_dict

    def has_section(self, *args):
        '''
        *args - string list with path to section
        '''
        if not args:
            raise KeyError

        try:
            item = self._get_item(args, self._items)
            return self._is_section(item)
        except KeyError:
            return False

    def has_option(self, *args):
        '''
        *args - string list with path to option
        '''
        if not args:
            raise KeyError

        try:
            item = self._get_item(args, self._items)
            return not self._is_section(item)
        except KeyError:
            return False

    def _is_section(self, item):
        return isinstance(item, MutableMapping)

    def _get_item(self, path_elements, items_dict):
        '''
        Return value or dictionary by path elements.

        path_elements - list of the node names to section or option
        items_dict - root dictionary to search an item
        '''
        if len(path_elements) == 1:
            return items_dict[path_elements[0]]

        next_section = items_dict[path_elements[0]]
        if not self._is_section(next_section):
            raise KeyError

        return self._get_item(path_elements[1:], next_section)

    def get(self, *args, **kwargs):
        '''
        args - list of the node names to option.
        kwargs can contain key 'default' for the value if option not exists.
        '''
        if not args:
            raise KeyError

        try:
            item = self._get_item(args, self._items)
        except KeyError:
            return kwargs['default']

        if self._is_section(item):
            raise KeyError

        return item
