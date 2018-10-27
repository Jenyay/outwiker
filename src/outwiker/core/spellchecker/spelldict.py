# -*- coding: utf-8 -*-

import os.path
import logging


logger = logging.getLogger('outwiker.core.spellchecker.dicfile')


def create_new_dic_file(dic_file):
    '''
    Create .dic file if it is not exists
    '''
    if not os.path.exists(dic_file):
        logger.debug('Create .dic file: {}'.format(dic_file))
        with open(dic_file, 'w', encoding='utf8') as fp:
            fp.write('1\ntest')


def create_new_aff_file(aff_file):
    '''
    Create .aff file if it is not exists
    '''
    if not os.path.exists(aff_file):
        logger.debug('Create .aff file: {}'.format(aff_file))
        with open(aff_file, 'w') as fp:
            fp.write('SET UTF-8')


def fix_dic_file(dic_file):
    '''
    Add word count to the begin of file
    '''
    with open(dic_file, encoding='utf8') as fp:
        lines = fp.readlines()

    lines = [line.strip() for line in lines if line.strip()]

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
