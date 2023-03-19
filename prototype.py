
#  программа вытягивания профиля мощности из прошлого счетчика

import sys
import os

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import *
import numpy as np
import datetime # обязательно до import sqlite3 as sql3  !!!!!
from datetime import date, timedelta
# from time import sleep
# import modulVM.moduleAppGUIQt as magqt
import modulVM.config as cfg
import modulVM.moduleSQLite as msql
import modulVM.moduleProtocolMercury as mpm
# import modulVM.moduleComThread as mct
# import modulVM.moduleLogging as ml
import modulVM.moduleGeneral as mg
# import modulVM.moduleParamSettingDataCounter as mpsdc




def create_arr_TimeAxes_for_counter(lst_of_dic_counters:list):
    # создание массива временных штампов из прошлого, которые потом надо проверить на наличие в DBPP
    lst_of_arr_timeshtamp = []
    for numCounter, item_dic_Counter in enumerate(lst_of_dic_counters):
    # создание массива штампов времени с P_plus = 0 или отсутствующими
    # создадим массив временной оси начиная с текущей минуты до 3 суток в прошлое
        date_now = datetime.datetime.now()
        date_past = date_now - timedelta(days=10)
        date_past = date_past.replace(hour=23,  minute = 30)
        lst_datetime_step30_full, lstsu_full, rezult = mg.createLstIntervalDateTime(dateFrom=date_past, dateTo=date_now, stepTime=30)
        arr_TimeAxis = np.array(lst_datetime_step30_full)
        lst_of_arr_timeshtamp.append(arr_TimeAxis)
    return lst_of_arr_timeshtamp

def veryfy_record_in_DBPP(lst_of_arr_timeshtamp:list, id_counter = 0):

    # проверим наличие записи в DBPP по данному счетчику.
    # Штамп времени берем самый верхний (с индеском=0)
    arr_TimeAxis = lst_of_arr_timeshtamp[id_counter]
    rezult, data = msql.select_zero_Power_from_DBPP(id_counter=id_counter, date_time=arr_TimeAxis[0])
    if (not rezult) or (data[0] == 0):
        # если записи не существует или P_plus=0
        flag_existence = False
    else:
        # если запись существует
        flag_existence = True
    return flag_existence

def translate_shtampDateTime_in_adr(lst_of_arr_timeshtamp:list, id_counter = 0):
    adr = 0x0010         # примем по умолчанию
    dic_data_pp, rezult_ReadRecordMassProfilPower = mpm.fn_ReadRecordMassProfilPower(net_adress_count, adr, id_counter)
    
    return adr



#  эту функцию поместить в конце цикла опроса счетчиков
# создание массива временных штампов из прошлого, которые потом надо проверить на наличие в DBPP
lst_of_dic_counters, rezult_getList = msql.getListCounterDB()
lst_of_arr_timeshtamp = create_arr_TimeAxes_for_counter(lst_of_dic_counters)

# написать функцию, определяющую сколько времени осталось до начала 3-минутки. 
# Успеем ли вытянуть прошлые данные в DBPP из счетчиков?
# Если времени осталось больше 30 секунд - запускаем вытягиваие одной записи прошлого
flag_have_time = True
if flag_have_time:
    # проверим наличие записи в DBPP по данному счетчику.
    flag_existence = veryfy_record_in_DBPP(lst_of_arr_timeshtamp, id_counter = 43)
    if not flag_existence:
        # если записи нет - вытягиваем ее
        # расчет на базе штампа времени адреса внутренного массива профиля для конкретного счетчика
        !!!!!!!!!!!
        adr = translate_shtampDateTime_in_adr(lst_of_arr_timeshtamp, id_counter = 43)
        net_adress_count = 71
        id_counter = 43
        dic_data_pp, rezult_ReadRecordMassProfilPower = mpm.fn_ReadRecordMassProfilPower(net_adress_count, adr, id_counter)
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
    