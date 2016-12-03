# -*- coding: utf-8 -*-

import os


class SnippetsCollection(object):
    def __init__(self, name):
        # List of SnippetsCollection
        self._dirs = []

        # List of paths
        self._snippets = []
        self._name = name

    @property
    def dirs(self):
        return self._dirs

    @property
    def snippets(self):
        return self._snippets

    @property
    def name(self):
        return self._name

    def addSnippet(self, fname):
        self._snippets.append(fname)

    def addDir(self, snippetCollection):
        self._dirs.append(snippetCollection)

    def __len__(self):
        return len(self._dirs) + len(self._snippets)


class SnippetsLoader(object):
    def __init__(self, dirname):
        self._ext = u'.tpl'
        self._snippets = SnippetsCollection(None)
        self._findSnippets(self._snippets, dirname)

    def _findSnippets(self, snippets, dirname):
        if not os.path.exists(dirname):
            return

        for fname in os.listdir(dirname):
            fullname = os.path.join(dirname, fname)
            if os.path.isdir(fullname):
                subdir = SnippetsCollection(fname)
                self._findSnippets(subdir, fullname)
                snippets.addDir(subdir)
            elif fullname.endswith(self._ext):
                snippets.addSnippet(fullname)

    def getSnippets(self):
        return self._snippets
