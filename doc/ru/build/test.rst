.. _ru_test:

Тестирование OutWiker
=====================


Для юнит-тестирования в OutWiker используется стандартный пакет unittest_, а также библиотека pytest_, которая позволяет удобно запускать тесты. Тесты проверяют работу внутренних компонентов OutWiker, а также элементов графического интерфейса.

.. _ru_test_dir:

Структура тестов
----------------

Все тесты располагаются в папке :file:`src/test`. Имена файлов, содержащие тесты, соответствуют маске :file:`test_*.py`. Все тесты разделены по темам:

:file:`test/core` - тесты основного ядра программы без тестов графического интерфейса.

:file:`test/actions` - тесты actions (см. раздел :ref:`ru_outwiker_actions`).

:file:`test/guitests` - тесты графического интерфейса.

:file:`test/wikiparser` - тесты википарсера (см. раздел :ref:`ru_outwiker_wiki_parser`).

:file:`test/plugins` - тесты плагинов. Для каждого плагина создана отдельная папка внутри :file:`src/test/plugins/`. Например, тесты для плагина markdown_ располагаются в папке :file:`src/test/plugins/markdown`.


.. _ru_test_params:

Параметры команды fab test
--------------------------

Для запуска тестов предназначен скрипт :file:`src/runtests.py`, который может принимать параметры из командной строки, чтобы затем передать их в pytest_. Для запуска тестов предназначена следующая команда fabfile (см. раздел :ref:`ru_fabfile`):

.. code:: bash

    fab test

С помощью дополнительных параметров команды `fab test` можно передать дополнительные параметры для pytest_. Например:

``fab test:"-v`` - более подробный вывод процесса тестирования.

``fab test:"-s"`` - если тест выводит что-то в stdout, то не подавлять этот вывод.

``fab test:"путь_до_тестов"`` - запуск тестов из указанной папки.

где `путь_до_тестов` отсчитывается, начиная с папки :file:`src`, т.е. если нужно запустить тесты графического интерфейса, то нужно выполнить команду:

``fab test:"test/guitests"``

Если нужно выполнить тесты из определенного файла, то:

``fab test:"test/guitests/test_actioncontroller.py"``

Если нужно выполнить тесты из определенного набора тестов (TestCase), то нужно выполнить команду наподобие:

``fab test:"test/guitests/test_actioncontroller.py::ActionControllerTest"``

Если нужно запустить определенный тест из определенного набора тестов (TestCase), то можно дополнительно передать имя теста:

``fab test:"test/guitests/test_actioncontroller.py::ActionControllerTest::testTitles"``


.. _unittest: https://docs.python.org/2/library/unittest.html
.. _markdown: http://jenyay.net/Outwiker/Markdown
.. _pytest: https://docs.pytest.org/en/latest/
