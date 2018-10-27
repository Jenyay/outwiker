# -*- coding: utf-8 -*-

import os
import tempfile

import outwiker.core.spellchecker.spelldict as spelldict


class TestFixDicFile:
    def setup_method(self, method):
        self.tempfilename = tempfile.mkstemp()[1]

    def teardown_method(self, method):
        os.remove(self.tempfilename)

    def test_fix_dic_file_empty(self):
        spelldict.fix_dic_file(self.tempfilename)
        with open(self.tempfilename, 'r', encoding='utf8') as fp:
            lines = [line.strip() for line in fp.readlines()]

        assert lines == ['1', 'test']

    def test_fix_dic_file_normal_single_word(self):
        lines_src = ['1', 'test']
        with open(self.tempfilename, 'w', encoding='utf8') as fp:
            fp.write('\n'.join(lines_src))

        spelldict.fix_dic_file(self.tempfilename)
        with open(self.tempfilename, 'r', encoding='utf8') as fp:
            lines = [line.strip() for line in fp.readlines()]

        assert lines == lines_src

    def test_fix_dic_file_normal_two_words(self):
        lines_src = ['2', 'test', 'example']
        with open(self.tempfilename, 'w', encoding='utf8') as fp:
            fp.write('\n'.join(lines_src))

        spelldict.fix_dic_file(self.tempfilename)
        with open(self.tempfilename, 'r', encoding='utf8') as fp:
            lines = [line.strip() for line in fp.readlines()]

        assert lines == lines_src

    def test_fix_dic_file_no_count_single_word(self):
        lines_src = ['test']
        with open(self.tempfilename, 'w', encoding='utf8') as fp:
            fp.write('\n'.join(lines_src))

        spelldict.fix_dic_file(self.tempfilename)
        with open(self.tempfilename, 'r', encoding='utf8') as fp:
            lines = [line.strip() for line in fp.readlines()]

        assert lines == ['1'] + lines_src

    def test_fix_dic_file_no_count_two_words(self):
        lines_src = ['test', 'пример']
        with open(self.tempfilename, 'w', encoding='utf8') as fp:
            fp.write('\n'.join(lines_src))

        spelldict.fix_dic_file(self.tempfilename)
        with open(self.tempfilename, 'r', encoding='utf8') as fp:
            lines = [line.strip() for line in fp.readlines()]

        assert lines == ['2'] + lines_src

    def test_fix_dic_file_invalie_count_single_word(self):
        lines_src = ['2', 'test']
        with open(self.tempfilename, 'w', encoding='utf8') as fp:
            fp.write('\n'.join(lines_src))

        spelldict.fix_dic_file(self.tempfilename)
        with open(self.tempfilename, 'r', encoding='utf8') as fp:
            lines = [line.strip() for line in fp.readlines()]

        assert lines == ['1', 'test']

    def test_fix_dic_file_invalie_count_two_words(self):
        lines_src = ['1', 'test', 'пример']
        with open(self.tempfilename, 'w', encoding='utf8') as fp:
            fp.write('\n'.join(lines_src))

        spelldict.fix_dic_file(self.tempfilename)
        with open(self.tempfilename, 'r', encoding='utf8') as fp:
            lines = [line.strip() for line in fp.readlines()]

        assert lines == ['2', 'test', 'пример']
