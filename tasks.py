#!/usr/bin/python
# -*- coding: utf-8 -*-

import builtins
import os
import os.path
import glob
import sys
import shutil
import re
from typing import List, Tuple, Callable, TextIO
from pathlib import Path

# from fabric.api import local, lcd, settings, task
from invoke import task

from buildtools.utilites import (getPython,
                                 tobool,
                                 print_info,
                                 windows_only,
                                 linux_only
                                 )
from buildtools.defines import DEB_BINARY_BUILD_DIR, COVERAGE_PARAMS
from buildtools.builders import (BuilderWindows,
                                 BuilderSources,
                                 BuilderPlugins,
                                 BuilderLinuxBinary,
                                 BuilderDebBinaryFactory,
                                 BuilderAppImage,
                                 BuilderSnap,
                                 )
from buildtools.versionstools import (display_version,
                                      InitUpdater,
                                      VersionsXmlUpdater,
                                      AppDataXmlUpdater)


@task
def plugins(c, updatedonly=False):
    '''
    Create an archive with plugins (7z required)
    '''
    updatedonly = tobool(updatedonly)
    builder = BuilderPlugins(c, updatedOnly=updatedonly)
    builder.build()


@task
def plugins_clear(c):
    '''
    Remove an archive with plugins (7z required)
    '''
    builder = BuilderPlugins(c)
    builder.clear()


@task
def sources(c, is_stable=False):
    '''
    Create the sources archives
    '''
    is_stable = tobool(is_stable)
    builder = BuilderSources(c, is_stable=tobool(is_stable))
    builder.build()


@task
def sources_clear(c):
    '''
    Remove the sources archives.
    '''
    builder = BuilderSources(c)
    builder.clear()


@task
def win(c, is_stable=False, skiparchives=False, skipinstaller=False):
    '''
    Build OutWiker for Windows
    '''
    builder = BuilderWindows(c,
                             is_stable=tobool(is_stable),
                             create_archives=not tobool(skiparchives),
                             create_installer=not tobool(skipinstaller)
                             )
    builder.build()


@task
def win_clear(c):
    '''
    Remove assemblies under Windows
    '''
    builder = BuilderWindows(c)
    builder.clear()


@task
def linux_binary(c, is_stable=False, skiparchives=False):
    '''
    Assemble binary builds for Linux
    '''
    builder = BuilderLinuxBinary(c,
                                 is_stable=tobool(is_stable),
                                 create_archive=not tobool(skiparchives)
                                 )
    builder.build()


@task
def linux_clear(c):
    '''
    Remove binary builds for Linux
    '''
    builder = BuilderLinuxBinary(c)
    builder.clear()


@task
def run(c, args=''):
    '''
    Run OutWiker from sources
    '''
    with c.cd("src"):
        c.run('{} runoutwiker.py {}'.format(getPython(), args))


@task(iterable=['params'])
def test(c, params=None):
    '''
    Run the unit tests
    '''
    if params is None:
        params = []

    command = getPython() if params else 'coverage run {}'.format(COVERAGE_PARAMS)

    c.run('{command} runtests.py {args}'.format(
          command=command, args=' '.join(params)))


def _runTests(c, testdir, prefix, section='', *args):
    files = [fname[len(testdir) + 1:]
             for fname
             in glob.glob(u'{path}/{prefix}*.py'.format(path=testdir,
                                                        prefix=prefix))]
    files.sort()

    with c.cd(testdir):
        if section:
            c.run('{python} {prefix}{section}.py {params}'.format(
                python=getPython(),
                prefix=prefix,
                section=section,
                params=u' '.join(args))
            )
        else:
            # with settings(warn_only=True):
            for fname in files:
                c.run('{python} {fname} {params}'.format(
                    python=getPython(),
                    fname=fname,
                    params=u' '.join(args))
                )


@task
def deb_binary(c, is_stable=False):
    '''
    Create binary deb package
    '''
    is_stable = tobool(is_stable)
    builder = BuilderDebBinaryFactory.get_default(DEB_BINARY_BUILD_DIR,
                                                  is_stable)
    builder.build()
    print_info('Deb created: {}'.format(builder.get_deb_files()))


@task
def deb_binary_clear(c):
    '''
    Remove binary deb package
    '''
    builder = BuilderDebBinaryFactory.get_default()
    builder.clear()


@task
def clear(c):
    '''
    Remove artifacts after all assemblies
    '''
    plugins_clear()
    sources_clear()

    if sys.platform.startswith('linux'):
        linux_clear()
        # deb_clear()
        deb_binary_clear()
    elif sys.platform.startswith('win32'):
        win_clear()


@task
def create_tree(c, maxlevel, nsiblings, path):
    '''
    Create wiki tree for the tests
    '''
    from outwiker.core.tree import WikiDocument

    builtins._ = _empty
    wikiroot = WikiDocument.create(path)
    _create_tree(1, int(maxlevel), int(nsiblings), wikiroot)


