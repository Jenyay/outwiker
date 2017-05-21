.. _ru_build:

Сборка OutWiker
===============

.. contents:: Содержание
   :depth: 3


Общие моменты, связанные со сборкой
-----------------------------------


Все задачи, связанные со сборкой, создают внутри папки :file:`build` папку, имя которой соответствует номеру текущей версии OutWiker в формате :file:`x.x.x.xxx`. Например, :file:`2.0.0.820`. Также внутри папки :file:`build` создается временная папка :file:`tmp`, предназначенная для хранения файлов во время сборки. Данная папка очищается перед каждой сборкой.

Также перед каждой задачей сборки создается папка :file:`tmp/src`, которая содержит копию исходников в соответствии с настройками сборщика: собирается стабильная версия или нестабильная. Если собирается нестабильная версия, то после копирования из исходников удаляется файл :file:`versions_stable.xml`, остается только файл :file:`versions.xml`, описывающий изменения в текущей версии в формате для нестабильной версии.

Если собирается стабильная версия, то после копирования исходников в :file:`tmp/src/` исходный файл :file:`versions.xml` удаляется, а файл :file:`versions_stable.xml` переименовывается в :file:`versions.xml`. Подробнее о формате файла :file:`versions.xml` см. раздел :ref:`ru_version_format`.

Разные классы сборок могут добавлять дополнительные файлы в папку :file:`tmp`.

Описанные возможности реализованы в классе :py:class:`buildtools.builders.base.BuilderBase`.

Сборка осуществляется с помощью команд Fabric (см. раздел :ref:`ru_fabfile`).


.. _ru_bool:

.. note::
    Многие команды сборки принимают булевы параметры. Чтобы в такую задачу передать значение `True`, в качестве параметра в командной строке нужно передать одно из следующих значений: 1 или true (независимо от регистра). Чтобы передать значение False, нужно передать какое-либо другое значение.


.. _ru_build_windows:

Сборка под Windows
------------------

.. _ru_fab_win_using:

Использование команды fab win
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Для того, чтобы собрать все виды дистрибутивов под Windows как нестабильную версию, используется команда

.. code:: bash

    fab win


Для того, чтобы собрать все виды дистрибутивов под Windows как стабильную версию, используется команда

.. code:: bash

    fab win:1


Для нестабильной версии будут созданы следующие артефакты в папке :file:`build/{{номер версии}}/windows`:

* Папка :file:`outwiker_exe`, содержащая все файлы, необходимые для запуска под Windows, включая все плагины в папке :file:`plugins`.
* :file:`outwiker_win_unstable.zip` - zip-архив, содержащий содержимое папки :file:`outwiker_exe`, но без плагинов во вложенной папке :file:`plugins`.
* :file:`outwiker_win_unstable.7z` - 7z-архив, содержащий содержимое папки :file:`outwiker_exe`, но без плагинов во вложенной папке :file:`plugins`.
* :file:`outwiker_win_unstable_all_plugins.zip` - zip-архив, содержащий содержимое папки :file:`outwiker_exe`, включая плагины во вложенной папке :file:`plugins`.
* :file:`outwiker_win_unstable_all_plugins.7z` - 7z-архив, содержащий содержимое папки :file:`outwiker_exe`, включая плагины во вложенной папке :file:`plugins`.
* :file:`outwiker_win_unstable.exe` - инсталятор, созданный с помощью `Inno Setup`_ (см. раздел :ref:`ru_windows_installer`).
* :file:`versions.xml` - манифест с описанием текущей версии программы OutWiker (см. раздел :ref:`ru_version_format`).


Для стабильной версии будут созданы следующие артефакты в папке :file:`build/{{номер версии}}/windows`:

* Папка :file:`outwiker_exe`, содержащая все файлы, необходимые для запуска под Windows, включая все плагины в папке :file:`plugins`.
* :file:`outwiker_{{x.x.x}}_win.zip` - zip-архив, содержащий содержимое папки :file:`outwiker_exe`, но без плагинов во вложенной папке :file:`plugins`.
* :file:`outwiker_{{x.x.x}}_win.7z` - 7z-архив, содержащий содержимое папки :file:`outwiker_exe`, но без плагинов во вложенной папке :file:`plugins`.
* :file:`outwiker_{{x.x.x}}_win_all_plugins.zip` - zip-архив, содержащий содержимое папки :file:`outwiker_exe`, включая плагины во вложенной папке :file:`plugins`.
* :file:`outwiker_{{x.x.x}}_win_all_plugins.7z` - 7z-архив, содержащий содержимое папки :file:`outwiker_exe`, включая плагины во вложенной папке :file:`plugins`.
* :file:`outwiker_win_unstable.exe` - инсталятор, созданный с помощью `Inno Setup`_ (см. раздел :ref:`ru_windows_installer`).
* :file:`versions.xml` - манифест с описанием текущей версии программы OutWiker. Этот файл является переименованным файлом :file:`src/versions_stable.xml` (см. раздел :ref:`ru_version_format`).


