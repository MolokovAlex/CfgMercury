
#  программа вытягивания профиля мощности из прошлого счетчика

import sys
import os

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import *
import numpy as np
# import datetime # обязательно до import sqlite3 as sql3  !!!!!
from datetime import date, timedelta
from datetime import datetime
import time
from time import sleep
import sqlite3 as sql3
# import modulVM.moduleAppGUIQt as magqt
import modulVM.config as cfg
import modulVM.moduleSQLite as msql
import modulVM.moduleProtocolMercury as mpm
# import modulVM.moduleComThread as mct
import modulVM.moduleLogging as ml
import modulVM.moduleGeneral as mg
# import modulVM.moduleParamSettingDataCounter as mpsdc








def translate_shtampDateTime_in_adr(lst_of_arr_timeshtamp:list, id_counter, net_adress_counter):
    adr = 0x0010         # примем по умолчанию
    # net_adress_count = 0
    dic_data_pp, rezult_ReadRecordMassProfilPower = mpm.fn_ReadRecordMassProfilPower(net_adress_counter, adr, id_counter)
    
    return adr

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

def how_much_time_is_left(datetimeStart):
    """ функция, определяющую сколько времени осталось до начала 3-минутки.
    """
    leftTime = 0
    date_now =  datetime.now()
    leftTime = date_now - datetimeStart + timedelta(minutes=3)
    if leftTime > (timedelta(seconds=30)): 
        flag_HaveTime = True
    else:
        flag_HaveTime = False
    return leftTime, flag_HaveTime

