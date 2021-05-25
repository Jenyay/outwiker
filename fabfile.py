#!/usr/bin/python
# -*- coding: utf-8 -*-


import builtins
import os
import os.path
import glob
import sys
import shutil
from typing import List

from fabric.api import local, lcd, settings, task
from colorama import Fore
from buildtools.info import show_plugins_info

from buildtools.utilites import (getPython,
                                 execute,
                                 tobool,
                                 print_info,
                                 windows_only,
                                 linux_only
                                 )
from buildtools.defines import (
    BUILD_DIR,
    BUILD_LIB_DIR,
    DEB_BINARY_BUILD_DIR,
    NEED_FOR_BUILD_DIR,
    COVERAGE_PARAMS,
)
from buildtools.versions import getOutwikerVersionStr
from buildtools.builders import (BuilderWindows,
                                 BuilderSources,
                                 BuilderPlugins,
                                 BuilderLinuxBinary,
                                 BuilderDebBinaryFactory,
                                 BuilderAppImage,
                                 BuilderSnap,
                                 )


DEPLOY_SERVER_NAME = os.environ.get('OUTWIKER_DEPLOY_SERVER_NAME', '')
DEPLOY_PLUGINS_PACK_PATH = os.environ.get(
    'OUTWIKER_DEPLOY_PLUGINS_PACK_PATH', '')


@task
def plugins(updatedonly=False):
    '''
    Create an archive with plugins (7z required)
    '''
    updatedonly = tobool(updatedonly)
    builder = BuilderPlugins(updatedOnly=updatedonly)
    builder.build()


@task
def plugins_clear():
    '''
    Remove an archive with plugins (7z required)
    '''
    builder = BuilderPlugins()
    builder.clear()


@task
def sources(is_stable=False):
    '''
    Create the sources archives
    '''
    is_stable = tobool(is_stable)
    builder = BuilderSources(is_stable=tobool(is_stable))
    builder.build()


@task
def sources_clear():
    '''
    Remove the sources archives.
    '''
    builder = BuilderSources()
    builder.clear()


@task
@windows_only
def win(is_stable=False, skiparchives=False, skipinstaller=False):
    '''
    Build OutWiker for Windows
    '''
    builder = BuilderWindows(is_stable=tobool(is_stable),
                             create_archives=not tobool(skiparchives),
                             create_installer=not tobool(skipinstaller)
                             )
    builder.build()


@task
@windows_only
def win_clear():
    '''
    Remove assemblies under Windows
    '''
    builder = BuilderWindows()
    builder.clear()


@task
@linux_only
def linux_binary(is_stable=False, skiparchives=False):
    '''
    Assemble binary builds for Linux
    '''
    builder = BuilderLinuxBinary(is_stable=tobool(is_stable),
                                 create_archive=not tobool(skiparchives)
                                 )
    builder.build()


@task
@linux_only
def linux_clear():
    '''
    Remove binary builds for Linux
    '''
    builder = BuilderLinuxBinary()
    builder.clear()


@task
def run(args=u''):
    '''
    Run OutWiker from sources
    '''
    with lcd("src"):
        execute(u'{} runoutwiker.py {}'.format(getPython(), args))


@task
def test(*args):
    '''
    Run the unit tests
    '''
    command = getPython() if args else 'coverage run {}'.format(COVERAGE_PARAMS)

    local('{command} runtests.py {args}'.format(
        command=command, args=' '.join(args)))

    if len(args) == 0:
        test_build()


@task
def test_build(*args):
    '''
    Run the build unit tests
    '''
    _runTests(u'.', u'test_build_', '', *args)


def _runTests(testdir, prefix, section=u'', *args):
    files = [fname[len(testdir) + 1:]
             for fname
             in glob.glob(u'{path}/{prefix}*.py'.format(path=testdir,
                                                        prefix=prefix))]
    files.sort()

    with lcd(testdir):
        if section:
            execute("{python} {prefix}{section}.py {params}".format(
                python=getPython(),
                prefix=prefix,
                section=section,
                params=u' '.join(args))
            )
        else:
            with settings(warn_only=True):
                for fname in files:
                    execute("{python} {fname} {params}".format(
                        python=getPython(),
                        fname=fname,
                        params=u' '.join(args))
                    )


@task
@linux_only
def deb_binary(is_stable=False):
    '''
    Create binary deb package
    '''
    is_stable = tobool(is_stable)
    builder = BuilderDebBinaryFactory.get_default(DEB_BINARY_BUILD_DIR,
                                                  is_stable)
    builder.build()
    print_info('Deb created: {}'.format(builder.get_deb_files()))


@task
@linux_only
def deb_binary_clear():
    '''
    Remove binary deb package
    '''
    builder = BuilderDebBinaryFactory.get_default()
    builder.clear()


