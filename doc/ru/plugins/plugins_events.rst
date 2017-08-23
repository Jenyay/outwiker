.. _ru_plugins_events:

Обработка событий в плагине
===========================

В разделе :ref:`ru_outwiker_plugins` было показано, как создать простейший плагин, который ничего не делает кроме как загружается и упоминается в списке плагинов. В данном разделе будет показано, как обрабатывать различные события. Прежде чем читать данный раздел рекомендуется ознакомиться с разделами :ref:`ru_application` и :ref:`ru_events`.

.. note::

    Для выполнения примеров данного раздела необходимо перевести OutWiker в режим отладки, для чего в файле :file:`outwiker.ini` в секции `[General]` необходимо добавить строку `debug = True`. Чтобы найти файл :file:`outwiker.ini`, см. раздел :ref:`ru_faq_settings`

В этом разделе будет создан плагин с именем `ExampleEventsPlugin`, который будет выводить в лог работы информацию о некоторых событиях, возникающих в процессе работы OutWiker. Исходные коды данного плагина расположены в папке :file:`plugins/examples/eventsplugin/` исходных кодов программы OutWiker.

Сначала создадим новую папку с плагином, которая будет называться, например, :file:`eventsplugin` (имя папки не существенно). Данная папка должна располагаться в папке с плагинами (см. раздел :ref:`ru_faq_plugins_install`).

Внутри этой папки создадим три файла:

#. :file:`__init__.py` - пустой файл.
#. :file:`plugin.py` - файл с классом плагина.
#. :file:`plugin.xml` - файл манифеста плагина.

Таким образом, структура каталога :file:`eventsplugin` будет следующая:

.. code-block:: text

    ..
    └── eventsplugin
        ├── __init__.py
        ├── plugin.py
        └── plugin.xml

Содержимое файла :file:`plugin.xml` соответствует структуре, описанной в разделе :ref:`ru_outwiker_plugins`, и не представляет особого интереса:

.. code-block:: xml

    <?xml version="1.1" encoding="UTF-8" ?>
    <info>
        <name>ExampleEventsPlugin</name>
        <updates>http://example.com/pluginname/plugin.xml</updates>
        <requirements>
            <os>Windows, Linux</os>
            <packages>
                <core>1.3</core>
                <actions>1.1</actions>
                <gui>1.5</gui>
                <pages>2.0</pages>
                <utilites>1.0</utilites>
                <libs>1.0</libs>
            </packages>
        </requirements>

        <data lang="en">
            <website>http://example.com/pluginnameEn</website>
            <description>Description.</description>

            <author>
                <name>Author name</name>
                <email>example@example.com</email>
                <site>http://example.com</site>
            </author>

            <changelog>
                <version number="0.1" date="August 20, 2017">
                    <download os="all">http://example.com/eventsplugin-0.1.zip</download>
                    <change>The first version.</change>
                </version>
            </changelog>
        </data>

        <data lang="ru">
            <website>http://example.com/pluginnameRu</website>
            <description>Описание.</description>

            <author>
                <name>Имя автора</name>
                <email>example@example.com</email>
                <site>http://example.com</site>
            </author>

            <changelog>
                <version number="0.1" date="20.08.2017">
                    <download os="all">http://example.com/eventsplugin-0.1.zip</download>
                    <change>Первая версия.</change>
                </version>
            </changelog>
        </data>
    </info>


Файл :file:`plugin.py` для начала будет минимально необходимый, только чтобы убедиться, что плагин загружается:

.. code-block:: python

    # -*- coding: utf-8 -*-

    from outwiker.core.pluginbase import Plugin


    class PluginExampleEvents(Plugin):
        def __init__(self, application):
            super(PluginExampleEvents, self).__init__(application)

        #########################################
        # Properties and methods to overloading #
        #########################################

        @property
        def name(self):
            return u"ExampleEventsPlugin"

        @property
        def description(self):
            return _(u"Example plugin")

        def initialize(self):
            pass

        def destroy(self):
            pass