# def run(self):
def run():
    ml.logger.debug('поток стартовал')
    # self.running =True
    cfg.running_thread1 = True

    # крутимся в этом цикле вечно - поток нельзя завершать пока открыто основное окно программы
    # залезем в БД для получкения списка счетчиков - чтобы каждые 3 минуты туда не лазить
    lst_of_dic_counters, rezult_getList = msql.getListCounterDB() 
    ml.logger.debug(f'cfg.ON_TRANSFER_DATA_COUNTER={cfg.ON_TRANSFER_DATA_COUNTER}')
    while True:
        # self.sleep(1)   # уменьшим скорость бесконечного цикла - сильно грузит процессор - введем паузы в 1 сек
        time.sleep(1)
        #  если константа опроса счетчиков установлена - пошел алгоритм опроса счетчиков
        # 
        past_minute =  datetime.now().minute
        while cfg.ON_TRANSFER_DATA_COUNTER:
            # self.sleep(1)
            time.sleep(1)
            date_now = datetime.now()
            datetime_start = datetime.now()
            minute_now =  datetime.now().minute
            #  поиск минут кратных 3 и запуск цикла опроса
            if minute_now != past_minute:
                if minute_now in [0,3,6,9,12,15,18,21,24,27,30,33,36,39,42,45,48,51,54,57]: # and not(flag_start_oprosa):
                    ml.logger.debug(f'{date_now} : --------------------------------поток - старт опроса!') # - {str(date_time_now)}")
                    datetime_start = datetime.now()
                    # открываем порт IP или COM
                    if mpm.connection_to_port():
                        # одновременно проверяем есть ли связь с БД и доастем спиское всех зарегистрированных счетчиков
                        # lst_counters, rezult_getList = msql.getListCounterDB()    # перенес выше
                        if rezult_getList:
                            # если связь с БД есть
                            ml.logger.info('поток - доступ к БД есть')
                            for numCounter, itemCounter in enumerate(lst_of_dic_counters):
                                net_adress_count = int(itemCounter['net_adress'])
                                ml.logger.info(f"---------------Опрос счетчика с NetAdress= {net_adress_count}-----------------")
                                #  сделаем 3 иттераций-попыток достучаться до счетчика
                                is_itteration = True
                                num_itteration = 0
                                while is_itteration:
                                    # net_adress_count = int(itemCounter['net_adress'])
                                    if mpm.fn_TestCanalConnection(net_adress_count):
                                        if mpm.fn_OpenCanalConnectionLevel1(net_adress_count):
                                            #
                                            # ТЕСТ Watchdog !!!!!!!!!!! в релизе удалить!!!!!
                                            # self.sleep(610000)
                                            # считывание параметров счетчика 
                                            read_ReadParam(net_adress_count, itemCounter)
                                            #
                                            # считывание мгновенных значений и запись в БД 
                                            read_InstantlyValue(net_adress_count, itemCounter)
                                            #
                                            # если наступила 30-минутка
                                            if minute_now in [0,30]:
                                                ml.logger.info('поток - эта минута есть 30-минутка-----------------------------------')
                                                # считывание последнйи записи профиля мощности и запись в БД
                                                read_ReadRecordProfilPower(net_adress_count, itemCounter)
                                            mpm.fn_CloseCanalConnection(net_adress_count)
                                            is_itteration = False
                                        else: 
                                            ml.logger.error(f" __не открылся канал связи с NetAdress= {net_adress_count}")
                                            num_itteration +=1
                                            if num_itteration == 3 : is_itteration = False 
                                    else: 
                                        ml.logger.error(f" __не прошел тест канала связи с NetAdress= {net_adress_count}")
                                        num_itteration +=1
                                        if num_itteration == 3 : is_itteration = False
                                # self.signal_progressRS.emit(numCounter) #  пусть порядковый номер счетчика в списке будет процентом выполненного объема цикла опроса
                        
                        # если связь с БД отсутствует
                        else:
                            #  если доступ к БД не произошел - сигнал в основную программу на вывод окна про ошибку
                            # и сразу отключим опрос счетсчиков, чтобы не захлебнуться в этих сигналах каждый оборот цикла
                            ml.logger.error("Поток - ошибка доступа к БД - Exception occurred", exc_info=True)
                            # self.signal_error_connect_to_DB.emit()
                            cfg.ON_TRANSFER_DATA_COUNTER = False
                        mpm.close_connection_to_port()
                    else:
                        #  если порт не открылся - сигнал в основную программу на вывод окна про ошибку
                        # и сразу отключим опрос счетсчиков, чтобы не захлебнуться в этих сигналах каждый оборот цикла
                        # self.signal_error_open_connect_port.emit()
                        cfg.ON_TRANSFER_DATA_COUNTER = False
                
                # конец опроса
                # self.signal_progressRS.emit(100)
                # self.signal_watchdog_thread.emit()
                # read_old_record_from_DBPP(datetime_start, lst_of_dic_counters)
                ml.logger.debug(f'{date_now} : поток - ожидание наступления ближайшей 3-х минутки')
                past_minute = minute_now





    return None




def read_old_record_from_DBPP(datetimeStart, lstOfDic_Counters):
    """ запуск процесса вынимания старых/прошлых записей профиля мощности из счетчика
    """
    # функця, определяющую сколько времени осталось до начала 3-минутки. 
    # Успеем ли вытянуть прошлые данные в DBPP из счетчиков?
    # Если времени осталось больше 30 секунд - запускаем вытягиваие одной записи прошлого
    left_time, flag_have_time = how_much_time_is_left(datetimeStart)
    ml.logger.debug(f'осталось {left_time} мин')
    if flag_have_time:
        



                # если записи нет - вытягиваем ее
                # расчет на базе штампа времени адреса внутренного массива профиля для конкретного счетчика
                adr = translate_shtampDateTime_in_adr(lst_of_arr_timeshtamp, id_counter = 43, net_adress_counter= net_adress_counter)
                # извлекаем старую запись из счетчика
                dic_data_pp, rezult_ReadRecordMassProfilPower = mpm.fn_ReadRecordMassProfilPower(net_adress_counter, adr, id_counter)
                if rezult_ReadRecordMassProfilPower: 
                    msql.insert_TableDBPP_value(dic_data_pp)
                    # если все прошло успешно - удалить штмп времени из массива временных штампов из прошлого
                    arr = lst_of_arr_timeshtamp[id_counter].copy()
                    arr =np.delete(arr, 0)
                    lst_of_arr_timeshtamp[id_counter] = arr
                    !!!!!!!!!!!!!!!!!!!!!!!!!!
                else:
                    # ml.logger.error("не удалось считать последнюю запись профиля мощности счетчика")
                    pass
    return None




