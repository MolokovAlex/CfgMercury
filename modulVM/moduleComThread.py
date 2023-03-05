from PyQt5.QtCore import *
# from time import sleep
from datetime import datetime
# from datetime import timedelta
# import queue
# import sqlite3 as sql3

import modulVM.config as cfg
import modulVM.moduleLogging as ml
# import modulVM.moduleAppGUIQt as magqt
import modulVM.moduleProtocolMercury as mpm
# import modulVM.moduleGeneral as mg
import modulVM.moduleSQLite as msql




class CommunicationCounterThread(QThread):
    signal_progressRS = pyqtSignal(int)
    signal_error_open_connect_port = pyqtSignal()
    signal_error_connect_to_DB = pyqtSignal()
    
    def __init__(self, parent = None):
        QThread.__init__(self, parent)
        # self._limit = limit
        self.running =False
        cfg.running_thread1 = False
        

    def run(self):
        ml.logger.debug('поток стартовал')
        self.running =True
        cfg.running_thread1 = True
        # cfg.lst_online_Counter = ""
        # i=0
        # крутимся в этом цикле вечно - поток нельзя завершать пока открыто основное окно программы
        ml.logger.debug(f'cfg.ON_TRANSFER_DATA_COUNTER={cfg.ON_TRANSFER_DATA_COUNTER}')
        while True:
            self.sleep(1)   # уменьшим скорость бесконечного цикла - сильно грузит процессор - введем паузы в 1 сек
            #  если константа опроса счетчиков установлена - пошел алгоритм опроса счетчиков
            # 
            past_minute =  datetime.now().minute
            while cfg.ON_TRANSFER_DATA_COUNTER:
                self.sleep(1)
                date_now = datetime.now()
                minute_now =  datetime.now().minute
                #  поиск минут кратных 3 и запуск цикла опроса
                if minute_now != past_minute:
                    if minute_now in [0,3,6,9,12,15,18,21,24,27,30,33,36,39,42,45,48,51,54,57]: # and not(flag_start_oprosa):
                        ml.logger.debug(f'{date_now} : --------------------------------поток - старт опроса!') # - {str(date_time_now)}")
                        self.signal_progressRS.emit(10)
                        # открываем порт IP или COM
                        if mpm.connection_to_port():
                            # одновременно проверяем есть ли связь с БД и доастем спиское всех зарегистрированных счетчиков
                            lst_counters, rezult_getList = msql.getListCounterDB() 
                            if rezult_getList:
                                # если связь с БД есть
                                ml.logger.info('поток - доступ к БД есть')
                                for itemCounter in lst_counters:
                                    ml.logger.info(f"---------------Опрос счетчика с NetAdress= {int(itemCounter['net_adress'])}-----------------")
                                    #  сделаем 3 иттераций-попыток достучаться до счетчика
                                    self.signal_progressRS.emit(20)
                                    is_itteration = True
                                    num_itteration = 0
                                    while is_itteration:
                                        net_adress_count = int(itemCounter['net_adress'])
                                        if mpm.fn_TestCanalConnection(net_adress_count):
                                            self.signal_progressRS.emit(40)
                                            if mpm.fn_OpenCanalConnectionLevel1(net_adress_count):
                                                self.signal_progressRS.emit(50)
                                                #
                                                # считывание параметров счетчика 
                                                read_ReadParam(net_adress_count, itemCounter)
                                                self.signal_progressRS.emit(60)
                                                #
                                                # считывание мгновенных значений и запись в БД 
                                                read_InstantlyValue(net_adress_count, itemCounter)
                                                self.signal_progressRS.emit(70)
                                                #
                                                # если наступила 30-минутка
                                                if minute_now in [0,30]:
                                                    ml.logger.info('поток - эта минута есть 30-минутка-----------------------------------')
                                                    # считывание последнйи записи профиля мощности и запись в БД
                                                    read_ReadRecordProfilPower(net_adress_count, itemCounter)
                                                #
                                                self.signal_progressRS.emit(90)
                                                mpm.fn_CloseCanalConnection(net_adress_count)
                                                self.signal_progressRS.emit(100)
                                                is_itteration = False
                                            else: 
                                                ml.logger.error(f" __не открылся канал связи с NetAdress= {net_adress_count}")
                                                num_itteration +=1
                                                if num_itteration == 3 : is_itteration = False
                                                
                                        else: 
                                            ml.logger.error(f" __не прошел тест канала связи с NetAdress= {net_adress_count}")
                                            num_itteration +=1
                                            if num_itteration == 3 : is_itteration = False
                            
                            # если связь с БД отсутствует
                            else:
                                #  если доступ к БД не произошел - сигнал в основную программу на вывод окна про ошибку
                                # и сразу отключим опрос счетсчиков, чтобы не захлебнуться в этих сигналах каждый оборот цикла
                                ml.logger.error("Поток - ошибка доступа к БД - Exception occurred", exc_info=True)
                                self.signal_error_connect_to_DB.emit()
                                cfg.ON_TRANSFER_DATA_COUNTER = False
                            mpm.close_connection_to_port()
                        else:
                            #  если порт не открылся - сигнал в основную программу на вывод окна про ошибку
                            # и сразу отключим опрос счетсчиков, чтобы не захлебнуться в этих сигналах каждый оборот цикла
                            self.signal_error_open_connect_port.emit()
                            cfg.ON_TRANSFER_DATA_COUNTER = False
                    
                    # конец опроса
                    ml.logger.debug(f'{date_now} : поток - ожидание наступления ближайшей 3-х минутки')
                    past_minute = minute_now



