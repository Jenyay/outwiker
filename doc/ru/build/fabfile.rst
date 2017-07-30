.. _ru_fabfile:

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

        apiversion            Print current OutWiker API versions
        apiversions           Print current OutWiker API versions
        clear                 Remove artifacts after all assemblies
        create_tree           Create wiki tree for the tests
        deb                   Assemble the deb packages
        deb_binary            Create binary deb package
        deb_binary_clear      Remove binary deb package
        deb_clear             Remove the deb packages
        deb_install           Assemble deb package for current Ubuntu release
        deb_single            Assemble the deb package for the current Ubuntu release
        deb_sources_included  Create files for uploading in PPA (including sources)
        deploy                Upload unstable version to site
        doc                   Build documentation
        linux_binary          Assemble binary builds for Linux
        linux_clear           Remove binary builds for Linux
        locale                Update the localization file (outwiker.pot)
        locale_plugin         Create or update the localization file for pluginname plug-in
        outwiker_changelog    Generate OutWiker's changelog for the site
        plugin_changelog      Generate plugin's changelog for the site
        plugin_locale         Create or update the localization file for pluginname plug-in
        plugins               Create an archive with plugins (7z required)
        plugins_clear         Remove an archive with plugins (7z required)
        plugins_list          Print plugins list for th site
        prepare_virtual       Prepare virtual machine
        run                   Run OutWiker from sources
        site_versions         Compare current OutWiker and plugins versions with versions on the site
        sources               Create the sources archives as stable version
        sources_clear         Remove the sources archives.
        test                  Run the unit tests
        test_build            Run the build unit tests
        upload_binary         Upload unstable version to site
        upload_plugin         Upload plugin to site
        upload_plugins_pack   Upload archive with all plugins to site
        vm_halt               Stop virtual machines for build
        vm_linux_binary       Create 32- and 64-bit assembly on virtual machines
        vm_prepare            Prepare virtual machines for build
        vm_remove_keys        Remove local SSH keys for remote virual machines
        vm_run                Run virtual machines for build
        vm_stop               Stop virtual machines for build
        win                   Build OutWiker for Windows with cx_Freeze
        win_clear             Remove assemblies under Windows


Все эти команды описаны ниже.

Чтобы выполнить команду, в консоли нужно написать:

.. code:: bash

    fab имя_команды

Некоторые команды могут (или должны) принимать некоторые параметры. Параметры передаются после имени команды и символа ":", как показано ниже:

.. code:: bash

    fab имя_команды:парам1,парам2

Обратите внимание, что после двоеточия и запятой в списке параметров не должно быть пробела. Если параметр должен содержать пробел, то такое значение должно быть заключено в кавычки:

.. code:: bash

    fab имя_команды:"параметр с пробелами"

.. note::
    Некоторые команды Fabric принимают булевы параметры. Чтобы в такую задачу передать значение `True`, в качестве параметра в командной строке нужно передать одно из следующих значений: 1 или true (независимо от регистра). Чтобы передать значение False, нужно передать какое-либо другое значение.



.. _ru_fabfile_win:

Сборка под Windows
------------------

win
    Сборка OutWiker под Windows с помощью PyInstaller_, а также инсталятор с помощью `Inno Setup`_. Подробнее см. раздел :ref:`ru_build_windows`.

win_clear
    Удалить все, что создается с помощью команды `win`.


.. _ru_fabfile_linux:

Сборка под Linux
----------------

`deb`
    Создать deb-пакет на основе исходных кодов для всех поддерживаемых версий Ubuntu.

`deb_single`
    Создать deb-пакет на основе исходных кодов под ту версию Ubuntu, в которой происходит сборка.

`deb_install`
    Создать deb-пакет на основе исходных кодов и установить его в систему.

`deb_clear`
    Удалить все артефакты, которые создаются с помощью команды `deb`.

`deb_sources_included`
    Создать deb-пакеты на основе исходных кодов для всех поддерживаемых версий Ubuntu. Используется для закачки на PPA.

`deb_binary`
    Создать deb-пакеты на основе бинарной сборки под Linux.

`deb_binary_clear`
    Удалить все, что создается с помощью команды `deb_binary`

`linux_binary`
    Создать бинарную сборку под Linux с помощью PyInstaller_.

`linux_clear`
    Удалить созданную бинарную сборку под Linux.


Подробнее о сборке OutWiker под Linux см. раздел :ref:`ru_build_linux`.


