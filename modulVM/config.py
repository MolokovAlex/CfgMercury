# config
# autor: MolokovAlex
# coding: utf-8

# модуль держатель конфигурацонных переменных

import os
from pathlib import Path
# import datetime

# ------------------------------------------------------------------
# --------------- константы всей программы --------------------------
# ------------------------------------------------------------------

#  версия программы
VERSION = '1.010323'

# коды ошибок из потока связи со счетчиками
# 0 = None error
# 1 = No open port
codeMessageFromThread = 0

# global handler SQL Database
sql_base_conn = None

# global handler SerialPort from class CommunicationCounterThread
handlerSerialPortConn = None

# global handler Socket
handlerSocketConn = None

# список выбранных счетчиков и групп в дереве
lst_checked_single_counter =[]
lst_checked_group = []
lst_checked_counter_in_group=[]

# флаг для остановки потока опроса счетчиков
stop_CommunicationCounterThread = False

# lst_progress_work = []

# window = None
# lock = None
running_thread1 = False
thread_handler = None
# глубина вытаскивания данных = 10 суток
length_put_date  = 10
# значения периода интегрирования в окне профиля мощности
VALUE_PERIOD_INTEGR_POFIL = ["30 мин","час", "день", "месяц"]

# список счетчиков, которые есть в БД, но не отвечают
lst_online_Counter =[]

# набор цветов дл содания линий графиков (набор в соответствии с библиотекой pyqtgraph)
lst_color_pen_graph = ['r', 'g', 'b', 'c',   'm', 'y', 'k', 'w',  'r', 'g', 'b', 'c',   'm', 'y', 'k', 'w', 'r', 'g', 'b', 'c',   'm', 'y', 'k', 'w']

#

# --------------------------------------------------------------
# ------ конфигурация параметров профиля мощности --------------
# --------------------------------------------------------------

lst_header_table = ['год', 'мес', 'день', 'час', 'мин' ]

# --------------------------------------------------------------
# ------ конфигурация мгновенных параметров --------------------
# --------------------------------------------------------------
# список Мгновенных параметров окна Мгновенные значения
# lst_InstanlyParam=["Ток по фазам", "Мощность P", "Мощность Q", "Мощность S", "Коэффициент мощности", "Зафиксированная энергия"]

# шаг на оси времени мгновенных параметров (в минутах)
stepTimeInGraph = 3

# глубина выборки мгновенных параметров из БД и вывода их на график (в часах)
# т.е. от текущей даты NOW назад в прошлое на эту глубину
# depthViewTimeBack = 100 не надо использовать

QueueRequestInDB = None

# ------------------------------------------------------------------------
# --------------- переменные БД SQLite программы --------------------------
# -------------------------------------------------------------------------


DB_FILE = 'ViewMercuryDB.sqlite'
DB_BACKUP_FILE = 'ViewMercuryDB_backup.sqlite'
LOG_FILE = 'VMlog.log'
TEST_DATA_PP_FILE = 'test_data_pp.json'
TEST_DATA_IC_FILE = 'test_data_ic.json'

# Demo_DB_FILE = 'ViewMercuryDB_demo.sqlite'
# Demo_DB_BACKUP_FILE = 'ViewMercuryDB_demo_backup.sqlite'

LOG_DIR = 'Log'
DB_DIR = 'DB'
TEST_DIR = 'Test_data'
    # основная папка запуска .py скрипта
BASE_DIR = Path(__file__).resolve().parent.parent

# абсолютный путь к DB_DIR
absDB_DIR= os.path.join(BASE_DIR, DB_DIR)
absDB_FILE= os.path.join(absDB_DIR, DB_FILE)
absDB_BACKUP_FILE= os.path.join(absDB_DIR, DB_BACKUP_FILE)
absLOG_DIR= os.path.join(BASE_DIR, LOG_DIR)
absLOG_FILE= os.path.join(absLOG_DIR, LOG_FILE)
absTEST_DIR= os.path.join(BASE_DIR, TEST_DIR)
absTEST_DATA_PP_FILE= os.path.join(absTEST_DIR, TEST_DATA_PP_FILE)
absTEST_DATA_IC_FILE= os.path.join(absTEST_DIR, TEST_DATA_IC_FILE)
# absDemoDB_DIR= os.path.join(BASE_DIR, DB_DIR)
# absDemoDB_FILE= os.path.join(absDB_DIR, Demo_DB_FILE)
# absDemoDB_BACKUP_FILE= os.path.join(absDB_DIR, Demo_DB_BACKUP_FILE)

#полный путь (abspath) c наименование файла резерной БД и полный путь (abspath) c наименование файла БД

# file_DBSql = os.path.abspath('DB\ViewMercuryDB.db')
# file_backup_DBSql =  os.path.abspath('DB\ViewMercuryDB_backup.db')



