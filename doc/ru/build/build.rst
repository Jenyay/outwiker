.. _ru_build:

Сборка OutWiker
===============

.. contents:: Содержание
   :depth: 2


Общие моменты, связанные со сборкой
-----------------------------------


Все задачи, связанные со сборкой, создают внутри папки :file:`build` папку, имя которой соответствует номеру текущей версии OutWiker в формате :file:`x.x.x.xxx`. Например, :file:`2.0.0.820`. Также внутри папки :file:`build` создается временная папка :file:`tmp`, предназначенная для хранения файлов во время сборки. Данная папка очищается перед каждой сборкой.

Также перед каждой задачей сборки создается папка :file:`tmp/src`, которая содержит копию исходников в соответствии с настройками сборщика: собирается стабильная версия или нестабильная. Если собирается нестабильная версия, то после копирования из исходников удаляется файл :file:`versions_stable.xml`, остается только файл :file:`versions.xml`, описывающий изменения в такущей версии в формате для нестабильной версии.

Если собирается стабильная версия, то после копирования исходников в :file:`tmp/src/` исходный файл :file:`versions.xml` удаляется, а файл :file:`versions_stable.xml` переименовывается в :file:`versions.xml`. Подробнее о формате файла :file:`versions.xml` см. раздел :ref:`ru_version_format`.

Разные классы сборок могут добавлять дополнительные файлы в папку :file:`tmp`.

Описанные возможности реализованы в классе :class:`buildtools.builders.base.BuilderBase`.


.. _ru_build_windows:

Сборка под Windows
------------------

.. _ru_fab_win_using:

Использование команды fab win
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


Для того, чтобы собрать все виды дистрибутивов под Windows как нестабильную версию, используется команда (см. раздел :ref:`ru_fabfile`)

.. code:: bash

    fab win


Для того, чтобы собрать все виды дистрибутивов под Windows как стабильную версию, используется команда (см. раздел :ref:`ru_fabfile`)

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


Команда `fab win` может принимать три булевых параметра.

.. py:function:: win(is_stable=False, skipinstaller=False, skiparchives=False)

    Сборка дистрибутивов под Windows

    :param bool is_stable: Собрать дистрибутивы как стабильную версию (True) или как нестабильную (False).
    :param bool skipinstaller: Пропустить шаг создания инсталлятора :file:`outwiker_win_unstable.exe` (если skipinstaller = True).
    :param bool skiparchives: Пропустить шаг создания архивов с собранной версией OutWiker (если skiparchives = True).

Чтобы удалить все артефакты, созданные командой `fab win`, предназначена команда:

.. code:: bash

    fab win_clear


.. _ru_fab_win_internal:

Как работает команда fab win
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Все действия, связанные со сборкой под Windows сосредоточены в классе :class:`buildtools.builders.windows.BuilderWindows`, который является производным от :class:`buildtools.builders.base.BuilderBase`.

В процессе сборки выполняются следующие действия:

Действия, выполняемые классом :class:`buildtools.builders.windows.BuilderBase`.


#. Создание папки :file:`build`.

#. Выполняется команда очистки. Для сборки под Windows это равносильно выполнению команды `fab win_clear`.

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

Самое важное, что делает команда `fab win` - это создание запускаемого приложения под Windows, чтобы пользователям не требовалось устанавливать интерпретатор Python. Это осуществляется с помощью утилиты cx_Freeze_. Для создания запускаемых файлов под Windows используется скрипт `src/setup.py`_ (см. раздел :ref:`ru_setup_py`)

В результате выполнения данного скрипта будет создана папка :file:`build/outwiker_exe`, содержащая запускаемый файл :file:`outwiker.exe`, динамически загружаемую библиотеку с интерпретатором Python :file:`python27.dll`, архив :file:`library.zip`, содержащий необходимые Python-библиотеки, а также дополнительные файлы, необхождимые для работы с библиотеками и папки, необходимые для работы OutWiker.

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

Команда `fab win` также создает графический инсталятор под Windows с помощью `Inno Setup`_. Скрипт для создания инсталлятора - это файл :file:`outwiker_setup.iss`, который расположен в папке :file:`need_for_build/windows`. В результате выполнения данной команды будет создан файл :file:`outwiker_win_unstable.exe`.

.. note::
    При обновлении номера версии OutWiker надо не забыть поменять номер версии в файле :file:`outwiker_setup.iss`. В будущем это надо будет автоматизировать.

.. note::
    В данный момент инсталятор всегда создается с именем :file:`outwiker_win_unstable.exe` независимо от того, создается стабильная или нестабильная версия OutWiker. В будущем надо сделать, чтобы файл :file:`outwiker_setup.iss` создавался по шаблону, в котором можно было бы задавать с помощью переменных имя создаваемого инсталятора и номер версии.

.. _ru_build_linux:

Сборка под Linux
----------------


.. _cx_Freeze: https://anthony-tuininga.github.io/cx_Freeze/
.. _`Inno Setup`: http://www.jrsoftware.org
.. _`src/setup.py`: https://github.com/Jenyay/outwiker/blob/master/src/setup.py