Запустите OutWiker и убедитесь, что плагин успешно загружен, он должен появиться в списке плагинов в разделе "Плагины" диалога настроек:


.. image:: /_static/plugins/ru_eventsplugin_01.png
    :width: 600 px
    :align: center
    :alt: Список плагинов


Теперь добавим функциональность плагину. Мы могли бы все делать в рамках класса :class:`PluginExampleEvents`, но лучше пусть этот класс работает только в процессе загрузки плагина, а функциональность плагина мы поместим в новый класс :class:`eventsplugin.controller.Controller`, поэтому в папке :file:`eventsplugin` создадим еще один файл :file:`controller.py` с классом контроллера:

.. code-block:: python

    # -*- coding: UTF-8 -*-

    import logging


    logger = logging.getLogger('ExampleEventsPlugin')


    class Controller(object):
        def __init__(self, application):
            self._application = application

        def initialize(self):
            logger.info(u'Initialize.')

        def destroy(self):
            logger.info(u'Destroy.')


Метод :py:meth:`initialize` будет вызываться во время инициализации плагина (его загрузки или включении в диалоге настроек), а метод :py:meth:`destroy` будет вызываться перед выгрузкой плагина (во время завершения программы OutWiker или после отключения плагина в диалоге настроек).

Пока единственное, что делает класс :class:`eventsplugin.controller.Controller` - это сообщает в логе работы о том, что плагин инициализируется и выгружается.

Чтобы начать использовать данный класс, изменим содержимое файла :file:`plugin.py`:

.. code-block:: python

    # -*- coding: utf-8 -*-

    from outwiker.core.pluginbase import Plugin

    from .controller import Controller


    class PluginExampleEvents(Plugin):
        def __init__(self, application):
            super(PluginExampleEvents, self).__init__(application)
            self.controller = Controller(application)

        #########################################
        # Properties and methods to overloading #
        #########################################

        @property
        def name(self):
            return u"ExampleEventsPlugin"

        @property
        def description(self):
            return _(u"Example plugin")

        def initialize(self):
            self.controller.initialize()

        def destroy(self):
            self.controller.destroy()


Перезапустите OutWiker и в логе работы вы должны увидеть строки вида

.. code:: text

    INFO       2017-08-20 21:36:40,987   ExampleEventsPlugin - controller - Initialize.
    INFO       2017-08-20 21:57:32,939   ExampleEventsPlugin - controller - Destroy.

Отключите и включите плагин в диалоге настроек, чтобы убедиться, что плагин инициализируется и выгружается. 

Если вы работаете под Linux или запускаете OutWiker из исходников под Windows, то данный текст лога работы должен выводиться в консоль. Если вы запускаете OutWiker с помощью файла outwiker.exe под Windows, то данные строки вы должны увидеть в файле :file:`outwiker.log` в папке профиля программы (см. раздел :ref:`ru_faq_dir_settings`). Если плагин загружен, но данные строки не появляются в логе работы, убедитесь, что вы перевели OutWiker в отладочный режим (см. примечание в начале данного раздела).

Теперь вернемся в файл :file:`controller.py` и подпишемся на некоторые события из класса :class:`outwiker.core.application.ApplicationParams`. Измененный файл :file:`controller.py` будет выглядеть следующим образом:

.. code-block:: python

    # -*- coding: UTF-8 -*-

    import logging


    logger = logging.getLogger('ExampleEventsPlugin')


    class Controller(object):
        def __init__(self, application):
            self._application = application

        def initialize(self):
            logger.info(u'Initialize.')
            self._application.onWikiOpen += self._onWikiOpen
            self._application.onPageSelect += self._onPageSelect
            self._application.onPageUpdate += self._onPageUpdate
            self._application.onEditorPopupMenu += self._onEditorPopupMenu

        def destroy(self):
            logger.info(u'Destroy.')
            self._application.onWikiOpen -= self._onWikiOpen
            self._application.onPageSelect -= self._onPageSelect
            self._application.onPageUpdate -= self._onPageUpdate
            self._application.onEditorPopupMenu -= self._onEditorPopupMenu

        def _onWikiOpen(self, root):
            logger.info(u'onWikiOpen. Path to notes: {}'.format(root.path))

        def _onPageSelect(self, sender):
            if sender is None:
                logger.info(u'onPageSelect. No page selected.')
            else:
                logger.info(u'onPageSelect. Selected page: {}'.format(sender.subpath))

        def _onPageUpdate(self, sender, *args, **kwargs):
            logger.info(u'onPageUpdate. Updated page: {}'.format(sender.subpath))

        def _onEditorPopupMenu(self, page, params):
            logger.info(u'onEditorPopupMenu. Current page: {}'.format(page.subpath))


