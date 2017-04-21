.. _fabfile:

Выполнение команд Fabric
========================

.. contents:: Содержание
   :depth: 2


.. _ru_fabric:

Основы использования Fabric
---------------------------


Для многих задач, связанных со сборкой, тестированием и выкладыванием новых версий на сайт, используется Fabric_ - удобный инструмент, который позволяет автоматизировать многие задачи как на удаленном сервере, так и на локальном компьютере. На русском языке про Fabric можно почитать в статье `Основы использования Fabric <http://jenyay.net/Programming/Fabric>`_.

Основная идея использования Fabric состоит в том, что все команды (или задачи) описываются в файле :file:`fabfile.py`, расположенном в корневой папке исходных кодов.

Чтобы узнать список имеющихся в данном :file:`fabfile.py` команд, выполните к консоли команду:

.. code:: bash

    fab -l


Будет выведен следующий список команд:

.. code-block:: text

    Available commands:

        apiversion
        apiversions
        clear                 Remove artifacts after all assemblies
        create_tree           Create wiki tree for the tests.
        deb                   Assemble the deb packages
        deb_binary
        deb_binary_clear
        deb_clear             Remove the deb packages
        deb_install           Assemble deb package for current Ubuntu release
        deb_single            Assemble the deb package for the current Ubuntu release
        deb_sources_included  Create files for uploading in PPA(including sources)
        deploy_unstable       Upload unstable version on the site
        doc
        linux                 Assemble binary builds for Linux
        linux_clear           Remove binary builds for Linux
        locale                Update the localization file(outwiker.pot)
        locale_plugin         Create or update the localization file for pluginname plug-in
        outwiker_changelog    Generate OutWiker's changelog for the site
        plugin_changelog      Generate plugin's changelog for the site
        plugin_locale         Create or update the localization file for pluginname plug-in
        plugins               Create an archive with plugins(7z required)
        plugins_clear         Remove an archive with plugins(7z required)
        plugins_list
        prepare_virtual       Prepare virtual machine
        run                   Run OutWiker from sources
        site_versions
        sources               Create the sources archives.
        sources_clear         Remove the sources archives.
        test                  Run the unit tests
        test_build            Run the build unit tests
        upload_plugin         Upload plugin to site
        upload_plugins_pack   Upload archive with all plugins.
        upload_unstable       Upload unstable version on the site
        win                   Build assemblies under Windows
        win_clear             Remove assemblies under Windows


Все эти команды описаны ниже.

Чтобы выполнить команду, в консол нужно написать:

.. code:: bash

    fab имя_команды

Некоторые команды могут (или должны) принимать некоторые параметры. Параметры передаются после имени команды и символа ":", как показано ниже:

.. code:: bash

    fab имя_команды:парам1,парам2

Обратите внимание, что после двоеточия и запятой в списке параметров не должно быть пробела. Если параметр должен содержать пробел, то такое значение должно быть заключено в кавычки:

.. code:: bash

    fab имя_команды:"параметр с пробелами"


.. _ru_fabfile_win:

Сборка под Windows
------------------

win
    Сборка OutWiker под Windows с помощью cx_Freeze_, а также инсталятор с помощью `Inno Setup`_. Результат помещается в папку :file:`/build`. Задача для сборки `win` может принимать два булевых параметра: если первый параметр равен 1, то не создается инсталятор; если второй параметр равен 1, то не создаются архивы со скомпилированной программой.

win_clear
    Удалить все, что создается с помощью команды `win`.


.. _ru_fabfile_linux:

Сборка под Linux
----------------

deb

deb_binary
    Создать deb-пакеты на основе бинарной сборки под Linux для всех поддерживаемых версий Ubuntu.

deb_binary_clear
    Удалить все, что создается с помощью команды `deb_binary`

deb_sources_included
    Создать deb-пакеты на основе исходных кодов для всех поддерживаемых версий Ubuntu. Используется для закачки на PPA.

deb_install
    Создать и установить deb-пакет (на основе исходных кодов) в систему.

deb_single
    Создать deb-пакет под ту версию Ubuntu, в которой происходит сборка.

deb_clear
    Удалить все deb-пакеты.

linux
    Создать бинарную сборку под Linux с помощью cx_Freeze_.

linux_clear
    Удалить созданную бинарную сборку под Linux.


.. _ru_fabfile_plugins:

Команды, связанные с плагинами
------------------------------

plugins
    Создать архивы с плагинами (отдельный архив на каждый плагин и общий архив со всеми плагинами). Эта команда может принимать булево значение. Если оно равно 1, то создаются архивы только для тех плагинов, которые имеют более новые версии по сравнению с теми, что выложены на сайте программы. Общий архив с плагинами создается в любом случае.

plugins_clear
    Удалить все архивы с плагинами.


Команды, помогающие при разработке
----------------------------------

run
    Запустить OutWiker из исходников.

apiversion или apiversions
    Вывести номера версий встроенных пакетов outwiker (см. раздел :ref:`ru_sources_struct_src`).

test
    Запустить юнит-тесты. Подробнее о тестировании см. раздел :ref:`ru_test`.

test_build
    Запустить юнит-тесты, связанные со сборкой. Подробнее о тестировании см. раздел :ref:`ru_test`.


.. _ru_fabfile_locale:

Команды, связанные с локализацией
---------------------------------

locale
    Создать файл src/locale/outwiker.pot, используемый для создания файлов локализации.

locale_plugin или plugin_locale
    Создать файл локализации \*.pot для плагина, указанного в качестве параметра команды.


.. _ru_fabfile_deploy:

Команды, связанные с развертыванием
-----------------------------------

deploy_unstable
    Закачать собранную нестабильную версию под Windows, а также собрать deb-пакеты и закачать их на PPA.

outwiker_changelog
    Вывести список изменений, который нужно будет вставить на сайт. В качестве параметра требуется указать язык: ru или en.

plugin_changelog
    Вывести список изменений для плагина. В качестве параметров требуется указать имя плагина и язык: ru или en.

site_versions
    Вывести номера версий OutWiker и всех плагинов. Показываются версии, закачанные на сайт и находящиеся в папке с исходиками.

upload_plugin
    Закачать плагин или плагины на сайт. Для плагинов требуется предварительно создать архивы с плагинами с помощью команды `plugins`.

upload_plugins_pack
    Закачать архив со всеми плагинами на сайт. Архив с плагинами требуется предварительно создать с помощью команды `plugins`.

upload_unstable
    Закачать нестабильную версию OutWiker на сайт.

plugins_list
    Создать таблицу со списком плагинов для сайта. Требуется указать язык: ru или en.


Другие команды
-----------------------

clear
    Удалить все, что создано в папке build

create_tree
    Создать тестовое дерево заметок для тестов.

doc
    Скомпилировать данную документацию.

prepare_virtual
    Подготовить виртуальную машину с Linux, чтобы в ней можно было бы запустить OutWiker из исходников.

sources
    Создать архив с исходниками.

sources_clear
    Удалить архив с исходниками.


.. _cx_Freeze: https://anthony-tuininga.github.io/cx_Freeze/
.. _Fabric: http://www.fabfile.org/
.. _`Inno Setup`: http://www.jrsoftware.org
