# moduleSQLite
# autor: MolokovAlex
# coding: utf-8

# модуль держатель функций работы с SQLite

import os
from logging import exception
from sys import getsizeof
import datetime # обязательно до import sqlite3 as sql3  !!!!!
import sqlite3 as sql3
from pathlib import Path
import traceback
import sys
import json
import logging
import modulVM.config as cfg
import modulVM.moduleLogging as ml





def connect_to_DB(nameFileDB:str)->bool:
    """ функция подключения файла БД с проверками на существование файла, правильность структуры, формировании backup файла
        Вход:
        nameFileDB:str - полный путь (abspath) c наименование файла БД
        Выход:
        Flag_connectDB - флаг результата подключения файла БД
    """
    Flag_connectDB = False
    # проверка наличия файла БД SQLite
    
    if CheckExistDBFile (nameFileDB):
        Flag_connectDB = True
        # функция создания резервного файла БД
        # if createBackUpDBFile (cfg.absDB_BACKUP_FILE, nameFileDB):
        #     Flag_connectDB = True
        # else: 
        #     Flag_connectDB = False
    elif createTableDBFile(nameFileDB):
        
        fill_TableDBC_demo_value(nameFileDB)
        fill_TableDBG_demo_value(nameFileDB)
        fill_TableDBGC_demo_value(nameFileDB)
        fill_TableDBPP_demo_value(nameFileDB)
        fill_TableDBIC_demo_value(nameFileDB)
        Flag_connectDB = True
    return Flag_connectDB

def progress(status, remaining, total):
    print(f'Скопировано {total-remaining} из {total}...')
    return None

def viewCodeError (sql_error):
    print("Ошибка при работе с sqlite", sql_error)
    print("Класс исключения: ", sql_error.__class__)
    print("Исключение", sql_error.args)
    print("Печать подробноcтей исключения SQLite: ")
    exc_type, exc_value, exc_tb = sys.exc_info()
    print(traceback.format_exception(exc_type, exc_value, exc_tb))


def CheckExistDBFile (nameFileDB:str)->bool:
    """ функция проверки файла БД на существование и правильность структуры
        Вход:
        nameFileDB:str - полный путь (abspath) c наименование файла БД
        Выход:
        - Flag_checkDBF - флаг результата проверки существования файла БД
    """ 
    ml.logger.info(f"Проверка наличия файла БД SQLite {nameFileDB}...")
    Flag_checkDBF = False
    # если файл БД существует - проверим его на открываемость (не битый ли?)
    if os.path.isfile(nameFileDB):
        try:
            ml.logger.info("файл БД найден")
            sqlite_connection = sql3.connect(nameFileDB)
            cursor = sqlite_connection.cursor()
            ml.logger.info("База данных создана и успешно подключена к SQLite")
            sqlite_select_query = "select sqlite_version();"
            cursor.execute(sqlite_select_query)
            record = cursor.fetchall()
            ml.logger.debug(f"Версия базы данных SQLite: {record}")
            cursor.close()
            Flag_checkDBF = True

        except sql3.Error as error_sql:
            ml.logger.error("Exception occurred", exc_info=True)
            viewCodeError (error_sql)
            Flag_checkDBF = False
        finally:
            if (sqlite_connection):
                sqlite_connection.close()
                ml.logger.debug("Соединение с SQLite закрыто")
    else:
        ml.logger.error("файл БД не найден")
        Flag_checkDBF = False
    return Flag_checkDBF


def createBackUpDBFile (nameBackupFileDBFile: str, nameFileDB: str)->bool:
    """ функция резервного создания файла БД
        Вход:
        nameBackUpDBFile -  полный путь (abspath) c наименование файла резерной БД
        nameFileDB:str - полный путь (abspath) c наименование файла БД
        Выход:
        - созданный файл резервной БД
        - Flag_createBackDBF - флаг результата создания резервной БД
    """    
    Flag_createBackDBF = False
    ml.logger.info("Авто-резервирование БД...")
    try:
        connectionDBFile = sql3.connect(nameFileDB)
        backup_connection = sql3.connect(nameBackupFileDBFile)
        with backup_connection, connectionDBFile:
            connectionDBFile.backup(backup_connection, pages=3, progress=progress)
            Flag_createBackDBF = True
        ml.logger.info("Резервное копирование выполнено успешно")
    except sql3.Error as error_sql:
        ml.logger.error("Exception occurred", exc_info=True)
        viewCodeError (error_sql)
        Flag_createBackDBF = False
    finally:
        if(backup_connection):
            backup_connection.close()
            connectionDBFile.close()
            ml.logger.debug("Соединение с SQLite закрыто")
    return Flag_createBackDBF



