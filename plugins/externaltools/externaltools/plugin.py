# -*- coding: utf-8 -*-

"""
Плагин для открытия файлов заметок с помощью внешних программ,
а также для создания ссылок на викистраницах, при клике на которые запускаются
внешние программы.
"""

from outwiker.api.core.plugins import Plugin

from .i18n import set_


class PluginExternalTools(Plugin):
    def __init__(self, application):
        """
        application - instance of core.application.ApplicationParams
        """
        from .controller import Controller

        super().__init__(application)
        self.__controller = Controller(self, application)

    @property
    def application(self):
        return self._application

    ###################################################
    # Свойства и методы, которые необходимо определить
    ###################################################

    @property
    def name(self):
        return "ExternalTools"

    @property
    def description(self):
        description = _(
            """ExternalTools plug-in allows to open the notes files with external applications.

The plug-in adds the (:exec:) command for creation link or button for execute external applications from wiki page.

The (:exec:) command allows to run many applications. Every application must be placed at the separated lines.

If a line begins with "#" this line will be ignored. "#" in begin of the line is sign of the comment.
"""
        )

        params = _(
            """The (:exec:) command has the following optional parameters:
<ul>
<li><b>format</b>. If the parameter equals "button" command will create a button instead of a link.</li>
<li><b>title</b>. The parameter sets the text for link or button.</li>
</ul>"""
        )

        macros = _(
            """Inside (:exec:) command may be macroses. The macroses will be replaced by appropriate paths:
<ul>
<li><b>%page%</b>. The macros will be replaced by full path to page text file.</li>
<li><b>%html%</b>. The macros will be replaced by full path to HTML content file.</li>
<li><b>%folder%</b>. The macros will be replaced by full path to page folder.</li>
<li><b>%attach%</b>. The macros will be replaced by full path to attach folder without slash on the end.</li>
</ul>"""
        )

        examples_title = _("""Examples""")

        example_1 = _(
            """Creating a link for running application.exe:
<code><pre>(:exec:)application.exe(:execend:)</pre></code>"""
        )

        example_2 = _(
            """Same but creating a button
<code><pre>(:exec format=button:)
application.exe
(:execend:)</pre></code>"""
        )

        example_3 = _(
            """Create a link for running application.exe with parameters:
<code><pre>(:exec:)
application.exe param1 "c:\\myfolder\\path to file name"
(:execend:)</pre></code>"""
        )

        example_4 = _(
            """Run a lot of applications:
<code><pre>(:exec title="Run application_1, application_2 and application_3":)
application_1.exe
application_2.exe param_1 param_2
application_3.exe param_1 param_2
(:execend:)</pre></code>"""
        )

        example_5 = _(
            """Open attached file with application.exe:
<code><pre>(:exec:)
application.exe Attach:my_file.txt
(:execend:)</pre></code>"""
        )

        example_6 = _(
            """Execute application.exe from attachments folder:
<code><pre>(:exec:)
%attach%/application.exe %attach%/my_file.txt
(:execend:)</pre></code>
or
<code><pre>(:exec:)
Attach:application.exe Attach:my_file.txt
(:execend:)</pre></code>"""
        )

        return (
            """{description}

{params}

{macros}

<b>{examples_title}</b>

{example_1}

{example_2}

{example_3}

{example_4}

{example_5}

{example_6}
"""
        ).format(
            description=description,
            params=params,
            macros=macros,
            examples_title=examples_title,
            example_1=example_1,
            example_2=example_2,
            example_3=example_3,
            example_4=example_4,
            example_5=example_5,
            example_6=example_6,
        )

    def initialize(self):
        set_(self.gettext)

        global _
        _ = self.gettext
        self.__controller.initialize()

    def destroy(self):
        """
        Уничтожение(выгрузка) плагина.
        Здесь плагин должен отписаться от всех событий
        """
        self.__controller.destroy()

    @property
    def url(self):
        return _("https://jenyay.net/Outwiker/ExternalToolsEn")
