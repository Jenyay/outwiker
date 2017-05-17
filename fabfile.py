#!/usr/bin/python
# -*- coding: UTF-8 -*-

from __future__ import print_function
import __builtin__
import os
import os.path
import glob
import sys
import urllib2
import shutil

from fabric.api import local, lcd, settings, task, cd, put, hosts
from buildtools.libs.colorama import Fore

from buildtools.utilites import (getPython,
                                 execute,
                                 getCurrentUbuntuDistribName,
                                 getPathToPlugin,
                                 getDebSourceResultPath
                                 )
from buildtools.defines import (
    UBUNTU_RELEASE_NAMES,
    BUILD_DIR,
    DEB_SOURCE_BUILD_DIR,
    PLUGINS_DIR,
    PLUGINS_LIST,
    PLUGIN_VERSIONS_FILENAME,
    FILES_FOR_UPLOAD_UNSTABLE_WIN,
    OUTWIKER_VERSIONS_FILENAME,
    NEED_FOR_BUILD_DIR,
    PPA_UNSTABLE_PATH,
)
from buildtools.versions import (getOutwikerVersion,
                                 downloadAppInfo,
                                 getLocalAppInfoList,
                                 readAppInfo,
                                 )
from buildtools.contentgenerators import (SiteChangelogGenerator,
                                          SitePluginsTableGenerator)
from buildtools.builders import (BuilderWindows,
                                 BuilderSources,
                                 BuilderPlugins,
                                 BuilderLinuxBinary,
                                 BuilderLinuxDebBinary,
                                 BuilderDebSource,
                                 BuilderDebSourcesIncluded,
                                 )

from outwiker.utilites.textfile import readTextFile
from outwiker.core.xmlversionparser import XmlVersionParser
import outwiker
import outwiker.core
import outwiker.gui
import outwiker.actions
import outwiker.pages
import outwiker.utilites
import outwiker.libs

try:
    from buildtools.serverinfo import (DEPLOY_SERVER_NAME,
                                       DEPLOY_UNSTABLE_PATH,
                                       DEPLOY_HOME_PATH,
                                       DEPLOY_SITE,
                                       PATH_TO_WINDOWS_DISTRIBS,
                                       DEPLOY_PLUGINS_PACK_PATH,
                                       )
except ImportError:
    shutil.copyfile(u'buildtools/serverinfo.py.example',
                    u'buildtools/serverinfo.py')
    from buildtools.serverinfo import (DEPLOY_SERVER_NAME,
                                       DEPLOY_UNSTABLE_PATH,
                                       DEPLOY_HOME_PATH,
                                       DEPLOY_SITE,
                                       PATH_TO_WINDOWS_DISTRIBS,
                                       DEPLOY_PLUGINS_PACK_PATH,
                                       )

# env.hosts = [DEPLOY_SERVER_NAME]


@task
def deb_sources_included():
    """
    Create files for uploading in PPA(including sources)
    """
    builder = BuilderDebSourcesIncluded(DEB_SOURCE_BUILD_DIR,
                                        UBUNTU_RELEASE_NAMES)
    builder.build()


@task
def deb():
    """
    Assemble the deb packages
    """
    builder = BuilderDebSource(DEB_SOURCE_BUILD_DIR, UBUNTU_RELEASE_NAMES)
    builder.build()
    return builder.getResultPath()


@task
def deb_clear():
    """
    Remove the deb packages
    """
    builder = BuilderDebSource(DEB_SOURCE_BUILD_DIR, UBUNTU_RELEASE_NAMES)
    builder.clear()


@task
def deb_single():
    """
    Assemble the deb package for the current Ubuntu release
    """
    builder = BuilderDebSource(DEB_SOURCE_BUILD_DIR,
                               [getCurrentUbuntuDistribName()])
    builder.build()
    return builder.getResultPath()


def _ppa_upload(ppa_path):
    """
    Upload the current OutWiker version in PPA
    """
    version = getOutwikerVersion()
    deb_source_path = getDebSourceResultPath()

    for distname in UBUNTU_RELEASE_NAMES:
        with lcd(deb_source_path):
            local("dput {} outwiker_{}+{}~{}_source.changes".format(
                ppa_path,
                version[0],
                version[1],
                distname))


@task
def plugins(updatedonly=False):
    """
    Create an archive with plugins (7z required)
    """
    builder = BuilderPlugins(updatedOnly=updatedonly)
    builder.build()


@task
def plugins_clear():
    """
    Remove an archive with plugins (7z required)
    """
    builder = BuilderPlugins()
    builder.clear()


@task
def sources():
    """
    Create the sources archives.
    """
    builder = BuilderSources()
    builder.build()


@task
def sources_clear():
    """
    Remove the sources archives.
    """
    builder = BuilderSources()
    builder.clear()


@task
def win(skipinstaller=False, skiparchives=False):
    """
    Build assemblies under Windows
    """
    builder = BuilderWindows(create_installer=not skipinstaller,
                             create_archives=not skiparchives)
    builder.build()