def createTableDBFile(nameFileDB:str)->bool:
    """
    создадим таблицы компонентов, групп, едИзмерений
        Вход:
        nameFileDB:str - полный путь (abspath) c наименование файла БД
        Выход:
        - созданный файл резервной БД
        - FlagCreateTableDBf - флаг результата создания таблиц в БД
    """
    ml.logger.info("Создание нового файла БД...")
    FlagCreateTableDBf = False
    try:
        connectionDBFile = sql3.connect(nameFileDB)
        cursorDB = connectionDBFile.cursor()
        with connectionDBFile:
            ml.logger.info("create_table_DBG")
            cursorDB.execute(cfg.sql_create_table_DBG)
            connectionDBFile.commit()
            ml.logger.info("create_table_DBC")
            cursorDB.execute(cfg.sql_create_table_DBC)
            connectionDBFile.commit()
            ml.logger.info("create_table_DBGC")
            cursorDB.execute(cfg.sql_create_table_DBGC)
            connectionDBFile.commit()
            ml.logger.info("create_table_DBPofilP")
            cursorDB.execute(cfg.sql_create_table_DBPofilP)
            connectionDBFile.commit()
            ml.logger.info("create_table_DBIC")
            cursorDB.execute(cfg.sql_create_table_DBIC)
            connectionDBFile.commit()
            # print ("create_table_DBIP")
            # cursorDB.execute(cfg.sql_create_table_DBIP)
            # connectionDBFile.commit()
            # print ("create_table_DBIKP")
            # cursorDB.execute(cfg.sql_create_table_DBIKP)
            # connectionDBFile.commit()
            # print ("create_table_DBIE")
            # cursorDB.execute(cfg.sql_create_table_DBIE)
            connectionDBFile.commit()
            FlagCreateTableDBf = True
    except sql3.Error as error_sql:
        ml.logger.error("Exception occurred", exc_info=True)
        viewCodeError (error_sql)
        FlagCreateTableDBf = False
    finally:
        if(connectionDBFile):
            connectionDBFile.close()
            ml.logger.debug("Соединение с SQLite закрыто")
    return FlagCreateTableDBf




# ------------------------------------------------------------------------------------
# ----------------- DBG -------------------------------------------------------------
# ------------------------------------------------------------------------------------

def getListGroupDB():
        rezult_get = False
        lst_groupDB = []
        cursorDB = cfg.sql_base_conn.cursor()
        with cfg.sql_base_conn:
            cursorDB.execute("""SELECT id, name_group_full FROM DBG""")
            b = cursorDB.fetchall()
            if b:
                lst_groupDB = []
                dict_group = {}
                for item in b:
                    dict_group=dict(zip(cfg.lst_name_poles_DBG, item))
                    lst_groupDB.append(dict_group)
                    dict_group = {}
                rezult_get = True
            else:
                rezult_get = False
        return lst_groupDB, rezult_get

def deleteGroupDB(nameGroup):
    rezult_delete = False
    try:
        cursorDB = cfg.sql_base_conn.cursor()
        with cfg.sql_base_conn:
                cursorDB.execute("""DELETE FROM DBG WHERE name_group_full=?;""", (nameGroup,))
                cfg.sql_base_conn.commit()
                rezult_delete = True
    except sql3.Error as error_sql:
        ml.logger.error("Exception occurred", exc_info=True)
        viewCodeError (error_sql)
        rezult_delete = False
    return rezult_delete

def editGroupDB(oldNameGroup, newNameGroup):
    rezult_edit = False
    try:
        cursorDB = cfg.sql_base_conn.cursor()
        with cfg.sql_base_conn:
                cursorDB.executemany("""UPDATE DBG SET name_group_full=? WHERE name_group_full=?;""", [(newNameGroup, oldNameGroup),])
                cfg.sql_base_conn.commit()
                rezult_edit = True
    except sql3.Error as error_sql:
        ml.logger.error("Exception occurred", exc_info=True)
        viewCodeError (error_sql)
        rezult_edit = False
    return rezult_edit