def read_ReadParam(net_adress_count, itemCounter):
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
                ml.logger.info('запись в таблицу данных счетчиков DBC_new protocol')
                msql.editCounterDB(dic_data)    # дополнение параметров счетчика из БД считанными параметрами из счетчика
            else:
                ml.logger.debug("не удалось получить параметры: коэфициент А счетчика по новому протоколу")
                dic_data, rezult_ReadParam_Variant = mpm.fn_ReadParam_VariantOld(net_adress_count, dic_data)
                if rezult_ReadParam_Variant:
                    ml.logger.info('запись в таблицу данных счетчиков DBC_old protocol')
                    msql.editCounterDB(dic_data)
                else:
                    ml.logger.error("не удалось получить параметры: коэфициент А счетчика ни по старому, ни по новому протоколу")
        else:
            ml.logger.error("не удалось получить параметры: коэфициенты KU и KI счетчика")
    else:
        ml.logger.error("не удалось получить параметры: серийный номер и дату выпуска счетчика")
    return None


def read_InstantlyValue(net_adress_count, itemCounter):
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
                            msql.insert_TableDBIC_value(net_adress_count,dic_data)
                        else:
                            ml.logger.error("не удалось считать зафиксировные значения мгн значений CosF счетчика")
                    else:
                        ml.logger.error("не удалось считать зафиксировные значения мгн значений PowerQ счетчика")
                else:
                    ml.logger.error("не удалось считать зафиксировные значения мгн значений PowerP счетчика")
            else:
                ml.logger.error("не удалось считать зафиксировные значения мгн значений токов счетчика")
        else:
            ml.logger.error("не удалось считать зафиксировные дату и время мгн значений счетчика")
    else:
        ml.logger.error("не удалось счетчику зафиксировать мгн значения")
    return None


def read_ReadRecordProfilPower(net_adress_count, itemCounter):
    """ Считывание последнйи записи профиля мощности и запись в БД
        Arg:
        net_adress_count:int - сетевой номер счетчика
        itemCounter:dic - словарь с полями БД счетчика
    """
    adr,rezult_ReadLastRecordMassProfilPower = mpm.fn_ReadLastRecordMassProfilPower(net_adress_count)
    if rezult_ReadLastRecordMassProfilPower: 
        dic_data_pp, rezult_ReadRecordMassProfilPower = mpm.fn_ReadRecordMassProfilPower(net_adress_count, adr, itemCounter["id"])
        if rezult_ReadRecordMassProfilPower: 
            msql.insert_TableDBPP_value(dic_data_pp)
        else:
            ml.logger.error("не удалось считать последнюю запись профиля мощности счетчика")
    else:
        ml.logger.error("не удалось считать параметры последней записи профиля мощности счетчика")
    return None