# --------------------------------------------------------------
# ------ настройки соединения связи со счетчиками---------------
# --------------------------------------------------------------
# общие настройки протокола с счетчиками
port_COM = 'Нет доступных портов'
baudrateRS485 = "9600"      # по default счетчики Меркурий имеют 9600-8N1
parityRS485 = "8N1"         # 
timeOutSerial = 0.5     # тайм-аут ожидания ответа от счетчика (по таблице не менее 150мс*N, стр.7 руководства по командам)

host_IP = '192.168.0.7'
port_IP = '20108' 

# переключатели режимов связи со счетчиками
# (должен быть выбран один из трех вариантов)
# 0x00  связь через преобразователь Ethernet-RS485, где преобразователь работает как Server
MODE_CONNECTION_IP_TO_SERVER = 0x00
# 0x01  связь через преобразователь Ethernet-RS485, где преобразователь работает как Client
MODE_CONNECTION_IP_TO_CLIENT = 0x01
# 0x02  связь через преобразователь COM-RS485
MODE_CONNECTION_COM = 0x02
MODE_CONNECT = MODE_CONNECTION_COM

#  включение режима опроса счетчиков (запуск  паралельного потока)
ON_TRANSFER_DATA_COUNTER = False

# modeIPtoServer = True   

# modeIPtoClient = False  

# modeConnectionCOM = False   

# ----------------------------------------------------------------------------
# --------------- БД групп счетчиков DBGroupCounter --------------------------
# ----------------------------------------------------------------------------
lst_name_poles_DBG = ['id', 'name_group_full'] 
sql_create_table_DBG = """ CREATE TABLE IF NOT EXISTS DBG (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name_group_full TEXT
        );
        """
data_list_demo_DBG = [
        (1,'Линия производства ГВВС'),     
        (2,'Линия производства Г5Б2'),        
        (3,'Линия производства Г5Б3'),            
        (4,'Производство Европлит'),
        (5,'Клмпрессоры 1-5 производство сжатого воздуха ГП'),
        (6,'Линия подготовки от склада камня до грохота'),
        (7,'Производство ПГП'),
        (8,'Производство сухих строительных смесей'),
        (9,'Склад готовой продукции'),
        (10,'АБК'),
        (11,'ОТК'),
        (12,'Мех. энергоцех'),
        (13,'Производство "1000 мелочей"'),
        (14,'БАМ участок выгрузки камня'),
        (15,'Резерв'),
        (16,'Ввод 1 от БТЭЦ'),
        (17,'Ввод 2 от ГПП АВИС')
        ]

# ----------------------------------------------------------------------------
# --------------- БД счетчиков --------------------------
# ----------------------------------------------------------------------------
lst_name_poles_DBC = ['id', 'schem', 'name_counter_full', 'net_adress', 'manuf_number', 'manuf_data', 'klass_react', 'klass_act', 'nom_u', 'ku', 'ki', 'koefA', 'comment']
lst_readOnly_poles_DBC = [True, False, False, False, True, True, True, True, True, True, True, True, False]
lst_rusname_poles_DBC =  ['id', 'Обозн на схеме', 'Имя счетчика полное', 'Сетевой адрес', 'Зав.номер', 'Дата изготовл.', 'Класс реакт.', 'Класс акт.', 'Номинальное напряжение', 'Коэфф.трансф. по напряжению', 'Коэфф.трансф. по току', 'Постоянная счетчика', 'Комментарии']
dic_template_DBC = {
        'id': 500,
        'schem': "",
        'name_counter_full': "", 
        'net_adress': "",
        'manuf_number': "",
        'manuf_data': "",
        'klass_react': "",
        'klass_act': "",
        'nom_u': "",
        'ku': "",
        'ki': "",
        'koefA': 0,
        'comment': ""
}
sql_create_table_DBC = """ CREATE TABLE IF NOT EXISTS DBC (
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        schem TEXT,
        name_counter_full TEXT, 
        net_adress TEXT,
        manuf_number TEXT,
        manuf_data TEXT,
        klass_react TEXT,
        klass_act TEXT,
        nom_u INTEGER,
        nom_i INTEGER,
        ku TEXT,    
        ki TEXT,
        koefA INTEGER,
        comment TEXT
        );
        """
