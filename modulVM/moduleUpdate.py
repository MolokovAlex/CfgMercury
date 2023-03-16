

import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import *
# from time import sleep
import sqlite3 as sql3
import modulVM.moduleAppGUIQt as magqt
import modulVM.config as cfg
import modulVM.moduleSQLite as msql
# import modulVM.moduleProtocolMercury as mpm
# import modulVM.moduleComThread as mct
import modulVM.moduleLogging as ml
# import modulVM.moduleGeneral as mg
# import modulVM.moduleParamSettingDataCounter as mpsdc




def createUpdate():
    # -------------------------------------------------------------------
    # update05032013
    # запись в БД кофф KU kI
    # отключить эти сроки на последющем update
    # msql.insert_kU_kI_in_DBC()

    # -------------------------------------------------------------------
    # update06032013
    # sql_create_table_SERVICE = """ CREATE TABLE IF NOT EXISTS SERVICE (
    #     id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
    #     updateVM TEXT,
    #     versionVM TEXT
    #     );
    #     """
    # создание служебной таблицы в БД
    # ml.logger.info("Создание служебной таблицы в БД")
    # FlagCreateTableDBf = False
    # try:
    #     cursorDB = cfg.sql_base_conn.cursor()
    #     with cfg.sql_base_conn:
    #         cursorDB.execute(sql_create_table_SERVICE)
    #         cfg.sql_base_conn.commit()
    # except sql3.Error as error_sql:
    #     ml.logger.error("Exception occurred", exc_info=True)
    #     msql.viewCodeError (error_sql)
    #     # rezult_edit = False 

    # try:
    #     cursorDB = cfg.sql_base_conn.cursor()
    #     with cfg.sql_base_conn:
    #         # запись в таблицу номера текущего апдейта
    #         cursorDB.execute("""INSERT INTO SERVICE (updateVM, versionVM)  VALUES ('060323', '1.060323');""")
    #         cfg.sql_base_conn.commit()  
    # except sql3.Error as error_sql:
    #     ml.logger.error("Exception occurred", exc_info=True)
    #     msql.viewCodeError (error_sql)
    #     # rezult_edit = False 
    # ml.logger.info("update_06032013 применен")     


# -------------------------------------------------------------------
    # update16032013
    # следующий апдейт



    # запись номера очередного апдейта в БД
    error = False
    try:
        cursorDB = cfg.sql_base_conn.cursor()
        with cfg.sql_base_conn:
            cursorDB.execute("""SELECT updateVM FROM SERVICE""")
            data = cursorDB.fetchall()
            if data:
                flag_found_current_update = False
                # пройдем по всем записям update -оф и проверим есть ли среди них текущий
                # Если есть - не применяем текущий апдейт и уходим
                # если нету - применяем апдейт
                for value_update in data:
                    if value_update[0] == '160323':
                        # программа уже прошла этот апдейт
                        flag_found_current_update = True
                        error = False
                        break
                    else:
                        flag_found_current_update = False
                # если апдейта так и не было найдено - сделаем его
                if not(flag_found_current_update):
                    # тело апдейта

                    cursorDB.execute("""UPDATE DBC SET name_counter_full="водоподготовка котельной+ бытовки мПГП" WHERE net_adress=3;""")
                    cfg.sql_base_conn.commit()


                    # запись в таблицу SERVICE номера текущего апдейта
                    cursorDB.execute("""INSERT INTO SERVICE (updateVM, versionVM)  VALUES ('160323', '1.160323');""")
                    cfg.sql_base_conn.commit() 
                    ml.logger.info("update_16032013 применен") 
                    error = False

            else:
                # если data пустые - таблица не заполнена, т.е. программа запускается с чистой БД
                cursorDB.execute("""INSERT INTO SERVICE (updateVM, versionVM)  VALUES ('160323', '1.160323');""")
                cfg.sql_base_conn.commit() 
                cursorDB.execute("""UPDATE DBC SET name_counter_full="водоподготовка котельной+ бытовки мПГП" WHERE net_adress=3;""")
                cfg.sql_base_conn.commit()
                ml.logger.info("БД SERVICE пуста... update_16032013 применен")
                error = False
    except sql3.Error as error_sql:
        ml.logger.error("Exception occurred", exc_info=True)
        msql.viewCodeError (error_sql)
        error = True
    
    if error:
        ml.logger.info("ошибка в применении update_16032013 ") 
    

    return None