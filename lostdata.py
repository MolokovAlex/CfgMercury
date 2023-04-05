
import os

from PyQt5.QtCore import *
# from time import sleep
from datetime import datetime
import numpy as np
# from datetime import timedelta
# import queue
import sqlite3 as sql3
from datetime import date, timedelta
from datetime import datetime
import time
from time import sleep
import traceback
import sys

import modulVM.config as cfg
import modulVM.moduleLogging as ml
# import modulVM.moduleAppGUIQt as magqt
import modulVM.moduleProtocolMercury as mpm
import modulVM.moduleGeneral as mg
# import modulVM.moduleSQLite as msql


class FindLostDataThread(QObject):
    def __init__(self, name_file_DB):
        # QThread.__init__(self)
        ml.logger.info('поток FindLostData: инициализация')
        self.running =False
        self.name_file_DB = name_file_DB
        #  созданим подключение БД из потока
        try:
            self.connectDB = sql3.connect(self.name_file_DB, check_same_thread=False)
            self.cursor = self.connectDB.cursor()
            ml.logger.info('поток FindLostData: доступ к БД есть')
        except sql3.Error as error_sql:
            ml.logger.error("поток FindLostData: Exception occurred", exc_info=True)
            # viewCodeError (error_sql)
            rezult_delete = False
        # одновременно проверяем есть ли связь с БД и доастем спиское всех зарегистрированных счетчиков
        self.lstOfDic_Counters, self.rezult_getList = self.getListCounterDB()
        if self.rezult_getList: ml.logger.info('поток FindLostData: доступ к БД есть -2')
        # если связь с БД отсутствует
        else:
            ml.logger.error("поток FindLostData: ошибка доступа к БД - Exception occurred", exc_info=True)

    def run(self):
        ml.logger.info('поток FindLostDataThread стартовал')
        arr_timeshtamp = self.create_arr_segment_of_TimeAxes(self.lstOfDic_Counters, durationDay = 80)
        self.create_multiarr_timestamp_of_TimeAxes(self.lstOfDic_Counters, arr_timeshtamp)
        ml.logger.info('поток FindLostDataThread закнчил работу')


    # def veryfy_record_in_DBPP(self, lst_of_arr_timeshtamp:list, id_counter):
    #     # проверим наличие записи в DBPP по данному счетчику.
    #     # Штамп времени берем самый верхний (с индеском=0)
    #     arr_TimeAxis = lst_of_arr_timeshtamp[id_counter]
    #     rezult, data = msql.select_zero_Power_from_DBPP(id_counter=id_counter, date_time=arr_TimeAxis[0])
    #     if (not rezult) or (data[0] == 0):
    #         # если записи не существует или P_plus=0
    #         flag_existence = False
    #     else:
    #         # если запись существует
    #         flag_existence = True
    #     return flag_existence


    def create_arr_segment_of_TimeAxes(self, lst_of_dic_counters:list, durationDay:int):
        """создание одномерного массива временных штампов из прошлого, которые потом надо проверить на наличие в DBPP
        глубина массива в прошлое = durationDay
        """
        lst_of_arr_timeshtamp = []
        for numCounter, item_dic_Counter in enumerate(lst_of_dic_counters):
        # создание массива штампов времени с P_plus = 0 или отсутствующими
        # создадим массив временной оси начиная с текущей минуты до 3 суток в прошлое
            date_now = datetime.now()
            date_past = date_now - timedelta(days=durationDay)
            # date_past = date_past.replace(hour=23,  minute = 30)
            date_past = date_past.replace(hour=0,  minute = 0)
            lst_datetime_step30_full, lstsu_full, rezult = mg.createLstIntervalDateTime(dateFrom=date_past, dateTo=date_now, stepTime=30)
            arr_TimeAxis = np.array(lst_datetime_step30_full)
            lst_of_arr_timeshtamp.append(arr_TimeAxis)
        # return lst_of_arr_timeshtamp
        return arr_TimeAxis

    def create_multiarr_timestamp_of_TimeAxes(self, lstOfDic_Counters, arr_timeshtamp):
        """создание много-мерного массива временных штампов из прошлого, которых нет в DBPP в таблице БД
        """
        for numCounter, itemCounter in enumerate(lstOfDic_Counters):
            # ml.logger.debug(f'анализ: номер счетчика по списку = {numCounter}')
            net_adress_counter = int(itemCounter['net_adress'])
            id_counter = int(itemCounter['id'])
            ml.logger.info(f'поток FindLostData: анализ: номер счетчика по списку = {numCounter}, сететвой номер = {net_adress_counter}')
            # найдем на каком штампе времени остановились
            rezult_LT_LOSTDATAPP, data_LT_LOSTDATAPP = self.select_lastTime_in_LOSTDATAPP(id_counter)
            last_datetime = datetime.strptime(data_LT_LOSTDATAPP, "%Y-%m-%d %H:%M:%S")
            for numTimeshtamp, itemTimeshtamp in enumerate(arr_timeshtamp):
                
                # проверим наличие записи в DBPP по данному счетчику.
                rezult_zero_DBPP, dataDBPP = self.select_zero_Power_from_DBPP(id_counter, itemTimeshtamp)
                rezult_LOSTDATAPP, dataLOSTDATAPP = self.select_in_LOSTDATAPP(id_counter, itemTimeshtamp)
                if (not rezult_zero_DBPP) and (not rezult_LOSTDATAPP):
                    # если записи не существует в DBPP и нет такой записи в LOSTDATAPP
                    flag_existence = False
                    self.sleep(10)
                    self.add_in_LOSTDATAPP(id_counter, itemTimeshtamp)
                else:
                    # если запись существует
                    flag_existence = True
        return None
    
    def select_zero_Power_from_DBPP(self, id_counter, date_time):
        flag_rezult = False
        try:
            # cursorDB = cfg.sql_base_conn.cursor()
            with self.connectDB:
                self.cursor.execute("""SELECT P_plus FROM DBPP WHERE id_counter=? AND 
                                                                    datetime = ? AND
                                                                    period_int ='30'
                                                                    """, (id_counter, date_time))
                data = self.cursor.fetchall() 
            if data:
                flag_rezult = True
            else:
                flag_rezult = False
        except sql3.Error as error_sql:
            ml.logger.error("Exception occurred", exc_info=True)
            self.viewCodeError (error_sql)
            rezult = False
        return flag_rezult, data

    def select_lastTime_in_LOSTDATAPP(self, id_counter):
        flag_rezult = False
        try:
            # cursorDB = cfg.sql_base_conn.cursor()
            with self.connectDB:
                self.cursor.execute("""SELECT datetime FROM LOSTDATAPP WHERE id_counter=? ORDER BY datetime DESC;
                                                                    """, (id_counter,))
                dataDB = self.cursor.fetchall() 
            if dataDB:
                flag_rezult = True
                data = dataDB[0]
            else:
                flag_rezult = False
        except sql3.Error as error_sql:
            ml.logger.error("Exception occurred", exc_info=True)
            self.viewCodeError (error_sql)
            rezult = False
        return flag_rezult, data[0]

    def select_in_LOSTDATAPP(self, id_counter, date_time):
        flag_rezult = False
        try:
            # cursorDB = cfg.sql_base_conn.cursor()
            with self.connectDB:
                self.cursor.execute("""SELECT datetime FROM LOSTDATAPP WHERE id_counter=? AND 
                                                                    datetime = ?
                                                                    """, (id_counter, date_time))
                data = self.cursor.fetchall() 
            if data:
                flag_rezult = True
            else:
                flag_rezult = False
        except sql3.Error as error_sql:
            ml.logger.error("Exception occurred", exc_info=True)
            self.viewCodeError (error_sql)
            rezult = False
        return flag_rezult, data

    def add_in_LOSTDATAPP(self, id_counter, date_time):
        rezult = False
        # newNameCounter.pop('id')
        # a = newNameCounter.values()
        # lst_newNameCounter = []
        # for item in a:
        #     lst_newNameCounter.append(item)
        try:
            # cursorDB = cfg.sql_base_conn.cursor()
            with self.connectDB:
                    self.cursor.execute("""INSERT INTO LOSTDATAPP (id_counter, datetime) VALUES (?,?);""", (id_counter, date_time))
                    self.connectDB.commit()
                    rezult = True
        except sql3.Error as error_sql:
            ml.logger.error("Exception occurred", exc_info=True)
            self.viewCodeError (error_sql)
            rezult = False
        return rezult

    def getListCounterDB(self):
        rezult_get = False
        lst_counterDB = []       
        with self.connectDB:
            self.cursor.execute("""SELECT id, schem, name_counter_full, net_adress, manuf_number, manuf_data, klass_react, klass_act, nom_u, ku, ki, koefA, comment FROM DBC ORDER BY name_counter_full ASC""")
            b = self.cursor.fetchall()
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

    def viewCodeError (self, sql_error):
        print("поток: Ошибка при работе с sqlite", sql_error)
        print("Класс исключения: ", sql_error.__class__)
        print("Исключение", sql_error.args)
        print("Печать подробноcтей исключения SQLite: ")
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))

if __name__ == "__main__": 
    if not os.path.isdir(cfg.absLOG_DIR): 
        os.mkdir(cfg.absLOG_DIR)
    if not os.path.isdir(cfg.absDB_DIR): 
        os.mkdir(cfg.absDB_DIR)
    ml.setup_logging(cfg.absLOG_FILE)
    ml.logger.debug('---------------------------- запуск программы -------------------------------------')
    fldt = FindLostDataThread(cfg.absDB_FILE)
    fldt.run()
    