data_list_demo_DBC = [
        ("A21", 'РП 21 - Сушильный барабан №3',                         '63',   '',     '',     '',     '',     '',     '',     '1',    '60' ,  '',     '',),
        ("A2", 'Дымосос на сепаратор и ФРИ-360',                        '60',   '',     '',     '',     '',     '',     '',     '1',    '60' ,  '',     '',),
        ("A3", 'РП 23 - Электрощитовая помольного отделения',           '89',   '',     '',     '',     '',     '',     '',     '1',    '60' ,  '',     '',),
        ("A4", 'Шаровая мельница №2',                                   '97',   '',     '',     '',     '',     '',     '',     '1',    '60' ,  '',     '',),
        ("A5", 'Шаровая мельница №1',                                   '134',  '',     '',     '',     '',     '',     '',     '1',    '60',   '',     '',),
        ("A5", 'Шаровая мельница №3',                                   '40',   '',     '',     '',     '',     '',     '',     '1',    '60' ,  '',     '',),
        ("A5", 'линия строительного гипса',                             '149',  '',     '',     '',     '',     '',     '',     '1',    '60',   '',     '',),
        ("A5", 'Шахтная мельница',                                      '22',   '',     '',     '',     '',     '',     '',     '1',    '60' ,  '',     '',),
        ("A5", 'ФРЗВ',                                                  '190',  '',     '',     '',     '',     '',     '',     '1',    '60',   '',     '',),
        ("A5", 'Строительная сепарированная РП2',                       '81',   '',     '',     '',     '',     '',     '',     '1',    '60',   '',     '',),
        ("A5", 'РП 18 - Дымосос сепарированной линии',                  '1',    '',     '',     '',     '',     '',     '',     '1',    '60',   '',     '',),
        ("A5", 'Дисмембратор',                                          '18',   '',     '',     '',     '',     '',     '',     '1',    '60',   '',     '',),
        ("A5", 'Европлиты упаковка',                                    '79',   '',     '',     '',     '',     '',     '',     '1',    '60',   '',     '',),
        ("A5", 'Европлиты формовка РП4',                                '146',  '',     '',     '',     '',     '',     '',     '1',    '60',   '',     '',),
        ("A5", 'Выбросная вентиляция компрессорной',                    '37',   '',     '',     '',     '',     '',     '',     '1',    '60',   '',     '',),
        ("A5", 'Приточная вентиляция компрессорной',                    '57',   '',     '',     '',     '',     '',     '',     '1',    '60',   '',     '',),
        ("A5", 'Компрессора 1-5, Осушители 1-5',                        '223',  '',     '',     '',     '',     '',     '',     '1',    '60',   '',     '',),
        ("A5", 'РП 8 - Дробилка',                                       '78',   '',     '',     '',     '',     '',     '',     '1',    '60',   '',     '',),
        ("A5", 'Склад камня, лебедка 1 и 2',                            '90',   '',     '',     '',     '',     '',     '',     '1',    '60',   '',     '',),
        ("A5", 'РП 17 - Склад камня, гараж',                            '16',   '',     '',     '',     '',     '',     '',     '1',    '60',   '',     '',),
        ("A5", 'РП 19 - грохот, весовая, питатели строительной линии',  '75',   '',     '',     '',     '',     '',     '',     '1',    '60',   '',     '',),
        ("A5", 'Сушильная камера ПГП',                                  '236',  '',     '',     '',     '',     '',     '',     '1',    '60',   '',     '',),
        ("A5", 'ПГП Сушила',                                            '145',  '',     '',     '',     '',     '',     '',     '1',    '60',   '',     '',),
        ("A5", 'Цех ПГП - старые установки',                            '3',    '',     '',     '',     '',     '',     '',     '1',    '60',   '',     '',),
        ("A5", '3Щ-ПССС "Затарка"',                                     '12',   '',     '',     '',     '',     '',     '',     '1',    '60',   '',     '',),
        ("A5", 'ЩХС-ПССС "Компрессорная"',                              '194',  '',     '',     '',     '',     '',     '',     '1',    '60',   '',     '',),
        ("A5", '2Щ- ПССС "Компрессорная"',                              '127',  '',     '',     '',     '',     '',     '',     '1',    '60',   '',     '',),
        ("A5", 'ПССС "Затарка"',                                        '94',   '',     '',     '',     '',     '',     '',     '1',    '60',   '',     '',),
        ("A5", '1Щ - ПССС "Операторная"',                               '234',  '',     '',     '',     '',     '',     '',     '1',    '60',   '',     '',),
        ("A5", 'Стр.Техн. Банки, здание логистики, Кран-балка',         '17',   '',     '',     '',     '',     '',     '',     '1',    '60',   '',     '',),
        ("A5", 'АБК',                                                   '23',   '',     '',     '',     '',     '',     '',     '1',    '60',   '',     '',),
        ("A5", 'ОТК',                                                   '8',    '',     '',     '',     '',     '',     '',     '1',    '60',   '',     '',),
        ("A5", 'Резерв',                                                '74',   '',     '',     '',     '',     '',     '',     '1',    '60',   '',     '',),
        ("A5", 'воздуходувка охлаждения ячеек РУ-04 Компрессорная',     '62',   '',     '',     '',     '',     '',     '',     '1',    '60',   '',     '',),
        ("A5", 'РП 16 - Мех. цех',                                      '46',   '',     '',     '',     '',     '',     '',     '1',    '60',   '',     '',),
        ("A5", '1000 Мелочей',                                          '99',   '',     '',     '',     '',     '',     '',     '1',    '60',   '',     '',),
        ("A5", 'РП 14 тяговая лебедка №3, склад камня',                 '96',   '',     '',     '',     '',     '',     '',     '1',    '60',   '',     '',),
        ("A5", 'резерв QF1',                                            '28',   '',     '',     '',     '',     '',     '',     '1',    '60',   '',     '',),
        ("A5", 'резрв QF53',                                            '95',   '',     '',     '',     '',     '',     '',     '1',    '60',   '',     '',),
        ("A5", ' резерв QF6',                                           '135',  '',     '',     '',     '',     '',     '',     '1',    '60',   '',     '',),
        ("A5", 'Резерв РП 7 QF7',                                       '34',   '',     '',     '',     '',     '',     '',     '1',    '60',   '',     '',),
        ("A5", 'Ввод №1 от БТЭЦ',                                       '245',  '',     '',     '',     '',     '',     '',     '1',    '60',   '',     '',),
        ("A5", 'Ввод №2 от ГПП АВИС',                                   '71',   '',     '',     '',     '',     '',     '',     '1',    '60',   '',     '',),
        ("A6", 'Тестовый счетчик #77',                                  '77',   '',     '',     '',     '',     '',     '',     '1',    '60',   '',     '',),
        ("A6", 'Тестовый счетчик #135 переимен в 136',                  '136',  '',     '',     '',     '',     '',     '',     '1',    '60',   '',     '',),
        ("A6", 'Виртуальный счетчик #255',                              '255',  '',     '',     '',     '',     '',     '',     '1',    '60',   '',     '',),
        ("A6", 'Виртуальный счетчик #254',                              '254',  '',     '',     '',     '',     '',     '',     '1',    '60',   '',     '',)
    ]