В классе :class:`eventsplugin.controller.Controller` была добавлена подписка на следующие события:

onWikiOpen
    Вызывается после открытия дерева заметок.

onPageSelect
    Вызывается после выбора новой страницы в дереве заметок.

onPageUpdate
    Вызывается после изменения содержимого страницы.

onEditorPopupMenu
    Вызывается перед созданием контекстного меню после клика правой кнопкой мыши в текстовом редакторе.

Чтобы увидеть эти события, пооткрывайте и позакрывайте дерево заметок, поизменяйте содержимое страниц и повызывайте контекстное меню с помощью правой кнопки мыши. Подробнее о параметрах каждого из этих событий написано в описании класса :class:`outwiker.core.application.ApplicationParams`.

Лог работы может выглядеть примерно следующим образом:

.. code-block:: text

    INFO       2017-08-20 22:33:14,963   ExampleEventsPlugin - controller - Initialize.
    INFO       2017-08-20 22:33:18,139   ExampleEventsPlugin - controller - onPageSelect. Selected page: test/page_01
    INFO       2017-08-20 22:33:18,140   ExampleEventsPlugin - controller - onWikiOpen. Path to notes: /home/jenyay/sync/wiki/samplewiki
    INFO       2017-08-20 22:33:18,140   root - plugin - Opening wiki /home/jenyay/sync/wiki/samplewiki: 1.09291815758 sec
    INFO       2017-08-20 22:33:20,662   ExampleEventsPlugin - controller - onPageSelect. No page selected.
    INFO       2017-08-20 22:33:21,801   ExampleEventsPlugin - controller - onPageUpdate. Updated page: # Поиск
    INFO       2017-08-20 22:33:21,803   ExampleEventsPlugin - controller - onPageUpdate. Updated page: # Поиск
    INFO       2017-08-20 22:33:21,804   ExampleEventsPlugin - controller - onPageUpdate. Updated page: # Поиск
    INFO       2017-08-20 22:33:21,859   ExampleEventsPlugin - controller - onPageSelect. Selected page: # Поиск
    INFO       2017-08-20 22:33:22,618   ExampleEventsPlugin - controller - onPageUpdate. Updated page: # Поиск
    INFO       2017-08-20 22:33:22,621   ExampleEventsPlugin - controller - onPageUpdate. Updated page: # Поиск
    INFO       2017-08-20 22:33:22,624   ExampleEventsPlugin - controller - onPageUpdate. Updated page: # Поиск
    INFO       2017-08-20 22:33:22,864   ExampleEventsPlugin - controller - onPageSelect. Selected page: test/page_01
    INFO       2017-08-20 22:33:53,506   ExampleEventsPlugin - controller - onEditorPopupMenu. Current page: test/page_01


Плагин готов. В данном разделе мы создали плагин, который обрабатывает некоторые события из класса :class:`outwiker.core.application.ApplicationParams` и выводит текст в лог работы. Исходные коды данного плагина расположены в папке :file:`plugins/examples/eventsplugin/`.

Развивая идею данного плагина, был создан плагин `DebugEvents`, который подобным образом следит за всеми событиями из класса :class:`outwiker.core.application.ApplicationParams`. Этот плагин предназначен исключительно для разработчиков плагина, поэтому не упоминается на сайте программы. Найти его можно в исходных кодах в папке :file:`plugins/debugevents`.
