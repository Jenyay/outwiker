��          T      �       �      �   �  �      f     o     v  %   �  a  �         9     S	     d	  3   y	  #   �	                                        (:spoiler:) Command Add (:spoiler:) wiki command to parser.

<B>Usage:</B>
<PRE>(:spoiler:)
Text
(:spoilerend:)</PRE>

For nested spoilers use (:spoiler0:), (:spoiler1:)...(:spoiler9:) commands. 

<U>Example:</U>

<PRE>(:spoiler:)
Text
&nbsp;&nbsp;&nbsp;(:spoiler1:)
&nbsp;&nbsp;&nbsp;Nested spoiler
&nbsp;&nbsp;&nbsp;(:spoiler1end:)
(:spoilerend:)</PRE>

<B>Params:</B>
<U>inline</U> - Spoiler will be in inline mode.
<U>expandtext</U> - Link text for the collapsed spoiler. Default: "Expand".
<U>collapsetext</U> - Link text for the expanded spoiler. Default: "Collapse".

<U>Example:</U>

<PRE>(:spoiler expandtext="More..." collapsetext="Less" inline :)
Text
(:spoilerend:)</PRE>
 Collapse Expand Insert (:spoiler:) wiki command https://jenyay.net/Outwiker/SpoilerEn Project-Id-Version: spoiler
Report-Msgid-Bugs-To: 
PO-Revision-Date: 2018-08-23 13:37+0300
Last-Translator: Eugeniy Ilin <jenyay.ilin@gmail.com>
Language-Team: Jenyay <jenyay.ilin@gmail.com>
Language: ru_RU
MIME-Version: 1.0
Content-Type: text/plain; charset=UTF-8
Content-Transfer-Encoding: 8bit
X-Poedit-SourceCharset: utf-8
X-Generator: Poedit 2.0.6
 Команда (:spoiler:) Добавляет викикоманду (:spoiler:) в парсер.

<B>Использование:</B>
<PRE>(:spoiler:)
Текст
(:spoilerend:)</PRE>

Для вложенных спойлеров можно использовать команды (:spoiler0:), (:spoiler1:)...(:spoiler9:). 

<U>Пример:</U>

<PRE>(:spoiler:)
Текст
&nbsp;&nbsp;&nbsp;(:spoiler1:)
&nbsp;&nbsp;&nbsp;Вложенный спойлер
&nbsp;&nbsp;&nbsp;(:spoiler1end:)
(:spoilerend:)</PRE>

<B>Параметры:</B>
<U>inline</U> - Спойлер будет помещен внутри строки.
<U>expandtext</U> - Текст ссылки для свернутого спойлера. Значение по умолчанию: "Развернуть".
<U>collapsetext</U> - Текст ссылки для развернутого спойлера. Значение по умолчанию: "Свернуть".

<U>Пример:</U>

<PRE>(:spoiler expandtext="Больше..." collapsetext="Меньше" inline :)
Текст
(:spoilerend:)</PRE>
 Свернуть Развернуть Вставить викикоманду (:spoiler:) https://jenyay.net/Outwiker/Spoiler 