# ----------------------------------------------------------------------------
# ------- промежуточная таблица сетчик-группа для реализации many-to-many ----
# ----------------------------------------------------------------------------
lst_name_poles_DBGC = ['id', 'id_group', 'id_counter'] 
sql_create_table_DBGC = """ CREATE TABLE IF NOT EXISTS DBGC (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_group INTEGER NOT NULL,
        id_counter INTEGER NOT NULL,
        FOREIGN KEY (id_group)  REFERENCES DBG (id) ON DELETE RESTRICT,
        FOREIGN KEY (id_counter)  REFERENCES DBC (id) ON DELETE RESTRICT   
        );
        """
# (id_group, id_counter) 
data_list_demo_DBGC = [
        (1, 1),     #id=1
        (1, 2),     #id=2
        (1, 3),     #id=3
        (1, 4),     #id=4
        (1, 5),     #id=5
        (1, 6),     #id=5
        
        (2, 7),     #id=6
        (2, 8),     #id=7
        (2, 9),     #id=8
        
        (3, 10),     #id=9
        (3, 11),     #id=10
        (3, 12),     #id=11
        
        (4, 13),
        (4, 14),
        
        (5, 15),
        (5, 16),
        (5, 17),
        
        (6, 18),
        (6, 19),
        (6, 20),
        (6, 21),
        
        (7, 22),
        (7, 23),
        (7, 24),
        
        (8, 25),
        (8, 26),
        (8, 27),
        (8, 28),
        (8, 29),
        
        (9, 30),
        
        (10, 31),
        
        (11, 32),
        
        (12, 33),
        (12, 34),
        (12, 35),
        
        (13, 36),
        
        (14, 37),
        
        (15, 38),
        (15, 39),
        (15, 40),
        (15, 41),
        
        (16, 42),

        (17, 43),
        ]

# ----------------------------------------------------------------------------
# --------------- БД профиля мощности счетчика -------------
# ----------------------------------------------------------------------------
dic_template_DBPP = {
        'id': None,
        'id_counter': None, 
        'datetime': "",
        'period_int': "",
        'P_plus': "",
        'P_minus': "",
        'Q_plus': "",
        'Q_minus': ""
}
sql_create_table_DBPofilP = """ CREATE TABLE IF NOT EXISTS DBPP (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_counter INTEGER NOT NULL,
        datetime timestamp,
        period_int TEXT,
        P_plus INTEGER,
        P_minus INTEGER,
        Q_plus INTEGER,
        Q_minus INTEGER,
        FOREIGN KEY (id_counter)  REFERENCES DBC (id) ON DELETE RESTRICT
        );
        """
# data_list_demo_table_DBPofilP = [
#         (1, datetime.datetime(2022,12,25,0,0), '30', '300', '350','400', '450'),
#         (1, datetime.datetime(2022,12,25,0,30), '30', '301', '351','401', '451'),
#         (1, datetime.datetime(2022,12,25,1,0), '30', '302', '352','402', '452'),
#         (1, datetime.datetime(2022,12,25,1,30), '30', '303', '353','403', '453'),
#         (1, datetime.datetime(2022,12,25,2,0), '30', '304', '354','404', '454'),
#         (1, datetime.datetime(2022,12,25,2,30), '30', '305', '355','405', '455'),
#         (1, datetime.datetime(2022,12,25,3,0), '30', '300', '350','400', '450'),
#         (1, datetime.datetime(2022,12,25,3,30), '30', '301', '351','401', '451'),
#         (1, datetime.datetime(2022,12,25,4,0), '30', '302', '352','402', '452'),
#         (1, datetime.datetime(2022,12,25,4,30), '30', '303', '353','403', '453'),
#         (1, datetime.datetime(2022,12,25,5,0), '30', '304', '354','404', '454'),
#         (1, datetime.datetime(2022,12,25,5,30), '30', '305', '355','405', '455'),

