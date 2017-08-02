.. _ru_application:

Application. Экземпляр класса ApplicationParams
===============================================

Чтобы плагин мог делать что-то полезное, в первую очередь нужно разобраться с классом :class:`outwiker.core.application.ApplicationParams`. Этот класс представлен глобальной переменной `Application` в модуле `outwiker.core.application`. Переменная `Application` - это интерфейс для доступа ко всем основным частям OutWiker. Идеология плагинов для OutWiker диктуется динамической сутью языка Python, т.е. вы можете добраться практически до любой части основной программы, но за свои действия отвечаете сами - никаких "песочниц" для плагинов не предусмотрено.


По историческим причинам во многих частях программы доступ к переменной Application осуществляется следующим образом:

.. code-block:: python

    from outwiker.core.application import Application

    ...

    # Использование переменной Application

Но лучше не использовать явлый импорт переменной `Application`, а передавать ее в явном виде между классами, которые нуждаются в этой переменной. Например, экземпляр класса :class:`outwiker.core.application.ApplicationParams` передается в конструктор класса :class:`outwiker.core.pluginbase.Plugin` и доступен через поле `self._application` внутри классов, производных от :class:`outwiker.core.pluginbase.Plugin`.

Основное назначение класса :class:`outwiker.core.application.ApplicationParams` - предоставить доступ к основным элементам OutWiker - главному окну, actions (см. раздел :ref:`ru_outwiker_actions`), дереву заметок, списку загруженных плагинов и др., а также дать возможность подписаться на внутренние события OutWiker или добавить свое событие. О событиях см. раздел :ref:`ru_events`.

Класс :class:`outwiker.core.application.ApplicationParams` содержит следующие члены:

.. py:class:: outwiker.core.application.ApplicationParams

    .. py:attribute:: config

        Экземпляр класса :class:`outwiker.core.config.Config`, предназначенный для работы с настройками OutWiker.

    .. py:attribute:: recentWiki

        Экземпляр класса :class:`outwiker.core.recent.RecentWiki`, предназначенный для работы со списком последних открытых деревьев заметок.

    .. py:attribute:: actionController

        Экземпляр класса :class:`outwiker.gui.actioncontroller.ActionController`, предназначенный для работы с actions (см. раздел :ref:`ru_outwiker_actions`).

    .. py:attribute:: plugins

        Экземпляр класса :class:`outwiker.core.pluginsloader.PluginsLoader`, предназначенный для работы с плагинами.

    .. py:attribute:: pageUidDepot

        Экземпляр класса :class:`outwiker.core.pageuiddepot.PageUidDepot`, предназначенный для работы с уникальными идентификаторами страниц.

    .. py:attribute:: sharedData

        Словарь общего назначения, предназначенный для временного хранения данных и передачи информации между сообщениями. Используется как буфер для хранения произвольных данных.

    .. py:attribute:: customEvents

        Экземпляр класса :class:`outwiker.core.event.CustomEvents`, предназначенный для работы с нестандартынми событиями (например, событиями, созданными плагинами).

    .. py:attribute:: onWikiOpen

        **Событие.** Экземпляр класса :class:`outwiker.core.event.Events`. Вызывается после открытия дерева заметок. Обработчик принимает параметр `root` - экземпляр класса :class:`outwiker.core.tree.WikiDocument`, который предназначен для работы с деревом заметок в целом.