def addNewGroupDB(addNameGroup):
        rezult_add = False
        try:
            cursorDB = cfg.sql_base_conn.cursor()
            with cfg.sql_base_conn:
                cursorDB.execute("""INSERT INTO DBG (name_group_full) VALUES (?);""", (addNameGroup,))
                cfg.sql_base_conn.commit()
            rezult_add = True
        except sql3.Error as error_sql:
            ml.logger.error("Exception occurred", exc_info=True)
            viewCodeError (error_sql)
            rezult_add = False
        return rezult_add


def fill_TableDBG_demo_value(nameFileDB:str):
    """
    заполнение таблицы DBG демо-значениями
    """
    ml.logger.info("Заполнение таблицы DBG демо-значениями...")
    insert_data_query = """INSERT INTO DBG 
                            (id, name_group_full) 
                        VALUES 
                            (?,?);"""
    
    Flag_fill_TableDBG_defaul_value = False
    try:
        connectionDBFile = sql3.connect(nameFileDB)
        cursorDB = connectionDBFile.cursor()
        with connectionDBFile: 
            cursorDB.executemany(insert_data_query, cfg.data_list_demo_DBG)
            connectionDBFile.commit()
            Flag_fill_TableDBG_defaul_value = True
            ml.logger.info("Заполнение таблицы DBG демо-значениями...OK")
    except sql3.Error as error_sql:
        ml.logger.error("Exception occurred", exc_info=True)
        viewCodeError (error_sql)
        Flag_fill_TableDBG_defaul_value = False
    finally:
        if(connectionDBFile):
            connectionDBFile.close()
            ml.logger.debug("Соединение с SQLite закрыто")
    return Flag_fill_TableDBG_defaul_value

    
# def fill_TableDBG_demo_value(nameFileDB:str):
#     """
#     заполнение таблицы DBG демо-значениями
#     """
#     insert_data_query = """INSERT INTO DBG 
#                             (id, name_group_full) 
#                         VALUES 
#                             (?,?);"""
    
#     Flag_fill_TableDBG_defaul_value = False
#     try:
#         connectionDBFile = sql3.connect(nameFileDB)
#         cursorDB = connectionDBFile.cursor()
#         with connectionDBFile: 
#             cursorDB.executemany(insert_data_query, cfg.data_list_demo_DBG)
#             connectionDBFile.commit()
#             Flag_fill_TableDBG_defaul_value = True

#     except sql3.Error as error_sql:
#         ml.logger.error("Exception occurred", exc_info=True)
#         viewCodeError (error_sql)
#         Flag_fill_TableDBG_defaul_value = False
#     finally:
#         if(connectionDBFile):
#             connectionDBFile.close()
#             ml.logger.info("Соединение с SQLite закрыто")
#     return Flag_fill_TableDBG_defaul_value







# ------------------------------------------------------------------------------------
# ----------------- DBC -------------------------------------------------------------
# ------------------------------------------------------------------------------------

def getListCounterDB():
        rezult_get = False
        lst_counterDB = []       
        cursorDB = cfg.sql_base_conn.cursor()
        with cfg.sql_base_conn:
            cursorDB.execute("""SELECT id, schem, name_counter_full, net_adress, manuf_number, manuf_data, klass_react, klass_act, nom_u, ku, ki, koefA, comment FROM DBC ORDER BY name_counter_full ASC""")
            b = cursorDB.fetchall()
            if b:
                lst_counterDB = []
                dict_counter = {}
                for item in b:
                    dict_counter=dict(zip(cfg.lst_name_poles_DBC, item))
                    lst_counterDB.append(dict_counter)
                    dict_counter = {}
                rezult_get = True
            else:
                rezult_get = False
        return lst_counterDB, rezult_get

def deleteCounterDB(nameCounter):
    rezult_delete = False
    try:
        cursorDB = cfg.sql_base_conn.cursor()
        with cfg.sql_base_conn:
                cursorDB.execute("""DELETE FROM DBC WHERE name_counter_full=?;""", (nameCounter,))
                cfg.sql_base_conn.commit()
                rezult_delete = True
    except sql3.Error as error_sql:
        ml.logger.error("Exception occurred", exc_info=True)
        viewCodeError (error_sql)
        rezult_delete = False
    return rezult_delete