@task
def win_clear():
    """
    Remove assemblies under Windows
    """
    builder = BuilderWindows()
    builder.clear()


@task
def linux(create_archive=True):
    """
    Assemble binary builds for Linux
    """
    builder = BuilderLinuxBinary(create_archive=create_archive)
    builder.build()


@task
def linux_clear():
    """
    Remove binary builds for Linux
    """
    builder = BuilderLinuxBinary()
    builder.clear()


@task
def deb_install():
    """
    Assemble deb package for current Ubuntu release
    """
    result_path = deb_single()

    version = getOutwikerVersion()

    with lcd(result_path):
        local("sudo dpkg -i outwiker_{}+{}~{}_all.deb".format(
            version[0],
            version[1],
            getCurrentUbuntuDistribName()))


@task
def locale():
    """
    Update the localization file (outwiker.pot)
    """
    with lcd("src"):
        local(r'find . -iname "*.py" | xargs xgettext -o locale/outwiker.pot')


@task(alias='plugin_locale')
def locale_plugin(pluginname):
    """
    Create or update the localization file for pluginname plug-in
    """
    with lcd(os.path.join("plugins", pluginname, pluginname)):
        local(r'find . -iname "*.py" | xargs xgettext -o locale/{}.pot'.format(pluginname))


@task
def run(args=u''):
    """
    Run OutWiker from sources
    """
    with lcd("src"):
        execute(u'{} runoutwiker.py {}'.format(getPython(), args.decode('utf8')))


@task
def test(section=u'', *args):
    """
    Run the unit tests
    """
    _runTests(u'src', u'tests_', section, *args)
    if len(section) == 0:
        test_build(section, *args)


@task
def test_build(section=u'', *args):
    """
    Run the build unit tests
    """
    _runTests(u'.', u'test_build_', section, *args)


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
def deb_binary():
    builder = BuilderLinuxDebBinary()
    builder.build()


@task
def deb_binary_clear():
    builder = BuilderLinuxDebBinary()
    builder.clear()


@task
def clear():
    """
    Remove artifacts after all assemblies
    """
    plugins_clear()
    sources_clear()

    if os.name == 'posix':
        linux_clear()
        deb_clear()
        deb_binary_clear()
    elif os.name == 'nt':
        win_clear()


@task
def plugin_changelog(plugin, lang):
    """
    Generate plugin's changelog for the site
    """
    path_to_xml = os.path.join(getPathToPlugin(plugin),
                               PLUGIN_VERSIONS_FILENAME)
    _print_changelog(path_to_xml, lang)


@task
def outwiker_changelog(lang):
    """
    Generate OutWiker's changelog for the site
    """
    path_to_xml = os.path.join(u'src', 'versions.xml')
    _print_changelog(path_to_xml, lang)


def _print_changelog(path_to_xml, lang):
    xml_content = readTextFile(path_to_xml)
    parser = XmlVersionParser([lang])
    appinfo = parser.parse(xml_content)
    generator = SiteChangelogGenerator(appinfo)
    changelog = generator.make()
    print(changelog)


@task
def plugins_list(lang):
    appinfo_list = []
    for plugin_name in PLUGINS_LIST:
        path_to_xml = os.path.join(PLUGINS_DIR,
                                   plugin_name,
                                   plugin_name,
                                   PLUGIN_VERSIONS_FILENAME)
        xml_content = readTextFile(path_to_xml)
        parser = XmlVersionParser([lang])
        appinfo = parser.parse(xml_content)
        appinfo_list.append(appinfo)

    generator = SitePluginsTableGenerator(appinfo_list)
    text = generator.make()
    print(text)


@task
def site_versions():
    app_list = getLocalAppInfoList()

    # Downloading versions info
    print(u'Downloading version info files...\n')
    print(u'{: <20}{: <20}{}'.format(u'Title',
                                     u'Deployed version',
                                     u'Dev. version'))
    print(u'-' * 60)
    for localAppInfo in app_list:
        url = localAppInfo.updatesUrl
        name = localAppInfo.appname

        print(u'{:.<20}'.format(name), end=u'')
        try:
            appinfo = downloadAppInfo(url)
            if appinfo.currentVersion == localAppInfo.currentVersion:
                font = Fore.GREEN
            else:
                font = Fore.RED

            print(u'{siteversion:.<20}{devversion}'.format(
                siteversion=str(appinfo.currentVersion),
                devversion=font + str(localAppInfo.currentVersion)
                ))
        except (urllib2.URLError, urllib2.HTTPError) as e:
            print(Fore.RED + u'Error')
            print(str(e))
            print(url)
            print('')


@task
def create_tree(maxlevel, nsiblings, path):
    '''
    Create wiki tree for the tests.
    '''
    from outwiker.core.tree import WikiDocument

    __builtin__._ = _empty
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


