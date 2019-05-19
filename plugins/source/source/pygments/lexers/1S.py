# -*- coding: utf-8 -*-
"""
    pygments.lexers.1S
    ~~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for language: 1S.

    :license: GNU LGPL, see LICENSE for more details.
"""

import re

from pygments.lexer import RegexLexer, include, bygroups, using, this
from pygments.token import \
    Text, Comment, Operator, Keyword, Name, String, Number, Literal


__all__ = ['OneSLexer']


class OneSLexer(RegexLexer):

    name = '1S'
    aliases = ['1s', '1c']
    filenames = ['*.1s', '*.prm', '*.1cpp']
    mimetypes = ['text/x-1s']

    #: optional Comment or Whitespace
    _ws = r'(?:\s|//.*?\n|/[*].*?[*]/)+'

    flags = re.IGNORECASE | re.MULTILINE | re.DOTALL | re.UNICODE
    tokens = {
        'whitespace': [
            (r'^\s*#', Comment.Preproc, 'macro'),
            (r'^\s*//#.*?\n', Comment.Preproc),
            (r'\n', Text),
            (r'\s+', Text),
            (r'\\\n', Text),  # line continuation
            (r'//.*?\n', Comment),
        ],
        'statements': [
            (r'L?"', String, 'string'),
            (r'(\s)*?\|', String, 'string'),
            (r'(0x[0-9a-fA-F]|0[0-7]+|(\d+\.\d*|\.\d+)|\d+)'
             r'e[+-]\d+[lL]?', Number.Float),
            (r'0x[0-9a-fA-F]+[Ll]?', Number.Hex),
            (r'0[0-7]+[Ll]?', Number.Oct),
            (r'(\d+\.\d*|\.\d+)', Number.Float),
            (r'\d+', Number.Integer),
            (r'\'[0-3][0-9]\.[0-1][0-9]\.([0-9][0-9]|[0-9][0-9][0-9][0-9])\'', Literal.Date),
            (r'[!%^&*()+=|\[\]:,.<>/?-]', Operator),
            (r'(Процедура|Функция|procedure|function)(\s+)',
             bygroups(Keyword, Text), 'funcname'),
            (r'(Перем|Var|Если|If|Тогда|Then|ИначеЕсли|Elsif|Иначе|Else|КонецЕсли|Endlf|'
             r'Цикл|Do|Для|For|По|To|Пока|While|'
             r'He|Not|Попытка|Try|Исключение|Except|КонецПопытки|'
             r'EndTry|ВызватьИсключение|Raise|Знач|Val|КонецЦикла|EndDo|Контекст|Context|'
             r'ОписаниеОшибки|GetErrorDescription|Перем|Var|Перейти|Goto|Возврат|Return|Продолжить|'
             r'Continue|Прервать|Break|И|And|Или|Or|Метаданные|MetaData)\b', Keyword.Reserved),
            # (r'(class|класс)(\s+)', bygroups(Keyword, Text), 'class'),  # классы 1С++
            (r'(ПолучитьБазовыйКласс|GetBaseClass|НазначитьБазовыйКласс|'  # Функционал классов 1С++
             r'ОтправитьСообщениеМодулюХоз|SendMessageOwnMod|ПолучитьПуть|'
             r'GetPathName|ПолучитьКонтекстОкружения|GetEnvContext|'
             r'ПолучитьСписокПараметров|GetParamsList|УстановитьПараметрПоИндексу|'
             r'SetOnIndexParams|стрИмяМетода|ЗаменитьЭксзБазовогоКласса|'
             r'ReplaceInstBaseClasses|_ПриОткрытии|_OnOpen|_ВыброситьИскл|'
             r'_Throw|_ПолучитьКод|_GetCode|_SQLCreate)\b', Keyword.Reserved),
            (r'(ИндексированнаяТаблица|IndexedTable|АктивИкс|ActiveX|'  # Классы 1С++
             r'РаботаСРегистромWin|WorkAsRegisterWin|ВыполняемыйМодуль|'
             r'ExecuteModule|Делегат|Delegate|МенеджерСобытий|EventManager|'
             r'Структура|Struct|DynaValue|Поток|Thread|GUID|BinaryData'
             r'ODBCDataBase|ODBCRecordSet|MetaDataWork|SQLLock)\b', Name.Class),
            (r'(РазделительСтраниц|PageBreak|РазделительСтрокLineBreak|'
             r'СимволТабуляции|TabSymbol)\b', Keyword.Constant),
            (r'(Число|Number|Строка|String|Дата|Date|Неопределенный|Undefine|void|'  # типы данных
             r'ТаблицаЗначений|ValueTable|СписокЗначений|ValueList|'
             r'Неопределенный|Undefine|Запрос|Query|Константа|Const|'
             r'Справочник|Reference|Перечисление|Enum|Документ Document|'
             r'Регистр|Register|ПланСчетов|ChartOfAccounts|Счет|Account|'
             r'ВидСубконто|SubcontoKind|Операция|Operation|БухгалтерскиеИтоги|'
             r'BookkeepingTotals|ЖурналРасчетов|CalcJournal|ВидРасчета|'
             r'CalculationKind|ГруппаРасчетов|CalculationGroup|Календарь|'
             r'Calendar|Запрос|Query|Текст|Text|Таблица|Table|СписокЗначений|'
             r'ValueList|ТаблицаЗначений|ValueTable|Картинка|Picture|'
             r'Периодический|Регiodic|ФС|FS|XBase|Xbase)\b', Keyword.Type),
            (r'(Окр|Round|Цел|Int|Мин|Min|Макс|Max|Лог10|Лог|Ln|СтрДлина|StrLen'  # Математические функции
             r'ПустаяСтрока|IsBlankString|СокрЛ|TrimL|СокрП|TrimR|СокрЛП|TrimAll|'  # Строковые функции
             r'Лев|Left|Прав|Right|Сред|Mid|Найти|Find|СтрЗаменить|StrReplace|'
             r'СтрЧислоВхождений|StrCountOccur|СтрКоличествоСтрок|StrLineCount|'
             r'СтрПолучитьСтроку|StrGetLine|Врег|Upper|НРег|Lower|OemToAnsi|'
             r'AnsiToOem|Симв|Chr|КодСимв|Asс|'
             # Функции работы с датой
             r'РабочаяДата|WorkingDate|ТекущаяДата|CurDate|ДобавитьМесяц|AddMonth|'
             r'НачМесяца|BegOfMonth|КонМесяца|EndOfMonth|НачКвартала|BegOfQuart|КонКвартала|'
             r'EndOfQuart|НачГода|BegOfYear|КонГода|EndOfYear|НачНедели|BegOfWeek|КонНедели|'
             r'EndOfWeek|ДатаГод|GetYear|ДатаМесяц|GetMonbh|ДатаЧисло|GetDay|НомерНеделиГода|'
             r'GetWeekOfYear|НомерДняГода|GetDayOfYear|НомерДняНедели|GetDayOfWeek|ПериодСтр|'
             r'РегiodStr|НачалоСтандартногоИнтервала|BegOfStandrdRange|КонецСтандартногоИнтервала|'
             r'ТекущееВремя|CurrentTime|'  # Функции работы с временем
             # Функции работы с позицией документа
             r'СформироватьПозициюДокумента|MakeDocPosition|РазобратьПозициюДокумента|SplitDocPosition|'
             # Процедуры и функции форматирования
             r'Пропись|Spelling|Формат|Format|Шаблон|Template|ФиксШаблон|FixTemplate'
             # Функции для вызова диалога ввода данных
             r'ВвестиЗначение|InputValue|ВвестиЧисло|InputNumeric|ВвестиСтроку|InputString|'
             r'ВвестиДату|InputDate|ВвестиПериод|InputРегiod|ВвестиПеречисление|InputEnum|'
             # Процедуры и функции общего назначения
             r'Вопрос|DoQueryBox|Предупреждение|DoMessageBox|Сообщить|Message|'
             r'ОчиститьОкноСообщений|ClearMessageWindow|Состояние|Status|Сигнал|Веер|Разм|Dim|'
             # Функции среды исполнения
             r'ЗаголовокСистемы|SystemCaption|ИмяКомпьютера|ComputerName|ИмяПользователя|'
             r'UserName|ПолноеИмяПользователя|UserFullName|НазваниеНабораПрав|RightName|'
             r'ПравоДоступа|AccessRight|НазваниеИнтерфейса|UserInterfaceName|КаталогПользователя|'
             r'UserDir|КаталогИБ|IBDir|КаталогПрограммы|BinDir|КаталогВременныхФайлов|'
             r'TempFilesDir|МонопольныйРежим|ExclusiveMode|ОсновнойЯзык|GeneralLanguage|'
             # Процедуры работы с транзакциями
             r'НачатьТранзакцию|BeginTransaction|ЗафиксироватьТранзакцию|CommitTransation|'
             r'ОтменитьТранзакцию|RollBackTransaction|'
             # Специальные процедуры и функции
             r'СоздатьОбъект|CreateObject|СтатусВозврата|ReturnStatus|ОткрытьФорму|'
             r'OpenForm|ОткрытьФормуМодально|OpenFormModal|ТипЗначения|ValueType|ТипЗначенияСтр|'
             r'ValueTypeStr|ПустоеЗначение|EmptyValue|ПолучитьПустоеЗначение|GetEmptyValue|'
             r'НазначитьВид|SetKind|ЗаписьЖурналаРегистрации|LogMessageWrite|ПрефиксАвтоНумерации|'
             r'AutoNumPrefix|ПолучитьЗначенияОтбора|GetSelectionValues|КомандаСистемы|System|'
             r'ЗапуститьПриложение|RunApp|ЗавершитьРаботуСистемы|ExitSystem|НайтиПомеченныеНаУдаление|'
             r'FindMarkedForDelete|НайтиСсылки|FindReferences|УдалитьОбъекты|DeleteObjects|'
             r'ОбработкаОжидания|IdleProcessing|'
             # Процедуры и функции обработки значений
             r'ЗначениеВСтрокуВнутр|ValueToStringInternal|ЗначениеИзСтрокиВнутр|ValueFromStringInternal|'
             r'ЗначениеВСтроку|ValueToString|ЗначениеИзСтроки|ValueFromString|ЗначениеВФайл|'
             r'ValueToFile|ЗначениеИзФайла|ValueFromFile|СохранитьЗначение|SaveValue|'
             r'ВосстановитьЗначение|'
             # Процедуры и функции компоненты <Оперативный учет>
             r'ПолучитьТА|GetAP|ПолучитьДатуТА|GetDateOfAP|ПолучитьВремяТА|GetTimeOfAP'
             r'ПолучитьДокументТА|GetDocOfAP|ПолучитьПозициюТА|GetAPPosition|УстановитьТАна|'
             r'SetAPToBeg|УстановитьТАпо|SetAPToEnd|'
             # Процедуры и функции компоненты <Бухгалтерский учет>
             r'ВыбранныйПланСчетов|DefaultChartOfAccounts|ОсновнойПланСчетов|MainChartOfAccounts|'
             r'СчетПоКоду|AccountByCode|НачалоПериодаБИ|BeginOfРегiodBT|КонецПериодаБИ|'
             r'EndOfРегiodBT|КонецРассчитанногоПериодаБИ|EndOfCalculatedРегiodBT|'
             r'НазначитьСчет|SetAccount|ВвестиПланСчетов|InputChartOfAccounts|ВвестиВидСубконто|'
             r'InputSubcontoKind|МаксимальноеКоличествоСубконто|MaxSubcontoCount|'
             # Процедуры и функции компоненты <Расчет>
             r'ОсновнойЖурналРасчетов|BasicCalcJournal|'
             r'ПодключитьВнешнююКомпоненту|AttachAddIn|ЗагрузитьВнешнююКомпоненту|LoadAddin)\b', Keyword.Pseudo),  # Внешние компоненты
            (r'(Экспорт|Export|Далее|Forward)\b', Keyword.Declaration),
            (r'~[a-zA-Zа-яА-Я_][a-zA-Zа-яА-Я0-9_]*:', Name.Label),
            (r'~[a-zA-Zа-яА-Я_][a-zA-Zа-яА-Я0-9_]*', Name.Label),
            (r'(КонецПроцедуры|EndProcedure|КонецФункции|EndFunction)\b', Keyword, '#pop'),
            (r'[a-zA-Zа-яА-Я_][a-zA-Zа-яА-Я0-9_]*', Name),
        ],
        'root': [
            include('whitespace'),
            # classes
            (r'(class|класс)(\s+)'                          # class keyword
             r'([a-zA-Zа-яА-Я_][a-zA-Zа-яА-Я0-9_.]*)(\s*)'   # class name
             r'(=)(\s*)'                                    # operator =
             r'([^:^{^/]*)(:{0,1})(.*?)({)',                  # class path
             bygroups(Keyword, Text, Name.Class, Text, Operator, Text, String, Operator, using(this), Keyword), 'classdef'),
            # functions
            # (r'(Процедура|Функция|procedure|function)(\s+)'
            # r'([a-zA-Zа-яА-Я_][a-zA-Zа-яА-Я0-9_]*)'
            # r'(\s*\([^;]*?\))',                           # signature
            # bygroups(Keyword, Text, Name.Function, using(this)), 'function'),
            ('', Text, 'statement'),
        ],
        'statement': [
            include('whitespace'),
            include('statements'),
            (';', Text, '#pop'),
        ],
        'classdef': [
            include('whitespace'),
            (r'([a-zA-Zа-яА-Я_][a-zA-Zа-яА-Я0-9_.]*)(\s+)'  # return arguments
             r'([a-zA-Zа-яА-Я_][a-zA-Zа-яА-Я0-9_]*)'      # method name
             r'(\s*\([^;]*?\))'                           # signature
             #r'(' + _ws + r')(;)',
             r'(;)',
             bygroups(using(this), Text, Name.Function, using(this), Text)),
            ('{', Keyword, '#push'),
            ('(}|}\s+;)', Keyword, '#pop'),
            include('statements'),
        ],
        #        'function': [
        #            (r'(КонецПроцедуры|EndProcedure|КонецФункции|EndFunction)\b', Keyword, '#pop'),
        #            include('whitespace'),
        #            include('statements'),
        #            (';', Text),
        #        ],
        'funcname': [
            (r'[a-zа-яA-ZА-Я_][a-zа-яA-ZА-Я0-9_]*', Name.Function, '#pop')
        ],
        'string': [
            (r'"', String, '#pop'),
            (r'\\([\\abfnrtv"\']|x[a-fA-F0-9]{2,4}|[0-7]{1,3})',
             String.Escape),
            (r'[^\\"\n]+', String),  # all other characters
            (r'\\\n', String),  # line continuation
            (r'\\', String),  # stray backslash
        ],
        'macro': [
            (r'[^/\n]+', Comment.Preproc),
            (r'/[*](.|\n)*?[*]/', Comment),
            (r'//.*?\n', Comment, '#pop'),
            (r'/', Comment.Preproc),
            (r'(?<=\\)\n', Comment.Preproc),
            (r'\n', Comment.Preproc, '#pop'),
        ]
    }