#         (2, datetime.datetime(2022,12,25,0,0), '30', '100', '250','300', '550'),
#         (2, datetime.datetime(2022,12,25,0,30), '30', '101', '251','301', '551'),
#         (2, datetime.datetime(2022,12,25,1,0), '30', '102', '252','302', '552'),
#         (2, datetime.datetime(2022,12,25,1,30), '30', '103', '253','303', '553'),
#         (2, datetime.datetime(2022,12,25,2,0), '30', '104', '254','304', '554'),
#         (2, datetime.datetime(2022,12,25,2,30), '30', '105', '255','305', '555'),
#         (2, datetime.datetime(2022,12,25,3,0), '30', '100', '250','300', '550'),
#         (2, datetime.datetime(2022,12,25,3,30), '30', '101', '251','301', '551'),
#         (2, datetime.datetime(2022,12,25,4,0), '30', '102', '252','302', '552'),
#         (2, datetime.datetime(2022,12,25,4,30), '30', '103', '253','303', '553'),
#         (2, datetime.datetime(2022,12,25,5,0), '30', '104', '254','304', '554'),
#         (2, datetime.datetime(2022,12,25,5,30), '30', '105', '255','305', '555'),

#         (3, datetime.datetime(2022,12,25,0,0), '30', '500', '650','700', '850'),
#         (3, datetime.datetime(2022,12,25,0,30), '30', '501', '651','701', '851'),
#         (3, datetime.datetime(2022,12,25,1,0), '30', '502', '652','702', '852'),
#         (3, datetime.datetime(2022,12,25,1,30), '30', '503', '653','703', '853'),
#         (3, datetime.datetime(2022,12,25,2,0), '30', '504', '654','704', '854'),
#         (3, datetime.datetime(2022,12,25,2,30), '30', '505', '655','705', '855'),
#         (3, datetime.datetime(2022,12,25,3,0), '30', '500', '650','700', '850'),
#         (3, datetime.datetime(2022,12,25,3,30), '30', '501', '651','701', '851'),
#         (3, datetime.datetime(2022,12,25,4,0), '30', '502', '652','702', '852'),
#         (3, datetime.datetime(2022,12,25,4,30), '30', '503', '653','703', '853'),
#         (3, datetime.datetime(2022,12,25,5,0), '30', '504', '654','704', '854'),
#         (3, datetime.datetime(2022,12,25,5,30), '30', '505', '655','705', '855'),
#     ]
# ----------------------------------------------------------------------------
# --------------- БД мгновенных значений счетчика (Instantly Counter)----
# ----------------------------------------------------------------------------
dic_inst_param = {
            "Ток": ["ток фаза A", "ток фаза B", "ток фаза C", "ток сумм"],
            "Мощность P": ["мощность P фаза A", "мощность P фаза B", "мощность P фаза C", "мощность P сумм"],
            "Мощность Q": ["мощность Q фаза A", "мощность Q фаза B", "мощность Q фаза C", "мощность Q сумм"],
            "Мощность S": ["мощность S фаза A", "мощность S фаза B", "мощность S фаза C", "мощность S сумм"],
            "Коэффициента мощности": ["коэффициент мощности фаза A", "коэффициент мощности фаза B", "коэффициент мощности фаза C", "коэффициент мощности сумм"],
            "Мощность по тарифам": ["мощность тариф 1", "мощность тариф 2", "мощность тариф 3", "мощность тариф 4"]
        }