def addNewCounterDB(newNameCounter:dict):
    rezult_edit = False
    newNameCounter.pop('id')
    a = newNameCounter.values()
    lst_newNameCounter = []
    for item in a:
        lst_newNameCounter.append(item)
    try:
        cursorDB = cfg.sql_base_conn.cursor()
        with cfg.sql_base_conn:
                cursorDB.executemany("""INSERT INTO DBC (schem, name_counter_full, net_adress, manuf_number, manuf_data, klass_react, klass_act, nom_u, ku, ki, koefA, comment) VALUES (?,?,?,?,?,?,?,?,?,?,?,?);""", (lst_newNameCounter,))
                cfg.sql_base_conn.commit()
                rezult_edit = True
    except sql3.Error as error_sql:
        ml.logger.error("Exception occurred", exc_info=True)
        viewCodeError (error_sql)
        rezult_edit = False
    return rezult_edit

def editCounterDB(new_NameCounter:dict):
    rezult_edit = False
    newNameCounter = new_NameCounter.copy()
    id_counter = int(newNameCounter['id'])
    newNameCounter.pop('id')
    a = newNameCounter.values()
    lst_newNameCounter = []
    for item in a:
        lst_newNameCounter.append(item)
    lst_newNameCounter.append(id_counter)
    # print (lst_newNameCounter)
    try:
        cursorDB = cfg.sql_base_conn.cursor()
        with cfg.sql_base_conn:
                cursorDB.executemany("""UPDATE DBC SET schem=?, name_counter_full=?, net_adress=?, manuf_number=?, manuf_data=?, klass_react=?, klass_act=?, nom_u=?, ku=?, ki=?, koefA=?, comment=? WHERE id=?;""", (lst_newNameCounter,))
                cfg.sql_base_conn.commit()
                rezult_edit = True
    except sql3.Error as error_sql:
        ml.logger.error("Exception occurred", exc_info=True)
        viewCodeError (error_sql)
        rezult_edit = False
    return rezult_edit

def getListCounterInGroupDB(self, textFullNameGroup):
    rezult_get = False
    lst_counterInGroupDB = []
    list_GroupDB, rezult_getListOfGroupDB = getListGroupDB()
    if rezult_getListOfGroupDB:
        for item in list_GroupDB:
            if item['name_group_full']==textFullNameGroup:
                id_group = item['id']
                break
        cursorDB = cfg.sql_base_conn.cursor()
        with cfg.sql_base_conn:
            cursorDB.execute("""SELECT * FROM DBC LEFT JOIN DBGC ON DBGC.id_counter = DBC.id WHERE DBGC.id_group = ?;""", (id_group,))
            b = cursorDB.fetchall()
            if b:
                lst_counterInGroupDB = []
                dict_group = {}
                for item in b:
                    dict_group=dict(zip(cfg.lst_name_poles_DBC, item))
                    lst_counterInGroupDB.append(dict_group)
                    dict_group = {}
                rezult_get = True
            else:
                rezult_get = False
    else:
        rezult_get = False
    return lst_counterInGroupDB, rezult_get

def fill_TableDBC_demo_value(nameFileDB:str):
    """
    заполнение таблицы DBC демо-значениями
    schem TEXT
    name_counter_full TEXT
    """
    ml.logger.info("Заполнение таблицы DBC демо-значениями...")
    insert_data_query = """INSERT INTO DBC (schem, name_counter_full, net_adress, manuf_number, manuf_data, klass_react, klass_act, nom_u, nom_i, ku, ki, koefA, comment) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);"""
    Flag_fill_TableDBC_defaul_value = False
    try:
        connectionDBFile = sql3.connect(nameFileDB)
        cursorDB = connectionDBFile.cursor()
        with connectionDBFile: 
            # for key, value in appDemoData.items():
            cursorDB.executemany(insert_data_query, cfg.data_list_demo_DBC)
            connectionDBFile.commit()
            Flag_fill_TableDBC_defaul_value = True
            ml.logger.info("Заполнение таблицы DBC демо-значениями...OK")
    except sql3.Error as error_sql:
        ml.logger.error("Exception occurred", exc_info=True)
        viewCodeError (error_sql)
        Flag_fill_TableDBC_defaul_value = False
    finally:
        if(connectionDBFile):
            connectionDBFile.close()
            ml.logger.debug("Соединение с SQLite закрыто")
    return Flag_fill_TableDBC_defaul_value








# ------------------------------------------------------------------------------------
# ----------------- DBGC -------------------------------------------------------------
# ------------------------------------------------------------------------------------