Команда :code:`fab win` может принимать три булевых параметра.

.. py:function:: win(is_stable=False, skipinstaller=False, skiparchives=False)

    Сборка дистрибутивов под Windows

    :param bool is_stable: Собрать дистрибутивы как стабильную версию (True) или как нестабильную (False).
    :param bool skipinstaller: Пропустить шаг создания инсталятора :file:`outwiker_win_unstable.exe` (если skipinstaller = True).
    :param bool skiparchives: Пропустить шаг создания архивов с собранной версией OutWiker (если skiparchives = True).

Чтобы удалить все артефакты, созданные командой :code:`fab win`, предназначена команда:

.. code:: bash

    fab win_clear


.. _ru_fab_win_internal:

Порядок сборки дистрибутивов под Windows
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Все действия, связанные со сборкой под Windows сосредоточены в классе :class:`buildtools.builders.windows.BuilderWindows`, который является производным от :class:`buildtools.builders.base.BuilderBase`.

В процессе сборки выполняются следующие действия:

Действия, выполняемые классом :class:`buildtools.builders.windows.BuilderBase`.


#. Создание папки :file:`build`.

#. Выполняется команда очистки. Для сборки под Windows это равносильно выполнению команды :code:`fab win_clear`.

#. Удаляется временная папка :file:`build/tmp`, если она существовала.

#. Создается временная папка :file:`build/tmp`.

#. Создается папка :file:`build/{{номер версии}}/windows`, если она не существовала.

#. Исходники копируются в папку :file:`build/tmp/src`.

#. В папке :file:`build/tmp/src` удаляется файл :file:`versions_stable.xml`, если создается нестабильная версия OutWiker, или :file:`versions_stable.xml` переименовывается в :file:`versions.xml`, если создается стабильная версия OutWiker.


Действия, выполняемые классом :class:`buildtools.builders.windows.BuilderWindows`.


#. В папку :file:`tmp` копируются файлы :file:`copyright.txt` и :file:`LICENSE.txt`.

#. Создается пустая папка для плагинов :file:`tmp/src/plugins`, если она не была создана.

#. Создается бинарная сборка в :file:`tmp/outwiker_exe` (см. раздел :ref:`ru_fab_win_exe`).

#. Удаляется и создается заново папка :file:`tmp/outwiker_exe/plugins`.

#. Создаются архивы с бинарной сборкой в формате zip и 7z без плагинов. Созданные архивы помещаются в :file:`build/{{номер версии}}/windows`.

#. Создается инсталятор (см. раздел :ref:`ru_windows_installer`).

#. Все плагины копируются в папку :file:`tmp/outwiker_exe/plugins`.

#. Создаются архивы с бинарной сборкой в формате zip и 7z с плагинами. Созданные архивы помещаются в :file:`build/{{номер версии}}/windows`.

#. Папка :file:`tmp/outwiker_exe` перемещается в :file:`build/{{номер версии}}/windows`.


.. _ru_fab_win_exe:

Создание бинарной сборки
~~~~~~~~~~~~~~~~~~~~~~~~

Самое важное, что делает команда :code:`fab win` - это создание запускаемого приложения под Windows, чтобы пользователям не требовалось устанавливать интерпретатор Python. Это осуществляется с помощью утилиты cx_Freeze_. Для создания запускаемых файлов под Windows используется скрипт `src/setup.py`_ (см. раздел :ref:`ru_setup_py`)

В результате выполнения данного скрипта будет создана папка :file:`build/outwiker_exe`, содержащая запускаемый файл :file:`outwiker.exe`, динамически загружаемую библиотеку с интерпретатором Python :file:`python27.dll`, архив :file:`library.zip`, содержащий необходимые Python-библиотеки, а также дополнительные файлы, необходимые для работы с библиотеками и папки, необходимые для работы OutWiker.

.. image:: /_static/build/cx_freeze_files.png

Содержимое :file:`library.zip` может выглядеть следующим образом:

.. image:: /_static/build/cx_freeze_library.png

.. warning::
    В данный момент для сборки OutWiker под Windows используется cx_Freeze 4.3.3. В cx_Freeze 5.x возникла проблема с тем, что запускаемое приложение стало гарантированно виснуть при запуске. Пока проблема не решена, используется предыдущая версия cx_Freeze.


