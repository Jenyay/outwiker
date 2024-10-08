��    +      t  ;   �      �  ,   �  %   �          ,     L     X     e     l     �  �   �  g   2     �     �  '   �  �   �     �     �  �  �  -   {  o   �  m   	  i   �	  n   �	     `
     g
  �  �
     V     [     u  x   �             �   ,  :        @  ;   Z  e   �  �   �     �  
   �  6     +   ;  M  g  S   �  D   	  6   N  D   �     �  !   �        ;     7   I  �   �  �   J     �     �  C   �    6  %   H     n  %  |  F   �  �   �  �   �  �   ~  �   8       &     4  6     k!  @   ~!  $   �!  �   �!  >   �"  %   �"    �"  �   �#  0   �$  �   �$  �   <%  �  �%     k'     ~'  �   �'  )   +(                  (                             '                
           %         !             "      	                                   &          )                   $       +   *      #               %attach%. Path to current attachments folder %folder%. Path to current page folder %html%. Current page. HTML file %page%. Current page. Text file All Files|* Append Tools Button Can't execute tools Can't save options Create a link for running application.exe with parameters:
<code><pre>(:exec:)
application.exe param1 "c:\myfolder\path to file name"
(:execend:)</pre></code> Creating a link for running application.exe:
<code><pre>(:exec:)application.exe(:execend:)</pre></code> Error Examples Executables (*.exe)|*.exe|All Files|*.* Execute application.exe from attachments folder:
<code><pre>(:exec:)
%attach%/application.exe %attach%/my_file.txt
(:execend:)</pre></code>
or
<code><pre>(:exec:)
Attach:application.exe Attach:my_file.txt
(:execend:)</pre></code> External Tools [Plugin] ExternalTools ExternalTools plug-in allows to open the notes files with external applications.

The plug-in adds the (:exec:) command for creation link or button for execute external applications from wiki page.

The (:exec:) command allows to run many applications. Every application must be placed at the separated lines.

If a line begins with "#" this line will be ignored. "#" in begin of the line is sign of the comment.
 ExternalTools plugin. Insert (:exec:) command ExternalTools plugin. Insert a %attach% macros. The macros will be replaced by a path to current attach folder. ExternalTools plugin. Insert a %folder% macros. The macros will be replaced by a path to current page folder. ExternalTools plugin. Insert a %html% macros. The macros will be replaced by a path to current HTML file. ExternalTools plugin. Insert a %page% macros. The macros will be replaced by a path to current page text file. Format Inserting (:exec:) command Inside (:exec:) command may be macroses. The macroses will be replaced by appropriate paths:
<ul>
<li><b>%page%</b>. The macros will be replaced by full path to page text file.</li>
<li><b>%html%</b>. The macros will be replaced by full path to HTML content file.</li>
<li><b>%folder%</b>. The macros will be replaced by full path to page folder.</li>
<li><b>%attach%</b>. The macros will be replaced by full path to attach folder without slash on the end.</li>
</ul> Link Open Content File with... Open Result HTML File with... Open attached file with application.exe:
<code><pre>(:exec:)
application.exe Attach:my_file.txt
(:execend:)</pre></code> Open file dialog... Remove tool Run a lot of applications:
<code><pre>(:exec title="Run application_1, application_2 and application_3":)
application_1.exe
application_2.exe param_1 param_2
application_3.exe param_1 param_2
(:execend:)</pre></code> Run application by ExternalTools plugin?
It may be unsafe. Run applications (:exec:) Run applications by ExternalTools plugin?
It may be unsafe. Same but creating a button
<code><pre>(:exec format=button:)
application.exe
(:execend:)</pre></code> The (:exec:) command has the following optional parameters:
<ul>
<li><b>format</b>. If the parameter equals "button" command will create a button instead of a link.</li>
<li><b>title</b>. The parameter sets the text for link or button.</li>
</ul> Title Tools List Warn before executing applications by (:exec:) command https://jenyay.net/Outwiker/ExternalToolsEn Project-Id-Version: outwiker
Report-Msgid-Bugs-To: 
PO-Revision-Date: 2018-08-23 13:04+0300
Last-Translator: Jenyay <jenyay.ilin@gmail.com>
Language-Team: Ukrainian
Language: uk_UA
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
Plural-Forms: nplurals=4; plural=((n%10==1 && n%100!=11) ? 0 : ((n%10 >= 2 && n%10 <=4 && (n%100 < 12 || n%100 > 14)) ? 1 : ((n%10 == 0 || (n%10 >= 5 && n%10 <=9)) || (n%100 >= 11 && n%100 <= 14)) ? 2 : 3));
X-Generator: Poedit 2.0.6
X-Crowdin-Project: outwiker
X-Crowdin-Language: uk
X-Crowdin-File: externaltools.po
 %attach%. Шлях до поточної папки долучених файлів %folder%. Шлях до папки поточної сторінки %html%. Поточна сторінка. HTML-файл %page%. Поточна сторінка. Текстовий файл Всі Файли|* Додати застосунок Кнопка Не вдалося запустити застосунок Не вдалося зберегти параметри Створити посилання для запуску application.exe з параметрами:
<code><pre>(:exec:)
application.exe param1 "c:\myfolder\path to file name"
(:execend:)</pre></code> Створення посилання для запуску application.exe:
<code><pre>(:exec:)application.exe(:execend:)</pre></code> Помилка Приклади Виконувані файли (*.exe)|*.exe|Всі файли|*.* Запустити application.exe з папки з долученими файлами:
<code><pre>(:exec:)
%attach%/application.exe %attach%/my_file.txt
(:execend:)</pre></code>
або
<code><pre>(:exec:)
Attach:application.exe Attach:my_file.txt
(:execend:)</pre></code> External Tools [Розширення] ExternalTools Додаток ExternalTools дозволяє відкривати файли нотаток за допомогою завнішніх застосунків.

Додаток додає команду (:exec:) для створення посилання або кнопки, які дозволяють запускати зовнішні застосункі з вікісторінок..

Команда (:exec:) дозволяє запускати декілька застосунків одночасно. Кожен застосунок має бути розміщений на окремому рядку.

Якщо рядок починається зі знаку "#", то цей рядок ігнорується. Знак "#" на початку рядка означає коментар.
 Додаток ExternalTools. Вставити команду (:exec:) Додаток ExternalTools. Вставити макрос %attach%. Цей макрос буде замінений на шлях до папки з долученими файлами поточної сторінки. Додаток ExternalTools. Вставити макрос %folder%. Цей макрос буде замінений на шлях до папки поточної сторінки. Додаток ExternalTools. Вставити макрос %html%. Цей макрос буде замінений на шлях до HTML-файлу поточної сторінки. Додаток ExternalTools. Вставити макрос %page%. Цей макрос буде замінений на шлях до текстового файлу поточної сторінки. Формат Вставка команди (:exec:) Всередині команди (:exec:) можуть використовуватися макроси. Ці макроси будуть замінені на відповідні шляхи:
<ul>
<li><b>%page%</b>. Цей макрос буде замінений на повний шлях до файлу з текстом сторінки.</li>
<li><b>%html%</b>. Цей макрос буде замінений на повний шлях до HTML-файлу сторінки.</li>
<li><b>%folder%</b>. Цей макрос буде замінений на повний шлях до папки сторінки.</li>
<li><b>%attach%</b>. Цей макрос буде замінений на повний шлях до папки з долученими файлами без слешу на кінці.</li>
</ul> Посилання Відкрити файл з текстом нотатки в... Відкрити HTML-файл в... Відкрити долучений файл за допомогою application.exe:
<code><pre>(:exec:)
application.exe Attach:my_file.txt
(:execend:)</pre></code> Діалогове вікно відкриття файлу... Видалити застосунок Запуск декількох застосунків:
<code><pre>(:exec title="Запустити application_1, application_2 та application_3":)
application_1.exe
application_2.exe param_1 param_2
application_3.exe param_1 param_2
(:execend:)</pre></code> Запустити застосунок за допомогою додатку ExternalTools?
Це може бути небезпечно. Запустити застосунок (:exec:) Запустити застосунки за допомогою додатку ExternalTools?
Це може бути небезпечно. Те ж саме, але для створення кнопки
<code><pre>(:exec format=button:)
application.exe
(:execend:)</pre></code> Команда (:exec:) має наступні необов'язкові параметри:
<ul>
<li>format. Якщо цей параметр дорівнює "button", то команда створить кнопку замість посилання (за замовчуванням).</li>
<li>title. Цей параметр встановлює текст для посилання або кнопки.</li>
</ul> Заголовок Список засобів Показувати попередження перед запуском
застосунків за допомогою команди (:exec:) https://jenyay.net/Outwiker/ExternalTools 