def getListDBGC():
    rezult_get = False
    lst_DBGC = []
    cursorDB = cfg.sql_base_conn.cursor()
    with cfg.sql_base_conn:
        cursorDB.execute("""SELECT id, id_group, id_counter FROM DBGC""")
        b = cursorDB.fetchall()
        if b:
            lst_DBGC = []
            dict_group = {}
            for item in b:
                dict_group=dict(zip(cfg.lst_name_poles_DBGC, item))
                lst_DBGC.append(dict_group)
                dict_group = {}
            rezult_get = True
            dic_all_DBCG = {}
            # поиск максимального id_group
            max_= b[0][1]
            for item_b in b:
                if item_b[1] > max_:
                    max_= item_b[1]
            #
            # создание из этих данныхБД словаря ключ/номерГруппы - значения/номераСчетчиков
            for id_group in range (0, max_+1,1):
                id_count = []
                b01=id_group
                for item_b in b:
                    if item_b[1] == b01:
                        id_count.append(item_b[2])
                if id_count: dic_all_DBCG[str(b01)] = id_count
        else:
            rezult_get = False
    return lst_DBGC, dic_all_DBCG, rezult_get

def get_list_counter_in_group_DBGC(id_group:int):
    rezult_get = False
    list_counter_in_group = []
    cursorDB = cfg.sql_base_conn.cursor()
    with cfg.sql_base_conn:
        cursorDB.execute("""SELECT id_counter FROM DBGC WHERE id_group=?""", (id_group,))
        data = cursorDB.fetchall()
        if data:
            for item in data:
                list_counter_in_group.append(item[0])
            rezult_get = True
        else:
            rezult_get = False
    return list_counter_in_group, rezult_get    

def deleteItemDBGC(id):
    rezult_delete = False
    try:
        cursorDB = cfg.sql_base_conn.cursor()
        with cfg.sql_base_conn:
                cursorDB.execute("""DELETE FROM DBGC WHERE id=?;""", (id,))
                cfg.sql_base_conn.commit()
                rezult_delete = True
    except sql3.Error as error_sql:
        ml.logger.error("Exception occurred", exc_info=True)
        viewCodeError (error_sql)
        rezult_delete = False
    return rezult_delete

def addDBGC(id_group,id_counter):
    rezult_add = False
    try:
        cursorDB = cfg.sql_base_conn.cursor()
        with cfg.sql_base_conn:
            cursorDB.executemany("""INSERT INTO DBGC (id_group, id_counter) VALUES (?,?);""", [(id_group,id_counter,),])
            cfg.sql_base_conn.commit()
            rezult_add = True
    except sql3.Error as error_sql:
        ml.logger.error("Exception occurred", exc_info=True)
        viewCodeError (error_sql)
        rezult_add = False
    return rezult_add



def fill_TableDBGC_demo_value(nameFileDB:str):
    """
    заполнение таблицы DBGC демо-значениями
    name_group_full TEXT
    id_group INTEGER NOT NULL,
    id_counter INTEGER NOT NULL,
    """
    ml.logger.info("Заполнение таблицы DBGC демо-значениями...")
    flag_rezult = False
    try:
        connectDB = sql3.connect(nameFileDB)
        cursorDB = connectDB.cursor()
        with connectDB:
            cursorDB.executemany("""INSERT INTO DBGC (id_group, id_counter) VALUES (?,?);""", cfg.data_list_demo_DBGC)
            connectDB.commit()
            ml.logger.info("Заполнение таблицы DBGC демо-значениями...OK")
            flag_rezult = True
    except sql3.Error as error_sql:
        ml.logger.error("Exception occurred", exc_info=True)
        viewCodeError (error_sql)
        flag_rezult = False
    finally:
        if connectDB:
            connectDB.close()
            ml.logger.debug("Соединение с SQLite закрыто")
    return flag_rezult







# ------------------------------------------------------------------------------------
# ----------------- DBPP -------------------------------------------------------------
# ------------------------------------------------------------------------------------
    # id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     name_counter TEXT NOT NULL CHECK(name_counter !=''),
    #     id_counter INTEGER NOT NULL,
    #     date TEXT,
    #     time TEXT,
    #     period_int TEXT,
    #     P_plus TEXT,
    #     P_minus TEXT,
    #     Q_plus TEXT,
    #     Q_minus TEXT,
    #     FOREIGN KEY (id_counter)  REFERENCES DBC (id) ON DELETE RESTRICT
    #     );
