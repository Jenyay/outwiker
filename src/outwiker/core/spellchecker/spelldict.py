# -*- coding: utf-8 -*-

import os.path
import logging
from typing import List


logger = logging.getLogger('outwiker.core.spellchecker.dicfile')


def get_words_from_dic_file(dic_file: str) -> List[str]:
    '''
    Return list of words from .dic file
    '''
    lines = []
    with open(dic_file, encoding='utf8') as fp:
        lines = [line.strip() for line in fp.readlines() if line.strip()]

    try:
        int(lines[0])
    except IndexError:
        return []
    except ValueError:
        return lines

    return lines[1:]


def write_to_dic_file(dic_file: str, words: List[str]):
    with open(dic_file, 'w', encoding='utf8') as fp:
        if words:
            fp.write('\n'.join([str(len(words))] + words))


def add_word_to_dic_file(dic_file: str, word: str):
    words = get_words_from_dic_file(dic_file)
    write_to_dic_file(dic_file, words + [word])


def create_new_dic_file(dic_file: str):
    '''
    Create .dic file if it is not exists
    '''
    if not os.path.exists(dic_file):
        logger.debug('Create .dic file: {}'.format(dic_file))
        with open(dic_file, 'w', encoding='utf8') as fp:
            fp.write('1\ntest')


def create_new_aff_file(aff_file: str):
    '''
    Create .aff file if it is not exists
    '''
    if not os.path.exists(aff_file):
        logger.debug('Create .aff file: {}'.format(aff_file))
        with open(aff_file, 'w') as fp:
            fp.write('SET UTF-8')


def fix_dic_file(dic_file: str):
    '''
    Add word count to the begin of file
    '''
    with open(dic_file, encoding='utf8') as fp:
        lines = [line.strip() for line in fp.readlines() if line.strip()]

    fixed = False
    try:
        count = int(lines[0])
        if count != len(lines) - 1:
            lines[0] = str(len(lines) - 1)
            fixed = True
    except IndexError:
        lines = ['1', 'test']
        fixed = True
    except ValueError:
        lines.insert(0, str(len(lines)))
        fixed = True

    if fixed:
        with open(dic_file, 'w', encoding='utf8') as fp:
            fp.write('\n'.join(lines))
