autor: MolokovAlex
lisence: GPL
coding: utf-8

Программа CfgMercury - ПО сбора и отображения данных с счетчиков технического учета электроэнергии Меркурий.

Стек:
Python
PyQt
QThread
Pyqtgraph
sqlite3
numpy
serial

06032013
- убрал считывание коэффициентов kI  и kU из счетчиков
- сделал поля коэффициентов kI  и kU редактируемыми
- сделал модуль Update

05032023
- пересмотрел все сообщения в консоль и лог-файл и поменял у некоторых статус с info на  debug

04032023
- продолжил наводить порядок с понятиями ИТОГО за день, месяц, период
- убрал верхюю таблицу имитации двухуровневой шапки - сделал выше шапку и раскраска background

03032023
- в иксель профиля мощности числа сохраняются как числа, а не строки
- отключение записи в БД коэффициентов kU, kI, т.к. в самих счетчиках они могут быть неверными
- одиночная запись в БД кофф KU kI. todo: отключить эти сроки на последющем update
- величины полученные из счетчика по профилю умножаются на KU и KI (значение * KU* KI)
- мгновенные значения тока умножаются на KI
- мгновенные значения мощностей на KU и KI
- навел порядок с понятиями ИТОГО за день, месяц, период + небольшой рефакторинг

01032023
рефакторинг
- убрал из дерева мгновенных параметров возможность установить "групповую" галочку
- устранил ошибку на тестовых данных в функции korrekt_dataDB

26022023_1420
рефакторинг

26022023_1300
рефакторинг

25022023_1800
рефакторинг

25022023_1530
функция корректировки данных профиля мощности  полученных из БД - добавление пустых пропущенных/напринятых профилей 30-минуток
а так же защита от дубликатов записей (с одинаковыми datetime). В конечном массиве остается первый дубликат

25022023_1212
сделал дополнение к тестовым виртуальным счетчикам, чтобы проверить алгритм подстчета и отображния ИТОГО в профиле мощности
скорректировал на базе этого алгоритм вставки строк итого

25022023_025
исправил дату = текущей даты в мгновенных парамерах
исправил даты в календарях профиля мощности

24022023_2324
Изменил модель временной оси на графиках мгновенных значений


Руководство оператора
по 
программному обеспечению
программу пока можно запускать и под Windows и под Linux
---------------------------------------------------------------------------------------
-------------------------------- Структура  программы
---------------------------------------------------------------------------------------
(Визуальное отображение UX/frontend) <---> БД <---> (обмен данных со счетчиками backend)
Три части:
1.Визуальное отображение - то что видите на экране. При заполнение визуальных таблиц данные _всегда_ 
беруться из БД
2.БД пока локальная. Предварительный подсчет объема на БД глубиной 1 год - около 100 Мб.
3.Обмен данных со счетчиками - паралельный поток основной программе (паралельно выполняющаяся программа без 
визуального обображения). Работает в фоне. Смотриит какие данные _на текущий момент_ отсуствуют в БД - и 
потихоньку (на скорости 9600) вытаскивает их из счетчиков. В том числе мгновенные значения.
Такое деление на части обусловлено разными скоростями работы по взаимодействию с БД: визуальный интерфейс на очень 
высокой скорости получает данные из БД. Счетчики относительно визуалки гораздо медленнее складывают свои данные
в БД.
---------------------------------------------------------------------------------------
--------------------------------- База данных
---------------------------------------------------------------------------------------
Вид БД
Используется БД SQLite 3
В виду достаточной распространенности и входжению в состав интерпретатора Python по-умолчанию
Заполнение базовой информацией и тестовыми данными
Алгоритм программы такой: при запуске она смотрит есть ли в папке DB файлы БД. Если нет - создает новый чистый файл БД с соответвующими таблицами.
При этом размер пустого файла около 32кб
Потом заполняет таблицы БД значениями базовой информации - названия групп, названия счетчиков, распределение счетчиков по группам (в соответвии с ТЗ).
Потом из папки Test_data загружает в БД данные из файлов test_data_ic.json и test_data_pp.json. 
Это данные по "виртуальный счетчик 254" и "виртуальный счетчик 255" - для оценки работы визуального интерфейса. 
Это случайные значения мгновенных параметров и профилей мощностей с 01.12.2022 по 30.06.2023. Размерность тестовых цифр - пока не важна одключиться при backend-е.
Их сетевые номера 254 и 255 соответственно.
Глубина хранения и размер
По результатам тестовых данных полу-годовые данные на 1 счетчик (параметры счетчика, профиль мощности с интегрированием 30 мин, 
мгновенные значения с интервалом 3 мин) будут занимать в файле БД около 12Мб. Соответвенно с глубиной 1 год = 24Мб.
---------------------------------------------------------------------------------------
--------------------------------- Описание пунктов Меню
---------------------------------------------------------------------------------------
Меню Настройки - предусмотрено три варианта подключения к счетчикам:
- при помощи преобразователя USB-СОМ-RS485
- при помощи преобразователя Ethernet-RS485.  Преобразователь в режиме Сервера.
- при помощи преобразователя Ethernet-RS485.  Преобразователь в режиме Клиента.
Меню Счетчики - параметры и установки: просмотр индивидуальных параметров счетчика
Меню Счетчики - Параметры. Просмотр основных параметров счетчика.
у счетчиков те, которые были недавно внесены пользователем, будет
отсуствовать дата выпуска и некоторые другие параметры (их запрещено вводить при вводе нового счетчика)
но если связь со счетчиком была проведена - то из него этот параметр/параметры будут считаны и изменены в БД 
 Меню Счетчики - Редактирование групп, счетчиков. Создание, исправление, удаление групп. Создание, 
исправление, удаление счетчиков. А так же виртуальное их перемещение в группы. При вводе нового счетчика или 
исправлении уже существующего доступны ограниченное количество полей - остальные поля программа сама возьмет со счетчика при сеансе связи.
Меню профиль мощности
Меню Мгновенные значения
По правой клавише мыши на графике мгоновенных значений - дополнительные средства визуализации.
К программе подключен модуль логгирования - поможет с проблемами при запусках и решении проблем.
В папке Log создается непрерывный лог-файл(VMlog.log) с debug сообщениями программы.
Если его удалить - он создасться заново при пуске программы

Так же информационные сообщения выводяться в консоль интерпретатора Python (но не все а особо важные)