# ------------------------------------------------------------------------------------
def fill_TableDBPP_demo_value(nameFileDB:str):
    """
    заполнение таблицы DBPP демо-значениями
    """
    ml.logger.info("Заполнение таблицы DBPP демо-значениями...")
    flag_rezult = False
    with open(cfg.absTEST_DATA_PP_FILE, "r") as file:
        data = json.load(file)
    for item in data:
        item['datetime'] = datetime.datetime.strptime(item['datetime'], "%d/%m/%Y %H:%M")
    # data2 = data.values()
    data2 = []
    data_values = []
    for item in data:
        data_values = []
        for key, val in item.items():
            data_values.append(val)
        data2.append(data_values)
    try:
        connectDB = sql3.connect(nameFileDB)
        cursorDB = connectDB.cursor()
        with connectDB:
            # cursorDB.executemany("""INSERT INTO DBPP (id_counter, datetime, period_int, P_plus, P_minus, Q_plus, Q_minus) VALUES (?,?,?,?,?,?,?);""", cfg.data_list_demo_table_DBPofilP)
            cursorDB.executemany("""INSERT INTO DBPP (id, id_counter, datetime, period_int, P_plus, P_minus, Q_plus, Q_minus) VALUES (?,?,?,?,?,?,?,?);""", data2)
            connectDB.commit()
            ml.logger.info("Заполнение таблицы DBPP демо-значениями...OK")
            flag_rezult = True
    except sql3.Error as error_sql:
        ml.logger.error("Exception occurred", exc_info=True)
        viewCodeError (error_sql)
        flag_rezult = False
    finally:
        if connectDB:
            connectDB.close()
            ml.logger.debug("Соединение с SQLite закрыто")
    return  flag_rezult


def insert_TableDBPP_value(dictData: dict):
    """
    заполнение таблицы DBPP значением с datetime
    """
    ml.logger.info("Заполнение таблицы DBPP значением с datetime")
    dict_data = dictData.copy()
    flag_rezult = False

    if "id" in dict_data: 
        del dict_data["id"]
        dict_data['datetime'] = datetime.datetime.strptime(dict_data['datetime'], "%d/%m/%Y %H:%M")#.timestamp()
        # dict_data['datetime'] = dict_data['datetime']
        lst_data = []
        for key, val in dict_data.items():
            lst_data.append(val)
        try:
            cursorDB = cfg.sql_base_conn.cursor()
            with cfg.sql_base_conn:
                # cursorDB.executemany("""INSERT INTO DBPP (id_counter, datetime, period_int, P_plus, P_minus, Q_plus, Q_minus) VALUES (?,?,?,?,?,?,?);""", cfg.data_list_demo_table_DBPofilP)
                cursorDB.execute("""INSERT INTO DBPP (id_counter, datetime, period_int, 
                                                P_plus, P_minus, Q_plus, Q_minus
                                                ) VALUES (?,?,?,?,?,?,?);""", lst_data)
                cfg.sql_base_conn.commit()
                ml.logger.info("Заполнение таблицы DBPP значением с datetime...OK")
                flag_rezult = True
        except sql3.Error as error_sql:
            ml.logger.error("Exception occurred", exc_info=True)
            viewCodeError (error_sql)
            flag_rezult = False
        # finally:
        #     if connectDB:
        #         connectDB.close()
        #         ml.logger.debug("Соединение с SQLite закрыто")
    else: flag_rezult = False
    return  flag_rezult


def selectPandQfromDBPP(item_counter, item_datetime=None,dateFrom=None, dateTo=None):
    flag_rezult = False
    dic_out_data = {}
    lst_pole = ['datetime','P_plus', 'P_minus', 'Q_plus', 'Q_minus']
    cursorDB = cfg.sql_base_conn.cursor()
    with cfg.sql_base_conn:
        # cursorDB.execute("""SELECT P_plus, P_minus, Q_plus, Q_minus FROM DBPP WHERE id_counter=? AND 
        #                                                                                 datetime = ? AND 
        #                                                                                 period_int ='30'""", (item_counter, item_datetime,))
        cursorDB.execute("""SELECT datetime, P_plus, P_minus, Q_plus, Q_minus FROM DBPP WHERE id_counter=? AND 
                                                                                        datetime >= ? AND
                                                                                        datetime <= ? AND
                                                                                        period_int ='30'
                                                                                        ORDER BY datetime ASC
                                                                                        """, (item_counter,dateFrom, dateTo))
        data = cursorDB.fetchall() 
    lst_out_data = []
    if data:
        # lst_out_data = []
        for num_row, item_row in enumerate(data):
            lst = []
            lst.append(int(item_row[0][:-15]))
            lst.append(int(item_row[0][5:-12]))
            lst.append(int(item_row[0][8:-9]))
            lst.append(int(item_row[0][11:-6]))
            lst.append(int(item_row[0][14:-3]))
            lst.append(    item_row[1])
            lst.append(    item_row[2])
            lst.append(    item_row[3])
            lst.append(    item_row[4])
            lst_out_data.append(lst)

            flag_rezult = True
    else:
        flag_rezult = False
        lst_out_data = []
    return flag_rezult, lst_out_data








