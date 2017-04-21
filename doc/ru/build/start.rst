.. _ru_start:

Быстрый старт
=============

Для получения исходного кода OutWiker вам понадобится git_. Также должны быть установлены `Python 2.7 <https://www.python.org/>`_ (в данный момент Python 3.x не поддерживается) и pip_.

1. Чтобы получить исходный код выполните команду консоли:

.. code:: bash

    git clone https://github.com/Jenyay/outwiker

Эта команда создаст папку с именем :file:`outwiker` в текущей папке.

2. Зайдите в эту папку с помощью команды

.. code:: bash

    cd outwiker

3. Установите требуемые библиотеки с помощью команд:

.. code:: bash

    pip install --user -r requirements.txt
    pip install --user -r requirements_dev.txt

Если вы работаете под Windows, также необходимо выполнить следующую команду:

.. code:: bash

    pip install --user -r requirements_win.txt


Если вы работаете под Linux, убедитесь, что у вас установлены требуемые пакеты:


.. literalinclude:: requirements_linux.txt
    :language: text

4. Если все установилось без ошибок, то следующая команда должна запустить программу OutWiker:

.. code:: bash

    fab run

5. Также можно запустить тесты (выполнение нестов может занять несколько минут, а под Windows в несколько раз больше времени):

.. code:: bash

    fab test


.. _git: https://git-scm.com/
.. _pip: https://pip.pypa.io/en/stable/
