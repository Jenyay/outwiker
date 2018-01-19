# -*- coding: UTF-8 -*-

"""
Плагин для открытия файлов заметок с помощью внешних программ,
а также для создания ссылок на викистраницах, при клике на которые запускаются
внешние программы.
"""

import os.path

from outwiker.core.pluginbase import Plugin

from .i18n import set_


class PluginExternalTools(Plugin):
    def __init__(self, application):
        """
        application - instance of core.application.ApplicationParams
        """
        from .controller import Controller
        Plugin.__init__(self, application)
        self.__controller = Controller(self)

    @property
    def application(self):
        return self._application

    ###################################################
    # Свойства и методы, которые необходимо определить
    ###################################################

    @property
    def name(self):
        return u"ExternalTools"

    @property
    def description(self):
        description = _(u'''Open notes files with external editor.

For OutWiker 1.9 and above ExternalTools adds the (:exec:) command for creation link or button for execute external applications from wiki page.

The (:exec:) command allow to run many applications. Every application must writed on the separated lines.

If line begins with "#" this line will be ignored. "#" in begin of the line is sign of the comment.
''')

        params = _(u'''The (:exec:) command has the following optional parameters:
<ul>
<li><b>format</b>. If the parameter equals "button" command will create a button instead of a link.</li>
<li><b>title</b>. The parameter sets the text for link or button.</li>
</ul>''')

        macros = _(u'''Inside (:exec:) command may be macroses. The macroses will be replaced by appropriate paths:
<ul>
<li><b>%page%</b>. The macros will be replaced by full path to page text file.</li>
<li><b>%html%</b>. The macros will be replaced by full path to HTML content file.</li>
<li><b>%folder%</b>. The macros will be replaced by full path to page folder.</li>
<li><b>%attach%</b>. The macros will be replaced by full path to attach folder without slash on the end.</li>
</ul>''')

        examples_title = _(u'''Examples''')

        example_1 = _(u'''Creating a link for running application.exe:
<code><pre>(:exec:)application.exe(:execend:)</pre></code>''')

        example_2 = _(u'''Same but creating a button
<code><pre>(:exec format=button:)
application.exe
(:execend:)</pre></code>''')

        example_3 = _(u'''Create a link for running application.exe with parameters:
<code><pre>(:exec:)
application.exe param1 "c:\\myfolder\\path to file name"
(:execend:)</pre></code>''')

        example_4 = _(u'''Run a lot of applications:
<code><pre>(:exec title="Run application_1, application_2 and application_3":)
application_1.exe
application_2.exe param_1 param_2
application_3.exe param_1 param_2
(:execend:)</pre></code>''')

        example_5 = _(u'''Open attached file with application.exe:
<code><pre>(:exec:)
application.exe Attach:my_file.txt
(:execend:)</pre></code>''')

        example_6 = _(u'''Execute application.exe from attachments folder:
<code><pre>(:exec:)
%attach%/application.exe %attach%/my_file.txt
(:execend:)</pre></code>
or
<code><pre>(:exec:)
Attach:application.exe Attach:my_file.txt
(:execend:)</pre></code>''')

        return (u'''{description}

{params}

{macros}

<b>{examples_title}</b>

{example_1}

{example_2}

{example_3}

{example_4}

{example_5}

{example_6}
''').format(description=description,
            params=params,
            macros=macros,
            examples_title=examples_title,
            example_1=example_1,
            example_2=example_2,
            example_3=example_3,
            example_4=example_4,
            example_5=example_5,
            example_6=example_6
            )

    def initialize(self):
        self.__initlocale()
        self.__controller.initialize()

    def destroy(self):
        """
        Уничтожение(выгрузка) плагина.
        Здесь плагин должен отписаться от всех событий
        """
        self.__controller.destroy()

    @property
    def url(self):
        return _(u"http://jenyay.net/Outwiker/ExternalToolsEn")

    #############################################

    def __initlocale(self):
        domain = u"externaltools"

        langdir = os.path.join(os.path.dirname(__file__), "locale")

        try:
            global _
            _ = self._init_i18n(domain, langdir)

            set_(_)
        except BaseException as e:
            print (e)