# ------------------------------------------------------------------------------------
# ----------------- DBIC -------------------------------------------------------------
# ------------------------------------------------------------------------------------
    # id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     id_counter INTEGER NOT NULL,
    #     datetime timestamp,
    #     CurrentFaze1 TEXT,
    #     CurrentFaze2 TEXT,
    #     CurrentFaze3 TEXT,
    #     FOREIGN KEY (id_counter)  REFERENCES DBC (id) ON DELETE RESTRICT
    #     );
# ------------------------------------------------------------------------------------
def fill_TableDBIC_demo_value(nameFileDB:str):
    """
    заполнение таблицы DBIC демо-значениями      
    """
    ml.logger.info("Заполнение таблицы DBIC демо-значениями...")
    flag_rezult = False
    # nameFile_DBf = cfg.absDB_FILE
    with open(cfg.absTEST_DATA_IC_FILE, "r") as file:
        data = json.load(file)

    for item in data:
        item['datetime'] = datetime.datetime.strptime(item['datetime'], "%d/%m/%Y %H:%M")
    
    data2 = []
    data_values = []
    for item in data:
        data_values = []
        for key, val in item.items():
            data_values.append(val)
        data2.append(data_values)
    
    try:
        connectDB = sql3.connect(nameFileDB)
        cursorDB = connectDB.cursor()
        with connectDB:
            # cursorDB.executemany("""INSERT INTO DBIC (id_counter, datetime, CurrentFaze1, CurrentFaze2, CurrentFaze3) VALUES (?,?,?,?,?);""", cfg.data_list_demo_table_DBIC)
            cursorDB.executemany("""INSERT INTO DBIC (id, id_counter, datetime, 
                                                    CurrentFaze1, CurrentFaze2, CurrentFaze3, CurrentSum, 
                                                    PowerPFaze1,PowerPFaze2, PowerPFaze3, PowerPFazeSum,
                                                    PowerQFaze1,PowerQFaze2, PowerQFaze3, PowerQFazeSum,
                                                    PowerSFaze1,PowerSFaze2, PowerSFaze3, PowerSFazeSum,
                                                    KPowerFaze1,KPowerFaze2, KPowerFaze3, KPowerFazeSum,
                                                    EnergyTarif1,EnergyTarif2,EnergyTarif3,EnergyTarif4
                                                    ) VALUES (?,?,?,
                                                    ?,?,?,?,
                                                    ?,?,?,?,
                                                    ?,?,?,?,
                                                    ?,?,?,?,
                                                    ?,?,?,?,
                                                    ?,?,?,?);""", data2)
            connectDB.commit()
            ml.logger.info("Заполнение таблицы DBIC демо-значениями...OK")
            flag_rezult = True
    except sql3.Error as error_sql:
        ml.logger.error("Exception occurred", exc_info=True)
        viewCodeError (error_sql)
        flag_rezult = False
    finally:
        if connectDB:
            connectDB.close()
            ml.logger.debug("Соединение с SQLite закрыто")
    return flag_rezult


