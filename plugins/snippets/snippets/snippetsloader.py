# -*- coding: utf-8 -*-

import os


class SnippetsCollection(object):
    def __init__(self, path):
        # List of SnippetsCollection
        self._dirs = []

        # List of paths
        self._snippets = []
        self._path = path

    @property
    def dirs(self):
        return self._dirs

    @property
    def snippets(self):
        return self._snippets

    @property
    def name(self):
        return os.path.basename(self._path)

    @property
    def path(self):
        return self._path

    def addSnippet(self, fname):
        self._snippets.append(fname)

    def addDir(self, snippetCollection):
        self._dirs.append(snippetCollection)

    def __len__(self):
        return len(self._dirs) + len(self._snippets)


class SnippetsLoader(object):
    def __init__(self, dirname):
        self._snippets = SnippetsCollection(dirname)
        self._findSnippets(self._snippets, dirname)
        self.rootdir = dirname

    def _findSnippets(self, snippets, dirname):
        if not os.path.exists(dirname):
            return

        for fname in os.listdir(dirname):
            fullname = os.path.join(dirname, fname)
            if os.path.isdir(fullname):
                subdir = SnippetsCollection(fullname)
                self._findSnippets(subdir, fullname)
                snippets.addDir(subdir)
            else:
                snippets.addSnippet(fullname)

    def getSnippets(self):
        return self._snippets