@hosts(DEPLOY_SERVER_NAME)
@task
def upload_plugin(*args):
    """
    Upload plugin to site
    """
    if len(args) == 0:
        args = PLUGINS_LIST

    for pluginname in args:
        path_to_plugin_local = os.path.join(BUILD_DIR, PLUGINS_DIR, pluginname)
        if not os.path.exists(path_to_plugin_local):
            continue

        path_to_xml_local = os.path.join(path_to_plugin_local, PLUGIN_VERSIONS_FILENAME)

        xml_content_local = readTextFile(path_to_xml_local)
        appinfo_local = XmlVersionParser().parse(xml_content_local)

        url = appinfo_local.updatesUrl
        try:
            appinfo_remote = downloadAppInfo(url)
        except Exception:
            appinfo_remote = None

        if (appinfo_remote is not None and
                appinfo_local.currentVersion < appinfo_remote.currentVersion):
            print(Fore.RED + 'Error. New version < Prev version')
            sys.exit(1)
        elif (appinfo_remote is not None and
                appinfo_local.currentVersion == appinfo_remote.currentVersion):
            print(Fore.RED + 'Warning: Uploaded the same version')
        print(Fore.GREEN + 'Uploading...')

        path_to_upload = os.path.dirname(appinfo_local.updatesUrl.replace(DEPLOY_SITE + u'/', DEPLOY_HOME_PATH))
        version_local = unicode(appinfo_local.currentVersion)
        archive_name = u'{}-{}.zip'.format(pluginname, version_local)
        path_to_archive_local = os.path.join(path_to_plugin_local, archive_name)

        with cd(path_to_upload):
            put(path_to_archive_local, archive_name)
            put(path_to_xml_local, PLUGIN_VERSIONS_FILENAME)
    site_versions()


@hosts(DEPLOY_SERVER_NAME)
@task
def upload_unstable():
    """
    Upload unstable version on the site
    """
    versions = os.path.join(PATH_TO_WINDOWS_DISTRIBS, OUTWIKER_VERSIONS_FILENAME)
    upload_files = map(lambda item: os.path.join(PATH_TO_WINDOWS_DISTRIBS, item),
                       FILES_FOR_UPLOAD_UNSTABLE_WIN)
    upload_files = upload_files + [versions]

    for fname in upload_files:
        print(u'Checking {}'.format(fname))
        assert os.path.exists(fname)

    print('Checking versions')
    newOutWikerAppInfo = readAppInfo(versions)
    print('Download {}'.format(newOutWikerAppInfo.updatesUrl))
    prevOutWikerAppInfo = downloadAppInfo(newOutWikerAppInfo.updatesUrl)

    if newOutWikerAppInfo.currentVersion < prevOutWikerAppInfo.currentVersion:
        print(Fore.RED + 'Error. New version < Prev version')
        sys.exit(1)
    elif newOutWikerAppInfo.currentVersion == prevOutWikerAppInfo.currentVersion:
        print (Fore.RED + 'Warning: Uploaded the same version')

    print ('Uploading...')
    for fname in upload_files:
        with cd(DEPLOY_UNSTABLE_PATH):
            basename = os.path.basename(fname)
            put(fname, basename)


@hosts(DEPLOY_SERVER_NAME)
@task
def upload_plugins_pack():
    '''
    Upload archive with all plugins.
    '''
    pluginsBuilder = BuilderPlugins()
    pack_path = pluginsBuilder.get_plugins_pack_path()
    with cd(DEPLOY_PLUGINS_PACK_PATH):
        basename = os.path.basename(pack_path)
        put(pack_path, basename)


@hosts(DEPLOY_SERVER_NAME)
@task
def deploy_unstable():
    """
    Upload unstable version on the site
    """
    ppa_path = PPA_UNSTABLE_PATH

    deb_sources_included()
    _ppa_upload(ppa_path)
    upload_unstable()
    upload_plugins_pack()


@task(alias='apiversions')
def apiversion():
    print(u'core: {}.{}'.format(outwiker.core.__version__[0],
                                outwiker.core.__version__[1]))
    print(u'gui: {}.{}'.format(outwiker.gui.__version__[0],
                               outwiker.gui.__version__[1]))
    print(u'actions: {}.{}'.format(outwiker.actions.__version__[0],
                                   outwiker.actions.__version__[1]))
    print(u'pages: {}.{}'.format(outwiker.pages.__version__[0],
                                 outwiker.pages.__version__[1]))
    print(u'utilites: {}.{}'.format(outwiker.utilites.__version__[0],
                                    outwiker.utilites.__version__[1]))
    print(u'libs: {}.{}'.format(outwiker.libs.__version__[0],
                                outwiker.libs.__version__[1]))


@task
def doc():
    with lcd('doc'):
        local('make html')


@task
def prepare_virtual():
    '''
    Prepare virtual machine
    '''
    with lcd(os.path.join(NEED_FOR_BUILD_DIR, u'virtual')):
        local(u'ansible-playbook virtual_prepare.yml -k --ask-sudo-pass')