dic_template_DBIC = {
        'id'              : None,
        'id_counter'      : None, 
        'datetime'        : None,
        'CurrentFaze1'    : 0,
        'CurrentFaze2'    : 0,
        'CurrentFaze3'    : 0,
        'CurrentSum'      : 0,
        'PowerPFaze1'     : 0,
        'PowerPFaze2'     : 0,
        'PowerPFaze3'     : 0,
        'PowerPFazeSum'   : 0,
        'PowerQFaze1'     : 0,
        'PowerQFaze2'     : 0,
        'PowerQFaze3'     : 0,
        'PowerQFazeSum'   : 0,
        'PowerSFaze1'     : 0,
        'PowerSFaze2'     : 0,
        'PowerSFaze3'     : 0,
        'PowerSFazeSum'   : 0,
        'KPowerFaze1'     : 0,
        'KPowerFaze2'     : 0,
        'KPowerFaze3'     : 0,
        'KPowerFazeSum'   : 0,
        'EnergyTarif1'    : 0,
        'EnergyTarif2'    : 0,
        'EnergyTarif3'    : 0,
        'EnergyTarif4'    : 0
}
sql_create_table_DBIC = """ CREATE TABLE IF NOT EXISTS DBIC (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_counter INTEGER NOT NULL,
        datetime timestamp,
        CurrentFaze1 INTEGER,
        CurrentFaze2 INTEGER,
        CurrentFaze3 INTEGER,
        CurrentSum INTEGER,
        PowerPFaze1 INTEGER,
        PowerPFaze2 INTEGER,
        PowerPFaze3 INTEGER,
        PowerPFazeSum INTEGER,
        PowerQFaze1 INTEGER,
        PowerQFaze2 INTEGER,
        PowerQFaze3 INTEGER,
        PowerQFazeSum INTEGER,
        PowerSFaze1 INTEGER,
        PowerSFaze2 INTEGER,
        PowerSFaze3 INTEGER,
        PowerSFazeSum INTEGER,
        KPowerFaze1 INTEGER,
        KPowerFaze2 INTEGER,
        KPowerFaze3 INTEGER,
        KPowerFazeSum INTEGER,
        EnergyTarif1 INTEGER,
        EnergyTarif2 INTEGER,
        EnergyTarif3 INTEGER,
        EnergyTarif4 INTEGER,
        EnergyTarifSum INTEGER,
        FOREIGN KEY (id_counter)  REFERENCES DBC (id) ON DELETE RESTRICT
        );
        """
        # CurrentFaze1 TEXT,
        # CurrentFaze2 TEXT,
        # CurrentFaze3 TEXT,
        # CurrentSum TEXT,
        # PowerPFaze1 TEXT,
        # PowerPFaze2 TEXT,
        # PowerPFaze3 TEXT,
        # PowerPFazeSum TEXT,
        # PowerQFaze1 TEXT,
        # PowerQFaze2 TEXT,
        # PowerQFaze3 TEXT,
        # PowerQFazeSum TEXT,
        # PowerSFaze1 TEXT,
        # PowerSFaze2 TEXT,
        # PowerSFaze3 TEXT,
        # PowerSFazeSum TEXT,
        # KPowerFaze1 TEXT,
        # KPowerFaze2 TEXT,
        # KPowerFaze3 TEXT,
        # KPowerFazeSum TEXT,
        # EnergyTarif1 TEXT,
        # EnergyTarif2 TEXT,
        # EnergyTarif3 TEXT,
        # EnergyTarif4 TEXT,
        # EnergyTarifSum TEXT,
# data_list_demo_table_DBIC = [
#         (1, datetime.datetime(2022,12,25,0,0), '3', '5', '5'),
#         (1, datetime.datetime(2022,12,25,0,3), '2', '5', '5'),
#         (1, datetime.datetime(2022,12,25,0,6), '1', '5', '5'),
#         (1, datetime.datetime(2022,12,25,0,9), '0', '5', '5'),
#         (1, datetime.datetime(2022,12,25,0,12), '2', '5', '5'),
#         (1, datetime.datetime(2022,12,25,0,15), '3', '5', '5'),
#         (1, datetime.datetime(2022,12,25,0,18), '4', '5', '5'),
#         (1, datetime.datetime(2022,12,25,0,21), '5', '5', '5'),
#         (1, datetime.datetime(2022,12,25,0,24), '6', '5', '5'),
#         (1, datetime.datetime(2022,12,25,0,27), '7', '5', '5'),
#         (1, datetime.datetime(2022,12,25,0,30), '8', '5', '5'),
#         (1, datetime.datetime(2022,12,25,0,33), '3', '5', '5'),
#         (1, datetime.datetime(2022,12,25,0,36), '4', '5', '5'),
#         (1, datetime.datetime(2022,12,25,0,39), '3', '5', '5'),
#         (1, datetime.datetime(2022,12,25,0,42), '6', '5', '5'),
#         (1, datetime.datetime(2022,12,25,0,45), '7', '5', '5'),
#         (1, datetime.datetime(2022,12,25,0,48), '8', '5', '5'),
#         (1, datetime.datetime(2022,12,25,0,51), '9', '6', '5'),
#         (1, datetime.datetime(2022,12,25,0,54), '10', '7', '5'),
#         (1, datetime.datetime(2022,12,25,0,57), '3', '8', '5'),
#         (1, datetime.datetime(2022,12,25,1,0), '4', '9', '5'),
#         (1, datetime.datetime(2022,12,25,1,3), '5', '10', '5'),
#         (1, datetime.datetime(2022,12,25,1,6), '6', '5', '5'),
#         (1, datetime.datetime(2022,12,25,1,9), '7', '5', '5'),
#         (1, datetime.datetime(2022,12,25,1,12), '3', '5', '5'),
#         (1, datetime.datetime(2022,12,25,1,15), '4', '5', '5'),
#         (1, datetime.datetime(2022,12,25,1,18), '5', '5', '5'),
#         (1, datetime.datetime(2022,12,25,1,21), '6', '3', '5'),
#         (1, datetime.datetime(2022,12,25,1,24), '7', '4', '5'),
#         (1, datetime.datetime(2022,12,25,1,27), '8', '2', '5'),
#         (1, datetime.datetime(2022,12,25,1,30), '1', '1', '5'),
#         (1, datetime.datetime(2022,12,25,1,33), '0', '0', '5'),
#         (1, datetime.datetime(2022,12,25,1,36), '0', '0', '5'),
#         (1, datetime.datetime(2022,12,25,1,39), '0', '5', '5'),
#         (1, datetime.datetime(2022,12,25,1,42), '10', '1', '5'),
#         (1, datetime.datetime(2022,12,25,1,45), '12', '2', '5'),
#         (1, datetime.datetime(2022,12,25,1,48), '3', '3', '5'),
#         (1, datetime.datetime(2022,12,25,1,51), '4', '5', '5'),
#         (1, datetime.datetime(2022,12,25,1,54), '5', '2', '5'),
#         (1, datetime.datetime(2022,12,25,1,57), '6', '2', '5'),
#         (1, datetime.datetime(2022,12,25,2,0), '7', '2', '5'),

