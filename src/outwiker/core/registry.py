# -*- coding: utf-8 -*-

from collections import MutableMapping
from numbers import Real


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

    def _get_with_type(self, type, *args, **kwargs):
        '''
        args - list of the node names to option.
        kwargs can contain key 'default' for the value if option not exists.
        '''
        result = self.get(*args, **kwargs)
        if not isinstance(result, type):
            if 'default' in kwargs:
                return kwargs['default']
            else:
                raise ValueError

        return result

    def getbool(self, *args, **kwargs):
        '''
        args - list of the node names to option.
        kwargs can contain key 'default' for the value if option not exists.
        '''
        return self._get_with_type(bool, *args, **kwargs)

    def getint(self, *args, **kwargs):
        '''
        args - list of the node names to option.
        kwargs can contain key 'default' for the value if option not exists.
        '''
        return self._get_with_type(int, *args, **kwargs)

    def getfloat(self, *args, **kwargs):
        '''
        args - list of the node names to option.
        kwargs can contain key 'default' for the value if option not exists.
        '''
        return float(self._get_with_type(Real, *args, **kwargs))

    def getstr(self, *args, **kwargs):
        '''
        args - list of the node names to option.
        kwargs can contain key 'default' for the value if option not exists.
        '''
        return self._get_with_type(str, *args, **kwargs)

    def create_section(self, *args):
        '''
        Create section and all parent sections.
        '''
        if not args:
            raise KeyError

        self._create_section(self._items, args)

    def _create_section(self, items_dict, path_elements):
        if path_elements:
            next_path_element = path_elements[0]
            if next_path_element in items_dict:
                if self._is_section(items_dict[next_path_element]):
                    self._create_section(items_dict[next_path_element],
                                         path_elements[1:])
                else:
                    raise KeyError
            else:
                items_dict[next_path_element] = {}
                self._create_section(items_dict[next_path_element],
                                     path_elements[1:])

    def _remove_item(self, args, remove_section):
        if not args:
            raise KeyError

        try:
            deleting_item = self._get_item(args, self._items)
        except KeyError:
            return False

        if self._is_section(deleting_item) != remove_section:
            raise KeyError

        if len(args) == 1:
            parent = self._items
        else:
            parent = self._get_item(args[:-1], self._items)

        option = args[-1]
        if option not in parent:
            return False

        del parent[option]
        return True

    def remove_option(self, *args):
        '''
        Remove an option (not a section).
        Return True if option was removed or False if option is not exists.
        If path to option is path to section then raises KeyError exception.
        '''
        return self._remove_item(args, False)

    def remove_section(self, *args):
        '''
        Remove an option (not a section).
        Return True if option was removed or False if option is not exists.
        If path to option is path to section then raises KeyError exception.
        '''
        return self._remove_item(args, True)

    def set(self, *args):
        '''
        Set value by path. Path to option is args[:-1], args[-1] is new value.
        '''
        if len(args) < 2:
            raise KeyError

        self._set(args[:-2], args[-2], args[-1])

    def _set(self, path, option_name, value):
        path_copy = list(path[:])
        parent = self._items

        # Find a parent section
        while path_copy:
            next = path_copy.pop(0)
            if next not in parent:
                parent[next] = {}

            next_parent = parent[next]
            if not self._is_section(next_parent):
                raise KeyError

            parent = next_parent

        if option_name in parent and self._is_section(parent[option_name]):
            raise KeyError

        parent[option_name] = value

    def get_subregistry(self, *args):
        if not args:
            raise KeyError

        item = self._get_item(args, self._items)
        if not self._is_section(item):
            raise KeyError

        return Registry(item)