.. _ru_fabfile_plugins:

Команды, связанные с плагинами
------------------------------

`plugins`
    Создать архивы с плагинами (отдельный архив на каждый плагин и общий архив со всеми плагинами). Эта команда может принимать булево значение. Если оно равно 1, то создаются архивы только для тех плагинов, которые имеют более новые версии по сравнению с теми, что выложены на сайте программы. Общий архив с плагинами создается в любом случае.

`plugins_clear`
    Удалить все архивы с плагинами.


.. _ru_fabfile_dev:

Команды, помогающие при разработке
----------------------------------

`run`
    Запустить OutWiker из исходников.

`apiversion` или `apiversions`
    Вывести номера версий встроенных пакетов outwiker (см. раздел :ref:`ru_sources_struct_src`).

`test`
    Запустить интеграционные и юнит-тесты. Подробнее о тестировании см. раздел :ref:`ru_test`.

`test_build`
    Запустить тесты, связанные со сборкой. Подробнее о тестировании см. раздел :ref:`ru_test`.


.. _ru_fabfile_locale:

Команды, связанные с локализацией
---------------------------------

`locale`
    Создать файл src/locale/outwiker.pot, используемый для создания файлов локализации.

`locale_plugin` или `plugin_locale`
    Создать файл локализации \*.pot для плагина, указанного в качестве параметра команды.


.. _ru_fabfile_deploy:

Команды, связанные с развертыванием
-----------------------------------

`deploy`
    Закачать собранную версию под Windows, собрать deb-пакеты и закачать их на PPA, установить тег в репозитории исходных кодов в соответствии с текущей версией OutWiker. Работает для стабильной и нестабильной версий.

`outwiker_changelog`
    Вывести список изменений, который нужно будет вставить на сайт. В качестве параметра требуется указать язык: ru или en.

`plugin_changelog`
    Вывести список изменений для плагина. В качестве параметров требуется указать имя плагина и язык: ru или en.

`site_versions`
    Вывести номера версий OutWiker и всех плагинов. Показываются версии, закачанные на сайт и находящиеся в папке с исходниками.

`upload_plugin`
    Закачать плагин или плагины на сайт. Для плагинов требуется предварительно создать архивы с плагинами с помощью команды `plugins`.

`upload_plugins_pack`
    Закачать архив со всеми плагинами на сайт. Архив с плагинами требуется предварительно создать с помощью команды `plugins`.

`upload_binary`
    Закачать бинарные версии OutWiker (под Windows и Linux) на сайт.

`plugins_list`
    Создать таблицу со списком плагинов для сайта. Требуется указать язык: ru или en.


.. _ru_fabfile_vm:

Команды для создания бинарных сборок на виртуальных машинах
-----------------------------------------------------------

Для создания бинарных сборок под различные версии Linux используются виртуальные машины. Для выполнения этих команд должны быть установлены VirtualBox_, Vagrant_ и Ansible_. Подробнее см. раздел :ref:`ru_build_virtual`.

`vm_run`
    Запустить все виртуальные машины.

`vm_stop` или `vm_halt`
    Остановить все виртуальные машины.

`vm_prepare`
    Запустить виртуальные машины и подготовить их к сборке OutWiker. Эта команда устанавливает все необходимые библиотеки.

`vm_linux_binary`
    Создать 32- и 64-битные бинарные сборки под Linux на виртуальных машинах.

`vm_remove_keys`
    Удалить ключи SSH из папки .ssh. Нужно выполнять после переустановки виртуальных машин.


.. _ru_fabfile_other:

Другие команды
-----------------------

`clear`
    Удалить все, что создано в папке build

`create_tree`
    Создать дерево заметок для тестов.

`doc`
    Скомпилировать данную документацию.

`prepare_virtual`
    Подготовить виртуальную машину с Linux, чтобы в ней можно было бы запустить OutWiker из исходников.

`sources`
    Создать архив с исходниками. Подробнее см. раздел :ref:`ru_build_sources`.

`sources_clear`
    Удалить архив с исходниками.


.. _Fabric: http://www.fabfile.org/
.. _PyInstaller: http://www.pyinstaller.org/
.. _`Inno Setup`: http://www.jrsoftware.org/
.. _VirtualBox: https://www.virtualbox.org/
.. _Ansible: https://www.ansible.com/
.. _Vagrant: https://www.vagrantup.com/
