.. _ru_events:

События
=======

Обработка событий в OutWiker реализована через класс :class:`outwiker.core.event.Event`. Каждый экземпляр класса :class:`outwiker.core.event.Event` отвечает за какое-то одно событие. Этот класс соответствует шаблону проектирования "издатель - подписчик" (publisher-subscriber). Пользователи класса подписываются на событие, указывая какую функцию или вызываемый объект нужно вызвать при срабатывании события, а когда событие срабатывает, вызывается указанная функция или вызываемый объект с теми параметрами, которые были переданы в событие кодом, который вызвал срабатывание события. 

На одно событие может быть подписано множество подписчиков, при этом все они имеют приоритет, определяемый целым числом, чем оно больше, тем выше приоритет, и тем раньше будет вызван обработчик с данным приоритетом. Если приоритет не указан, то по умолчанию он равен значению `EVENT_PRIORITY_DEFAULT=0` из модуля `outwiker.core.event`. Величина приоритета на должно превышать значения `EVENT_PRIORITY_MAX_CORE=100` и не должно быть меньше `EVENT_PRIORITY_MIN_CORE=-100`. Рекомендуется всегда оставлять приоритет по умолчанию и писать код так, чтобы не рассчитывать на порядок вызова обработчиков событий.

Многие события содержит в себе класс :class:`outwiker.core.application.ApplicationParams` (см. раздел :ref:`ru_application`). Содержимое класса :class:`outwiker.core.event.Event`:

.. py:class:: outwiker.core.event.Event

    .. py:method:: __init__()

        Конструктор. Не принимает параметров.

    .. py:method:: bind(handler, priority=EVENT_PRIORITY_DEFAULT)

        Подписаться на событие.

        :param function handler: функция или вызываемый объект, который должен принимать те же параметры, что будут использованы при вызове события (см. документацию к каждому конкретному событию).
        :param int priority: приоритет данного подписчика. Чем выше приоритет, тем раньше будет вызван подписчик. Порядок вызова подписчиков с одинаковыми приоритетами не определен.
        :return: None

    .. py:method:: __iadd__(handler)

        Более короткий аналог метода :py:meth:`bind`. Не позволяет указывать приоритет.

        :param function handler: функция или вызываемый объект, который должен принимать те же параметры, что будут использованы при вызове события (см. документацию к каждому конкретному событию).
        :return: None

    .. py:method:: unbind(handler)

        Отписаться от события.

        :param function handler: функция или вызываемый объект, который был указан при подписке на событие с помощью метода :py:meth:`bind` или :py:meth:`__iadd__`.
        :return: None

    .. py:method:: __isub__(handler)

        Аналог метода :py:meth:`unbind`

        :param function handler: функция или вызываемый объект, который был указан при подписке на событие с помощью метода :py:meth:`bind` или :py:meth:`__iadd__`.
        :return: None

    .. py:method:: __call__(*args, **kwargs)

        Вызов события с параметрами `*args` и `**kwargs`. Метод вызывает все обработчики, которые были добавлены с помощью методов :py:meth:`bind` или :py:meth:`__iadd__`.

    .. py:method:: clear()

        Отписывает всех подписчиков данного события.


Примеры использования класса :class:`outwiker.core.event.Event`
---------------------------------------------------------------

Пример 1
~~~~~~~~

.. code:: python

    from outwiker.core.event import Event

    def handler(param1, param2):
        ...

    event = Event()
    event += handler
    event(10, 100)
    ...
    event -= handler


Пример 2
~~~~~~~~

.. code:: python

    from outwiker.core.event import Event

    def handler(param1, param2):
        ...

    event = Event()
    event.bind(handler)
    event(10, 100)
    ...
    event.unbind(handler)


Пример 3. Использование приоритетов
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from outwiker.core.event import Event, EVENT_PRIORITY_DEFAULT

    def handler1(param1, param2):
        ...

    def handler2(param1, param2):
        ...

    event = Event()
    event.bind(handler1, priority=EVENT_PRIORITY_DEFAULT + 1)
    event.bind(handler2, priority=EVENT_PRIORITY_DEFAULT - 1)
    event(10, 100)
    ...
    event.unbind(handler1)
    event.unbind(handler2)


Пример 4. Использование событий из :class:`outwiker.core.application.ApplicationParams`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from outwiker.core.application import Application


    def pageSelect(sender):
        ...

    Application.onPageSelect += pageSelect

    ...

    Application.onPageSelect -= pageSelect



.. _ru_custom_events:

Пользовательские события
========================

Помимо класса :class:`outwiker.core.event.Event` внутри модуля :py:mod:`outwiker.core.event` содержится класс :class:`outwiker.core.event.CustomEvents`, предназначенный для хранения списка событий (экземпляров класса :class:`outwiker.core.event.Event`), доступ к которым осуществляется по имени (по ключу). Этот класс может быть полезен в тех случаях, когда нужно подписаться на событие, которое создается динамически (например, с помощью плагина). Класс :class:`outwiker.core.event.CustomEvents` создает экземпляр класса :class:`outwiker.core.event.Event` внутри себя только тогда, когда кто-то подписывается на событие с новым ключом.

.. py:class:: outwiker.core.event.CustomEvents

    .. py:method:: bind(key, handler, priority=EVENT_PRIORITY_DEFAULT)

        Подписаться на событие с ключом `key`.

        :param str key: ключ, с помощью которого идентифицируется событие. Рекомендуется использовать строку. Если не существует события с ключом `key`, будет создано новое событие (экземпляр класса :class:`outwiker.core.event.Event`) с данным ключом.
        :param function handler: функция или вызываемый объект, который должен принимать те же параметры, что будут использованы при вызове события (см. документацию к каждому конкретному событию).
        :param int priority: приоритет данного подписчика. Чем выше приоритет, тем раньше будет вызван подписчик. Порядок вызова подписчиков с одинаковыми приоритетами не определен.
        :return: None

    .. py:method:: unbind(key, handler)

        Отписаться от события с ключом `key`.

        :param str key: ключ, с помощью которого идентифицируется событие. Если не существует события с ключом `key`, то ничего не происходит.
        :param function handler: функция или вызываемый объект, который был указан при подписке на событие с помощью метода :py:meth:`bind` или :py:meth:`__iadd__`.
        :return: None

    .. py:method:: __call__(key *args, **kwargs)

        Вызов события, которое определяется ключом `key`, с параметрами `*args` и `**kwargs`. Метод вызывает все обработчики, которые были добавлены с помощью метода :py:meth:`bind`. Если не существует события с ключом `key`, то ничего не происходит.

    .. py:method:: clear(key)

        Отписывает всех подписчиков события, которое определяется ключом `key`. Если не существует события с ключом `key`, то ничего не происходит.

    .. py:method:: get(key)

        Возвращает экземпляр класса :class:`outwiker.core.event.Event`, который определяется ключом `key`.

        :param str key: ключ, с помощью которого идентифицируется событие. Если не существует события с ключом `key`, то оно создается.
        :rtype: outwiker.core.event.Event
