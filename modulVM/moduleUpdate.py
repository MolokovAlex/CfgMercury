

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
    msql.insert_kU_kI_in_DBC()

    # -------------------------------------------------------------------
    # update06032013
    sql_create_table_SERVICE = """ CREATE TABLE IF NOT EXISTS SERVICE (
        id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
        update TEXT,
        version TEXT
        );
        """
    # создание служебной таблицы в БД
    ml.logger.info("Создание служебной таблицы в БД")
    FlagCreateTableDBf = False
    try:
        cursorDB = cfg.sql_base_conn.cursor()
        with cfg.sql_base_conn:
            cursorDB.execute(sql_create_table_SERVICE)
            cfg.sql_base_conn.commit()
    except sql3.Error as error_sql:
        ml.logger.error("Exception occurred", exc_info=True)
        msql.viewCodeError (error_sql)
        # rezult_edit = False 

    try:
        cursorDB = cfg.sql_base_conn.cursor()
        with cfg.sql_base_conn:
            # запись в таблицу номера текущего апдейта
            cursorDB.execute("""INSERT INTO SERVICE (update, version)  VALUES ('060323', '1.060323');""")
            cfg.sql_base_conn.commit()  
    except sql3.Error as error_sql:
        ml.logger.error("Exception occurred", exc_info=True)
        msql.viewCodeError (error_sql)
        # rezult_edit = False 
    ml.logger.info("update_06032013 применен")     

    # следующий апдейт
    # try:
    #     cursorDB = cfg.sql_base_conn.cursor()

    #     with cfg.sql_base_conn:
    #         cursorDB.execute("""SELECT update, version FROM SERVICE """)
    #         data = cursorDB.fetchall()
    # except sql3.Error as error_sql:
    #     ml.logger.error("Exception occurred", exc_info=True)
    #     msql.viewCodeError (error_sql)



    return None