.. note::
    В cx_Freeze 5.0 изменился способ сохранения необходимых Python-библиотек, и по умолчанию они не архивируются в :file:`library.zip`. С помощью дополнительных параметров можно явно указать, какие библиотеки должны быть включены в :file:`library.zip`. Это нужно будет сделать, если решится проблема с зависаниями, описанная выше. В данный момент эти параметры закомментарены в файле :file:`src/setup.py` (см. раздел :ref:`ru_setup_py`).

Подробное описание работы скрипта `src/setup.py`_ приводится в разделе :ref:`ru_setup_py`.


.. _ru_windows_installer:

Создание инсталятора под Windows
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Команда :code:`fab win` также создает графический инсталятор под Windows с помощью `Inno Setup`_. Скрипт для создания инсталятора - это файл :file:`outwiker_setup.iss`, который расположен в папке :file:`need_for_build/windows`. В результате выполнения данной команды будет создан файл :file:`outwiker_win_unstable.exe`.

.. note::
    При обновлении номера версии OutWiker надо не забыть поменять номер версии в файле :file:`outwiker_setup.iss`. В будущем это надо будет автоматизировать.

.. note::
    В данный момент инсталятор всегда создается с именем :file:`outwiker_win_unstable.exe` независимо от того, создается стабильная или нестабильная версия OutWiker. В будущем надо сделать, чтобы файл :file:`outwiker_setup.iss` создавался по шаблону, в котором можно было бы задавать с помощью переменных имя создаваемого инсталятора и номер версии (см. github issue `#344 <https://github.com/Jenyay/outwiker/issues/344>`_).



.. _ru_build_linux:

Сборка под Linux
----------------

В данный момент для установки под Linux есть возможность создания только deb-пакетов, которые могут быть установлены с помощью команды :code:`sudo dpkg -i {имя пакета}` или закачан на PPA (Personal Packages Archive). В данный момент существуют три PPA-репозитория:

* Для нестабильных версий OutWiker - https://launchpad.net/~outwiker-team/+archive/ubuntu/unstable.
* Для стабильных версий OutWiker - https://launchpad.net/~outwiker-team/+archive/ubuntu/ppa.
* Для тестирования сборки - https://launchpad.net/~outwiker-team/+archive/ubuntu/dev.

Создание deb-пакетов осуществляется через команды Fabric (см. раздел :ref:`ru_fabfile`):

* :code:`fab deb` создает deb-пакеты для всех поддерживаемых версий Ubuntu.
* :code:`fab deb_single` создает единственный deb-пакет под ту версию Ubuntu, в которой запускается данная команда.
* :code:`fab deb_install` создает единственный deb-пакет под ту версию Ubuntu, в которой запускается данная команд, и устанавливает созданный пакет в систему с помощью команды `sudo dpkg -i {имя пакета}`.
* :code:`fab deb_sources_included` создает необходимые файлы для загрузки OutWiker на PPA.

Перечисленные команды могут принимать один булев параметр, который обозначает, что создается сборка в качестве стабильной версии (параметр равен строке, которую можно интерпретировать как True) или нестабильной (параметр равен строке, которую не удается интерпретировать как True) - см. :ref:`примечание <ru_bool>`.

Для удаления файлов, созданных с помощью команд :code:`fab deb...`, предназначена команда :code:`fab deb_clear`.

Список поддерживаемых версий Ubuntu содержится в модуле :py:mod:`buildtools.defines` в переменной :py:const:`UBUNTU_RELEASE_NAMES`.


.. _ru_build_linux_impl:

Порядок сборки deb-пакетов
~~~~~~~~~~~~~~~~~~~~~~~~~~

Для выполнения задач Fabric `deb`, `deb_single` и `deb_install` предназначен класс :py:class:`buildtools.builders.linux.debsource.BuilderDebSource`. Для выполнения задачи `deb_sources_included` предназначен класс :py:class:`buildtools.builders.linux.debsource.BuilderDebSourcesIncluded`. Оба этих класса являются производными от класса :py:class:`buildtools.builders.linux.debsource.BuilderBaseDebSource`, который в свою очередь, является производным от :py:class:`buildtools.builders.base.BuilderBase`.

.. _ru_debuild:

Классы :py:class:`BuilderDebSource` и :py:class:`BuilderDebSourcesIncluded` отличаются только параметрами, которые передаются в утилиту сборки deb-пакетов `debuild`.

В классе :py:class:`BuilderDebSource` используется набор параметров для сборки deb-пакета, предназначенного для непосредственной установки:

.. code:: bash

    debuild --source-option=--include-binaries --source-option=--auto-commit

