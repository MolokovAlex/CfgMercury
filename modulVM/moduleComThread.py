from PyQt5.QtCore import *
import time
# from datetime import datetime
import datetime
from datetime import timedelta
# from datetime import timedelta
# import queue
import sqlite3 as sql3
import traceback
import sys

import modulVM.config as cfg
import modulVM.moduleLogging as ml
# import modulVM.moduleAppGUIQt as magqt
import modulVM.moduleProtocolMercury as mpm
# import modulVM.moduleGeneral as mg
# import modulVM.moduleSQLite as msql



################ раскомментировать в релизе ####  строки 22-23, 52-52
class CommunicationCounterThread(QThread):
# class CommunicationCounterThread(QObject):
    signal_progressRS = pyqtSignal(int)
    signal_error_open_connect_port = pyqtSignal()
    signal_error_connect_to_DB = pyqtSignal()
    signal_thread_is_working = pyqtSignal()
    signal_errorCount = pyqtSignal()
    

    def __init__(self, name_file_DB):
        QThread.__init__(self)
        ml.logger.debug('поток: инициализация')
        self.running =False
        self.name_file_DB = name_file_DB
        #  созданим подключение БД из потока
        self.connectDB = sql3.connect(self.name_file_DB, check_same_thread=False)
        self.cursor = self.connectDB.cursor()

        # залезем в БД для получкения списка счетчиков - чтобы каждые 3 минуты туда не лазить
        # одновременно проверяем есть ли связь с БД и доастем спиское всех зарегистрированных счетчиков
        self.lstOfDic_Counters, self.rezult_getList = self.getListCounterDB()
        if self.rezult_getList: ml.logger.info('поток: доступ к БД есть')
        # если связь с БД отсутствует
        else:
            #  если доступ к БД не произошел - сигнал в основную программу на вывод окна про ошибку
            # и сразу отключим опрос счетсчиков, чтобы не захлебнуться в этих сигналах каждый оборот цикла
            ml.logger.error("поток: ошибка доступа к БД - Exception occurred", exc_info=True)
            if not(cfg.MODE_QOBJECT): self.signal_error_connect_to_DB.emit()
            cfg.ON_TRANSFER_DATA_COUNTER = False

    ################ комментировать в релизе ####
    # def sleep(self, num):
    #     time.sleep(num)
    #     return None

    def stop_th(self):
        self.running = False
        ml.logger.debug(f'поток: self.running = {self.running}') 
        return None

    def find_3minute(self, past_minute):
        is_find = False
        while not(is_find):
            minute_now =  datetime.datetime.now().minute
            self.sleep(5)
            if minute_now != past_minute:
                if minute_now in [0,3,6,9,12,15,18,21,24,27,30,33,36,39,42,45,48,51,54,57]:
                    is_find = True
        return is_find

    def run(self):
        ml.logger.info(f"поток: версия = {cfg.VERSION}")
        ml.logger.debug('поток: старт')
        self.running =True
        count_error = 0
        # открываем порт IP или COM
        if mpm.connection_to_port():
            ml.logger.info('поток: успешное откр порта')
            if not(cfg.MODE_QOBJECT): self.signal_thread_is_working.emit()  #  сигнал о том что поток жив и не завис
            # считывание параметров счетчика  и запись в БД 
            self.reception_data_form_counter(self.read_ReadParam)
            while self.running:
                self.sleep(1)   # уменьшим скорость бесконечного цикла - сильно грузит процессор - введем паузы в 1 сек
                #  если константа опроса счетчиков установлена - пошел алгоритм опроса счетчиков
                past_minute =  datetime.datetime.now().minute

                #  поиск минут кратных 3 и запуск цикла опроса
                ml.logger.info('поток: ожидание наступления ближайшей 3-х минутки')
                if not(cfg.MODE_QOBJECT): self.signal_thread_is_working.emit()  #  сигнал о том что поток жив и не завис
                while not(self.find_3minute(past_minute)):
                    a=0
                if not(cfg.MODE_QOBJECT): self.signal_progressRS.emit(0)
                if not(cfg.MODE_QOBJECT): self.signal_thread_is_working.emit()  #  сигнал о том что поток жив и не завис
                ml.logger.debug('--------------------------------поток: старт опроса!') # - {str(date_time_now)}")
                datetime_start =  datetime.datetime.now()
                minute_now = datetime_start.minute
                mpm.fn_fixInstantlyValue_UDP()
                mpm.fn_fixInstantlyValue_UDP()
                self.reception_data_form_counter(self.read_InstantlyValue)
                if not(cfg.MODE_QOBJECT): self.signal_thread_is_working.emit()  #  сигнал о том что поток жив и не завис
                # !!!!!!!!!!!!!!!!! ТОЛЬКО ДЛЯ ОТЛАДКИ ТЕСТ Watchdog !!!!!!!!!!! в релизе удалить!!!!!
                # ml.logger.debug('имитация зависания потока для проверки watchdog')
                # self.sleep(310000)
                ## !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                
                # в конеце опроса счетчиков если хватает времени до следующей3-х минутки вытянем немного данных из истории счетчиков 
                # datetime_now =  datetime.datetime.now()
                # datetime_now=datetime_now.replace(second=0, microsecond=0)
                # if self.how_much_time_is_left(datetime_now):

                # вытянем немного данных из истории счетчиков 
                self.reception_data_form_counter(self.read_old_record_from_DBPP_full)

                # конец опроса
                if not(cfg.MODE_QOBJECT): 
                    self.signal_progressRS.emit(100)
                    self.signal_thread_is_working.emit()  #  сигнал о том что поток жив и не завис
                    self.signal_progressRS.emit(0)
                past_minute = minute_now
        else:
            #  если порт не открылся - сигнал в основную программу на вывод окна про ошибку
            # и сразу отключим опрос счетсчиков, чтобы не захлебнуться в этих сигналах каждый оборот цикла
            ml.logger.error("поток: ошибка доступа к порту - Exception occurred", exc_info=True)
            if not(cfg.MODE_QOBJECT): self.signal_error_open_connect_port.emit()
            self.sleep(30)

    def read_old_record_from_DBPP_full(self, itemCounter):#,datetime_start):
        """ считывание истории профиля мощности счетчиков и запись в БД 
        """

        net_adress_count = int(itemCounter['net_adress'])
        id_counter = int(itemCounter['id'])

        ml.logger.info(f"---------------поток: Опрос ИСТОРИИ профиля мощности счетчика с NetAdress= {net_adress_count}-----------------")

        # если в таблице LOSTDATAPP вместо адреса стоит значение по умолчанию 0 - считаем со счетчика адрес последней записи профиля и положим в LOSTDATAPP
        rezult_LOSTDATAPP, adress = self.read_record_from_LOSTDATAPP(id_counter)
        if rezult_LOSTDATAPP:
            if adress == 0:
                adr_last_record,  rezult = mpm.fn_ReadLastRecordMassProfilPower(net_adress_count)
                if rezult :
                    rezult = self.update_adress_in_LOSTDATAPP(id_counter, adr_last_record)
                    if rezult: 
                        ml.logger.debug(f"поток: обновлено значение adr_last_record= {adr_last_record} в БД LOSTDATAPP")
                        adress = adr_last_record
            # считываем по этому адресу из счетчика - получаем словарь с полями datetime и P+...
            # проверяем есть ли такой datetime в DBPP
            # если есть - update запись в DBPP
            # если нет - insert запись в DBPP

            for itter in range (1,7,1):
                dic_data_pp, rezult_ReadRecordMassProfilPower = mpm.fn_ReadRecordMassProfilPower(itemCounter, adress) #adress, id_counter)
                dt = dic_data_pp['datetime']
                ml.logger.debug(f"поток: считывание записи adr = {adress}, datetime = {dt}")
                if rezult_ReadRecordMassProfilPower:
                    rezult_is_record, data = self.is_record_from_DBPP(id_counter, dt)
                    if rezult_is_record:
                        ml.logger.debug(f"поток: update в таблицу DBPP")
                        self.update_TableDBPP_value(dic_data_pp)
                    else:
                        ml.logger.debug(f"поток: insert в таблицу DBPP")
                        self.insert_TableDBPP_value(dic_data_pp)
                    # ml.logger.debug(f"поток: удаление записи из LOSTDATAPP")
                    # self.delete_record_in_LOSTDATAPP(id_record)
    
                    # уменьшаем адрес и записываем его в LOSTDATAPP
                    adress = adress - 0x0010
                    if adress <= 0x0010:
                        ml.logger.debug("поток: дошли до 0х0010")
                        adress = 0
                    rezult = self.update_adress_in_LOSTDATAPP(id_counter, adress)

                        #
                        # count_error = 0
                        # mpm.fn_CloseCanalConnection(net_adress_count)
                # else:
                #     count_error +=1
                #     ml.logger.debug(f'----------------------------------------------------count_error = {count_error} ')
                #     if count_error > 50: 
                #         self.stop_th()
                #         ml.logger.error(" поток: посылка сигнала на пере-сброс потока по ошибкам")
                #         if not(cfg.MODE_QTHREAD): self.signal_errorCount.emit()  #  при большом количестве ошибок - перезагрузим поток
                # if not(cfg.MODE_QTHREAD): self.signal_progressRS.emit(numCounter) #  пусть порядковый номер счетчика в списке будет процентом выполненного объема цикла опроса
        return None
    
    def is_record_from_DBPP(self, id_counter, date_time):
        flag_rezult = False
        try:
            # cursorDB = cfg.sql_base_conn.cursor()
            with self.connectDB:
                self.cursor.execute("""SELECT datetime FROM DBPP WHERE id_counter=? AND 
                                                                    datetime = ? AND
                                                                    period_int ='30'
                                                                    """, (id_counter, date_time))
                data = self.cursor.fetchone() 
            if data:
                flag_rezult = True
            else:
                flag_rezult = False
        except sql3.Error as error_sql:
            ml.logger.error("Exception occurred", exc_info=True)
            self.viewCodeError (error_sql)
            flag_rezult = False
        return flag_rezult, data

    def delete_record_in_LOSTDATAPP(self, id_record):
        rezult = False
        try:
            cursorDB = cfg.sql_base_conn.cursor()
            with cfg.sql_base_conn:
                    cursorDB.execute("""DELETE FROM LOSTDATAPP WHERE id=?;""", (id_record,))
                    cfg.sql_base_conn.commit()
                    rezult = True
        except sql3.Error as error_sql:
            ml.logger.error("Exception occurred", exc_info=True)
            self.viewCodeError (error_sql)
            rezult = False
        return rezult


    def select_one_record_datetime_from_LOSTDATAPP(self, id_counter):#, date_time):
        flag_rezult = False
        id_record = 0
        dt = None
        adress = 0
        try:
            # cursorDB = cfg.sql_base_conn.cursor()
            with self.connectDB:
                self.cursor.execute("""SELECT id, id_counter, datetime, adress FROM LOSTDATAPP WHERE id_counter=? 
                                                                    ORDER BY datetime DESC
                                                                    """, (id_counter,))
                # data = self.cursor.fetchall() 
                data = self.cursor.fetchone()
            if data:
                id_record, id_counter, dt, adress = data 
                flag_rezult = True
            else:
                flag_rezult = False
        except sql3.Error as error_sql:
            ml.logger.error("Exception occurred", exc_info=True)
            self.viewCodeError (error_sql)
            flag_rezult = False
        return flag_rezult, id_record, id_counter, dt, adress
    
    def read_record_from_LOSTDATAPP(self, id_counter):#, date_time):
        rezult = False
        # id_record = 0
        # dt = None
        adress = 0
        try:
            # cursorDB = cfg.sql_base_conn.cursor()
            with self.connectDB:
                self.cursor.execute("""SELECT adress FROM LOSTDATAPP WHERE id_counter=? 
                                                                    """, (id_counter,))
                data = self.cursor.fetchone()
            if data:
                adress = data[0] 
                rezult = True
            else:
                rezult = False
        except sql3.Error as error_sql:
            ml.logger.error("Exception occurred", exc_info=True)
            self.viewCodeError (error_sql)
            rezult = False
        return rezult, adress
    
    def reception_data_form_counter(self, function_for_counter):
        """ тест канал связи, открытие канала связи, применение функции _______ для связи со счетчиками и закрытие канала связи
        """
        count_error = 0
        for numCounter, itemCounter in enumerate(self.lstOfDic_Counters):
            net_adress_count = int(itemCounter['net_adress'])
            # if True:
            # !!!!!!!!!!!!!!!!! ТОЛЬКО ДЛЯ ОТЛАДКИ   в релизе удалить!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            # if not(cfg.MODE_DEBUG) or (cfg.MODE_DEBUG and (net_adress_count in [255,254,136,77])):
            # if not(cfg.MODE_ONLY_DEBUG_COUNTER) or (cfg.MODE_ONLY_DEBUG_COUNTER and (net_adress_count in [255,254,136,77])):
            if not(cfg.MODE_ONLY_DEBUG_COUNTER) or (cfg.MODE_ONLY_DEBUG_COUNTER and (net_adress_count in [136,77])):
            # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                ml.logger.info(f"---------------поток: Опрос счетчика с NetAdress= {net_adress_count}-----------------")
                if mpm.test_canal_connection(net_adress_count):
                    if mpm.open_canal_connection_level1(net_adress_count):
                        # считывание datetime счетчика с адреса 0x0010 и запись в DBC
                        # adr_0x0010 = 0x0010
                        # dic_data_pp_0x0010, rezult_ReadRecordMassProfilPower = mpm.fn_ReadRecordMassProfilPower(itemCounter, adr_0x0010)
                        # if rezult_ReadRecordMassProfilPower:
                        #     datetime_adr0 =  dic_data_pp_0x0010['datetime']
                        #     itemCounter['datetime_adr0'] = dic_data_pp_0x0010['datetime']
                        #     ml.logger.info(f'поток: запись в DBC datetime_adr0={datetime_adr0}')
                        #     self.editCounterDB(itemCounter)

                        function_for_counter(itemCounter)
                        #
                        count_error = 0
                        mpm.fn_CloseCanalConnection(net_adress_count)
                else:
                    count_error +=1
                    ml.logger.debug(f'----------------------------------------------------count_error = {count_error} ')
                    if count_error > 50: 
                        self.stop_th()
                        ml.logger.error(" поток: посылка сигнала на пере-сброс потока по ошибкам")
                        if not(cfg.MODE_QOBJECT): self.signal_errorCount.emit()  #  при большом количестве ошибок - перезагрузим поток
                if not(cfg.MODE_QOBJECT): self.signal_progressRS.emit(numCounter) #  пусть порядковый номер счетчика в списке будет процентом выполненного объема цикла опроса
        return None

    def getListCounterDB(self):
        rezult = False
        lst_of_dict_counterDB = []       
        with self.connectDB:
            self.cursor.execute("""SELECT id, schem, name_counter_full, 
                                net_adress, manuf_number, manuf_data, 
                                klass_react, klass_act, nom_u, ku, ki, 
                                koefA, datetime, adress_last_record, datetime_adr0, comment 
                                FROM DBC 
                                ORDER BY net_adress ASC""")
            dataDB = self.cursor.fetchall()
            if dataDB:
                lst_of_dict_counterDB = []
                dict_counter = {}
                for item in dataDB:
                    dict_counter=dict(zip(cfg.lst_name_poles_DBC, item))
                    lst_of_dict_counterDB.append(dict_counter)
                    dict_counter = {}
                rezult = True
            else:
                rezult = False
        return lst_of_dict_counterDB, rezult
    
    def editCounterDB(self, counter:dict):
        rezult = False

        edited_counter = counter.copy()
        id_counter = int(edited_counter['id'])
        edited_counter.pop('id')

        values_edited_counter = edited_counter.values()
        lst_newNameCounter = []
        for item in values_edited_counter:
            lst_newNameCounter.append(item)
        lst_newNameCounter.append(id_counter)
        try:
            with self.connectDB:
                    self.cursor.executemany("""UPDATE DBC SET schem=?, name_counter_full=?, 
                                            net_adress=?, manuf_number=?, manuf_data=?, 
                                            klass_react=?, klass_act=?, nom_u=?, ku=?, 
                                            ki=?, koefA=?, datetime=?, adress_last_record=?, datetime_adr0=?,
                                            comment=? 
                                            WHERE id=?;""", (lst_newNameCounter,))
                    self.connectDB.commit()
                    rezult = True
        except sql3.Error as error_sql:
            ml.logger.error("поток: Exception occurred", exc_info=True)
            self.viewCodeError (error_sql)
            rezult = False
        return rezult


    def insert_TableDBIC_value(self, dic_data_DBIC: dict):
        """
        заполнение таблицы DBIC значением с datetime    
        """
        # ml.logger.debug("поток: Заполнение таблицы DBIC значением с datetime...")
        dict_data = dic_data_DBIC.copy()
        rezult = False
        if "id" in dict_data: 
            del dict_data["id"]
            dict_data['datetime'] = datetime.datetime.strptime(dict_data['datetime'], "%d/%m/%Y %H:%M")
            lst_data = []
            # lst_data = dict_data.values()
            for key, val in dict_data.items():
                lst_data.append(val)
            # for val in dict_data.values():
            #     lst_data.append(val)
        
                # проверим есть ли такой датавремя уже в таблице у этого счетчика
                # если есть - делаем update, если нет - insert
            try:
                with self.connectDB:
                    self.cursor.execute("""SELECT datetime
                                                FROM DBIC 
                                                WHERE   id_counter=? AND 
                                                        datetime = ?
                                                        """, (dict_data['id_counter'], dict_data['datetime']))
                    data = self.cursor.fetchone() 
                    if data:
                        # update
                        self.cursor.execute("""UPDATE DBIC SET 
                                                                CurrentFaze1=?, CurrentFaze2=?, CurrentFaze3=?, CurrentSum=?, 
                                                                PowerPFaze1=?,PowerPFaze2=?, PowerPFaze3=?, PowerPFazeSum=?,
                                                                PowerQFaze1=?,PowerQFaze2=?, PowerQFaze3=?, PowerQFazeSum=?,
                                                                PowerSFaze1=?,PowerSFaze2=?, PowerSFaze3=?, PowerSFazeSum=?,
                                                                KPowerFaze1=?,KPowerFaze2=?, KPowerFaze3=?, KPowerFazeSum=?,
                                                                EnergyTarif1=?,EnergyTarif2=?,EnergyTarif3=?,EnergyTarif4=? 
                                                WHERE   id_counter=? AND datetime = ?;""", (dict_data['CurrentFaze1'], dict_data['CurrentFaze2'], dict_data['CurrentFaze3'], dict_data['CurrentSum'], 
                                                                dict_data['PowerPFaze1'],dict_data['PowerPFaze2'], dict_data['PowerPFaze3'], dict_data['PowerPFazeSum'],
                                                                dict_data['PowerQFaze1'],dict_data['PowerQFaze2'], dict_data['PowerQFaze3'], dict_data['PowerQFazeSum'],
                                                                dict_data['PowerSFaze1'],dict_data['PowerSFaze2'], dict_data['PowerSFaze3'], dict_data['PowerSFazeSum'],
                                                                dict_data['KPowerFaze1'],dict_data['KPowerFaze2'], dict_data['KPowerFaze3'], dict_data['KPowerFazeSum'],
                                                                dict_data['EnergyTarif1'],dict_data['EnergyTarif2'],dict_data['EnergyTarif3'],dict_data['EnergyTarif4'], 
                                                                dict_data['id_counter'], dict_data['datetime']))
                        self.connectDB.commit()
                        ml.logger.info(f"поток: update таблицы DBIC значением с datetime={dict_data['datetime']}...OK")
                        rezult = True
                    else:
                        # insert
                        self.cursor.execute("""INSERT INTO DBIC ( id_counter, datetime, 
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
                        self.connectDB.commit()
                        ml.logger.info(f"поток: insert таблицы DBIC значением с datetime={dict_data['datetime']}...OK")
                        rezult = True
            except sql3.Error as error_sql:
                ml.logger.error("поток: Exception occurred", exc_info=True)
                self.viewCodeError (error_sql)
                rezult = False
        return rezult

    def insert_TableDBPP_value(self, dictData: dict):
        """
        заполнение таблицы DBPP значением с datetime
        """
        # ml.logger.info("поток: Заполнение таблицы DBPP значением с datetime")
        dict_data = dictData.copy()
        flag_rezult = False

        if "id" in dict_data: 
            del dict_data["id"]
            dict_data['datetime'] = datetime.datetime.strptime(dict_data['datetime'], "%d/%m/%Y %H:%M")#.timestamp()
            lst_data = []
            for key, val in dict_data.items():
                lst_data.append(val)
            try:
                with self.connectDB:
                    self.cursor.execute("""INSERT INTO DBPP (id_counter, datetime, period_int, 
                                                    P_plus, P_minus, Q_plus, Q_minus
                                                    ) VALUES (?,?,?,?,?,?,?);""", lst_data)
                    self.connectDB.commit()
                    ml.logger.info(f"поток: Заполнение таблицы DBPP значением с datetime {dict_data['datetime']}...OK")
                    flag_rezult = True
            except sql3.Error as error_sql:
                ml.logger.error("поток: Exception occurred", exc_info=True)
                self.viewCodeError (error_sql)
                flag_rezult = False
        else: flag_rezult = False
        return  flag_rezult
    
    


    def update_TableDBPP_value(self, dictData: dict):
        """
        обновление в таблице DBPP записи
        """
        dict_data = dictData.copy()
        flag_rezult = False

        if "id" in dict_data: 
            del dict_data["id"]
            dict_data['datetime'] = datetime.datetime.strptime(dict_data['datetime'], "%d/%m/%Y %H:%M")#.timestamp()
            # lst_data = []
            # for key, val in dict_data.items():
            #     lst_data.append(val)
            try:
                with self.connectDB:
                    # self.cursor.execute("""UPDATE DBPP SET P_plus=?, P_minus=?, Q_plus=?, Q_minus=?
                    self.cursor.execute("""UPDATE DBPP SET P_plus=?, P_minus=?, Q_plus=?, Q_minus=? 
                                            WHERE id_counter=? AND datetime=?;
                                            """, (dict_data['P_plus'], dict_data['P_minus'], dict_data['Q_plus'], dict_data['Q_minus'], 
                                                  dict_data['id_counter'], dict_data['datetime']))
                    self.connectDB.commit()
                    ml.logger.info(f"поток: UPDATE таблицы DBPP значением с datetime {dict_data['datetime']}...OK")
                    flag_rezult = True
            except sql3.Error as error_sql:
                ml.logger.error("поток: Exception occurred", exc_info=True)
                self.viewCodeError (error_sql)
                flag_rezult = False
        else: flag_rezult = False
        return  flag_rezult

    def read_ReadParam(self, itemCounter):
        """ Cчитывание параметров счетчика 
            Arg:
            net_adress_count:int - сетевой номер счетчика
            itemCounter:dic - словарь с полями БД счетчика    
        """
        net_adress_count = int(itemCounter['net_adress'])
        # id_counter = int(itemCounter['id'])
        dic_data, rezult_ReadParam_SerND = mpm.fn_ReadParam_SerND(net_adress_count, itemCounter)
        if rezult_ReadParam_SerND: 
            dic_data, rezult_ReadParam_KoefUI = mpm.fn_ReadParam_KoefUI(net_adress_count, dic_data)
            if rezult_ReadParam_KoefUI:
                # ml.logger.debug(f'поток: считывание записи по адресу 0х0010')
                # adr_0x0010 = 0x0010
                # id_counter = dic_data['id']
                # net_adress_count = dic_data['net_adress']
                # dic_data_pp_0x0010, rezult_ReadRecordMassProfilPower = mpm.fn_ReadRecordMassProfilPower(net_adress_count, adr_0x0010, id_counter)
                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                # dic_data['datetime_adr0'] = dic_data_pp_0x0010['datetime']
                # ml.logger.info(f"поток: Начало памяти содержит штамп времени = {dic_data_pp_0x0010['datetime']}")
                dic_data, rezult_ReadParam_Variant = mpm.fn_ReadParam_VariantNew(net_adress_count, dic_data)
                if rezult_ReadParam_Variant:
                    ml.logger.info('поток: запись в таблицу данных счетчиков DBC_new protocol')
                    self.editCounterDB(dic_data)    # дополнение параметров счетчика из БД считанными параметрами из счетчика
                else:
                    ml.logger.debug("поток: не удалось получить параметры: коэфициент А счетчика по новому протоколу")
                    dic_data, rezult_ReadParam_Variant = mpm.fn_ReadParam_VariantOld(net_adress_count, dic_data)
                    if rezult_ReadParam_Variant:
                        ml.logger.info('поток: запись в таблицу данных счетчиков DBC_old protocol')
                        self.editCounterDB(dic_data)
                    else:
                        ml.logger.error("поток: не удалось получить параметры: коэфициент А счетчика ни по старому, ни по новому протоколу")
            else:
                ml.logger.error("поток: не удалось получить параметры: коэфициенты KU и KI счетчика")
        else:
            ml.logger.error("поток: не удалось получить параметры: серийный номер и дату выпуска счетчика")
        return None


    def read_InstantlyValue(self, itemCounter):
        """ Считывание мгновенных значений и запись в БД
            Arg:
            net_adress_count:int - сетевой номер счетчика
            itemCounter:dic - словарь с полями БД счетчика
        """
        # net_adress_count = int(itemCounter['net_adress'])
        # сделаем словарь для записи строки в DBIC, словарь будем заполнять в каждой фукции, которая считывает мгн значения
        dic_data_DBIC = cfg.dic_template_DBIC.copy()
        # rezult_fix_datetime = mpm.fn_fixInstantlyValue(net_adress_count)
        # if rezult_fix_datetime:
        if True:
            dic_data_DBIC, rezult_ReadInstantlyValue_TimeFix = mpm.fn_ReadInstantlyValue_TimeFix(dic_data_DBIC, itemCounter)
            if rezult_ReadInstantlyValue_TimeFix: 
                dic_data_DBIC, rezult_ReadInstantlyValue_I = mpm.fn_ReadInstantlyValue_I(dic_data_DBIC, itemCounter)
                if rezult_ReadInstantlyValue_I:
                    dic_data_DBIC, rezult_ReadInstantlyValue_PowerP = mpm.fn_ReadInstantlyValue_PowerP(dic_data_DBIC, itemCounter)
                    if rezult_ReadInstantlyValue_PowerP:
                        dic_data_DBIC, rezult_ReadInstantlyValue_PowerQ = mpm.fn_ReadInstantlyValue_PowerQ(dic_data_DBIC, itemCounter)
                        if rezult_ReadInstantlyValue_PowerQ:
                            dic_data_DBIC, rezult_ReadInstantlyValue_Cos = mpm.fn_ReadInstantlyValue_Cos(dic_data_DBIC, itemCounter)
                            if rezult_ReadInstantlyValue_Cos:
                                self.insert_TableDBIC_value(dic_data_DBIC)
                            else:
                                ml.logger.error("поток: не удалось считать зафиксировные значения мгн значений CosF счетчика")
                        else:
                            ml.logger.error("поток: не удалось считать зафиксировные значения мгн значений PowerQ счетчика")
                    else:
                        ml.logger.error("поток: не удалось считать зафиксировные значения мгн значений PowerP счетчика")
                else:
                    ml.logger.error("поток: не удалось считать зафиксировные значения мгн значений токов счетчика")
            else:
                ml.logger.error("поток: не удалось считать зафиксировные дату и время мгн значений счетчика")
        # else:
        #     ml.logger.error("поток: не удалось счетчику зафиксировать мгн значения")
        return None

    def viewCodeError (self, sql_error):
        print("поток: Ошибка при работе с sqlite", sql_error)
        print("Класс исключения: ", sql_error.__class__)
        print("Исключение", sql_error.args)
        print("Печать подробноcтей исключения SQLite: ")
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))
    
    def update_adress_in_LOSTDATAPP(self, id_counter, adr):
        rezult = False
        # newNameCounter.pop('id')
        # a = newNameCounter.values()
        # lst_newNameCounter = []
        # for item in a:
        #     lst_newNameCounter.append(item)
        try:
            # cursorDB = cfg.sql_base_conn.cursor()
            with self.connectDB:
                    self.cursor.execute("""UPDATE LOSTDATAPP SET adress=? WHERE id_counter=?;""", (adr, id_counter))
                    self.connectDB.commit()
                    rezult = True
        except sql3.Error as error_sql:
            ml.logger.error("Exception occurred", exc_info=True)
            self.viewCodeError (error_sql)
            rezult = False
        return rezult
    



    # def select_zero_Power_from_DBPP(self, id_counter, dict_data):
    #     flag_rezult = False
    #     date_time = datetime.datetime.strptime(dict_data['datetime'], "%d/%m/%Y %H:%M")
    #     try:
    #         with self.connectDB:
    #             self.cursor.execute("""SELECT datetime FROM DBPP WHERE id_counter=? AND 
    #                                                                 datetime = ? AND
    #                                                                 period_int ='30'
    #                                                                 """, (id_counter, date_time))
    #             data = self.cursor.fetchall() 
    #         if data:
    #             flag_rezult = True
    #             ml.logger.debug("поток: запись есть в DBPP")
    #         else:
    #             flag_rezult = False
    #             ml.logger.debug("поток: запись НЕТ в DBPP")
    #     except sql3.Error as error_sql:
    #         ml.logger.error("Exception occurred", exc_info=True)
    #         self.viewCodeError (error_sql)
    #         flag_rezult = False
    #     return flag_rezult, data
    

    # def how_much_time_is_left(self, datetimeStart):
    #     """ функция, определяющую сколько времени осталось до начала 3-минутки.
    #     datetimeStart - во сколько начался опрос счетчиков
    #     """
    #     leftTime = 0
    #     date_now =  datetime.datetime.now()
    #     leftTime = date_now - datetimeStart + timedelta(minutes=3)
    #     if leftTime > (timedelta(seconds=30)): 
    #         flag_HaveTime = True
    #     else:
    #         flag_HaveTime = False
    #     ml.logger.debug(f'поток: осталось {leftTime} мин до ближайшей 3-х минутки')
    #     return flag_HaveTime
    
    # def select_listDateTime_in_DBPP(self, date_now,date_past):
    #     rezult = False
    #     try:
            
    #         with self.connectDB:
    #             self.cursor.execute("""SELECT id_counter, datetime FROM DBPP WHERE  
    #                                                         datetime <= ? AND
    #                                                         datetime >= ? ORDER BY datetime DESC;
    #                                                                 """, (date_now,date_past ))
    #             # self.cursor.execute("""SELECT id_counter, datetime FROM DBPP WHERE  
    #             #                                             datetime <= ? AND
    #             #                                             datetime >= ? ORDER BY datetime ASC;
    #             #                                                     """, (date_now,date_past ))
    #                                                                 # ASC
    #             dataDB = self.cursor.fetchall() 
    #         if dataDB:
    #             rezult = True
    #         else:
    #             rezult = False
    #     except sql3.Error as error_sql:
    #         ml.logger.error("Exception occurred", exc_info=True)
    #         self.viewCodeError (error_sql)
    #         rezult = False
    #     return rezult, dataDB



    # def create_listOfDict_loss_datetime_from_DBPP(self, date_time_Start):
    #     """ получим список datetime по всем счетчикам глубиной 80 суток с сортировкой по уменьшению
    #     """
    #     rezult = False
    #     dictt = dict()
    #     date_past = date_time_Start - timedelta(days=80)
    #     date_past = date_past.replace(hour=0,  minute = 0, second=0, microsecond=0)
    #     rezult_select_listDateTime, dataDBPP = self.select_listDateTime_in_DBPP(date_time_Start,date_past)
    #     if dataDBPP:
    #         # перобразуем dataDBPP в словарь {ключ это id_counter: список потерянных штампов датавремени}
            
    #         for tuple_val in dataDBPP:
    #             list_val = list(tuple_val)
    #             key = list_val[0]
    #             if key in dictt.keys():
    #                 l_v = dictt[key]
    #                 list_val.pop(0)
    #                 l_v.append(list_val[0])
    #                 dictt[key] = l_v
    #             else:

    #                 list_val.pop(0)
    #                 dictt[key] = list_val
    #     return dictt
 

    # def read_old_record_from_DBPP(self, net_adress_count, id_counter, date_time_Start, data):
    #     num_recordPP = 0    # счетчик количества успешно вынутых и записаннных в БД записей
        
    #     ml.logger.debug(f'поток: считывание записи по адресу 0х0010')
    #     adr_0x0010 = 0x0010
    #     dic_data_pp_0x0010, rezult_ReadRecordMassProfilPower = mpm.fn_ReadRecordMassProfilPower(net_adress_count, adr_0x0010, id_counter)
    #     ml.logger.info(f"поток: Начало памяти содержит штамп времени = {dic_data_pp_0x0010['datetime']}")
        
    #     # если не получим даташтамп из адреса 0х0010 - нет смысла что-то делать дальше
    #     if not rezult_ReadRecordMassProfilPower:    return None
    #     #  пройдемся по временной оси глубиной в 80 суток 
    #     # ищем отстутсвующие в списке от DBPP штампы datetime
    #     date_past = date_time_Start - timedelta(days=80)
    #     date_past = date_past.replace(hour=0,  minute = 0, second=0, microsecond=0)
    #     newdatetime = date_time_Start.replace(minute = 0, second=0, microsecond=0)
    #     flag_existence = False
    #     while newdatetime >= date_past:
    #         for index_data in range(0, len(data),1):
    #             if datetime.datetime.strptime(data[index_data],"%Y-%m-%d %H:%M:%S")  == newdatetime:
    #                 # если штамп времени newdatetime оси совпадает со элементом списка data[]
    #                 # переходим к следующему штампу newdatetime                    
    #                 flag_existence = True
    #                 break
    #             else:
    #                 # это не тот штамп времени в списке из БД
    #                 flag_existence = False
    #         if not flag_existence:
    #             ml.logger.debug(f'поток: штамп времени {newdatetime} так и не был найден в DBPP')
    #             # если штамп времени newdatetime так и не был найден - запросим его у счетчика
    #             # запрашиваем у счетчика данные для DBPP на дату newdatetime
    #             # если записи не существует в DBPP
    #             # считываем из счетчика
    #             # рассчитываем адрес
    #             # узнаем длительность интервала времени от штампа адреса 0x0010 до требуемой даты newdatetime
    #             interval_of_time = newdatetime - datetime.datetime.strptime(dic_data_pp_0x0010['datetime'], "%d/%m/%Y %H:%M") #- dic_data_pp['datetime']
    #             # ml.logger.debug(f'{interval_of_time} - длительность интервала времени  от штампа адреса 0x0010={dic_data_pp_0x0010}  до требуемой даты newdatetime= {newdatetime} ')
    #             step_of_time = int(interval_of_time/(timedelta(seconds=30*60)))     # 30*60=1800 секунд = 30 мин
    #             adr_newdatetime = 0x0010+ step_of_time*0x0010
    #             # ml.logger.debug(f'step_of_time = {step_of_time} ')
    #             # ml.logger.debug(f'adr_newdatetime = {adr_newdatetime} ')
    #             if adr_newdatetime <= 0x0010: 
    #                 ml.logger.debug("поток: в вычислении адреса дошли до 0х0010")
    #                 return None # в вычислении адреса дошли до 0х0010
    #             # считываем и добавляем в DBPP
    #             ml.logger.debug(f"поток: считывание предыдущюю запись профиля adr = {adr_newdatetime}")
    #             dic_data_pp, rezult_ReadRecordMassProfilPower = mpm.fn_ReadRecordMassProfilPower(net_adress_count, adr_newdatetime, id_counter)
                
    #             #  если отметка на оси времени совпадает с даташтампом из счетчика
    #             # if (rezult_ReadRecordMassProfilPower) and (newdatetime == dict_dataDT):
    #             if rezult_ReadRecordMassProfilPower:
    #                 dict_dataDT = datetime.datetime.strptime(dic_data_pp['datetime'], "%d/%m/%Y %H:%M")
    #                 if newdatetime == dict_dataDT:
    #                     rezult_zero_DBPP, dataDBPP = self.select_zero_Power_from_DBPP(id_counter, dic_data_pp)
    #                     if not rezult_zero_DBPP:
    #                         self.insert_TableDBPP_value(dic_data_pp)
    #                         num_recordPP += 1
    #                         if num_recordPP >= 1: 
    #                         # if num_recordPP >= 1:
    #                             # ml.logger.debug("поток: вытащили 3 записей")
    #                             ml.logger.debug("поток: вытащили 1 запись")
    #                             return None # за каждую трехминутку вытаскиваем не более 1 записей
    #                     else:
    #                         ml.logger.debug("поток: предыдущюю запись профиля из счетчика уже есть в DBPP")
    #             else:
    #                 ml.logger.debug("поток: не удалось считать предыдущюю запись профиля мощности счетчика")
    #         flag_existence = False
    #         newdatetime=newdatetime-timedelta(minutes=30)    
    #     return None