def insert_TableDBIC_value(nameFileDB:str, dictData: dict):
    """
    заполнение таблицы DBIC значением с datetime    
    """
    ml.logger.info("Заполнение таблицы DBIC значением с datetime...")
    dict_data = dictData.copy()
    flag_rezult = False

    if "id" in dict_data: 
        del dict_data["id"]
        dict_data['datetime'] = datetime.datetime.strptime(dict_data['datetime'], "%d/%m/%Y %H:%M")
        lst_data = []
        for key, val in dict_data.items():
            lst_data.append(val)
        # lst_data = dict_data.values()
    try:
        cursorDB = cfg.sql_base_conn.cursor()
        with cfg.sql_base_conn:
            # cursorDB.executemany("""INSERT INTO DBIC (id_counter, datetime, CurrentFaze1, CurrentFaze2, CurrentFaze3) VALUES (?,?,?,?,?);""", cfg.data_list_demo_table_DBIC)
            cursorDB.execute("""INSERT INTO DBIC ( id_counter, datetime, 
                                                    CurrentFaze1, CurrentFaze2, CurrentFaze3, CurrentSum, 
                                                    PowerPFaze1,PowerPFaze2, PowerPFaze3, PowerPFazeSum,
                                                    PowerQFaze1,PowerQFaze2, PowerQFaze3, PowerQFazeSum,
                                                    PowerSFaze1,PowerSFaze2, PowerSFaze3, PowerSFazeSum,
                                                    KPowerFaze1,KPowerFaze2, KPowerFaze3, KPowerFazeSum,
                                                    EnergyTarif1,EnergyTarif2,EnergyTarif3,EnergyTarif4
                                                    ) VALUES (?,?,
                                                    ?,?,?,?,
                                                    ?,?,?,?,
                                                    ?,?,?,?,
                                                    ?,?,?,?,
                                                    ?,?,?,?,
                                                    ?,?,?,?);""", lst_data)
            cfg.sql_base_conn.commit()
            ml.logger.info("Заполнение таблицы DBIC значением с datetime...OK")
            flag_rezult = True
    except sql3.Error as error_sql:
        ml.logger.error("Exception occurred", exc_info=True)
        viewCodeError (error_sql)
        flag_rezult = False
    # finally:
    #     if connectDB:
    #         connectDB.close()
    #         ml.logger.debug("Соединение с SQLite закрыто")
    return flag_rezult


def selectItemFromDBIC_all_param(item_counter, item_datetime, dateFrom=None, dateTo=None):
    cursorDB = cfg.sql_base_conn.cursor()
    with cfg.sql_base_conn:
        cursorDB.execute("""SELECT CurrentFaze1, CurrentFaze2, CurrentFaze3, CurrentSum, 
                                                    PowerPFaze1,PowerPFaze2, PowerPFaze3, PowerPFazeSum,
                                                    PowerQFaze1,PowerQFaze2, PowerQFaze3, PowerQFazeSum,
                                                    PowerSFaze1,PowerSFaze2, PowerSFaze3, PowerSFazeSum,
                                                    KPowerFaze1,KPowerFaze2, KPowerFaze3, KPowerFazeSum,
                                                    EnergyTarif1,EnergyTarif2,EnergyTarif3,EnergyTarif4
                         FROM DBIC WHERE id_counter=? AND datetime = ? """, (item_counter, item_datetime,))
        data = cursorDB.fetchall()    
    return data  

def selectItemFromDBIC_all_param_v2(item_counter, dateFrom=None, dateTo=None):
    lst_out_data = []
    cursorDB = cfg.sql_base_conn.cursor()
    with cfg.sql_base_conn:
        cursorDB.execute("""SELECT datetime, CurrentFaze1, CurrentFaze2, CurrentFaze3, CurrentSum, 
                                                    PowerPFaze1,PowerPFaze2, PowerPFaze3, PowerPFazeSum,
                                                    PowerQFaze1,PowerQFaze2, PowerQFaze3, PowerQFazeSum,
                                                    PowerSFaze1,PowerSFaze2, PowerSFaze3, PowerSFazeSum,
                                                    KPowerFaze1,KPowerFaze2, KPowerFaze3, KPowerFazeSum,
                                                    EnergyTarif1,EnergyTarif2,EnergyTarif3,EnergyTarif4
                                                    FROM DBIC 
                                                    WHERE   id_counter=? AND 
                                                            datetime >= ? AND
                                                            datetime <= ?
                                                            ORDER BY datetime ASC
                                                            """, (item_counter, dateFrom, dateTo))
        data = cursorDB.fetchall() 
    if data:
        lst_out_data = []
        for num_row, item_row in enumerate(data):
            lst = []
            # lst.append(int(item_row[0][:-15]))
            # lst.append(int(item_row[0][5:-12]))
            # lst.append(int(item_row[0][8:-9]))
            # lst.append(int(item_row[0][11:-6]))
            # lst.append(int(item_row[0][14:-3]))
            for i in range(0,25,1):
                lst.append(    item_row[i])
            # lst.append(    item_row[1])
            # lst.append(    item_row[2])
            # lst.append(    item_row[3])
            # lst.append(    item_row[4])
            lst_out_data.append(lst)

            flag_rezult = True
    else:
        flag_rezult = False
    return flag_rezult, lst_out_data 