def _empty(param):
    return param


def _create_tree(level, maxlevel, nsiblings, parent):
    from outwiker.pages.wiki.wikipage import WikiPageFactory

    if level <= maxlevel:
        for n in range(nsiblings):
            pagename = u'page_{:03g}_{:03g}'.format(level, n)
            print(u'Create page {}'.format(pagename))

            newpage = WikiPageFactory().create(parent, pagename, [])
            newpage.content = u'Абырвалг'
            newpage.icon = u'images/outwiker_16.png'
            _create_tree(level + 1, maxlevel, nsiblings, newpage)


@task
def build(c, is_stable=False):
    '''
    Create artifacts for current version.
    '''
    is_stable = tobool(is_stable)

    if is_stable:
        build(False)

    sources(is_stable)
    plugins(True)

    if sys.platform.startswith('win32'):
        win(is_stable)


@task
def doc(c):
    '''
    Build documentation
    '''
    doc_path = u'doc/_build'
    if os.path.exists(doc_path):
        shutil.rmtree(doc_path)

    with c.cd('doc'):
        c.run('make html')


@task
def appimage(c, is_stable=False):
    '''
    Build AppImage package
    '''
    builder = BuilderAppImage(c, is_stable=tobool(is_stable))
    builder.build()
    print_info('AppImage created: {}'.format(builder.get_appimage_files()))


@task
def coverage(c):
    '''
    Create test coverage statistics
    '''
    c.run('coverage report {} -i'.format(COVERAGE_PARAMS))
    c.run('coverage html {} -i'.format(COVERAGE_PARAMS))


@task
def docker_build_create(c):
    '''
    Create a Docker image to build process
    '''
    with c.cd('need_for_build/build_docker'):
        c.run('docker build -t outwiker/build_linux .')


@task
def docker_build(c, *args):
    '''
    Run the build process inside the Docker container
    '''
    docker_build_create()

    tasks_str = ' '.join(args)
    current_dir = os.path.abspath('.')
    command = 'docker run -v "{path}:/home/user/project" --user $(id -u):$(id -g) -i -t outwiker/build_linux {tasks}'.format(
        path=current_dir,
        tasks=tasks_str
    )
    c.run(command)


@task(iterable=['params'])
def snap(c, params):
    '''
    Build clean snap package
    '''
    builder = BuilderSnap(c, params)
    builder.build()


@task
def set_version(c, version_str=''):
    """Set new OutWiker version for all files with versions"""
    if not version_str.strip():
        display_version()
        version_str = input(
            'Enter new OutWiker version in the format: "x.x.x.xxx [status]": ')

    version, status = _parse_version(version_str)
    for fname, updater in _get_version_updaters():
        _update_version_for_file(fname, updater.set_version, version, status)


@task
def add_new_version(c, version_str=''):
    """Append new version information to all files with versions"""
    if not version_str.strip():
        display_version()
        version_str = input(
            'Enter new OutWiker version in the format: "x.x.x.xxx [status]": ')

    version, status = _parse_version(version_str)
    for fname, updater in _get_version_updaters():
        _update_version_for_file(fname, updater.add_version, version, status)


@task
def set_release_date(c, date=''):
    """Set release date for current version"""
    if not date.strip():
        display_version()
        date = input('Enter OutWiker release date in the format: YYYY-MM-DD: ')

    for fname, updater in _get_version_updaters():
        _set_release_date_for_file(fname, updater, date)


def _get_version_updaters():
    return [
        (Path('src', 'outwiker', '__init__.py'), InitUpdater()),
        (Path('need_for_build', 'versions.xml'), VersionsXmlUpdater()),
        (Path('need_for_build', 'linux',
         'net.jenyay.Outwiker.appdata.xml'), AppDataXmlUpdater()),
    ]


def _parse_version(version_str: str) -> Tuple[List[int], str]:
    regexp = re.compile(r'(?P<numbers>(\d+)(\.\d+)*)(?P<status>\s+.*)?')
    match = regexp.match(version_str)
    numbers = [int(number) for number in match.group('numbers').split('.')]
    status = match.group('status')
    if status is None:
        status = ''
    return (numbers, status.strip())


def _update_version_for_file(path: str,
                             updater_func: Callable[[TextIO, List[int], str], str],
                             version: List[int],
                             status: str):
    with open(path) as fp_in:
        content_new = updater_func(fp_in, version, status)

    with open(path, 'w') as fp_out:
        fp_out.write(content_new)


def _set_release_date_for_file(path: str, updater, date_str: str):
    with open(path) as fp_in:
        content_new = updater.set_release_date(fp_in, date_str)

    with open(path, 'w') as fp_out:
        fp_out.write(content_new)
