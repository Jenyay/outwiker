.. _ru_application:

Application. Экземпляр класса ApplicationParams
===============================================

Чтобы плагин мог делать что-то полезное, в первую очередь нужно разобраться с классом :class:`outwiker.core.application.ApplicationParams`. Этот класс представлен глобальной переменной `Application` в модуле `outwiker.core.application`. Переменная `Application` - это интерфейс для доступа ко всем основным частям OutWiker. Идеология плагинов для OutWiker диктуется динамической сутью языка Python, т.е. вы можете добраться практически до любой части основной программы, но за свои действия отвечаете сами - никаких "песочниц" для плагинов не предусмотрено.


По историческим причинам во многих частях программы доступ к переменной Application осуществляется следующим образом:

.. code-block:: python

    from outwiker.core.application import Application

    ...

    # Использование переменной Application

Но лучше не использовать явный импорт переменной `Application`, а передавать ее в явном виде между классами, которые нуждаются в этой переменной. Например, экземпляр класса :class:`outwiker.core.application.ApplicationParams` передается в конструктор класса :class:`outwiker.core.pluginbase.Plugin` и доступен через поле `self._application` внутри классов, производных от :class:`outwiker.core.pluginbase.Plugin`.

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

    .. py:attribute:: wikiroot

        Корень открытого в данный момент дерева заметок. Экземпляр класса :class:`outwiker.core.tree.WikiDocument` или `None`, если в данный момент нет открытого дерева заметок.

    .. py:attribute:: selectedPage

        Выбранная в данный момент страница. Экземпляр класса, производного от :class:`outwiker.core.tree.WikiPage` или `None`, если в данный момент нет открытого дерева заметок или никакая страница не выбрана.

    .. py:attribute:: mainWindow

        Ссылка на экземпляр класса :class:`outwiker.gui.mainwikdow.MainWindow` главного окна программы.

    .. py:attribute:: customEvents

        Экземпляр класса :class:`outwiker.core.event.CustomEvents`, предназначенный для работы с нестандартными событиями (например, событиями, созданными плагинами).

    .. py:attribute:: onWikiOpen

        **Событие.** Экземпляр класса :class:`outwiker.core.event.Events`. Вызывается после открытия дерева заметок. Обработчик должен принимать параметры:
            * `root` - экземпляр класса :class:`outwiker.core.tree.WikiDocument`, который предназначен для работы с деревом заметок в целом. `root` может быть равен `None`.

    .. py:attribute:: onWikiClose

        **Событие.** Экземпляр класса :class:`outwiker.core.event.Events`. Вызывается перед закрытием дерева заметок (например, перед открытием нового дерева заметок или в процессе закрытия программы). Обработчик должен принимать параметры:
            * `root` - экземпляр класса :class:`outwiker.core.tree.WikiDocument`. `root` может быть равен `None`.

    .. py:attribute:: onPageUpdate

        **Событие.** Экземпляр класса :class:`outwiker.core.event.Events`. Вызывается после изменения содержимого страницы. Обработчик должен принимать параметры:
            * `sender` - страница, которая изменилась (это может быть не обязательно текущая страница). Экземпляр класса :class:`outwiker.core.tree.WikiPage` или производного от него.
            * `change` - переменная, содержащая флаги, обозначающие, что именно изменилось. Возможные значения флагов описаны в :file:`src/outwiker/core/events.py`: 
                * `PAGE_UPDATE_CONTENT` - изменилось содержимое страницы; 
                * `PAGE_UPDATE_ICON` - изменилась иконка страницы;
                * `PAGE_UPDATE_TAGS` - изменились теги страницы;
                * `PAGE_UPDATE_STYLE` - изменился стиль страницы.

    .. py:attribute:: onPageCreate

        **Событие.** Экземпляр класса :class:`outwiker.core.event.Events`. Вызывается после создания новой страницы. Обработчик должен принимать параметры:
            * `sender` - только что созданная страница. Экземпляр класса :class:`outwiker.core.tree.WikiPage` или производного от него.

    .. py:attribute:: onTreeUpdate

        **Событие.** Экземпляр класса :class:`outwiker.core.event.Events`. Вызывается после каких-либо изменений в дереве заметок. Обработчик должен принимать параметры:
            * `sender` - Страница, из-за которой было вызвано событие. Экземпляр класса :class:`outwiker.core.tree.WikiPage` или производного от него. Может быть равен `None`.

    .. py:attribute:: onPageSelect

        **Событие.** Экземпляр класса :class:`outwiker.core.event.Events`. Вызывается после изменения выбранной страницы. Обработчик должен принимать параметры:
            * `sender` - Новая выбранная страница. Экземпляр класса :class:`outwiker.core.tree.WikiPage` или производного от него. Может быть равен `None` (например, если выбирается корень дерева, который не является полноценной страницей).

    .. py:attribute:: onAttachmentPaste

        **Событие.** Экземпляр класса :class:`outwiker.core.event.Events`. Вызывается после нажатия кнопки "Вставить" на панели прикрепленных файлов. Обработчик должен отреагировать на то, что пользователь хочет вставить ссылки на прикрепленные файлы в текст страницы. Обработчик должен принимать параметры:
            * `fnames` - список имен выбранных прикрепленных файлов (только имена без полных путей).

    .. py:attribute:: onBookmarksChanged

        **Событие.** Экземпляр класса :class:`outwiker.core.event.Events`. Вызывается после добавления страницы в закладки или удаления из них. Обработчик должен принимать параметры:
            * `bookmark` - экземпляр класса :class:`outwiker.core.bookmarks.Bookmarks`.

    .. py:attribute:: onPageRemove

        **Событие.** Экземпляр класса :class:`outwiker.core.event.Events`. Вызывается после удаления страницы из дерева заметок. Обработчик должен принимать параметры:
            * `page` - удаленная страница. Экземпляр класса :class:`outwiker.core.tree.WikiPage` или производного от него.

    .. py:attribute:: onPageRename

        **Событие.** Экземпляр класса :class:`outwiker.core.event.Events`. Вызывается после переименования страницы. Обработчик должен принимать параметры:
            * `page` - переименованная страница. Экземпляр класса :class:`outwiker.core.tree.WikiPage` или производного от него.
            * `oldSubpath` - строка, содержащая старый относительный путь до переименованной страницы.

    .. py:attribute:: onStartTreeUpdate

        **Событие.** Экземпляр класса :class:`outwiker.core.event.Events`. Вызывается, чтобы сообщить о том, что над деревом заметок будет производиться множество операций, которые будут вызывать события, которые, возможно, нет смысла обрабатывать по отдельности. В этом случае часто полезно временно отписаться от всех событий кроме `onEndTreeUpdate` (см. далее), по пришествию которого опять подписаться на интересующие события. Обработчик должен принимать параметры:
            * `root` - экземпляр класса :class:`outwiker.core.tree.WikiDocument`. `root` может быть равен `None`.

    .. py:attribute:: onEndTreeUpdate

        **Событие.** Экземпляр класса :class:`outwiker.core.event.Events`. Вызывается, чтобы сообщить о том, что над деревом заметок было произведено множество операций, которые могли вызывать события, которые, возможно, нет смысла обрабатывать по отдельности. Обычно событие `onEndTreeUpdate` вызывается после `onStartTreeUpdate`. Обработчик должен принимать параметры:
            * `root` - экземпляр класса :class:`outwiker.core.tree.WikiDocument`. `root` может быть равен `None`.

    .. py:attribute:: onHtmlRenderingBegin

        **Событие.** Экземпляр класса :class:`outwiker.core.event.Events`. Вызывается в начале процесса создания и отображения HTML, например, при переключении с викинотации на вкладку просмотра на викистраницах или с HTML-кода на вкладку просмотра на HTML-страницах. Полный порядок вызова событий показан на рисунке в разделе :ref:`ru_events_wiki`. Обработчик должен принимать параметры:
            * `page` - Страница, для которой происходит рендеринг HTML (скорее всего это выбранная в данный момент страница). Экземпляр класса :class:`outwiker.core.tree.WikiPage` или производного от него.
            * `htmlView` - окно для отображения HTML.

    .. py:attribute:: onHtmlRenderingEnd

        **Событие.** Экземпляр класса :class:`outwiker.core.event.Events`. Вызывается в конце процесса создания и отображения HTML, например, при переключении с викинотации на вкладку просмотра на викистраницах или с HTML-кода на вкладку просмотра на HTML-страницах. Полный порядок вызова событий показан на рисунке в разделе :ref:`ru_events_wiki`. Обработчик должен принимать параметры:
            * `page` - Страница, для которой происходит рендеринг HTML (скорее всего это выбранная в данный момент страница). Экземпляр класса :class:`outwiker.core.tree.WikiPage` или производного от него.
            * `htmlView` - окно для отображения HTML.

    .. py:attribute:: onPageOrderChange

        **Событие.** Экземпляр класса :class:`outwiker.core.event.Events`. Вызывается после изменения порядка следования страницы в дереве заметок. Обработчик должен принимать параметры:
            * `page` - страница, которую переместили выше или ниже. Экземпляр класса :class:`outwiker.core.tree.WikiPage` или производного от него.

    .. py:attribute:: onForceSave

        **Событие.** Экземпляр класса :class:`outwiker.core.event.Events`. Можно вызвать, чтобы принудительно заставить сохранить текущую страницу. Обработчик не должен принимать никакие параметры.

    .. py:attribute:: onWikiParserPrepare

        **Событие.** Экземпляр класса :class:`outwiker.core.event.Events`. Вызывается перед тем как запустится разбор викинотации. Событие предназначено для того, чтобы плагины могли дополнить викинотацию. Обработчик должен принимать параметры:
            * `parser` - парсер викинотации. Экземпляр класса :class:`outwiker.pages.wiki.parser.wikiparser.Parser`.

    .. py:attribute:: onPreferencesDialogCreate

        **Событие.** Экземпляр класса :class:`outwiker.core.event.Events`. Вызывается во время создания диалога настроек программы. Событие предназначено для того, чтобы плагины могли добавить новые разделы в диалог настроек. Обработчик должен принимать параметры:
            * `dialog` - диалог настроек. Экземпляр класса :class:`outwiker.gui.preferences.prefdialog.PrefDialog`.

    .. py:attribute:: onPreferencesDialogClose

        **Событие.** Экземпляр класса :class:`outwiker.core.event.Events`. Вызывается после закрытия диалога настроек программы. Событие предназначено для того, чтобы программа OutWiker или плагины могли применить новые настройки. Обработчик должен принимать параметры:
            * `dialog` - диалог настроек. Экземпляр класса :class:`outwiker.gui.preferences.prefdialog.PrefDialog`.

    .. py:attribute:: onPageViewCreate

        **Событие.** Экземпляр класса :class:`outwiker.core.event.Events`. Вызывается после создания интерфейса отображения страницы. Это событие можно использовать для настройки интерфейса программы под выбранный в данный момент тип страницы. Обработчик должен принимать параметры:
            * `page` - страница, для которой был создан интерфейс. Экземпляр класса :class:`outwiker.core.tree.WikiPage` или производного от него.

    .. py:attribute:: onTreePopupMenu

        **Событие.** Экземпляр класса :class:`outwiker.core.event.Events`. Вызывается, когда пользователь щелкает правой кнопкой на дереве заметок, но до того, как будет отображено всплывающее меню. Событие предназначено для того, чтобы плагин мог изменить всплывающее меню, например, добавить новые пункты. Обработчик должен принимать параметры:
            * `menu` - меню, которое будет показано пользователю. Экземпляр класса :class:`wx.Menu`.
            * `page` - страница, на которую щелкнули правой кнопкой мыши в дереве заметок. Экземпляр класса :class:`outwiker.core.tree.WikiPage` или производного от него.

    .. py:attribute:: onPreprocessing

        **Событие.** Экземпляр класса :class:`outwiker.core.event.Events`. Вызывается перед началом преобразования текста страниц в HTML для их отображения. В данный момент используется для HTML-, вики- и Markdown-страниц. Это событие можно использовать для изменения содержимого страницы перед его преобразованием в HTML. Полный порядок вызова событий показан на рисунке в разделе :ref:`ru_events_wiki`. Обработчик должен принимать параметры:
            * `page` - страница, которую в данный момент обрабатывают. Экземпляр класса :class:`outwiker.core.tree.WikiPage` или производного от него.
            * `params` - экземпляр класса :class:`outwiker.core.events.PreprocessingParams`.

    .. py:attribute:: onPostprocessing

        **Событие.** Экземпляр класса :class:`outwiker.core.event.Events`. Вызывается после преобразования текста страниц в HTML для их отображения. В данный момент используется для HTML-, вики- и Markdown-страниц. Это событие можно использовать для изменения содержимого страницы после его парсинга, но до его отображения в виде HTML. Полный порядок вызова событий показан на рисунке в разделе :ref:`ru_events_wiki`. Обработчик должен принимать параметры:
            * `page` - страница, которую в данный момент обрабатывают. Экземпляр класса :class:`outwiker.core.tree.WikiPage` или производного от него.
            * `params` - экземпляр класса :class:`outwiker.core.events.PostprocessingParams`.

    .. py:attribute:: onPreHtmlImproving

        **Событие.** Экземпляр класса :class:`outwiker.core.event.Events`. Вызывается после преобразования текста страницы в HTML, но до "улучшения" полученного HTML-кода. Полный порядок вызова событий показан на рисунке в разделе :ref:`ru_events_wiki`. Обработчик должен принимать параметры:
            * `page` - страница, которую в данный момент обрабатывают. Экземпляр класса :class:`outwiker.core.tree.WikiPage` или производного от него.
            * `params` - экземпляр класса :class:`outwiker.core.events.PreHtmlImprovingParams`.

    .. py:attribute:: onPrepareHtmlImprovers

        **Событие.** Экземпляр класса :class:`outwiker.core.event.Events`. Вызывается после создания списка "улучшателей" HTML-кода, но до выбора конкретного "улучшателя" для работы. Улучшатели предназначены для преобразования HTML-кода (разделения текста на абзацы, форматирование кода и т.п.). Это событие можно использовать, чтобы добавить свой "улучшатель". Полный порядок вызова событий показан на рисунке в разделе :ref:`ru_events_wiki`. Обработчик должен принимать параметры:
            * `factory` - фабрика для создания "улучшателей". Экземпляр класса :class:`outwiker.core.htmlimproverfactory.HtmlImproverFactory`. С помощью этого класса можно добавлять новые "улучшатели", которые должны быть производными класса :class:`outwiker.core.htmlimprover.HtmlImprover`.

    .. py:attribute:: onHoverLink

        **Событие.** Экземпляр класса :class:`outwiker.core.event.Events`. Вызывается, когда пользователь проводит курсором мыши над ссылкой в окне просмотра страницы. В данный момент из-за особенности работы wxPython данное событие вызывается только в Windows. Обработчик должен принимать параметры:
            * `page` - текущая страница. Экземпляр класса :class:`outwiker.core.tree.WikiPage` или производного от него.
            * `params` - экземпляр класса :class:`outwiker.core.events.HoverLinkParams`.

    .. py:attribute:: onLinkClick

        **Событие.** Экземпляр класса :class:`outwiker.core.event.Events`. Вызывается, когда пользователь щелкает на ссылку на странице в режиме просмотра. Обработчик должен принимать параметры:
            * `page` - текущая страница. Экземпляр класса :class:`outwiker.core.tree.WikiPage` или производного от него.
            * `params` - экземпляр класса :class:`outwiker.core.events.LinkClickParams`.

    .. py:attribute:: onPageDialogInit

        **Событие.** Экземпляр класса :class:`outwiker.core.event.Events`. Вызывается, когда пользователь щелкает правой кнопкой мыши в текстовом редакторе, но до отображения всплывающего меню. Это событие можно использовать для изменения контекстного меню редактора. Обработчик должен принимать параметры:
            * `page` - текущая страница. Экземпляр класса :class:`outwiker.core.tree.WikiPage` или производного от него.
            * `params` - экземпляр класса :class:`outwiker.core.events.EditorPopupMenuParams`.

    .. py:attribute:: onPageDialogInit

        **Событие.** Экземпляр класса :class:`outwiker.core.event.Events`. Вызывается, во время создания диалога для установки свойств страницы. Это событие можно использовать для того, чтобы добавить новый тип страниц в данный диалог. Обработчик должен принимать параметры:
            * `page` - страница, для которой вызывается диалог. Экземпляр класса :class:`outwiker.core.tree.WikiPage` или производного от него.
            * `params` - экземпляр класса :class:`outwiker.core.events.PageDialogInitParams`.

    .. py:attribute:: onPageDialogDestroy

        **Событие.** Экземпляр класса :class:`outwiker.core.event.Events`. Вызывается, в процессе уничтожения диалога для установки свойств страницы. Обработчик должен принимать параметры:
            * `page` - страница, для которой вызывается диалог. Экземпляр класса :class:`outwiker.core.tree.WikiPage` или производного от него.
            * `params` - экземпляр класса :class:`outwiker.core.events.PageDialogDestroyParams`.

    .. py:attribute:: onPageDialogPageTypeChanged

        **Событие.** Экземпляр класса :class:`outwiker.core.event.Events`. Вызывается, когда в диалоге изменения свойств страницы пользователь меняет тип страницы. Это событие можно использовать, например, для настройки внешнего вида диалога изменения свойств страницы в зависимости от выбранного типа страницы. Обработчик должен принимать параметры:
            * `page` - страница, для которой вызывается диалог. Экземпляр класса :class:`outwiker.core.tree.WikiPage` или производного от него.
            * `params` - экземпляр класса :class:`outwiker.core.events.PageDialogPageTypeChangedParams`.

    .. py:attribute:: onPageDialogPageTitleChanged

        **Событие.** Экземпляр класса :class:`outwiker.core.event.Events`. Вызывается, когда в диалоге изменения свойств страницы пользователь меняет заголовок страницы. Обработчик должен принимать параметры:
            * `page` - страница, для которой вызывается диалог. Экземпляр класса :class:`outwiker.core.tree.WikiPage` или производного от него.
            * `params` - экземпляр класса :class:`outwiker.core.events.PageDialogPageTitleChangedParams`.

    .. py:attribute:: onPageDialogPageStyleChanged

        **Событие.** Экземпляр класса :class:`outwiker.core.event.Events`. Вызывается, когда в диалоге изменения свойств страницы пользователь меняет стиль страницы. Обработчик должен принимать параметры:
            * `page` - страница, для которой вызывается диалог. Экземпляр класса :class:`outwiker.core.tree.WikiPage` или производного от него.
            * `params` - экземпляр класса :class:`outwiker.core.events.PageDialogPageStyleChangedParams`.

    .. py:attribute:: onPageDialogPageIconChanged

        **Событие.** Экземпляр класса :class:`outwiker.core.event.Events`. Вызывается, когда в диалоге изменения свойств страницы пользователь меняет иконку страницы. Обработчик должен принимать параметры:
            * `page` - страница, для которой вызывается диалог. Экземпляр класса :class:`outwiker.core.tree.WikiPage` или производного от него.
            * `params` - экземпляр класса :class:`outwiker.core.events.PageDialogPageIconChangedParams`.

    .. py:attribute:: onPageDialogPageTagsChanged

        **Событие.** Экземпляр класса :class:`outwiker.core.event.Events`. Вызывается, когда в диалоге изменения свойств страницы пользователь меняет теги страницы. Обработчик должен принимать параметры:
            * `page` - страница, для которой вызывается диалог. Экземпляр класса :class:`outwiker.core.tree.WikiPage` или производного от него.
            * `params` - экземпляр класса :class:`outwiker.core.events.PageDialogPageTagsChangedParams`.

    .. py:attribute:: onPageDialogPageFactoriesNeeded

        **Событие.** Экземпляр класса :class:`outwiker.core.event.Events`. Вызывается во время создания диалога редактирования свойств страницы. Обработчик этого события может добавлять нестандартные типы фабрик страниц, чтобы пользователь мог выбрать новый тип страниц в соответствующем выпадающем списке. В основном событие нежно для плагинов, которые добавляют новые типы страниц. Обработчик должен принимать параметры:
            * `page` - страница, для которой вызывается диалог. Экземпляр класса :class:`outwiker.core.tree.WikiPage` или производного от него.
            * `params` - экземпляр класса :class:`outwiker.core.events.PageDialogPageFactoriesNeededParams`.

    .. py:attribute:: onEditorStyleNeeded

        **Событие.** Экземпляр класса :class:`outwiker.core.event.Events`. Вызывается в процессе раскраски текста страницы в редакторе заметок. Обработчик должен принимать параметры:
            * `page` - страница, для которой вызывается диалог. Экземпляр класса :class:`outwiker.core.tree.WikiPage` или производного от него.
            * `params` - экземпляр класса :class:`outwiker.core.events.EditorStyleNeededParams`.

    .. py:attribute:: onPageUpdateNeeded

        **Событие.** Экземпляр класса :class:`outwiker.core.event.Events`. Вызывается, чтобы принудительно обновить текущую страницу. Обработчик должен принимать параметры:
            * `page` - страница, для которой вызывается диалог. Экземпляр класса :class:`outwiker.core.tree.WikiPage` или производного от него.
            * `params` - экземпляр класса :class:`outwiker.core.events.PageUpdateNeededParams`.

    .. py:attribute:: onPreWikiOpen

        **Событие.** Экземпляр класса :class:`outwiker.core.event.Events`. Вызывается до того, как будет открыто новое дерево заметок. Обработчик должен принимать параметры:
            * `page` - страница, для которой вызывается диалог. Экземпляр класса :class:`outwiker.core.tree.WikiPage` или производного от него.
            * `params` - экземпляр класса :class:`outwiker.core.events.PreWikiOpenParams`.

    .. py:attribute:: onPostWikiOpen

        **Событие.** Экземпляр класса :class:`outwiker.core.event.Events`. Вызывается после попытки открытия нового дерева заметок. Отличие от события `onWikiOpen` заключается в том, что `onPostWikiOpen` вызывается также после неудачных попыток открыть дерево заметок. Обработчик должен принимать параметры:
            * `page` - страница, для которой вызывается диалог. Экземпляр класса :class:`outwiker.core.tree.WikiPage` или производного от него.
            * `params` - экземпляр класса :class:`outwiker.core.events.PostWikiOpenParams`.

    .. py:attribute:: onIconsGroupsListInit

        **Событие.** Экземпляр класса :class:`outwiker.core.event.Events`. Вызывается после во время создания списка групп иконок. Обрабатывая это событие, плагин может добавлять или редактировать имеющийся список групп иконок. Обработчик должен принимать параметры:
            * `page` - страница, для которой вызывается диалог. Экземпляр класса :class:`outwiker.core.tree.WikiPage` или производного от него.
            * `params` - экземпляр класса :class:`outwiker.core.events.IconsGroupsListInitParams`.

    .. py:attribute:: onPageModeChange

        **Событие.** Экземпляр класса :class:`outwiker.core.event.Events`. Вызывается после переключения страницы из одного режима в другой (текст / просмотр / HTML). Обработчик должен принимать параметры:
            * `page` - страница, для которой вызывается диалог. Экземпляр класса :class:`outwiker.core.tree.WikiPage` или производного от него.
            * `params` - экземпляр класса :class:`outwiker.core.events.PageModeChangeParams`.

    .. py:attribute:: onAttachListChanged

        **Событие.** Экземпляр класса :class:`outwiker.core.event.Events`. Вызывается после изменения списка прикрепленных файлов: после добавления новых файлов, удаления или переименования файлов. Обработчик вызывается независимо от того, изменение списка файлов было сделано через интерфейс OutWiker или через файловый менеджер операционной системы. Обработчик должен принимать параметры:
            * `page` - страница, для которой вызывается диалог. Экземпляр класса :class:`outwiker.core.tree.WikiPage` или производного от него.
            * `params` - экземпляр класса :class:`outwiker.core.events.AttachListChangedParams`.



.. _ru_events_wiki:

Порядок событий, в процессе отображения викистраниц
---------------------------------------------------

.. warning::

    Некоторые события могут быть еще не реализованы.
.. image:: /_static/ru_api_events.png
    :align: center
    :alt: Порядок событий, в процессе отображения викистраниц
