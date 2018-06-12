# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import json
import logging
import pickle
from collections import MutableMapping

from .registry import Registry
from .defines import REGISTRY_SECTION_PAGES
from outwiker.utilites.textfile import readTextFile, writeTextFile

logger = logging.getLogger('outwiker.core.notestreeregistry')


class BaseSaver(object, metaclass=ABCMeta):
    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def save(self, items_dict):
        pass


class JSONSaver(BaseSaver):
    def __init__(self, fname):
        self._fname = fname

    def load(self):
        try:
            text = readTextFile(self._fname)
            items = json.loads(text)
        except (IOError, json.JSONDecodeError):
            logger.error('Error reading a notes tree registry')
            items = {}

        return items

    def save(self, items):
        text = json.dumps(items)
        try:
            writeTextFile(self._fname, text)
        except IOError:
            logger.error('Error saving a notes tree registry')


class PickleSaver(BaseSaver):
    def __init__(self, fname):
        self._fname = fname

    def load(self):
        try:
            with open(self._fname, 'rb') as fp:
                items = pickle.load(fp)
        except (IOError, pickle.PickleError):
            logger.error('Error reading a notes tree registry')
            items = {}

        return items

    def save(self, items):
        try:
            with open(self._fname, 'wb') as fp:
                pickle.dump(items, fp)
        except IOError:
            logger.error('Error saving a notes tree registry')


class NotesTreeRegistry(Registry):
    def __init__(self, saver):
        '''
        saver - interface with two methods - save() and load().
        '''
        self._saver = saver
        self._version = 1
        self._VERSION_OPTION = '__version'

        items = saver.load()

        if items.get(self._VERSION_OPTION, None) != self._version:
            logger.warning('Invalid notes tree registry version')
            items = {}

        if not isinstance(items, MutableMapping):
            logger.error('Invalid notes tree registry format')
            items = {}

        items[self._VERSION_OPTION] = self._version
        super().__init__(items)

    def save(self):
        self._saver.save(self._items)

    def _get_pages_section(self):
        try:
            subregistry = self.get_subregistry(REGISTRY_SECTION_PAGES)
        except KeyError:
            self._items[REGISTRY_SECTION_PAGES] = {}
            subregistry = self.get_subregistry(REGISTRY_SECTION_PAGES)

        return subregistry

    def get_section_or_create(self, *path_elements):
        path_elements_list = list(path_elements[:])
        parent = self._items

        while path_elements_list:
            next = path_elements_list.pop(0)
            if next not in parent or not self._is_section(parent[next]):
                parent[next] = {}

            parent = parent[next]

        return Registry(parent)

    def get_page_registry(self, page):
        return self.get_section_or_create(REGISTRY_SECTION_PAGES,
                                          self.get_key_for_page(page))

    def remove_page_section(self, page):
        page_key = self.get_key_for_page(page)
        path = (REGISTRY_SECTION_PAGES, page_key)

        if self.has_section(*path):
            self.remove_section(*path)
        elif self.has_option(*path):
            logger.error("Item must be a section, not option: {}".format(page_key))
            self.remove_option(*path)

    def has_section_for_page(self, page):
        return self.has_section(REGISTRY_SECTION_PAGES,
                                self.get_key_for_page(page))

    def get_key_for_page(self, page):
        return page.subpath

    def rename_page_sections(self, old_subpath, new_subpath):
        if REGISTRY_SECTION_PAGES not in self._items:
            return

        pages = self._items[REGISTRY_SECTION_PAGES]

        # Rename all supbath in the REGISTRY_SECTION_PAGES section
        for name in pages:
            item = pages[name]
            if not self._is_section(item):
                continue

            if name.startswith(old_subpath):
                new_name = new_subpath + name[len(old_subpath):]
                del pages[name]
                pages[new_name] = item