@task
def clear():
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
def plugins_info():
    show_plugins_info()


@task
def create_tree(maxlevel, nsiblings, path):
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
def build(is_stable=False):
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
def deploy(apply=False, is_stable=False):
    '''
    apply -- True if deploy to server and False if print commands only
    is_stable -- False for unstable version and True for stable version
    '''
    apply = tobool(apply)
    is_stable = tobool(is_stable)

    linter_result = check_errors()
    if linter_result != LinterStatus.OK:
        return

    if apply:
        print(Fore.GREEN + 'Run deploy...')
    else:
        print(Fore.GREEN + 'Print commands only')

    plugins()
    upload_plugins()
    upload_plugins_pack()
    upload_distribs(is_stable)

    snap_channels = ['edge', 'beta']
    if is_stable:
        snap_channels += ['stable']

    snap_publish(*snap_channels)


@task
def add_sources_tag(apply=False, is_stable=False):
    '''
    Add the tag to git repository and push
    '''
    apply = tobool(apply)
    is_stable = tobool(is_stable)

    _add_sources_tag(apply, False)
    if is_stable:
        _add_sources_tag(apply, True)


def _add_sources_tag(apply=False, is_stable=False):
    version_str = getOutwikerVersionStr()
    if is_stable:
        tagname = u'stable_{}'.format(version_str)
    else:
        tagname = u'unstable_{}'.format(version_str)

    _add_git_tag(tagname, apply)


def _add_git_tag(tagname, apply):
    commands = [
        'git checkout master',
        'git tag {}'.format(tagname),
        'git push --tags',
    ]
    _run_commands(commands, apply)


def _run_commands(commands: List[str], apply=False):
    for command in commands:
        if apply:
            local(command)
        else:
            print(command)


@task
def update_sources_branches(apply=False, is_stable=False):
    '''
    Update the git repository

    apply -- True if deploy to server and False if print commands only
    '''
    apply = tobool(apply)
    is_stable = tobool(is_stable)

    commands = [
        'git checkout dev',
        'git pull',
        'git checkout master',
        'git pull',
        'git merge dev',
        'git push'
    ]
    if is_stable:
        commands += [
            'git switch stable',
            'git pull',
            'git merge master',
            'git push',
            'git switch master'
        ]
    _run_commands(commands, apply)
    add_sources_tag(apply, is_stable)


@task
def doc():
    '''
    Build documentation
    '''
    doc_path = u'doc/_build'
    if os.path.exists(doc_path):
        shutil.rmtree(doc_path)

    with lcd('doc'):
        local('make html')


@task(alias='linux_appimage')
@linux_only
def appimage(is_stable=0):
    '''
    Build AppImage package
    '''
    builder = BuilderAppImage(is_stable=tobool(is_stable))
    builder.build()
    print_info('AppImage created: {}'.format(builder.get_appimage_files()))


@task
def coverage():
    '''
    Create test coverage statistics
    '''
    local('coverage report {} -i'.format(COVERAGE_PARAMS))
    local('coverage html {} -i'.format(COVERAGE_PARAMS))


@task
@linux_only
def docker_build_create():
    '''
    Create a Docker image to build process
    '''
    with lcd('need_for_build/build_docker'):
        local('docker build -t outwiker/build_linux .')


@task
@linux_only
def docker_build(*args):
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
    local(command)


@task
def docker_build_wx(ubuntu_version: str, wx_version: str):
    '''
    Build a wxPython library from sources
    '''
    # Create dest dir
    build_dir = os.path.abspath(os.path.join(BUILD_DIR, BUILD_LIB_DIR))
    if not os.path.exists(build_dir):
        os.mkdir(build_dir)

    # Create Docker image
    docker_image = 'wxpython/ubuntu_{ubuntu_version}_webkit2'.format(
        ubuntu_version=ubuntu_version)

    dockerfile_path = os.path.join(
        NEED_FOR_BUILD_DIR,
        'build_wxpython',
        'ubuntu_{ubuntu_version}'.format(ubuntu_version=ubuntu_version)
    )

    with lcd(dockerfile_path):
        local(
            'docker build -t {docker_image} .'.format(docker_image=docker_image))

    # Build wxPython
    command = 'docker run -v "{path}:/home/user/build" --rm --user $(id -u):$(id -g) -i -t -e "WX_VERSION={wx_version}" {docker_image}'.format(
        path=build_dir,
        docker_image=docker_image,
        wx_version=wx_version
    )
    local(command)


@task(alias='linux_snap')
@linux_only
def snap(*params):
    '''
    Build clean snap package
    '''
    builder = BuilderSnap(*params)
    builder.build()
