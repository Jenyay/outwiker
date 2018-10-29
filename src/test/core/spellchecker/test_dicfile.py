# -*- coding: utf-8 -*-

import os
import tempfile

import outwiker.core.spellchecker.spelldict as spelldict


class TestReadDicFile:
    def setup_method(self, method):
        fp, self.tempfilename = tempfile.mkstemp()
        os.close(fp)

    def teardown_method(self, method):
        os.remove(self.tempfilename)

    def test_empty(self):
        lines_src = []
        with open(self.tempfilename, 'w', encoding='utf8') as fp:
            fp.write('\n'.join(lines_src))

        words = spelldict.get_words_from_dic_file(self.tempfilename)

        assert words == []

    def test_dic_without_count_single_word(self):
        lines_src = ['пример']
        with open(self.tempfilename, 'w', encoding='utf8') as fp:
            fp.write('\n'.join(lines_src))

        words = spelldict.get_words_from_dic_file(self.tempfilename)

        assert words == ['пример']

    def test_dic_without_count_two_words(self):
        lines_src = ['пример', 'test']
        with open(self.tempfilename, 'w', encoding='utf8') as fp:
            fp.write('\n'.join(lines_src))

        words = spelldict.get_words_from_dic_file(self.tempfilename)

        assert words == ['пример', 'test']

    def test_dic_with_count_valid(self):
        lines_src = ['2', 'пример', 'test']
        with open(self.tempfilename, 'w', encoding='utf8') as fp:
            fp.write('\n'.join(lines_src))

        words = spelldict.get_words_from_dic_file(self.tempfilename)

        assert words == ['пример', 'test']

    def test_dic_with_count_invalid(self):
        lines_src = ['200', 'пример', 'test']
        with open(self.tempfilename, 'w', encoding='utf8') as fp:
            fp.write('\n'.join(lines_src))

        words = spelldict.get_words_from_dic_file(self.tempfilename)

        assert words == ['пример', 'test']

    def test_dic_with_count_only(self):
        lines_src = ['200']
        with open(self.tempfilename, 'w', encoding='utf8') as fp:
            fp.write('\n'.join(lines_src))

        words = spelldict.get_words_from_dic_file(self.tempfilename)

        assert words == []


class TestWriteDicFile:
    def setup_method(self, method):
        fp, self.tempfilename = tempfile.mkstemp()
        os.close(fp)

    def teardown_method(self, method):
        os.remove(self.tempfilename)

    def test_empty(self):
        words = []
        spelldict.write_to_dic_file(self.tempfilename, words)

        with open(self.tempfilename, 'r', encoding='utf8') as fp:
            lines = [line.strip() for line in fp.readlines()]

        assert lines == []

    def test_single_word(self):
        words = ['пример']
        spelldict.write_to_dic_file(self.tempfilename, words)

        with open(self.tempfilename, 'r', encoding='utf8') as fp:
            lines = [line.strip() for line in fp.readlines()]

        assert lines == ['1', 'пример']

    def test_two_words(self):
        words = ['пример', 'test']
        spelldict.write_to_dic_file(self.tempfilename, words)

        with open(self.tempfilename, 'r', encoding='utf8') as fp:
            lines = [line.strip() for line in fp.readlines()]

        assert lines == ['2', 'пример', 'test']

    def test_add_word_empty(self):
        spelldict.add_word_to_dic_file(self.tempfilename, 'пример')

        with open(self.tempfilename, 'r', encoding='utf8') as fp:
            lines = [line.strip() for line in fp.readlines()]

        assert lines == ['1', 'пример']

    def test_add_words_manu(self):
        spelldict.add_word_to_dic_file(self.tempfilename, 'пример')
        spelldict.add_word_to_dic_file(self.tempfilename, 'test')
        spelldict.add_word_to_dic_file(self.tempfilename, 'OutWiker')

        with open(self.tempfilename, 'r', encoding='utf8') as fp:
            lines = [line.strip() for line in fp.readlines()]

        assert lines == ['3', 'пример', 'test', 'OutWiker']