def main():
    cfg.ON_TRANSFER_DATA_COUNTER = True
    cfg.MODE_CONNECT == cfg.MODE_CONNECTION_COM
    cfg.port_COM = 'COM9'

    #  подключение лога
    if not os.path.isdir(cfg.absLOG_DIR): 
        os.mkdir(cfg.absLOG_DIR)
    if not os.path.isdir(cfg.absDB_DIR): 
        os.mkdir(cfg.absDB_DIR)
    ml.setup_logging(cfg.absLOG_FILE)
    
    #  подключение БД
    try:
        # self.open_window_wait()
        name_file_DB = cfg.absDB_FILE
        ml.logger.info('подключение файла БД...')
        if msql.connect_to_DB(name_file_DB):
            cfg.sql_base_conn = sql3.connect(name_file_DB, check_same_thread=False)
        # self.window2.hide()
    except sql3.Error as error_sql:
        ml.logger.error("Ошибка в подключении БД - Exception occurred", exc_info=True)
    run()



    # flag_have_time = True
    # if flag_have_time:
    #     # проверим наличие записи в DBPP по данному счетчику.
    #     flag_existence = veryfy_record_in_DBPP(lst_of_arr_timeshtamp, id_counter = 43)
    #     if not flag_existence:
    #         # если записи нет - вытягиваем ее
    #         # расчет на базе штампа времени адреса внутренного массива профиля для конкретного счетчика
    #         !!!!!!!!!!!
    #         adr = translate_shtampDateTime_in_adr(lst_of_arr_timeshtamp, id_counter = 43)
    #         net_adress_count = 71
    #         id_counter = 43
    #         dic_data_pp, rezult_ReadRecordMassProfilPower = mpm.fn_ReadRecordMassProfilPower(net_adress_count, adr, id_counter)
    #         if rezult_ReadRecordMassProfilPower: 
    #             msql.insert_TableDBPP_value(dic_data_pp)
    #             # если все прошло успешно - удалить штмп времени из массива временных штампов из прошлого
    #             arr = lst_of_arr_timeshtamp[id_counter].copy()
    #             arr =np.delete(arr, 0)
    #             lst_of_arr_timeshtamp[id_counter] = arr
    #             !!!!!!!!!!!!!!!!!!!!!!!!!!
    #         else:
    #             # ml.logger.error("не удалось считать последнюю запись профиля мощности счетчика")
    #             pass
    return None


if __name__ == "__main__": 
    main()







    # # по каждому штампу временной оси проверим -есть ли запись в БД
    # # если записи нет - то сделаем запись с нулевыми мощностями
    # # если запись есть - ничего не делаем
    # id_counter = 43
    # for num_arrTimeAxis, val_arrTimeAxis in enumerate(arr_TimeAxis):
    # #     dt_arrTimeAxis = datetime.datetime(val_arrTimeAxis[0], val_arrTimeAxis[1], val_arrTimeAxis[2], val_arrTimeAxis[3], val_arrTimeAxis[4])
    #     rezult, data = msql.select_zero_Power_from_DBPP(id_counter=id_counter, date_time=arr_TimeAxis[0])
    # #     if not rezult:
    # #         a=0
    # #         dic = cfg.dic_template_DBPP.copy()
    # #         dic['P_plus'] = 0
    # #         dic['P_minus'] = 0
    # #         dic['Q_plus'] = 0
    # #         dic['Q_minus'] = 0
    # #         dic['id_counter'] = id_counter
    # #         dic['datetime'] = dt_arrTimeAxis.strftime("%d/%m/%Y %H:%M")
    # #         dic['period_int'] = '30'
    # #         msql.insert_TableDBPP_value(dic)
    # #     else:
    # #         b= 0
    # #
    