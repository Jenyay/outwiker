# -*- coding: utf-8 -*-
"""
    pygments.lexers.1S
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for language: 1S.

    :license: GNU LGPL, see LICENSE for more details.
"""

import re

from pygments.lexer import RegexLexer, RegexLexerMeta, include, bygroups, using, this
from pygments.token import \
     Text, Comment, Operator, Keyword, Name, String, Number, Literal


__all__ = ['OneSLexer']


class OneSLexer(RegexLexer):

    name = '1S'
    aliases = ['1s', '1c']
    filenames = ['*.1s', '*.prm', '*.1cpp']
    mimetypes = ['text/x-1s']

    #: optional Comment or Whitespace
    _ws = ur'(?:\s|//.*?\n|/[*].*?[*]/)+'


    flags = re.IGNORECASE | re.MULTILINE | re.DOTALL | re.UNICODE
    tokens = {
        'whitespace': [
            (ur'^\s*#', Comment.Preproc, 'macro'),
            (ur'^\s*//#.*?\n', Comment.Preproc),
            (ur'\n', Text),
            (ur'\s+', Text),
            (ur'\\\n', Text), # line continuation
            (ur'//.*?\n', Comment),
        ],
        'statements': [
            (ur'L?"', String, 'string'),
            (ur'(\s)*?\|', String, 'string'),
            (ur'(0x[0-9a-fA-F]|0[0-7]+|(\d+\.\d*|\.\d+)|\d+)'
             ur'e[+-]\d+[lL]?', Number.Float),
            (ur'0x[0-9a-fA-F]+[Ll]?', Number.Hex),
            (ur'0[0-7]+[Ll]?', Number.Oct),
            (ur'(\d+\.\d*|\.\d+)', Number.Float),
            (ur'\d+', Number.Integer),
            (ur'\'[0-3][0-9]\.[0-1][0-9]\.([0-9][0-9]|[0-9][0-9][0-9][0-9])\'', Literal.Date),
            (ur'[!%^&*()+=|\[\]:,.<>/?-]', Operator),
            (ur'(Процедура|Функция|procedure|function)(\s+)', bygroups(Keyword, Text), 'funcname'),
            (ur'(Перем|Var|Если|If|Тогда|Then|ИначеЕсли|Elsif|Иначе|Else|КонецЕсли|Endlf|'
             ur'Цикл|Do|Для|For|По|To|Пока|While|'
             ur'He|Not|Попытка|Try|Исключение|Except|КонецПопытки|'
             ur'EndTry|ВызватьИсключение|Raise|Знач|Val|КонецЦикла|EndDo|Контекст|Context|'
             ur'ОписаниеОшибки|GetErrorDescription|Перем|Var|Перейти|Goto|Возврат|Return|Продолжить|'
             ur'Continue|Прервать|Break|И|And|Или|Or|Метаданные|MetaData)\b', Keyword.Reserved),
            #(ur'(class|класс)(\s+)', bygroups(Keyword, Text), 'class'), # классы 1С++
            (ur'(ПолучитьБазовыйКласс|GetBaseClass|НазначитьБазовыйКласс|' # Функционал классов 1С++
            ur'ОтправитьСообщениеМодулюХоз|SendMessageOwnMod|ПолучитьПуть|'
            ur'GetPathName|ПолучитьКонтекстОкружения|GetEnvContext|'
            ur'ПолучитьСписокПараметров|GetParamsList|УстановитьПараметрПоИндексу|'
            ur'SetOnIndexParams|стрИмяМетода|ЗаменитьЭксзБазовогоКласса|'
            ur'ReplaceInstBaseClasses|_ПриОткрытии|_OnOpen|_ВыброситьИскл|'
            ur'_Throw|_ПолучитьКод|_GetCode|_SQLCreate)\b', Keyword.Reserved),
            (ur'(ИндексированнаяТаблица|IndexedTable|АктивИкс|ActiveX|' #  Классы 1С++
            ur'РаботаСРегистромWin|WorkAsRegisterWin|ВыполняемыйМодуль|'
            ur'ExecuteModule|Делегат|Delegate|МенеджерСобытий|EventManager|'
            ur'Структура|Struct|DynaValue|Поток|Thread|GUID|BinaryData'
            ur'ODBCDataBase|ODBCRecordSet|MetaDataWork|SQLLock)\b', Name.Class),
            (ur'(РазделительСтраниц|PageBreak|РазделительСтрокLineBreak|'
            ur'СимволТабуляции|TabSymbol)\b', Keyword.Constant),
            (ur'(Число|Number|Строка|String|Дата|Date|Неопределенный|Undefine|void|' # типы данных
            ur'ТаблицаЗначений|ValueTable|СписокЗначений|ValueList|'
            ur'Неопределенный|Undefine|Запрос|Query|Константа|Const|'
            ur'Справочник|Reference|Перечисление|Enum|Документ Document|' 
            ur'Регистр|Register|ПланСчетов|ChartOfAccounts|Счет|Account|'
            ur'ВидСубконто|SubcontoKind|Операция|Operation|БухгалтерскиеИтоги|'
            ur'BookkeepingTotals|ЖурналРасчетов|CalcJournal|ВидРасчета|'
            ur'CalculationKind|ГруппаРасчетов|CalculationGroup|Календарь|'
            ur'Calendar|Запрос|Query|Текст|Text|Таблица|Table|СписокЗначений|'
            ur'ValueList|ТаблицаЗначений|ValueTable|Картинка|Picture|'
            ur'Периодический|Регiodic|ФС|FS|XBase|Xbase)\b', Keyword.Type),
            (ur'(Окр|Round|Цел|Int|Мин|Min|Макс|Max|Лог10|Лог|Ln|СтрДлина|StrLen' # Математические функции
            ur'ПустаяСтрока|IsBlankString|СокрЛ|TrimL|СокрП|TrimR|СокрЛП|TrimAll|' # Строковые функции
            ur'Лев|Left|Прав|Right|Сред|Mid|Найти|Find|СтрЗаменить|StrReplace|'
            ur'СтрЧислоВхождений|StrCountOccur|СтрКоличествоСтрок|StrLineCount|'
            ur'СтрПолучитьСтроку|StrGetLine|Врег|Upper|НРег|Lower|OemToAnsi|'
            ur'AnsiToOem|Симв|Chr|КодСимв|Asс|'
            ur'РабочаяДата|WorkingDate|ТекущаяДата|CurDate|ДобавитьМесяц|AddMonth|' # Функции работы с датой
            ur'НачМесяца|BegOfMonth|КонМесяца|EndOfMonth|НачКвартала|BegOfQuart|КонКвартала|'
            ur'EndOfQuart|НачГода|BegOfYear|КонГода|EndOfYear|НачНедели|BegOfWeek|КонНедели|'
            ur'EndOfWeek|ДатаГод|GetYear|ДатаМесяц|GetMonbh|ДатаЧисло|GetDay|НомерНеделиГода|'
            ur'GetWeekOfYear|НомерДняГода|GetDayOfYear|НомерДняНедели|GetDayOfWeek|ПериодСтр|'
            ur'РегiodStr|НачалоСтандартногоИнтервала|BegOfStandrdRange|КонецСтандартногоИнтервала|'
            ur'ТекущееВремя|CurrentTime|' # Функции работы с временем
            ur'СформироватьПозициюДокумента|MakeDocPosition|РазобратьПозициюДокумента|SplitDocPosition|' # Функции работы с позицией документа
            ur'Пропись|Spelling|Формат|Format|Шаблон|Template|ФиксШаблон|FixTemplate' # Процедуры и функции форматирования
            ur'ВвестиЗначение|InputValue|ВвестиЧисло|InputNumeric|ВвестиСтроку|InputString|' # Функции для вызова диалога ввода данных
            ur'ВвестиДату|InputDate|ВвестиПериод|InputРегiod|ВвестиПеречисление|InputEnum|'
            ur'Вопрос|DoQueryBox|Предупреждение|DoMessageBox|Сообщить|Message|' #Процедуры и функции общего назначения
            ur'ОчиститьОкноСообщений|ClearMessageWindow|Состояние|Status|Сигнал|Веер|Разм|Dim|'
            ur'ЗаголовокСистемы|SystemCaption|ИмяКомпьютера|ComputerName|ИмяПользователя|' # Функции среды исполнения
            ur'UserName|ПолноеИмяПользователя|UserFullName|НазваниеНабораПрав|RightName|'
            ur'ПравоДоступа|AccessRight|НазваниеИнтерфейса|UserInterfaceName|КаталогПользователя|'
            ur'UserDir|КаталогИБ|IBDir|КаталогПрограммы|BinDir|КаталогВременныхФайлов|'
            ur'TempFilesDir|МонопольныйРежим|ExclusiveMode|ОсновнойЯзык|GeneralLanguage|'
            ur'НачатьТранзакцию|BeginTransaction|ЗафиксироватьТранзакцию|CommitTransation|' # Процедуры работы с транзакциями
            ur'ОтменитьТранзакцию|RollBackTransaction|'
            ur'СоздатьОбъект|CreateObject|СтатусВозврата|ReturnStatus|ОткрытьФорму|' # Специальные процедуры и функции
            ur'OpenForm|ОткрытьФормуМодально|OpenFormModal|ТипЗначения|ValueType|ТипЗначенияСтр|'
            ur'ValueTypeStr|ПустоеЗначение|EmptyValue|ПолучитьПустоеЗначение|GetEmptyValue|'
            ur'НазначитьВид|SetKind|ЗаписьЖурналаРегистрации|LogMessageWrite|ПрефиксАвтоНумерации|'
            ur'AutoNumPrefix|ПолучитьЗначенияОтбора|GetSelectionValues|КомандаСистемы|System|'
            ur'ЗапуститьПриложение|RunApp|ЗавершитьРаботуСистемы|ExitSystem|НайтиПомеченныеНаУдаление|'
            ur'FindMarkedForDelete|НайтиСсылки|FindReferences|УдалитьОбъекты|DeleteObjects|'
            ur'ОбработкаОжидания|IdleProcessing|'
            ur'ЗначениеВСтрокуВнутр|ValueToStringInternal|ЗначениеИзСтрокиВнутр|ValueFromStringInternal|' # Процедуры и функции обработки значений
            ur'ЗначениеВСтроку|ValueToString|ЗначениеИзСтроки|ValueFromString|ЗначениеВФайл|'
            ur'ValueToFile|ЗначениеИзФайла|ValueFromFile|СохранитьЗначение|SaveValue|'
            ur'ВосстановитьЗначение|'
            ur'ПолучитьТА|GetAP|ПолучитьДатуТА|GetDateOfAP|ПолучитьВремяТА|GetTimeOfAP' # Процедуры и функции компоненты <Оперативный учет>
            ur'ПолучитьДокументТА|GetDocOfAP|ПолучитьПозициюТА|GetAPPosition|УстановитьТАна|'
            ur'SetAPToBeg|УстановитьТАпо|SetAPToEnd|'
            ur'ВыбранныйПланСчетов|DefaultChartOfAccounts|ОсновнойПланСчетов|MainChartOfAccounts|' # Процедуры и функции компоненты <Бухгалтерский учет>
            ur'СчетПоКоду|AccountByCode|НачалоПериодаБИ|BeginOfРегiodBT|КонецПериодаБИ|'
            ur'EndOfРегiodBT|КонецРассчитанногоПериодаБИ|EndOfCalculatedРегiodBT|'
            ur'НазначитьСчет|SetAccount|ВвестиПланСчетов|InputChartOfAccounts|ВвестиВидСубконто|'
            ur'InputSubcontoKind|МаксимальноеКоличествоСубконто|MaxSubcontoCount|'
            ur'ОсновнойЖурналРасчетов|BasicCalcJournal|' # Процедуры и функции компоненты <Расчет>
            ur'ПодключитьВнешнююКомпоненту|AttachAddIn|ЗагрузитьВнешнююКомпоненту|LoadAddin)\b', Keyword.Pseudo), # Внешние компоненты
            (ur'(Экспорт|Export|Далее|Forward)\b', Keyword.Declaration),
            (ur'~[a-zA-Zа-яА-Я_][a-zA-Zа-яА-Я0-9_]*:', Name.Label),
            (ur'~[a-zA-Zа-яА-Я_][a-zA-Zа-яА-Я0-9_]*', Name.Label),
            (ur'(КонецПроцедуры|EndProcedure|КонецФункции|EndFunction)\b', Keyword, '#pop'),
            (ur'[a-zA-Zа-яА-Я_][a-zA-Zа-яА-Я0-9_]*', Name),
        ],
        'root': [
            include('whitespace'),
            # classes
            (ur'(class|класс)(\s+)'                          # class keyword
             ur'([a-zA-Zа-яА-Я_][a-zA-Zа-яА-Я0-9_.]*)(\s*)'   # class name
             ur'(=)(\s*)'                                    # operator =
             ur'([^:^{^/]*)(:{0,1})(.*?)({)',                  # class path
             bygroups(Keyword, Text, Name.Class, Text, Operator, Text, String, Operator, using(this), Keyword), 'classdef'),
            # functions
            #(ur'(Процедура|Функция|procedure|function)(\s+)'
            #ur'([a-zA-Zа-яА-Я_][a-zA-Zа-яА-Я0-9_]*)'
            #ur'(\s*\([^;]*?\))',                           # signature
            #bygroups(Keyword, Text, Name.Function, using(this)), 'function'),
            ('', Text, 'statement'),
        ],
        'statement' : [
            include('whitespace'),
            include('statements'),
            (';', Text, '#pop'),
        ],
        'classdef': [
            include('whitespace'),
            (ur'([a-zA-Zа-яА-Я_][a-zA-Zа-яА-Я0-9_.]*)(\s+)' # return arguments
             ur'([a-zA-Zа-яА-Я_][a-zA-Zа-яА-Я0-9_]*)'      # method name
             ur'(\s*\([^;]*?\))'                           # signature
             #ur'(' + _ws + ur')(;)',
             ur'(;)',
             bygroups(using(this), Text, Name.Function, using(this), Text)),
            ('{', Keyword, '#push'),
            ('(}|}\s+;)', Keyword, '#pop'),
            include('statements'),
        ],
#        'function': [
#            (ur'(КонецПроцедуры|EndProcedure|КонецФункции|EndFunction)\b', Keyword, '#pop'),
#            include('whitespace'),
#            include('statements'),
#            (';', Text),
#        ],
        'funcname': [
            (ur'[a-zа-яA-ZА-Я_][a-zа-яA-ZА-Я0-9_]*', Name.Function, '#pop')
        ],
        'string': [
            (ur'"', String, '#pop'),
            (ur'\\([\\abfnrtv"\']|x[a-fA-F0-9]{2,4}|[0-7]{1,3})', String.Escape),
            (ur'[^\\"\n]+', String), # all other characters
            (ur'\\\n', String), # line continuation
            (ur'\\', String), # stray backslash
        ],
        'macro': [
            (ur'[^/\n]+', Comment.Preproc),
            (ur'/[*](.|\n)*?[*]/', Comment),
            (ur'//.*?\n', Comment, '#pop'),
            (ur'/', Comment.Preproc),
            (ur'(?<=\\)\n', Comment.Preproc),
            (ur'\n', Comment.Preproc, '#pop'),
        ]
    }
