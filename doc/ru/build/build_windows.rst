.. _ru_build_windows:

Сборка под MS Windows
=====================

.. contents:: Содержание
   :depth: 2


.. _ru_fab_win_using:

Использование команды fab win
-----------------------------


Для того, чтобы собрать все виды дистрибутивов под Windows, используется команда (см. раздел :ref:`ru_fabfile`)

.. code:: bash

    fab win

Подразумевается, что данная версия OutWiker считается нестабильной. Если вызывать указанную выше команду без параметров, то будут созданы следующие артефакты в папке :file:`build`:

* Папка :file:`outwiker_win`, содержащая все файлы, необходимые для запуска под Windows, включая все плагины в папке :file:`plugins`.
* :file:`outwiker_win_unstable.zip` - zip-архив, содержащий содержимое папки :file:`outwiker_win`, но без плагинов во вложенной папке :file:`plugins`.
* :file:`outwiker_win_unstable.7z` - 7z-архив, содержащий содержимое папки :file:`outwiker_win`, но без плагинов во вложенной папке :file:`plugins`.
* :file:`outwiker_win_unstable_all_plugins.zip` - zip-архив, содержащий содержимое папки :file:`outwiker_win`, включая плагины во вложенной папке :file:`plugins`.
* :file:`outwiker_win_unstable_all_plugins.7z` - 7z-архив, содержащий содержимое папки :file:`outwiker_win`, включая плагины во вложенной папке :file:`plugins`.
* :file:`outwiker_win_unstable.exe` - инсталятор, созданный с помощью `Inno Setup`_ (см. раздел :ref:`ru_windows_installer`).
* :file:`versions.xml` - манифест с описанием текущей версии программы OutWiker (см. раздел :ref:`ru_version_format`).

Команда `fab win` может принимать два булевых параметра.

Первый параметр позволяет пропустить создание инсталятора :file:`outwiker_win_unstable.exe`, если значение этого параметра равно `True` или другому значению, которое преобразуется в `True` (например, `1`), т.е.:

.. code:: bash

    fab win:1

Второй параметр позволяет пропустить создание архивов :file:`outwiker_win_unstable.zip`, :file:`outwiker_win_unstable.7z`, :file:`outwiker_win_unstable_all_plugins.zip` и :file:`outwiker_win_unstable_all_plugins.7z`. Т.е. в процессе выполнения следующей команды будут созданы только артефакты :file:`outwiker_win`, :file:`outwiker_win_unstable.exe` и :file:`versions.xml`:

.. code:: bash

    fab win:0,1

.. note::
    Обратите внимание, что после знака запятой при перечислении параметров не должно быть пробела.

Эти параметры можно использовать совместно. Т.е. в результате запуска следующей команды будут созданы только папка :file:`outwiker_win` с ее содержимым и файл манифеста :file:`versions.xml`:

.. code:: bash

    fab win:1,1

Чтобы удалить все артефакты, созданные командой `fab win`, предназначена команда:

.. code:: bash

    fab win_clear


.. _ru_fab_win_internal:

Как работает команда fab win
----------------------------

Все действия, связанные со сборкой под Windows сосредоточены в классе :class:`buildtools.builders.windows.BuilderWindows`.

Самое главное, что делает команда `fab win` - это создание запускаемого приложения под Windows, чтобы пользователям не требовалось устанавливать интерпретатор Python. Это осуществляется с помощью утилиты cx_Freeze_. Для создания запускаемых файлов под Windows используется скрипт `src/setup.py`_ (см. раздел :ref:`ru_setup_py`)

В результате выполнения данного скрипта будет создана папка :file:`build/outwiker_win`, содержащая запускаемый файл :file:`outwiker.exe`, динамически загружаемую библиотеку с интерпретатором Python :file:`python27.dll`, архив :file:`library.zip`, содержащий необходимые Python-библиотеки, а также дополнительные файлы, необхождимые для работы с библиотеками и папки, необходимые для работы OutWiker.

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
================================

Команда `fab win` также создает графический инсталятор под Windows с помощью `Inno Setup`_. Скрипт для создания инсталлятора - это файл :file:`outwiker_setup.iss` в корне папки исходников. В результате будет создан файл :file:`outwiker_win_unstable.exe`.

.. note::
    При обновлении номера версии OutWiker надо не забыть поменять номер версии в файле :file:`outwiker_setup.iss`. В будущем это надо будет автоматизировать.


.. _cx_Freeze: https://anthony-tuininga.github.io/cx_Freeze/
.. _`Inno Setup`: http://www.jrsoftware.org
.. _`src/setup.py`: https://github.com/Jenyay/outwiker/blob/master/src/setup.py