В классе :py:class:`BuilderDebSourcesIncluded` используется набор параметров для создания файлов, предназначенных для закачки пакета на сервер PPA, где будут создаваться необходимые для установки файлы.

.. code:: bash

    debuild -S -sa --source-option=--include-binaries --source-option=--auto-commit

Основные действия по сборке пакетов под Linux выполняет базовый класс :py:class:`BuilderBaseDebSource`.

Порядок сборки deb-пакета следующий.


Действия, выполняемые классом :class:`buildtools.builders.windows.BuilderBase` (те же самые действия, что и при сборке под Windows).


#. Создание папки :file:`build`.

#. Выполняется команда очистки. Для сборки под Windows это равносильно выполнению команды :code:`fab win_clear`.

#. Удаляется временная папка :file:`build/tmp`, если она существовала.

#. Создается временная папка :file:`build/tmp`.

#. Создается папка :file:`build/{{номер версии}}/linux/deb_source`, если она не существовала.

#. Исходники копируются в папку :file:`build/tmp/src`.

#. В папке :file:`build/tmp/src` удаляется файл :file:`versions_stable.xml`, если создается нестабильная версия OutWiker, или :file:`versions_stable.xml` переименовывается в :file:`versions.xml`, если создается стабильная версия OutWiker.


Действия, выполняемые классом :py:class:`buildtools.builders.linux.debsource.BuilderBaseDebSource` (внутри метода :py:meth:`buildtools.builders.linux.debsource.BuilderBaseDebSource._debuild`). Действия выполняются для каждой поддерживаемой версии Ubuntu.

#. Создается папка вида :file:`build/{{номер версии}}/linux/deb_source/outwiker-x.x.x+xxx`, где `x.x.x+xxx` соответствует номеру версии OutWiker.

#. Внутрь созданной папки :file:`outwiker-x.x.x+xxx` копируются минимальный набор исходников из :file:`build/tmp/src`. Копирование осуществляется с помощью утилиты `rsync`, которая позволяет задать маски для файлов и папок, которые нужно пропустить при копировании. Также копируются дополнительные файлы, необходимые для сборки. В частности, папка :file:`need_for_build/debian_debsource/{{ubuntu_name}}/debian`, содержащая инструкции для сборки deb-пакета под конкретную версию Ubuntu. Также копируются другие файлы и папки из :file:`need_for_build/debian_debsource/{{ubuntu_name}}`. Также копируются файлы :file:`copyright.txt`, :file:`README` и папка :file:`images` из корня исходных кодов. 

#. В папке :file:`build/{{номер версии}}/linux/deb_source` создается архив с "оригинальными" (original) исходниками. Имя архива выглядит следующим образом: :file:`outwiker_2.0.0+817~{{ubuntu_name}}.orig.tar.gz`, где {ubuntu_name} - кодовое имя дистрибутива Ubuntu, для которого создается сборка, число после знака "+" соответствует номеру сборки OutWiker.

#. Создается файл :file:`:file:`build/{{номер версии}}/linux/deb_source/outwiker-x.x.x+xxx/changelog`, содержащий список изменений для данной версии OutWiker.

#. Выполняется команда `debuild`, соответствующая цели сборки (параметры команды `debuild` показаны :ref:`выше <ru_debuild>`).

#. Удаляется папка :file:`build/{{номер версии}}/linux/deb_source/outwiker-x.x.x+xxx`.


.. _ru_build_sources:

Создание архивов с исходниками
------------------------------

Для создания архивов с исходниками предназначена команда :code:`fab sources`, которая может принимать один булев параметр (см. :ref:`примечание <ru_bool>`), указывающий, будет создаваться архив исходников в виде стабильной или нестабильной версии.

Во время сборки архивов с исходниками создается папка :file:`build/{{номер версии}}/sources`, в которую будут помещены архивы. Независимо от выбранного режима сборки создается архив :file:`outwiker-src-full-{{номер версии}}.zip` с полной копией исходников (создается с помощью команды :code:`git archive`).

Если создается архив исходников как нестабильной версии, то создается файл :file:`outwiker-src-min-{{номер версии}}-unstable.zip`, который содержит минимально необходимый набор файлов, чтобы запустить OutWiker. Если создается архив стабильной версии, то этот файл будет называться :file:`outwiker-src-min-{{номер версии}}.zip`. Содержимое архивов в двух режимах сборки отличается только текстом файла :file:`versions.xml`.


.. _cx_Freeze: https://anthony-tuininga.github.io/cx_Freeze/
.. _`Inno Setup`: http://www.jrsoftware.org
.. _`src/setup.py`: https://github.com/Jenyay/outwiker/blob/master/src/setup.py
