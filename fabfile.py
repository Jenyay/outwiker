#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import os.path

from fabric.api import local, lcd

# Поддерживаемые дистрибутивы Ubuntu
distribs = ["saucy", "quantal", "precise"]


def _getVersion():
    """
    Возвращает кортеж вида (номер версии, номер сборки)
    """
    # Файл с номером версии
    fname = u"src/version.txt"

    with open (fname) as fp_in:
        lines = fp_in.readlines()

    return (lines[0].strip(), lines[1].strip())


def _getDebSourceDirName():
    """
    Возвращает имя папки, куда будут сохранены исходники для сборки deb-пакета
    """
    version = _getVersion()
    return "outwiker-{}+{}".format (version[0], version[1])


def _getOrigName (distname):
    version = _getVersion()
    return "outwiker_{}+{}~{}.orig.tar".format (version[0], version[1], distname)


def debclean():
    """
    Очистка папки build/<distversion>
    """
    local ('rm -rf build/{}'.format (_getDebSourceDirName() ) )


def _source():
    """
    Создать папку с исходниками для сборки deb-пакета
    """
    debclean()
    
    dirname = os.path.join ("build", _getDebSourceDirName() )
    os.mkdir (dirname)

    local ("rsync -avz --exclude=.bzr --exclude=distrib --exclude=build --exclude=*.pyc --exclude=*.dll --exclude=*.exe * --exclude=src/.ropeproject --exclude=src/test --exclude=src/setup_win.py --exclude=src/setup_tests.py --exclude=src/profile.py --exclude=src/tests.py --exclude=src/Microsoft.VC90.CRT.manifest --exclude=src/profiles --exclude=src/tools --exclude=doc --exclude=plugins --exclude=profiles --exclude=test --exclude=_update_version_bzr.py --exclude=outwiker_setup.iss --exclude=updateversion --exclude=updateversion.py {dirname}/".format (dirname=dirname) )


def orig (distname):
    """
    Создать архив с "оригинальными" исходниками для сборки deb-пакета.
    distname - имя дистрибутива Ubuntu
    """
    _source()

    origname = _getOrigName(distname)

    with lcd ("build"):
        local ("tar -cvf {} {}".format (origname, _getDebSourceDirName() ) )

    local ("gzip -f build/{}".format (origname) )


def debsourceinclude():
    """
    Создать файлы для закачки в репозиторий, включающие в себя исходники
    """
    _debuild ("debuild -S -sa --source-option=--include-binaries --source-option=--auto-commit",
            distribs)


def debsource():
    """
    Создать файлы для закачки в репозиторий, НЕ включающие в себя исходники
    """
    _debuild ("debuild -S --source-option=--include-binaries --source-option=--auto-commit",
            distribs)


def deb():
    """
    Создать deb-пакет
    """
    _debuild ("debuild --source-option=--include-binaries --source-option=--auto-commit", 
            distribs)


def debsingle ():
    """
    Создать deb-пакет только для первого дистрибутива в списке
    """
    _debuild ("debuild --source-option=--include-binaries --source-option=--auto-commit", 
            [distribs[0]])


def _debuild (command, distriblist):
    """
    Выполнение команд, связанные со сборкой deb с помощью debuild. Создает пакеты сразу для всех дистрибутивов, перечисленных в distriblist
    """
    for distname in distriblist:
        # Поменяем дистрибутив в changelog
        _makechangelog (distribs[0], distname)

        orig(distname)

        with lcd ("build/{}/debian".format (_getDebSourceDirName() ) ):
            local (command)

        # Вернем старый дистрибутив
        _makechangelog (distname, distribs[0])


def ppaunstable ():
    """
    Выполнение команд, связанные со сборкой deb с помощью debuild. Создает пакеты сразу для всех дистрибутивов, перечисленных в distriblist
    """
    version = _getVersion()

    for distname in distribs:
        with lcd ("build".format (_getDebSourceDirName() ) ):
            local ("dput ppa:outwiker-team/unstable outwiker_{}+{}~{}_source.changes".format (version[0], version[1], distname) )


def plugins():
    """
    Создание архивов с плагинами
    """
    plugins = ["source",
            "style",
            "export2html",
            "spoiler",
            "livejournal",
            "lightbox",
            "thumbgallery",
            "externaltools",
            "statistics",
            "updatenotifier",
            ]

    local ("rm -f build/plugins/outwiker-plugins-all.zip")

    for plugin in plugins:
        local ("rm -f build/plugins/{}.zip".format (plugin))

        with lcd ("plugins/{}".format (plugin)):
            local ("7z a -r -aoa -xr!*.pyc ../../build/plugins/{}.zip ./*; 7z a -r -aoa -xr!*.pyc ../../build/plugins/outwiker-plugins-all.zip ./*".format (plugin) )


def win():
    """
    Создание сборок под Windows
    """
    with lcd ("src"):
        local ("python setup_win.py build")

    with lcd ("build/outwiker_win"):
        local ("7z a ..\outwiker_win32_unstable.zip .\* .\plugins -r -aoa")
        local ("7z a ..\outwiker_win32_unstable.7z .\* .\plugins -r -aoa")

    local ("iscc outwiker_setup.iss")


def wintests():
    """
    Сборка тестов в exe-шники
    """
    with lcd ("src"):
        local ("python setup_tests.py build")


def nextversion():
    """
    Увеличить номер сборки (запускать под Linux, поскольку еще увеличивается номер сборки deb-пакета)
    """
    # Файл с номером версии
    fname = u"src/version.txt"

    with open (fname) as fp_in:
        lines = fp_in.readlines()

    lines[1] = str (int (lines[1]) + 1) + "\n"

    result = u"".join (lines)

    with open (fname, "w") as fp_out:
        fp_out.write (result)

    local ('dch -v "{}+{}~{}"'.format (lines[0].strip(), lines[1].strip(), distribs[0] ) )


def _makechangelog (distrib_src, distrib_new):
    """
    Подправить changelog под текущий дистрибутив Ubuntu. 
    
    Считаем, что у нас в исходном состоянии changelog всегда создан под distrib_src, а мы в первой строке его название заменим на distrib_new.
    """
    fname = "debian/changelog"

    with open (fname) as fp:
        lines = fp.readlines()

    lines[0] = lines[0].replace (distrib_src, distrib_new)

    with open (fname, "w") as fp:
        fp.write (u"".join (lines))
