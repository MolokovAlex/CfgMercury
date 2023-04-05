from PyQt5.QtCore import *
# from time import sleep
# from datetime import datetime
import datetime
from datetime import timedelta
# from datetime import timedelta
# import queue
import sqlite3 as sql3
import traceback
import sys
import os
import time

import modulVM.config as cfg
import modulVM.moduleLogging as ml
# import modulVM.moduleAppGUIQt as magqt
import modulVM.moduleProtocolMercury as mpm
# import modulVM.moduleGeneral as mg
# import modulVM.moduleSQLite as msql




# class CommunicationCounterThread(QThread):
class CommunicationCounterThread(QObject):
    signal_progressRS = pyqtSignal(int)
    signal_error_open_connect_port = pyqtSignal()
    signal_error_connect_to_DB = pyqtSignal()
    signal_thread_is_working = pyqtSignal()
    signal_errorCount = pyqtSignal()
    

    def __init__(self, name_file_DB):
        # QThread.__init__(self)
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
            # self.signal_error_connect_to_DB.emit()
            cfg.ON_TRANSFER_DATA_COUNTER = False


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
        ml.logger.debug('поток: старт')
        self.running =True
        count_error = 0
        # открываем порт IP или COM
        if mpm.connection_to_port():
            ml.logger.info('поток: успешное откр порта')

            while self.running:
                self.sleep(1)   # уменьшим скорость бесконечного цикла - сильно грузит процессор - введем паузы в 1 сек
                #  если константа опроса счетчиков установлена - пошел алгоритм опроса счетчиков
                past_minute =  datetime.datetime.now().minute

                #  поиск минут кратных 3 и запуск цикла опроса
                ml.logger.info('поток: ожидание наступления ближайшей 3-х минутки')
                # self.signal_thread_is_working.emit()  #  сигнал о том что поток жив и не завис
                while not(self.find_3minute(past_minute)):
                    a=0
                # self.signal_progressRS.emit(0)
                ml.logger.debug('--------------------------------поток: старт опроса!') # - {str(date_time_now)}")
                datetime_start =  datetime.datetime.now()
                minute_now = datetime_start.minute
                for numCounter, itemCounter in enumerate(self.lstOfDic_Counters):
                    net_adress_count = int(itemCounter['net_adress'])
                    # if True:
                    # !!!!!!!!!!!!!!!!! ТОЛЬКО ДЛЯ ОТЛАДКИ   в релизе удалить!!!!!
                    if net_adress_count in [255,254,136,77]:
                        ml.logger.info(f"---------------поток: Опрос счетчика с NetAdress= {net_adress_count}-----------------")
                        if mpm.test_canal_connection(net_adress_count):
                            if mpm.open_canal_connection_level1(net_adress_count):
                                # !!!!!!!!!!!!!!!!! ТОЛЬКО ДЛЯ ОТЛАДКИ ТЕСТ Watchdog !!!!!!!!!!! в релизе удалить!!!!!
                                # ml.logger.debug('имитация зависания потока для проверки watchdog')
                                # self.sleep(310000)
                                # считывание параметров счетчика 
                                # self.read_ReadParam(net_adress_count, itemCounter)
                                #
                                # считывание мгновенных значений и запись в БД 
                                # self.read_InstantlyValue(net_adress_count, itemCounter)
                                #
                                count_error = 0
                                # здесь отключим, т.к. все равно будем выбирать данные в прошлом
                                # # если наступила 30-минутка
                                # if minute_now in [0,30]:
                                #     ml.logger.info('поток: эта минута есть 30-минутка-----------------------------------')
                                #     # считывание последнйи записи профиля мощности и запись в БД
                                #     self.read_ReadRecordProfilPower(net_adress_count, itemCounter)
                                #
                                self.read_old_record_from_DBPP(net_adress_count,itemCounter["id"],datetime_start)
                                mpm.fn_CloseCanalConnection(net_adress_count)
                        else:
                            count_error +=1
                            ml.logger.debug(f'----------------------------------------------------count_error = {count_error} ')
                            if count_error > 50: 
                                self.stop_th()
                                ml.logger.debug(" поток: посылка сигнала на пере-сброс потока по ошибкам")
                                # self.signal_errorCount.emit()  #  при большом количестве ошибок - перезагрузим поток
                        # self.signal_progressRS.emit(numCounter) #  пусть порядковый номер счетчика в списке будет процентом выполненного объема цикла опроса
                # конец опроса
                # self.signal_progressRS.emit(100)
                # self.signal_thread_is_working.emit()  #  сигнал о том что поток жив и не завис
                # self.signal_progressRS.emit(0)
                past_minute = minute_now
        else:
            #  если порт не открылся - сигнал в основную программу на вывод окна про ошибку
            # и сразу отключим опрос счетсчиков, чтобы не захлебнуться в этих сигналах каждый оборот цикла
            ml.logger.error("поток: ошибка доступа к порту - Exception occurred", exc_info=True)
            # self.signal_error_open_connect_port.emit()
            self.sleep(30)

    def sleep(self, num):
        time.sleep(num)
        return None

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
    
    def editCounterDB(self, new_NameCounter:dict):
        rezult_edit = False
        newNameCounter = new_NameCounter.copy()
        id_counter = int(newNameCounter['id'])
        newNameCounter.pop('id')
        a = newNameCounter.values()
        lst_newNameCounter = []
        for item in a:
            lst_newNameCounter.append(item)
        lst_newNameCounter.append(id_counter)
        try:
            with self.connectDB:
                    self.cursor.executemany("""UPDATE DBC SET schem=?, name_counter_full=?, net_adress=?, manuf_number=?, manuf_data=?, klass_react=?, klass_act=?, nom_u=?, ku=?, ki=?, koefA=?, comment=? WHERE id=?;""", (lst_newNameCounter,))
                    self.connectDB.commit()
                    rezult_edit = True
        except sql3.Error as error_sql:
            ml.logger.error("поток: Exception occurred", exc_info=True)
            self.viewCodeError (error_sql)
            rezult_edit = False
        return rezult_edit


    def insert_TableDBIC_value(self, nameFileDB:str, dictData: dict):
        """
        заполнение таблицы DBIC значением с datetime    
        """
        ml.logger.info("поток: Заполнение таблицы DBIC значением с datetime...")
        dict_data = dictData.copy()
        flag_rezult = False

        if "id" in dict_data: 
            del dict_data["id"]
            dict_data['datetime'] = datetime.datetime.strptime(dict_data['datetime'], "%d/%m/%Y %H:%M")
            lst_data = []
            for key, val in dict_data.items():
                lst_data.append(val)
        try:
            with self.connectDB:
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
                ml.logger.info("поток: Заполнение таблицы DBIC значением с datetime...OK")
                flag_rezult = True
        except sql3.Error as error_sql:
            ml.logger.error("поток: Exception occurred", exc_info=True)
            self.viewCodeError (error_sql)
            flag_rezult = False
        return flag_rezult

    def insert_TableDBPP_value(self, dictData: dict):
        """
        заполнение таблицы DBPP значением с datetime
        """
        ml.logger.info("поток: Заполнение таблицы DBPP значением с datetime")
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
                    ml.logger.info("поток: Заполнение таблицы DBPP значением с datetime...OK")
                    flag_rezult = True
            except sql3.Error as error_sql:
                ml.logger.error("поток: Exception occurred", exc_info=True)
                self.viewCodeError (error_sql)
                flag_rezult = False
        else: flag_rezult = False
        return  flag_rezult

    def read_ReadParam(self, net_adress_count, itemCounter):
        """ Cчитывание параметров счетчика 
            Arg:
            net_adress_count:int - сетевой номер счетчика
            itemCounter:dic - словарь с полями БД счетчика    
        """
        dic_data, rezult_ReadParam_SerND = mpm.fn_ReadParam_SerND(net_adress_count, itemCounter)
        if rezult_ReadParam_SerND: 
            dic_data, rezult_ReadParam_KoefUI = mpm.fn_ReadParam_KoefUI(net_adress_count, dic_data)
            if rezult_ReadParam_KoefUI:
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


    def read_InstantlyValue(self, net_adress_count, itemCounter):
        """ Считывание мгновенных значений и запись в БД
            Arg:
            net_adress_count:int - сетевой номер счетчика
            itemCounter:dic - словарь с полями БД счетчика
        """
        rezult_fix_datetime = mpm.fn_fixInstantlyValue(net_adress_count)
        if rezult_fix_datetime:
            dic_data, rezult_ReadInstantlyValue_TimeFix = mpm.fn_ReadInstantlyValue_TimeFix(net_adress_count, itemCounter["id"])
            if rezult_ReadInstantlyValue_TimeFix: 
                dic_data, rezult_ReadInstantlyValue_I = mpm.fn_ReadInstantlyValue_I(net_adress_count, itemCounter["id"],dic_data)
                if rezult_ReadInstantlyValue_I:
                    dic_data, rezult_ReadInstantlyValue_PowerP = mpm.fn_ReadInstantlyValue_PowerP(net_adress_count, itemCounter["id"],dic_data)
                    if rezult_ReadInstantlyValue_PowerP:
                        dic_data, rezult_ReadInstantlyValue_PowerQ = mpm.fn_ReadInstantlyValue_PowerQ(net_adress_count, itemCounter["id"],dic_data)
                        if rezult_ReadInstantlyValue_PowerQ:
                            dic_data, rezult_ReadInstantlyValue_Cos = mpm.fn_ReadInstantlyValue_Cos(net_adress_count, itemCounter["id"],dic_data)
                            if rezult_ReadInstantlyValue_Cos:
                                self.insert_TableDBIC_value(net_adress_count,dic_data)
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
        else:
            ml.logger.error("поток: не удалось счетчику зафиксировать мгн значения")
        return None

    def viewCodeError (self, sql_error):
        print("поток: Ошибка при работе с sqlite", sql_error)
        print("Класс исключения: ", sql_error.__class__)
        print("Исключение", sql_error.args)
        print("Печать подробноcтей исключения SQLite: ")
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))

    def read_ReadRecordProfilPower(self,net_adress_count, itemCounter):
        """ Считывание последнйи записи профиля мощности и запись в БД
            Arg:
            net_adress_count:int - сетевой номер счетчика
            itemCounter:dic - словарь с полями БД счетчика
        """
        adr,rezult_ReadLastRecordMassProfilPower = mpm.fn_ReadLastRecordMassProfilPower(net_adress_count)
        if rezult_ReadLastRecordMassProfilPower: 
            dic_data_pp, rezult_ReadRecordMassProfilPower = mpm.fn_ReadRecordMassProfilPower(net_adress_count, adr, itemCounter["id"])
            if rezult_ReadRecordMassProfilPower: 
                self.insert_TableDBPP_value(dic_data_pp)
            else:
                ml.logger.error("поток: не удалось считать последнюю запись профиля мощности счетчика")
        else:
            ml.logger.error("поток: не удалось считать параметры последней записи профиля мощности счетчика")
        # self.read_old_record_from_DBPP(self, net_adress_count, adr, itemCounter["id"])
        return None
    
    
    def select_zero_Power_from_DBPP(self, id_counter, dict_data):
        flag_rezult = False
        date_time = datetime.datetime.strptime(dict_data['datetime'], "%d/%m/%Y %H:%M")
        try:
            with self.connectDB:
                self.cursor.execute("""SELECT datetime FROM DBPP WHERE id_counter=? AND 
                                                                    datetime = ? AND
                                                                    period_int ='30'
                                                                    """, (id_counter, date_time))
                data = self.cursor.fetchall() 
            if data:
                flag_rezult = True
                ml.logger.debug("поток: запись есть в DBPP")
            else:
                flag_rezult = False
                ml.logger.debug("поток: запись НЕТ в DBPP")
        except sql3.Error as error_sql:
            ml.logger.error("Exception occurred", exc_info=True)
            self.viewCodeError (error_sql)
            flag_rezult = False
        return flag_rezult, data
    

    def how_much_time_is_left(self, datetimeStart):
        """ функция, определяющую сколько времени осталось до начала 3-минутки.
        datetimeStart - во сколько начался опрос счетчиков
        """
        leftTime = 0
        date_now =  datetime.datetime.now()
        leftTime = date_now - datetimeStart + timedelta(minutes=3)
        if leftTime > (timedelta(seconds=30)): 
            flag_HaveTime = True
        else:
            flag_HaveTime = False
        return leftTime, flag_HaveTime


    def read_old_record_from_DBPP(self, net_adress_count, id_counter, date_time_Start):
        num_recordPP = 0    # счетчик количества успешно вынутых и записаннных в БД записей
        # функця, определяющую сколько времени осталось до начала 3-минутки. 
        # Успеем ли вытянуть прошлые данные в DBPP из счетчиков?
        # Если времени осталось больше 30 секунд - запускаем вытягиваие одной записи прошлого
        date_time_Start=date_time_Start.replace(second=0, microsecond=0)
        left_time, flag_have_time = self.how_much_time_is_left(date_time_Start)
        ml.logger.debug(f'поток: осталось {left_time} мин до ближайшей 3-х минутки')
        if flag_have_time:
            # получим список datetime по конкретному счетчику глубиной 80 суток с сортировкой по уменьшению
            # date_time_Start =  datetime.datetime.now()
            date_past = date_time_Start - timedelta(days=80)
            date_past = date_past.replace(hour=0,  minute = 0, second=0, microsecond=0)
            rezult_select_listDateTime, dataDBPP = self.select_listDateTime_in_DBPP(id_counter,date_time_Start,date_past)
            # if rezult_select_listDateTime:  #  на пустой БД это условие никогда не сработает
            if True:
                # сделаем данные плоскими
                data = [name for group in dataDBPP for name in group]
                #  считать штамп времени по адресу 0x0010
                ml.logger.debug(f'поток: считывание записи по адресу 0х0010')
                adr_0x0010 = 0x0010
                dic_data_pp_0x0010, rezult_ReadRecordMassProfilPower = mpm.fn_ReadRecordMassProfilPower(net_adress_count, adr_0x0010, id_counter)
                            
                            # ДЛЯ ОТЛАДКИ!!!!!!!!!!!!!типа это храниться по адресу 0x0010
                            # dic_data_pp = cfg.dic_template_DBPP.copy()
                            # dic_data_pp_0x0010['datetime'] = datetime.datetime(2023, 3, 30, 16, 00).strftime("%d/%m/%Y %H:%M")
                            #
                #  пройдемся по временной оси глубиной в 80 суток 
                # ищем отстутсвующие в списке от DBPP штампы datetime
                newdatetime = date_time_Start.replace(minute = 0, second=0, microsecond=0)
                flag_existence = False
                while newdatetime >= date_past:
                # for newdatetime in range(date_time_Start, date_past, -timedelta(minutes=30)):
                    for index_data in range(0, len(data),1):
                        if datetime.datetime.strptime(data[index_data],"%Y-%m-%d %H:%M:%S")  == newdatetime:
                            # если штамп времени newdatetime оси совпадает со элементом списка data[]
                            # переходим к следующему штампу newdatetime                    
                            flag_existence = True
                            break
                        else:
                            # это не тот штамп времени в списке из БД
                            flag_existence = False
                    if not flag_existence:
                        ml.logger.debug(f'поток: штамп времени {newdatetime} так и не был найден в DBPP')
                        # если штамп времени newdatetime так и не был найден - запросим его у счетчика
                        # запрашиваем у счетчика данные для DBPP на дату newdatetime
                        # не всякий случай еще раз - проверим наличие записи в DBPP по данному счетчику.
                        # dicdata = cfg.dic_template_DBPP.copy()
                        # dicdata['datetime']=newdatetime.strftime("%d/%m/%Y %H:%M")
                        # rezult_zero_DBPP, dataDBPP = self.select_zero_Power_from_DBPP(id_counter, dicdata)
                        # if (not rezult_zero_DBPP):
                        if True:
                            # если записи не существует в DBPP
                            # считываем из счетчика
                            # рассчитываем адрес
                            
                            
                            # узнаем длительность интервала времени от штампа адреса 0x0010 до требуемой даты newdatetime
                            interval_of_time = newdatetime - datetime.datetime.strptime(dic_data_pp_0x0010['datetime'], "%d/%m/%Y %H:%M") #- dic_data_pp['datetime']
                            step_of_time = int(interval_of_time/(timedelta(seconds=30*60)))
                            adr_newdatetime = 0x0010+ step_of_time*0x0010
                            if adr_newdatetime <= 0x0010: 
                                ml.logger.debug("поток: в вычислении адреса дошли до 0х0010")
                                return None # в вычислении адреса дошли до 0х0010
                            # считываем и добавляем в DBPP
                            ml.logger.debug(f"поток: считывание предыдущюю запись профиля adr = {adr_newdatetime}")
                            dic_data_pp, rezult_ReadRecordMassProfilPower = mpm.fn_ReadRecordMassProfilPower(net_adress_count, adr_newdatetime, id_counter)
                            if rezult_ReadRecordMassProfilPower:
                                rezult_zero_DBPP, dataDBPP = self.select_zero_Power_from_DBPP(id_counter, dic_data_pp)
                                if not rezult_zero_DBPP:
                                    self.insert_TableDBPP_value(dic_data_pp)
                                    num_recordPP += 1
                                    if num_recordPP >= 10: 
                                        ml.logger.debug("поток: вытащили 10 записей")
                                        return None # за каждую трехминутку вытаскиваем не более 3 записей
                                else:
                                    ml.logger.debug("поток: предыдущюю запись профиля из счетчика уже есть в DBPP")
                            else:
                                ml.logger.debug("поток: не удалось считать предыдущюю запись профиля мощности счетчика")
                    flag_existence = False
                    newdatetime=newdatetime-timedelta(minutes=30)
                

                    
        return None
    
    def select_listDateTime_in_DBPP(self, id_counter,date_now,date_past):
        flag_rezult = False
        try:
            
            with self.connectDB:
                self.cursor.execute("""SELECT datetime FROM DBPP WHERE id_counter=? AND 
                                                            datetime <= ? AND
                                                            datetime >= ? ORDER BY datetime DESC;
                                                                    """, (id_counter,date_now,date_past ))
                dataDB = self.cursor.fetchall() 
            if dataDB:
                flag_rezult = True
                # data = dataDB[0]
            else:
                flag_rezult = False
        except sql3.Error as error_sql:
            ml.logger.error("Exception occurred", exc_info=True)
            self.viewCodeError (error_sql)
            rezult = False
        return flag_rezult, dataDB
    

if __name__ == "__main__": 
    if not os.path.isdir(cfg.absLOG_DIR): 
        os.mkdir(cfg.absLOG_DIR)
    if not os.path.isdir(cfg.absDB_DIR): 
        os.mkdir(cfg.absDB_DIR)
    ml.setup_logging(cfg.absLOG_FILE)
    cfg.port_COM = 'COM9'
    # cfg.port_COM = '/dev/ttyUSB0'
    cfg.MODE_CONNECT=2
    ml.logger.debug('---------------------------- запуск программы -------------------------------------')
    cct = CommunicationCounterThread(cfg.absDB_FILE)
    cct.run()
    # cct.read_old_record_from_DBPP(77, 44, datetime.datetime.now())
    a=0