#         (2, datetime.datetime(2022,12,25,0,0), '3', '10', '5'),
#         (2, datetime.datetime(2022,12,25,0,3), '2', '5', '5'),
#         (2, datetime.datetime(2022,12,25,0,6), '2', '5', '5'),
#         (2, datetime.datetime(2022,12,25,0,9), '0', '10', '5'),
#         (2, datetime.datetime(2022,12,25,0,12), '2', '5', '5'),
#         (2, datetime.datetime(2022,12,25,0,15), '3', '6', '4'),
#         (2, datetime.datetime(2022,12,25,0,18), '4', '7', '3'),
#         (2, datetime.datetime(2022,12,25,0,21), '5', '8', '2'),
#         (2, datetime.datetime(2022,12,25,0,24), '6', '9', '1'),
#         (2, datetime.datetime(2022,12,25,0,27), '7', '2', '5'),
#         (2, datetime.datetime(2022,12,25,0,30), '8', '1', '5'),
#         (2, datetime.datetime(2022,12,25,0,33), '3', '2', '5'),
#         (2, datetime.datetime(2022,12,25,0,36), '4', '3', '0'),
#         (2, datetime.datetime(2022,12,25,0,39), '3', '4', '0'),
#         (2, datetime.datetime(2022,12,25,0,42), '6', '5', '0'),
#         (2, datetime.datetime(2022,12,25,0,45), '7', '5', '0'),
#         (2, datetime.datetime(2022,12,25,0,48), '8', '6', '0'),
#         (2, datetime.datetime(2022,12,25,0,51), '9', '6', '5'),
#         (2, datetime.datetime(2022,12,25,0,54), '10', '7', '5'),
#         (2, datetime.datetime(2022,12,25,0,57), '3', '8', '0'),
#         (2, datetime.datetime(2022,12,25,1,0), '4', '9', '0'),
#         (2, datetime.datetime(2022,12,25,1,3), '5', '0', '0'),
#         (2, datetime.datetime(2022,12,25,1,6), '6', '0', '0'),
#         (2, datetime.datetime(2022,12,25,1,9), '7', '5', '5'),
#         (2, datetime.datetime(2022,12,25,1,12), '3', '0', '5'),
#         (2, datetime.datetime(2022,12,25,1,15), '4', '5', '5'),
#         (2, datetime.datetime(2022,12,25,1,18), '5', '5', '5'),
#         (2, datetime.datetime(2022,12,25,1,21), '6', '3', '5'),
#         (2, datetime.datetime(2022,12,25,1,24), '7', '0', '0'),
#         (2, datetime.datetime(2022,12,25,1,27), '8', '2', '5'),
#         (2, datetime.datetime(2022,12,25,1,30), '1', '1', '5'),
#         (2, datetime.datetime(2022,12,25,1,33), '0', '0', '5'),
#         (2, datetime.datetime(2022,12,25,1,36), '0', '0', '5'),
#         (2, datetime.datetime(2022,12,25,1,39), '0', '5', '5'),
#         (2, datetime.datetime(2022,12,25,1,42), '10', '1', '5'),
#         (2, datetime.datetime(2022,12,25,1,45), '12', '2', '5'),
#         (2, datetime.datetime(2022,12,25,1,48), '3', '3', '5'),
#         (2, datetime.datetime(2022,12,25,1,51), '4', '5', '5'),
#         (2, datetime.datetime(2022,12,25,1,54), '5', '2', '5'),
#         (2, datetime.datetime(2022,12,25,1,57), '6', '2', '5'),
#         (2, datetime.datetime(2022,12,25,2,0), '7', '2', '5'),
        
#         (3, datetime.datetime(2022,12,25,0,0), '3', '10', '1'),
#         (3, datetime.datetime(2022,12,25,0,3), '2', '5', '2'),
#         (3, datetime.datetime(2022,12,25,0,6), '2', '1', '3'),
#         (3, datetime.datetime(2022,12,25,0,9), '0', '1', '5'),
#         (3, datetime.datetime(2022,12,25,0,12), '2', '2', '2'),
#         (3, datetime.datetime(2022,12,25,0,15), '10', '3', '1'),
#         (3, datetime.datetime(2022,12,25,0,18), '4', '10', '4'),
#         (3, datetime.datetime(2022,12,25,0,21), '11', '9', '3'),
#         (3, datetime.datetime(2022,12,25,0,24), '10', '8', '2'),
#         (3, datetime.datetime(2022,12,25,0,27), '9', '7', '5'),
#         (3, datetime.datetime(2022,12,25,0,30), '8', '6', '5'),
#         (3, datetime.datetime(2022,12,25,0,33), '7', '5', '10'),
#         (3, datetime.datetime(2022,12,25,0,36), '6', '4', '9'),
#         (3, datetime.datetime(2022,12,25,0,39), '5', '3', '8'),
#         (3, datetime.datetime(2022,12,25,0,42), '4', '2', '7'),
#         (3, datetime.datetime(2022,12,25,0,45), '3', '1', '6'),
#         (3, datetime.datetime(2022,12,25,0,48), '2', '1', '5'),
#         (3, datetime.datetime(2022,12,25,0,51), '1', '2', '4'),
#         (3, datetime.datetime(2022,12,25,0,54), '10', '9', '3'),
#         (3, datetime.datetime(2022,12,25,0,57), '10', '10', '2'),
#         (3, datetime.datetime(2022,12,25,1,0), '9', '11', '1'),
#         (3, datetime.datetime(2022,12,25,1,3), '8', '12', '10'),
#         (3, datetime.datetime(2022,12,25,1,6), '7', '1', '9'),
#         (3, datetime.datetime(2022,12,25,1,9), '7', '2', '8'),
#         (3, datetime.datetime(2022,12,25,1,12), '6', '3', '7'),
#         (3, datetime.datetime(2022,12,25,1,15), '5', '4', '6'),
#         (3, datetime.datetime(2022,12,25,1,18), '4', '5', '5'),
#         (3, datetime.datetime(2022,12,25,1,21), '3', '6', '4'),
#         (3, datetime.datetime(2022,12,25,1,24), '2', '7', '3'),
#         (3, datetime.datetime(2022,12,25,1,27), '1', '8', '2'),
#         (3, datetime.datetime(2022,12,25,1,30), '1', '5', '1'),
#         (3, datetime.datetime(2022,12,25,1,33), '0', '6', '10'),
#         (3, datetime.datetime(2022,12,25,1,36), '0', '7', '9'),
#         (3, datetime.datetime(2022,12,25,1,39), '0', '8', '8'),
#         (3, datetime.datetime(2022,12,25,1,42), '10', '9', '7'),
#         (3, datetime.datetime(2022,12,25,1,45), '12', '10', '6'),
#         (3, datetime.datetime(2022,12,25,1,48), '3', '12', '5'),
#         (3, datetime.datetime(2022,12,25,1,51), '4', '5', '4'),
#         (3, datetime.datetime(2022,12,25,1,54), '5', '5', '3'),
#         (3, datetime.datetime(2022,12,25,1,57), '6', '5', '2'),
#         (3, datetime.datetime(2022,12,25,2,0), '7', '5', '1'),

#     ]
# ----------------------------------------------------------------------------
# --------------- БД мгновенных значений мощности счетчика (Instantly Power)----
# ----------------------------------------------------------------------------
# sql_create_table_DBIP = """ CREATE TABLE IF NOT EXISTS DBIP (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         id_counter INTEGER NOT NULL,
#         datetime timestamp,
#         PowerPFaze1 TEXT,
#         PowerPFaze2 TEXT,
#         PowerPFaze3 TEXT,
#         PowerPFazeSum TEXT,
#         PowerQFaze1 TEXT,
#         PowerQFaze2 TEXT,
#         PowerQFaze3 TEXT,
#         PowerQFazeSum TEXT,
#         PowerSFaze1 TEXT,
#         PowerSFaze2 TEXT,
#         PowerSFaze3 TEXT,
#         PowerSFazeSum TEXT,
#         FOREIGN KEY (id_counter)  REFERENCES DBC (id) ON DELETE RESTRICT
#         );
#         """
# ----------------------------------------------------------------------------
# --------------- БД мгновенных значений мгновенного коэффициента мощности счетчика (Instantly KPower)----
# ----------------------------------------------------------------------------
# sql_create_table_DBIKP = """ CREATE TABLE IF NOT EXISTS DBIKP (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         id_counter INTEGER NOT NULL,
#         datetime timestamp,
#         KPowerFaze1 TEXT,
#         KPowerFaze2 TEXT,
#         KPowerFaze3 TEXT,
#         KPowerFazeSum TEXT,
#         FOREIGN KEY (id_counter)  REFERENCES DBC (id) ON DELETE RESTRICT
#         );
#         """
# # ----------------------------------------------------------------------------
# # --------------- БД мгновенных значений зафиксированная энергии счетчика (Instantly Energy)----
# # ----------------------------------------------------------------------------
# sql_create_table_DBIE = """ CREATE TABLE IF NOT EXISTS DBIE (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         id_counter INTEGER NOT NULL,
#         datetime timestamp,
#         EnergyTarif1 TEXT,
#         EnergyTarif2 TEXT,
#         EnergyTarif3 TEXT,
#         EnergyTarif4 TEXT,
#         EnergyTarifSum TEXT,
#         FOREIGN KEY (id_counter)  REFERENCES DBC (id) ON DELETE RESTRICT
#         );
#         """





















