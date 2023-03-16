# moduleConfigApp
# autor: MolokovAlex
# coding: utf-8

# модуль общих функций

from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
# from PyQt5.QtCore import QDateTime
from PyQt5.QtGui import *
from datetime import date, timedelta
import numpy as np
import math
import sys
import glob
import serial
# from serial.tools import list_ports

import modulVM.moduleSQLite as msql
import modulVM.config as cfg


def createHeaderTable(dd_date_from, dd_date_to, step, period_View):
            """Создание массива шапки для таблицы данных

            Args:
                dd_date_from (_type_): _description_
                dd_date_to (_type_): _description_
                step  - шаг в минутах
                periodIntegr - период интегрирования из cfg.VALUE_PERIOD_INTEGR_POFIL
            """
            arrHeaderTable = None
            newdatetime = dd_date_from
            lst_date = []
            lst_mounth = []
            lst_year = []
            lst_time = []
            while (newdatetime < (dd_date_to + timedelta(days=1))):

                lst_year.append(newdatetime.strftime("%Y"))
                lst_mounth.append(newdatetime.strftime("%m"))
                if (period_View == "день") or (period_View == "месяц"): lst_time.append("")
                else: lst_time.append(newdatetime.strftime("%H:%M"))
                if period_View == "месяц": lst_date.append("")
                else: lst_date.append(newdatetime.strftime("%d"))
                
                newdatetime = newdatetime + timedelta(minutes=step)

            a = np.array((lst_year,lst_mounth,lst_date, lst_time))
            if (period_View == "час") or (period_View == "30 мин"):
                arrHeaderTable = np.insert(a, 0, ["год", "месяц", "день", "время"], axis=1)
            elif period_View == "день":
                arrHeaderTable = np.insert(a, 0, ["год", "месяц", "день", ""], axis=1)
            elif period_View == "месяц":
                arrHeaderTable = np.insert(a, 0, ["год", "месяц", "", ""], axis=1)
            # arrHeaderTable = np.insert(a, 0, ["год", "месяц", "день", "время"], axis=1)
            return arrHeaderTable

def createHeaderTable_ver2(dateFrom:datetime, dateTo:datetime, step, periodIntegr):
            """Создание массива шапки для таблицы данных

            Args:
                dateFrom:datetime: _description_
                dateTo:datetime: _description_
                step  - шаг в минутах
                periodIntegr - период интегрирования из cfg.VALUE_PERIOD_INTEGR_POFIL
            """
            arrHeaderTable = None
            newdatetime = dateFrom
            lst_date = []
            lst_mounth = []
            lst_year = []
            lst_hour = []
            lst_minute = []

            while (newdatetime < (dateTo + timedelta(days=1))):
                lst_year.append(int(newdatetime.strftime("%Y")))
                lst_mounth.append(int(newdatetime.strftime("%m")))
                if (periodIntegr == "день") or (periodIntegr == "месяц"): 
                    lst_hour.append(0)
                else: 
                    lst_hour.append(int(newdatetime.strftime("%H")))
                    lst_minute.append(int(newdatetime.strftime("%M")))
                
                if periodIntegr == "месяц": 
                    lst_date.append("")
                else: 
                    lst_date.append(int(newdatetime.strftime("%d")))
                
                newdatetime = newdatetime + timedelta(minutes=step)

            arrHeaderTable = np.array((lst_year,lst_mounth,lst_date, lst_hour, lst_minute))

            return arrHeaderTable

def createLstIntervalDateTime(dateFrom:datetime, dateTo:datetime, stepTime:int):
            """
                    создает список с штампами времени типа datetime от даты dateFrom до даты dateTo
                    с шагом step  в минутах
            Args:
                dateFrom (QDateEdit): _description_
                dateTo (QDateEdit): _description_
            Returns:
                _type_: _description_
            """
            lst_IntervalDateTime = []
            lst_su = []
            lst = []
            rezult =False
            #проверка что дата FROM меньше чем дата ТО
            if (dateFrom <= dateTo):
                # создадим список с интервалом между штампами времени stepTime минут
                newdatetime = dateFrom
                while newdatetime <= dateTo:# + timedelta(days=1))):
                    lst_IntervalDateTime.append(newdatetime)
                    lst = []
                    lst.append(int(newdatetime.strftime("%Y")))
                    lst.append(int(newdatetime.strftime("%m")))
                    lst.append(int(newdatetime.strftime("%d")))
                    lst.append(int(newdatetime.strftime("%H")))
                    lst.append(int(newdatetime.strftime("%M")))
                    lst_su.append(lst)
                    newdatetime = newdatetime + timedelta(minutes=stepTime)
                rezult = True
            else:
                rezult = False
                
            return lst_IntervalDateTime, lst_su, rezult



def createLstCheckedCounterAndGroups(listcheckItemTree):
            """создаем список выбранных пользователем групп и список выбранных счетчиков - все по отдельности
                выход:
                lst_checked_group  - список id_group по полям БД
                lst_checked_counter_in_group    - список id_counter содержащиеся во всех группах lst_checked_group
                lst_checked_single_counter - список id_counter по полям БД
            """
            lst_checked_group = [] 
            lst_checked_counter_in_group = []
            lst_checked_single_counter = []
            
            list_CounterDB, rezult_getListOfCounterDB = msql.getListCounterDB()
            list_GroupDB, rezult_getListOfGroupDB = msql.getListGroupDB()
            for itemLst in listcheckItemTree:
                for itemGroup in list_GroupDB:
                    if itemLst == itemGroup['name_group_full']:
                        lst_checked_group.append(itemGroup['id'])
                        #  и найдем какие счетчики есть в этой группу и начнем заполнять список счетчиками группы
                        list_counter_in_group, rezult_get = msql.get_list_counter_in_group_DBGC(itemGroup['id'])
                        for item_list in list_counter_in_group:
                            lst_checked_counter_in_group.append(item_list)

                    
            for itemLst in listcheckItemTree:
                for itemCounter in list_CounterDB:
                    if itemLst == itemCounter['name_counter_full']:
                        lst_checked_single_counter.append(itemCounter['id'])
                        break
            return lst_checked_counter_in_group, lst_checked_group, lst_checked_single_counter
        
# def roundDateTimeToN(dateTime:datetime, N:int):
#     """ округление минут до кратности N в меньшую сторону
#     """
#     #  костыль - округление даты времени до бижайших минут кратных N
#     dateTimeNow = datetime.now()    
#     #  распакуем в кортеж и отрезаем секунды и милисекунды
#     a = list(dateTimeNow.timetuple()[:5])
#     # Округление до числа, кратного N
#     # N = 3 
#     # a[4] = round(a[4]/N)*N
#     a[4] = math.floor(a[4]/N)*N 
#     # собираем обратно в формат datetime    
#     return datetime(a[0], a[1], a[2], a[3], a[4])



    #     if sys.platform == "linux" or sys.platform == "linux2":
    # if sys.platform.startswith('linux'):
    #     # linux
    #     app.title("Программа считывания данных со счетчиков Меркурий 230 ART  - платформа Linux")
    # # elif platform == "darwin":
    # #     # OS X
    # elif sys.platform == "win32":
    #     # Windows...
    #     app.title("Программа считывания данных со счетчиков Меркурий 230 ART  - платформа Winodws")

    
def list_of_serial_ports():
    """ поиск доступных последовательных портов

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for a_port in ports:
        try:
            s = serial.Serial(a_port)
            s.close()
            result.append(a_port)
        except serial.SerialException:
            pass
    if result == []:
        result = [cfg.port_COM,]

    return result

def createView_periodView(arr_data, arr_TimeAxis, periodIntegr:str):
    """ приведение к виду периода отображения
    """
    num_period_integr = 3       # номер колонки в numpy array для отслеживания что будет меняться
    if periodIntegr != "30 мин":
        if periodIntegr == "час":
            num_period_integr = 3   # оттслеживаем изменение цифры часа - а это столбец 3
        elif periodIntegr == "день":
            num_period_integr = 2
        elif periodIntegr == "месяц":
            num_period_integr = 1

        for num, item_time in enumerate(arr_data):
            if (num+1) >= arr_data.shape[0]:
                break
            if arr_TimeAxis[num][num_period_integr] != arr_TimeAxis[num+1][num_period_integr]:
                time_cur = arr_TimeAxis[num][num_period_integr]
                for num_counter, item_counter in enumerate(cfg.lst_checked_counter_in_group + cfg.lst_checked_single_counter):
                    arr_data[num+1][num_counter] = (arr_data[num][num_counter] + arr_data[num+1][num_counter])/2 # вычисляем среднее арифметическое
                arr_data = np.delete(arr_data, num , axis = 0)
                arr_TimeAxis = np.delete(arr_TimeAxis, num , axis = 0)
            
            
            # while arr_TimeAxis[num][num_period_integr] == arr_TimeAxis[num+1][num_period_integr]:
            #     if arr_TimeAxis[num][num_period_integr] == arr_TimeAxis[num+1][num_period_integr]:
            #         for num_counter, item_counter in enumerate(cfg.lst_checked_counter_in_group + cfg.lst_checked_single_counter):
            #             arr_data[num][num_counter] = (arr_data[num][num_counter] + arr_data[num+1][num_counter])/2 # вычисляем среднее арифметическое
            #         arr_data = np.delete(arr_data, num+1 , axis = 0)
            #         arr_TimeAxis = np.delete(arr_TimeAxis, num+1 , axis = 0)
            #     if (num+1) >= arr_data.shape[0]: break
    return arr_data, arr_TimeAxis


def _insert_row(arr_ins, arr_axis, num_ins:int, key_strng:int):
    arr_ins = np.insert(arr_ins, num_ins+1, np.nan, axis=0)
    # arr_axis = np.insert(arr_axis, num_ins+1, np.nan, axis=0)
    arr_axis = np.insert(arr_axis, num_ins+1, 0, axis=0)
    arr_axis[num_ins+1][0] = key_strng
    return arr_ins, arr_axis

def _insert_row_itogo_month_group(arr_data, arr_TimeAxis, num_time, key_monthgr, len_arr, mesto, num_month, arr_summ_time_Group):
    arr_data, arr_TimeAxis = _insert_row(arr_data, arr_TimeAxis, num_time, key_monthgr)
    len_arr +=1
    for num_group, item_group in enumerate(cfg.lst_checked_group):
        arr_data[num_time+1][mesto[num_group]] = str(arr_summ_time_Group[1][num_month][num_group])
    num_time = num_time+1
    return arr_data, arr_TimeAxis, num_time, len_arr

def _insert_row_itogo_month_counter(arr_data, arr_TimeAxis, num_time, key_month, len_arr, num_month, arr_summ_time):
    arr_data, arr_TimeAxis = _insert_row(arr_data, arr_TimeAxis, num_time, key_month)
    len_arr +=1
    for num_counter, item_counter in enumerate(cfg.lst_checked_counter_in_group + cfg.lst_checked_single_counter):
        arr_data[num_time+1][num_counter] = str(arr_summ_time[1][num_month][num_counter])
    num_time = num_time+1
    return arr_data, arr_TimeAxis, num_time, len_arr

def _insert_row_itogo_day_counter(arr_data, arr_TimeAxis, num_time, key_day, len_arr, num_day, arr_summ_time):
    arr_data, arr_TimeAxis = _insert_row(arr_data, arr_TimeAxis, num_time, key_day)
    len_arr +=1
    for num_counter, item_counter in enumerate(cfg.lst_checked_counter_in_group + cfg.lst_checked_single_counter):
        arr_data[num_time+1][num_counter] = str(arr_summ_time[0][num_day][num_counter])
    num_time = num_time+1
    return arr_data, arr_TimeAxis, num_time, len_arr

def _insert_row_itogo_day_group(arr_data, arr_TimeAxis, num_time, key_daygr, len_arr, mesto, num_day, arr_summ_time_Group):
    arr_data, arr_TimeAxis = _insert_row(arr_data, arr_TimeAxis, num_time, key_daygr)
    len_arr +=1
    for num_group, item_group in enumerate(cfg.lst_checked_group):
        arr_data[num_time+1][mesto[num_group]] = str(arr_summ_time_Group[0][num_day][num_group])
    num_time = num_time+1
    return arr_data, arr_TimeAxis, num_time, len_arr

def insert_summ_v2 (arr_data, arr_TimeAxis, period_View:str, arr_summ_Alltime, arr_summ_Alltime_Group, arr_summ_time, arr_summ_time_Group, arr_symm_GroupPeriod):
    """вставка строк 'итого'
    """

    # ключи для установки в эти места определнных слов ИТОГО... или ВСЕГО...
    key_allday = 111  # 'ВСЕГО ДЕНЬ'
    # key_alldaygr = 222  # 'ВСЕГО ДЕНЬ ПО ГРУППЕ'
    # key_allmoth = 333  # 'ВСЕГО МЕСЯЦ'
    # key_allmothgr = 444  # 'ВСЕГО МЕСЯЦ ПО ГРУППЕ'
    # key_allyear = 555       # 'ВСЕГО ГОД'
    # key_allyeargr = 777     # 'ВСЕГО ГОД ПО ГРУППЕ'
    key_day = 110           # 'ИТОГО ДЕНЬ'
    key_daygr = 220         # 'ИТОГО ДЕНЬ ПО ГРУППЕ'
    key_month = 330          # 'ИТОГО МЕСЯЦ'
    key_monthgr = 440        # 'ИТОГО МЕСЯЦ ПО ГРУППЕ'
    # key_year = 550          # 'ИТОГО ГОД'
    # key_yeargr = 770        # 'ИТОГО ГОД ПО ГРУППЕ'
    key_groupPeriod = 880       # 'ИТОГО ПО ГРУППЕ ЗА ПЕРИОД'
    key_counterPeriod = 990       # 'ИТОГО ПО счетчику ЗА ПЕРИОД'

    # вычисление в какой столбец поместить Цифру Итого по группе
    # выход - список содержащий индексы столбцов для Итого
    mesto = []
    sm_mesto = 0
    for num_group, itemGroup in enumerate(cfg.lst_checked_group):
        mesto.append(sm_mesto)  # для первго Итого - нулевой столбец
        # узнаем какие счетчики содержит группа
        list_counter_in_group, rezult_get = msql.get_list_counter_in_group_DBGC(itemGroup)
        sm_mesto = sm_mesto + len(list_counter_in_group)
        

    # for num in range (arr.shape[0]-1,0,-1):
    len_arr = np.shape(arr_data)[0]
    num_time=0
    # num_lst_sum_day = 0
    # num_lst_sum_month = 0
    # num_lst_sum_year = 0
    # num_lst_sum_day_in_group = 0
    # num_lst_sum_month_in_group = 0
    # num_lst_sum_year_in_group = 0
    num_day = 0
    num_month = 0
    num_year = 0

    while num_time < len_arr-1:
        if (num_time+1) > len_arr-1: 
            break
        # если меняется число дня или месяца
        if  (arr_TimeAxis[num_time][2] != arr_TimeAxis[num_time+1][2]) or (arr_TimeAxis[num_time][1] != arr_TimeAxis[num_time+1][1]):
            # фиксируем день, месяц, год до шага и вставки строки и после
            day_past = arr_TimeAxis[num_time+1][2]
            day_future = arr_TimeAxis[num_time][2]
            month_past = arr_TimeAxis[num_time+1][1]
            month_future = arr_TimeAxis[num_time][1]
            year_past = arr_TimeAxis[num_time+1][0]
            year_future = arr_TimeAxis[num_time][0]
# если период отображения ДЕНЬ - то должны поставить ИТОГО МЕСЯЦ и ИТОГО ГОД
            if period_View == "день":
                # если меняется месяц - добавим ИТОГО МЕСЯЦ
                if month_past != month_future:
                    
                    arr_data, arr_TimeAxis, num_time, len_arr = _insert_row_itogo_month_counter(arr_data, arr_TimeAxis, num_time, key_month, len_arr, num_month,arr_summ_time)
                    # arr_data, arr_TimeAxis = _insert_row(arr_data, arr_TimeAxis, num_time, key_month)
                    # len_arr +=1
                    # for num_counter, item_counter in enumerate(cfg.lst_checked_counter_in_group + cfg.lst_checked_single_counter):
                    #     arr_data[num_time+1][num_counter] = str(arr_summ_time[1][num_month][num_counter])
                    # num_time = num_time+1

                    arr_data, arr_TimeAxis, num_time, len_arr = _insert_row_itogo_month_group(arr_data, arr_TimeAxis, num_time, key_monthgr, len_arr, mesto, num_month, arr_summ_time_Group)
                    # arr_data, arr_TimeAxis = insert_row(arr_data, arr_TimeAxis, num_time, key_mothgr)
                    # len_arr +=1
                    # for num_group, item_group in enumerate(cfg.lst_checked_group):
                    #     arr_data[num_time+1][mesto[num_group]] = str(arr_summ_time_Group[1][num_month][num_group])
                    # num_time = num_time+1

                    num_month +=1
                    

                if year_past != year_future:
                    pass
                    # # отключим ИТОГО год по группе
                    # arr_data, arr_TimeAxis = insert_row(arr_data, arr_TimeAxis, num_time, key_yeargr)
                    # len_arr +=1
                    # for num_group, item_group in enumerate(cfg.lst_checked_group):
                    #     arr_data[num_time+1][mesto[num_group]] = str(arr_summ_time_Group[2][num_year][num_group])

                    # num_time = num_time+1

                    # # отключим ИТОГО год по счетчику
                    # arr_data, arr_TimeAxis = insert_row(arr_data, arr_TimeAxis, num_time, key_year)
                    # len_arr +=1
                    # for num_counter, item_counter in enumerate(cfg.lst_checked_counter_in_group + cfg.lst_checked_single_counter):
                    #     arr_data[num_time+1][num_counter] = str(arr_summ_time[2][num_year][num_counter])
                    

                    # num_year +=1
                    # num_time = num_time+1
# если период отображения ЧАС - то должны поставить ИТОГО ДЕНЬ и ИТОГО МЕСЯЦ и ИТОГО ГОД
            if (period_View == "час") or (period_View == "30 мин"):
                # если меняется день - добавим ИТОГО ДЕНЬ
                if day_past != day_future:

                    arr_data, arr_TimeAxis, num_time, len_arr = _insert_row_itogo_day_counter(arr_data, arr_TimeAxis, num_time, key_day, len_arr, num_day, arr_summ_time)
                    # arr_data, arr_TimeAxis = _insert_row(arr_data, arr_TimeAxis, num_time, key_day)
                    # len_arr +=1
                    # for num_counter, item_counter in enumerate(cfg.lst_checked_counter_in_group + cfg.lst_checked_single_counter):
                    #     arr_data[num_time+1][num_counter] = str(arr_summ_time[0][num_day][num_counter])
                    # num_time = num_time+1

                    arr_data, arr_TimeAxis, num_time, len_arr = _insert_row_itogo_day_group(arr_data, arr_TimeAxis, num_time, key_daygr, len_arr, mesto, num_day, arr_summ_time_Group)
                    # arr_data, arr_TimeAxis = _insert_row(arr_data, arr_TimeAxis, num_time, key_daygr)
                    # len_arr +=1
                    # for num_group, item_group in enumerate(cfg.lst_checked_group):
                    #     arr_data[num_time+1][mesto[num_group]] = str(arr_summ_time_Group[0][num_day][num_group])
                    # num_time = num_time+1

                    num_day +=1                    
                    

                if month_past != month_future:

                    arr_data, arr_TimeAxis, num_time, len_arr = _insert_row_itogo_month_counter(arr_data, arr_TimeAxis, num_time, key_month, len_arr, num_month, arr_summ_time)
                    # arr_data, arr_TimeAxis = _insert_row(arr_data, arr_TimeAxis, num_time, key_month)
                    # len_arr +=1
                    # for num_counter, item_counter in enumerate(cfg.lst_checked_counter_in_group + cfg.lst_checked_single_counter):
                    #     arr_data[num_time+1][num_counter] = str(arr_summ_time[1][num_month][num_counter])
                    # num_time = num_time+1

                    arr_data, arr_TimeAxis, num_time, len_arr = _insert_row_itogo_month_group(arr_data, arr_TimeAxis, num_time, key_monthgr, len_arr, mesto, num_month,arr_summ_time_Group)
                    # arr_data, arr_TimeAxis = _insert_row(arr_data, arr_TimeAxis, num_time, key_monthgr)
                    # len_arr +=1
                    # for num_group, item_group in enumerate(cfg.lst_checked_group):
                    #     arr_data[num_time+1][mesto[num_group]] = str(arr_summ_time_Group[1][num_month][num_group])
                    # num_time = num_time+1

                    num_month +=1
                    

                if year_past != year_future:
                    pass
                    # # отключим ИТОГО год по группе
                    # arr_data, arr_TimeAxis = insert_row(arr_data, arr_TimeAxis, num_time, key_yeargr)
                    # len_arr +=1
                    # for num_group, item_group in enumerate(cfg.lst_checked_group):
                    #     arr_data[num_time+1][mesto[num_group]] = str(arr_summ_time_Group[2][num_year][num_group])

                    # num_time = num_time+1

                    # отключим ИТОГО год по счетчику
                    # arr_data, arr_TimeAxis = insert_row(arr_data, arr_TimeAxis, num_time, key_year)
                    # len_arr +=1
                    # for num_counter, item_counter in enumerate(cfg.lst_checked_counter_in_group + cfg.lst_checked_single_counter):
                    #     arr_data[num_time+1][num_counter] = str(arr_summ_time[2][num_year][num_counter])
                    

                    # num_year +=1
                    # num_time = num_time+1
# если период отображения МЕСЯЦ - то должны поставить ИТОГО ГОД , ИТОГО ГОД
            if period_View == "месяц":
                if year_past != year_future:
                    pass
                    # # отключим ИТОГО год по группе
                    # arr_data, arr_TimeAxis = insert_row(arr_data, arr_TimeAxis, num_time, key_yeargr)
                    # len_arr +=1
                    # for num_group, item_group in enumerate(cfg.lst_checked_group):
                    #     arr_data[num_time+1][mesto[num_group]] = str(arr_summ_time_Group[2][num_year][num_group])

                    # num_time = num_time+1

                    # # отключим ИТОГО год по счетчику
                    # arr_data, arr_TimeAxis = insert_row(arr_data, arr_TimeAxis, num_time, key_year)
                    # len_arr +=1
                    # for num_counter, item_counter in enumerate(cfg.lst_checked_counter_in_group + cfg.lst_checked_single_counter):
                    #     arr_data[num_time+1][num_counter] = str(arr_summ_time[2][num_year][num_counter])
                    

                    # num_year +=1
                    # num_time = num_time+1
        num_time +=1
#  если это последняя строка таблицы - сделаем заключительные ИТОГО для дня, месяца и года
        if num_time == len_arr-1: 

            if period_View == "день":
                
                arr_data, arr_TimeAxis, num_time, len_arr = _insert_row_itogo_month_counter(arr_data, arr_TimeAxis, num_time, key_month, len_arr, num_month, arr_summ_time)
                # arr_data, arr_TimeAxis = _insert_row(arr_data, arr_TimeAxis, num_time, key_month)
                # for num_counter, item_counter in enumerate(cfg.lst_checked_counter_in_group + cfg.lst_checked_single_counter):
                #     arr_data[num_time+1][num_counter] = str(arr_summ_time[1][num_month][num_counter])
                # num_time += 1

                arr_data, arr_TimeAxis, num_time, len_arr = _insert_row_itogo_month_group(arr_data, arr_TimeAxis, num_time, key_monthgr, len_arr, mesto, num_month, arr_summ_time_Group)
                # arr_data, arr_TimeAxis = _insert_row(arr_data, arr_TimeAxis, num_time, key_monthgr)
                # for num_group, item_group in enumerate(cfg.lst_checked_group):
                #     arr_data[num_time+1][mesto[num_group]] = str(arr_summ_time_Group[1][num_month][num_group])
                # num_time += 1

                # Добавлю пусую строку для наглядности
                # arr_data = np.insert(arr_data, num_time+1, np.nan, axis=0)
                # arr_TimeAxis = np.insert(arr_TimeAxis, num_time+1, 0, axis=0)
                # num_time += 1

                arr_data, arr_TimeAxis = _insert_row(arr_data, arr_TimeAxis, num_time, key_counterPeriod)
                for num_counter, item_counter in enumerate(cfg.lst_checked_counter_in_group + cfg.lst_checked_single_counter):
                    arr_data[num_time+1][num_counter] = str(arr_summ_time[2][num_year][num_counter])       # ПЕРЕДЕЛАТЬ!!!
                num_time += 1

                arr_data, arr_TimeAxis = _insert_row(arr_data, arr_TimeAxis, num_time, key_groupPeriod)
                for num_group, item_group in enumerate(cfg.lst_checked_group):
                    # arr_data[num_time+1][mesto[num_group]] = str(arr_symm_GroupPeriod[num_group])
                    arr_data[num_time+1][mesto[num_group]] = str(arr_summ_time_Group[2][num_year][num_group])       # ПЕРЕДЕЛАТЬ!!!
                num_time += 1

                
                
                num_month +=1
                

                # # отключим ИТОГО год по группе
                # arr_data, arr_TimeAxis = insert_row(arr_data, arr_TimeAxis, num_time, key_yeargr)
                # for num_group, item_group in enumerate(cfg.lst_checked_group):
                #         arr_data[num_time+1][mesto[num_group]] = str(arr_summ_time_Group[2][num_year][num_group])

                # num_time += 1

                # # отключим ИТОГО год по счетчику
                # arr_data, arr_TimeAxis = insert_row(arr_data, arr_TimeAxis, num_time, key_year)
                # for num_counter, item_counter in enumerate(cfg.lst_checked_counter_in_group + cfg.lst_checked_single_counter):
                #     arr_data[num_time+1][num_counter] = str(arr_summ_time[2][num_year][num_counter])


                break

            if period_View == "месяц":
                # # отключим ИТОГО год по группе
                # arr_data, arr_TimeAxis = insert_row(arr_data, arr_TimeAxis, num_time, key_yeargr)
                # for num_group, item_group in enumerate(cfg.lst_checked_group):
                #     arr_data[num_time+1][mesto[num_group]] = str(arr_summ_time_Group[2][num_year][num_group])

                # num_time += 1

                # # отключим ИТОГО год по счетчику
                # arr_data, arr_TimeAxis = insert_row(arr_data, arr_TimeAxis, num_time, key_year)
                # for num_counter, item_counter in enumerate(cfg.lst_checked_counter_in_group + cfg.lst_checked_single_counter):
                #     arr_data[num_time+1][num_counter] = str(arr_summ_time[2][num_year][num_counter])

                # Добавлю пусую строку для наглядности
                # arr_data = np.insert(arr_data, num_time+1, np.nan, axis=0)
                # arr_TimeAxis = np.insert(arr_TimeAxis, num_time+1, 0, axis=0)
                # num_time += 1

                arr_data, arr_TimeAxis = _insert_row(arr_data, arr_TimeAxis, num_time, key_counterPeriod)
                for num_counter, item_counter in enumerate(cfg.lst_checked_counter_in_group + cfg.lst_checked_single_counter):
                    arr_data[num_time+1][num_counter] = str(arr_summ_time[2][num_year][num_counter])       # ПЕРЕДЕЛАТЬ!!!
                num_time += 1
                
                arr_data, arr_TimeAxis = _insert_row(arr_data, arr_TimeAxis, num_time, key_groupPeriod)
                for num_group, item_group in enumerate(cfg.lst_checked_group):
                    arr_data[num_time+1][mesto[num_group]] = str(arr_summ_time_Group[2][num_year][num_group])       # ПЕРЕДЕЛАТЬ!!!
                num_time += 1

                break

            if (period_View == "час") or (period_View == "30 мин"):

                arr_data, arr_TimeAxis = _insert_row(arr_data, arr_TimeAxis, num_time, key_day)
                arr_data[num_time+1][0] = key_allday
                for num_counter, item_counter in enumerate(cfg.lst_checked_counter_in_group + cfg.lst_checked_single_counter):
                    arr_data[num_time+1][num_counter] = str(arr_summ_time[0][num_day][num_counter])
                num_time = num_time+1

                arr_data, arr_TimeAxis, num_time, len_arr = _insert_row_itogo_day_group(arr_data, arr_TimeAxis, num_time, key_daygr, len_arr, mesto, num_day, arr_summ_time_Group)
                # arr_data, arr_TimeAxis = _insert_row(arr_data, arr_TimeAxis, num_time, key_daygr)
                # for num_group, item_group in enumerate(cfg.lst_checked_group):
                #         arr_data[num_time+1][mesto[num_group]] = str(arr_summ_time_Group[0][num_day][num_group])
                # num_time = num_time+1


                
                arr_data, arr_TimeAxis, num_time, len_arr = _insert_row_itogo_month_counter(arr_data, arr_TimeAxis, num_time, key_month, len_arr, num_month, arr_summ_time)
                # arr_data, arr_TimeAxis = _insert_row(arr_data, arr_TimeAxis, num_time, key_month)
                # for num_counter, item_counter in enumerate(cfg.lst_checked_counter_in_group + cfg.lst_checked_single_counter):
                #     arr_data[num_time+1][num_counter] = str(arr_summ_time[1][num_month][num_counter])
                # num_time = num_time+1

                arr_data, arr_TimeAxis, num_time, len_arr = _insert_row_itogo_month_group(arr_data, arr_TimeAxis, num_time, key_monthgr, len_arr, mesto, num_month, arr_summ_time_Group)
                # arr_data, arr_TimeAxis = _insert_row(arr_data, arr_TimeAxis, num_time, key_monthgr)
                # for num_group, item_group in enumerate(cfg.lst_checked_group):
                #     arr_data[num_time+1][mesto[num_group]] = str(arr_summ_time_Group[1][num_month][num_group])
                # num_time = num_time+1

                

                # Добавлю пусую строку для наглядности
                # arr_data = np.insert(arr_data, num_time+1, np.nan, axis=0)
                # arr_TimeAxis = np.insert(arr_TimeAxis, num_time+1, 0, axis=0)
                # num_time += 1

                arr_data, arr_TimeAxis = _insert_row(arr_data, arr_TimeAxis, num_time, key_counterPeriod)
                for num_counter, item_counter in enumerate(cfg.lst_checked_counter_in_group + cfg.lst_checked_single_counter):
                    arr_data[num_time+1][num_counter] = str(arr_summ_time[2][num_year][num_counter])       # ПЕРЕДЕЛАТЬ!!!
                num_time += 1
                
                arr_data, arr_TimeAxis = _insert_row(arr_data, arr_TimeAxis, num_time, key_groupPeriod)
                for num_group, item_group in enumerate(cfg.lst_checked_group):
                    arr_data[num_time+1][mesto[num_group]] = str(arr_summ_time_Group[2][num_year][num_group])       # ПЕРЕДЕЛАТЬ!!!
                num_time += 1

                num_month +=1
                

                # # отключим ИТОГО год по группе
                # arr_data, arr_TimeAxis = insert_row(arr_data, arr_TimeAxis, num_time, key_yeargr)
                # for num_group, item_group in enumerate(cfg.lst_checked_group):
                #     arr_data[num_time+1][mesto[num_group]] = str(arr_summ_time_Group[2][num_year][num_group])

                # num_time = num_time+1

                # # отключим ИТОГО год по счетчику
                # arr_data, arr_TimeAxis = insert_row(arr_data, arr_TimeAxis, num_time, key_year)
                # for num_counter, item_counter in enumerate(cfg.lst_checked_counter_in_group + cfg.lst_checked_single_counter):
                #     arr_data[num_time+1][num_counter] = str(arr_summ_time[2][num_year][num_counter])

                break
    return arr_data, arr_TimeAxis, mesto



def calc_full_power(arr):
    """ вычисление полной мощьности
    """
    for num, val in enumerate(arr):
        # s=np.sqrt((arr[num][5]-arr[num][6])**2+(arr[num][7]-arr[num][8])**2)

        arr[num][5] = arr[num][5]-arr[num][6]
    # удалим лишние столбцы
    arr = np.delete(arr, [6,7,8] , axis = 1)
    return arr

def kWT(arr_data, arr_axisTime, lst_checked_group_and_conters):
    """приведение цифр из БД в реальные цифры кВт*час
    """
    # запросить из БД все счетчики  
    lst_counterDB, rezult_get = msql.getListCounterDB()
    if rezult_get:
        # по каждому счетчику
        for num_counter, item_counter in enumerate(lst_checked_group_and_conters):
            # ищем конкретный счетчик
            for itemCounter in lst_counterDB:
                if itemCounter['id'] == item_counter:
                    # применим постоянную счетчика A и коэфф ku,ki
                    koefA = itemCounter['koefA']
                    ki = 1 #float(itemCounter['ki'])
                    ku = 1 #float(itemCounter['ku'])
                    if (koefA == 0) or (koefA == ''): 
                        koefA = 1.0     # защита от дел на ноль ели в базе каким-то образом не оказалось этого коэффициента
                    # по всем временным меткам
                    for num, val in enumerate(arr_axisTime):
                        arr_data[num][num_counter] = (arr_data[num][num_counter]*ki*ku)/koefA


    return arr_data

def summ_per_day_and_month_and_year_v2(arr_data, arr_TimeAxis, lst_checked_group, lst_checked_counter_in_group, lst_checked_single_counter):
    """ найдем сумму для Итого за месяц (num_period_sum=1) - по каждому месяцу
    и для Итого за год (num_period_sum=0) 
    """
    num_period_view_day = 2 # индекс в массиве чисел дней
    num_period_view_month = 1 # индекс в массиве чисел месяца
    num_period_view_year = 0 # индекс в массиве чисел года
    num_counter = 0

    #  для сумм по полному времени
    arr_summ_Alltime = np.full(shape=(3, np.shape(arr_data)[0], len(lst_checked_counter_in_group + lst_checked_single_counter)),fill_value=0.0, dtype=float)
    # arr_summ_Alltime_day = np.full(shape=(np.shape(arr_data)[0], len(cfg.lst_checked_counter_in_group + cfg.lst_checked_single_counter)),fill_value=0.0, dtype=float)
    # arr_summ_Alltime_month = np.full(shape=(np.shape(arr_data)[0], len(cfg.lst_checked_counter_in_group + cfg.lst_checked_single_counter)),fill_value=0.0, dtype=float)
    # arr_summ_Alltime_year = np.full(shape=(np.shape(arr_data)[0], len(cfg.lst_checked_counter_in_group + cfg.lst_checked_single_counter)),fill_value=0.0, dtype=float)

    # для сумм по группам полного времени
    arr_summ_Alltime_Group = np.full(shape=(3, np.shape(arr_data)[0], len(lst_checked_group)),fill_value=0.0, dtype=float)
    # arr_summ_Alltime_dayGroup = np.full(shape=(np.shape(arr_data)[0], len(cfg.lst_checked_group)),fill_value=0.0, dtype=float)
    # arr_summ_Alltime_monthGroup = np.full(shape=(np.shape(arr_data)[0], len(cfg.lst_checked_group)),fill_value=0.0, dtype=float)
    # arr_summ_Alltime_yearGroup = np.full(shape=(np.shape(arr_data)[0], len(cfg.lst_checked_group)),fill_value=0.0, dtype=float)

    # по всем временным меткам
    num_day = 0
    num_month = 0
    num_year = 0
    num_group = 0
    for num_time, val in enumerate(arr_data):
        nv = 0
        # пройдемся по спску выбранных пльзователем групп
        for num_group, itemGroup in enumerate(lst_checked_group):
           # узнаем какие счетчики содержит группа
            list_counter_in_group, rezult_get = msql.get_list_counter_in_group_DBGC(itemGroup)
            for n, v in enumerate(list_counter_in_group):
                arr_summ_Alltime_Group[0][num_day][num_group] = arr_summ_Alltime_Group[0][num_day][num_group] + val[nv]
                arr_summ_Alltime_Group[1][num_month][num_group] = arr_summ_Alltime_Group[1][num_month][num_group] + val[nv]
                arr_summ_Alltime_Group[2][num_year][num_group] = arr_summ_Alltime_Group[2][num_year][num_group] + val[nv]
                nv +=1
        # по каждому счетчику
        for num_counter, item_counter in enumerate(lst_checked_counter_in_group + lst_checked_single_counter):
            arr_summ_Alltime[0][num_day][num_counter] =    arr_summ_Alltime[0][num_day][num_counter] +           val[num_counter]
            arr_summ_Alltime[1][num_month][num_counter] =  arr_summ_Alltime[1][num_month][num_counter] +   val[num_counter]
            arr_summ_Alltime[2][num_year][num_counter] =   arr_summ_Alltime[2][num_year][num_counter] +       val[num_counter]

        if num_time < np.shape(arr_data)[0]-1:
            # поменяется цифра дня ?
            if arr_TimeAxis[num_time][num_period_view_day] != arr_TimeAxis[num_time+1][num_period_view_day]:
                # запомнм сумму в выходном массиве Итого, т.е. перейдем на след день
                num_day +=1
            # поменяется цифра месяца ?
            if arr_TimeAxis[num_time][num_period_view_month] != arr_TimeAxis[num_time+1][num_period_view_month]:
                # запомнм сумму в выходном массиве Итого, т.е. перейдем на след месяц
                num_month +=1
            # поменяется цифра года ?
            if arr_TimeAxis[num_time][num_period_view_year] != arr_TimeAxis[num_time+1][num_period_view_year]:
                # запомнм сумму в выходном массиве Итого, т.е. перейдем на след год
                num_year +=1


    return arr_summ_Alltime, arr_summ_Alltime_Group


# def summ_per_day_and_month_and_year(arr_data, arr_TimeAxis):
#     """ найдем сумму для Итого за месяц (num_period_sum=1) - по каждому месяцу
#     и для Итого за год (num_period_sum=0) 
#     """
#     num_period_view_day = 2 # индекс в массиве чисел дней
#     num_period_view_month = 1 # индекс в массиве чисел месяца
#     num_period_view_year = 0 # индекс в массиве чисел года
#     num_counter = 0

#     #  для сумм по полному времени
#     arr_summ_Alltime_day = np.full(shape=(np.shape(arr_data)[0], len(cfg.lst_checked_counter_in_group + cfg.lst_checked_single_counter)),fill_value=0.0, dtype=float)
#     arr_summ_Alltime_month = np.full(shape=(np.shape(arr_data)[0], len(cfg.lst_checked_counter_in_group + cfg.lst_checked_single_counter)),fill_value=0.0, dtype=float)
#     arr_summ_Alltime_year = np.full(shape=(np.shape(arr_data)[0], len(cfg.lst_checked_counter_in_group + cfg.lst_checked_single_counter)),fill_value=0.0, dtype=float)

#     # для сумм по группам полного времени
#     arr_summ_Alltime_dayGroup = np.full(shape=(np.shape(arr_data)[0], len(cfg.lst_checked_group)),fill_value=0.0, dtype=float)
#     arr_summ_Alltime_monthGroup = np.full(shape=(np.shape(arr_data)[0], len(cfg.lst_checked_group)),fill_value=0.0, dtype=float)
#     arr_summ_Alltime_yearGroup = np.full(shape=(np.shape(arr_data)[0], len(cfg.lst_checked_group)),fill_value=0.0, dtype=float)

#     # по всем временным меткам
#     num_day = 0
#     num_month = 0
#     num_year = 0
#     num_group = 0
#     for num_time, val in enumerate(arr_data):
#         if num_time < np.shape(arr_data)[0]-1:        # защита от шага вперед - проверка на конец массива

#             nv = 0
#             # пройдемся по спску выбранных пльзователем групп
#             for num_group, itemGroup in enumerate(cfg.lst_checked_group):
#                 # узнаем какие счетчики содержит группа
#                 list_counter_in_group, rezult_get = msql.get_list_counter_in_group_DBGC(itemGroup)
#                 for n, v in enumerate(list_counter_in_group):
#                     # arr_summ_Alltime_dayGroup[num_day][num_group] = arr_summ_Alltime_dayGroup[num_day][num_group] + val[5+nv]
#                     # arr_summ_Alltime_monthGroup[num_month][num_group] = arr_summ_Alltime_monthGroup[num_month][num_group] + val[5+nv]
#                     # arr_summ_Alltime_yearGroup[num_year][num_group] = arr_summ_Alltime_yearGroup[num_year][num_group] + val[5+nv]
#                     arr_summ_Alltime_dayGroup[num_day][num_group] = arr_summ_Alltime_dayGroup[num_day][num_group] + val[nv]
#                     arr_summ_Alltime_monthGroup[num_month][num_group] = arr_summ_Alltime_monthGroup[num_month][num_group] + val[nv]
#                     arr_summ_Alltime_yearGroup[num_year][num_group] = arr_summ_Alltime_yearGroup[num_year][num_group] + val[nv]
#                     nv +=1

#             # по каждому счетчику
#             for num_counter, item_counter in enumerate(cfg.lst_checked_counter_in_group + cfg.lst_checked_single_counter):
#                 # arr_summ_Alltime_day[num_day][num_counter] = arr_summ_Alltime_day[num_day][num_counter] + val[5+num_counter]
#                 # arr_summ_Alltime_month[num_month][num_counter] = arr_summ_Alltime_month[num_month][num_counter] + val[5+num_counter]
#                 # arr_summ_Alltime_year[num_year][num_counter] = arr_summ_Alltime_year[num_year][num_counter] + val[5+num_counter]
#                 arr_summ_Alltime_day[num_day][num_counter] = arr_summ_Alltime_day[num_day][num_counter] +           val[num_counter]
#                 arr_summ_Alltime_month[num_month][num_counter] = arr_summ_Alltime_month[num_month][num_counter] +   val[num_counter]
#                 arr_summ_Alltime_year[num_year][num_counter] = arr_summ_Alltime_year[num_year][num_counter] +       val[num_counter]

#             # поменяется цифра дня ?
#             if arr_TimeAxis[num_time][num_period_view_day] != arr_TimeAxis[num_time+1][num_period_view_day]:
#                 # запомнм сумму в выходном массиве Итого, т.е. перейдем на след день
#                 num_day +=1
        
#             # поменяется цифра месяца ?
#             if arr_TimeAxis[num_time][num_period_view_month] != arr_TimeAxis[num_time+1][num_period_view_month]:
#                 # запомнм сумму в выходном массиве Итого, т.е. перейдем на след месяц
#                 num_month +=1

#             # поменяется цифра года ?
#             if arr_TimeAxis[num_time][num_period_view_year] != arr_TimeAxis[num_time+1][num_period_view_year]:
#                 # запомнм сумму в выходном массиве Итого, т.е. перейдем на след год
#                 num_year +=1


#     return arr_summ_Alltime_day, arr_summ_Alltime_month, arr_summ_Alltime_year, arr_summ_Alltime_dayGroup, arr_summ_Alltime_monthGroup, arr_summ_Alltime_yearGroup



def create_header_table(lst_checked_counter):
    """сделаем список для заголовки шапки таблицы на экране названиями выбранных счетчиков
    """
    lst_index_backgroundcolor_group = []
    index_color = 0
    lst_header_table = ['Дата', 'Время']
    # lst_header_table = ["",""]
    lst_index_backgroundcolor_group.append(index_color)
    lst_index_backgroundcolor_group.append(index_color)
    list_GroupDB, rezult_getListOfGroupDB = msql.getListGroupDB()
        # узнаем полное наименование счетчика через id  и добавим его в первую строку массива
    list_counterDB, rezult_getListOfCounterDB = msql.getListCounterDB()
    if rezult_getListOfCounterDB:
# вначале выходного списка для создания Header внесем сочетание Группа/счетчик
        num_counters_in_groups = 0  # посчитаем общее количество счетчиков в выбранных группах
        # пройдемся по спску выбранных пльзователем групп
        for itemGroup in cfg.lst_checked_group:
            
            
            # узнаем какие счетчики содержит группа
            list_counter_in_group, rezult_get = msql.get_list_counter_in_group_DBGC(itemGroup)
            for item_counter in list_counter_in_group:
                lst_index_backgroundcolor_group.append(index_color)
                # узнаю имя счетчика
                for item in list_counterDB:
                    if item['id'] == item_counter:
                        name_counter = item["name_counter_full"]
                # узнаю имя группы 
                for item in list_GroupDB:
                    if item['id'] == itemGroup:
                        name_group = item["name_group_full"]
                #
                lst_header_table.append("Группа:" + name_group +"\n"+"\n"+name_counter)
                # lst_header_table.append(name_counter)
                num_counters_in_groups +=1
            index_color +=1

# после выходной список дополним одиночными счетчиками
        #  для начала выделим из списка только одиночные счетчики         
        lst_checked_counter = lst_checked_counter[num_counters_in_groups:]

        for item_checked in lst_checked_counter:
            for item in list_counterDB:
                if item['id'] == item_checked:
                    lst_header_table.append(item["name_counter_full"])
                    lst_index_backgroundcolor_group.append(index_color)
                    index_color +=1

    return lst_header_table, lst_index_backgroundcolor_group


def create_header_table2(lst_checked_counter):
    """сделаем список для заголовки шапки таблицы на экране названиями выбранных счетчиков
    """

    lst_header_table = ['Дата', 'Время']
    list_GroupDB, rezult_getListOfGroupDB = msql.getListGroupDB()
        # узнаем полное наименование счетчика через id  и добавим его в первую строку массива
    list_counterDB, rezult_getListOfCounterDB = msql.getListCounterDB()
    if rezult_getListOfCounterDB:
# вначале выходного списка для создания Header внесем сочетание Группа/счетчик
        num_counters_in_groups = 0  # посчитаем общее количество счетчиков в выбранных группах
        # пройдемся по спску выбранных пльзователем групп
        for itemGroup in cfg.lst_checked_group:
            # узнаем какие счетчики содержит группа
            list_counter_in_group, rezult_get = msql.get_list_counter_in_group_DBGC(itemGroup)
            for item_counter in list_counter_in_group:
                # узнаю имя счетчика
                for item in list_counterDB:
                    if item['id'] == item_counter:
                        name_counter = item["name_counter_full"]
                # узнаю имя группы 
                for item in list_GroupDB:
                    if item['id'] == itemGroup:
                        name_group = item["name_group_full"]
                #
                lst_header_table.append("\nГруппа:\n" + name_group+"\n\n")# +"\n"+name_counter)
                num_counters_in_groups +=1

# после выходной список дополним одиночными счетчиками
        #  для начала выделим из списка только одиночные счетчики         
        lst_checked_counter = lst_checked_counter[num_counters_in_groups:]

        for item_checked in lst_checked_counter:
            for item in list_counterDB:
                if item['id'] == item_checked:
                    # lst_header_table.append(item["name_counter_full"])
                    lst_header_table.append("")

    return lst_header_table



# def kWT_summ(arr_summ_Alltime_day, arr_summ_Alltime_month, arr_summ_Alltime_year, arr_summ_Alltime_dayGroup, arr_summ_Alltime_monthGroup, arr_summ_Alltime_yearGroup):

#     # # по каждому счетчику
#     # for num_counter, item_counter in enumerate(cfg.lst_checked_counter_in_group + cfg.lst_checked_single_counter):
#     #     # по всем временным меткам
#     #     for num, val in enumerate(arr):
#     #         # запросить из БД все счетчики  
#     #         lst_counterDB, rezult_get = msql.getListCounterDB()
#     #         if rezult_get:
#     #             for itemCounter in lst_counterDB:
#     #                 if itemCounter['koefA']:
#     #                     # делим на постоянную счетчика A
#     #                     koefA = itemCounter['koefA']
#     #                     if koefA == 0: koefA =1     # защита от дел на ноль
#     #                     arr[num][num_counter] = arr[num][num_counter]/itemCounter['koefA']
#     #                     arr_summ_Alltime_day[num_day][num_counter] = arr_summ_Alltime_day[num_day][num_counter] + val[5+num_counter]
#     #                     arr_summ_Alltime_month[num_month][num_counter] = arr_summ_Alltime_month[num_month][num_counter] + val[5+num_counter]
#     #                     arr_summ_Alltime_year[num_year][num_counter] = arr_summ_Alltime_year[num_year][num_counter] + val[5+num_counter]

#     arr_summ_Alltime_day = arr_summ_Alltime_day /1000
#     arr_summ_Alltime_month = arr_summ_Alltime_month /1000
#     arr_summ_Alltime_year = arr_summ_Alltime_year /1000
#     arr_summ_Alltime_dayGroup = arr_summ_Alltime_dayGroup /1000
#     arr_summ_Alltime_monthGroup = arr_summ_Alltime_monthGroup /1000
#     arr_summ_Alltime_yearGroup = arr_summ_Alltime_yearGroup /1000
#     # # по каждому счетчику
#     # for num_counter, item_counter in enumerate(cfg.lst_checked_counter_in_group + cfg.lst_checked_single_counter):
#     #     # по всем временным меткам
#     #     for num, val in enumerate(arr_summ_Alltime_day):
#     #         # делим на постоянную счетчика A=1000
#     #         arr_summ_Alltime_day[num][num_counter] = arr_summ_Alltime_day[num][num_counter]/1000
#     #     for num, val in enumerate(arr_summ_Alltime_day):
#     #         # делим на постоянную счетчика A=1000
#     #         arr_summ_Alltime_month[num][num_counter] = arr_summ_Alltime_month[num][num_counter]/1000
#     #     for num, val in enumerate(arr_summ_Alltime_day):
#     #         # делим на постоянную счетчика A=1000
#     #         arr_summ_Alltime_year[num][num_counter] = arr_summ_Alltime_year[num][num_counter]/1000
#     return arr_summ_Alltime_day, arr_summ_Alltime_month, arr_summ_Alltime_year, arr_summ_Alltime_dayGroup, arr_summ_Alltime_monthGroup, arr_summ_Alltime_yearGroup

def appendZero(a:str):
    if (len(a) == 1):
        a='0'+ a
    return a


def cut_arr_custom_time(arr_data, arr_TimeAxis_full, dateFrom, dateTo):
    """ Обрезка массивов в соответвии с датами, которые выбрал пользователь
        Arg:
        arr_data, arr_TimeAxis_full: array of numpy- должны быть равны по длинному измерению оси времени
        dateFrom, dateTo:datetime - дата/время начала и конца обрезки массивов
    """
    num_dateFrom = 0
    num_dateTo = 0
    stop_from = False
    stop_to = False
    dateFrom = dateFrom.replace(hour=0,  minute = 30)
    for num_arrTimeAxis, val_arrTimeAxis in enumerate(arr_TimeAxis_full):
        dt_arrTimeAxis = datetime(val_arrTimeAxis[0], val_arrTimeAxis[1], val_arrTimeAxis[2], val_arrTimeAxis[3], val_arrTimeAxis[4])
        if (dateFrom <= dt_arrTimeAxis) and not(stop_from):
            num_dateFrom = num_arrTimeAxis
            stop_from = True
        # if (dateTo < dt_arrTimeAxis) and not(stop_to):
        if (dt_arrTimeAxis >= dateTo) and not(stop_to):
            num_dateTo = num_arrTimeAxis+1
            stop_to = True
        if stop_from and stop_to: 
            break
    arr_data_cust = arr_data[num_dateFrom:num_dateTo,:]
    arr_TimeAxis_cust = arr_TimeAxis_full[num_dateFrom:num_dateTo,:]
    return arr_data_cust, arr_TimeAxis_cust



def korrekt_dataDB(arr_dataDB, dateFrom:datetime, dateTo:datetime):
    """ корректировка данных профиля мощности  полученных из БД - добавление пустых пропущенных/напринятых профилей 30-минуток
    """
    num_rowDB = 0
    tick_datetime = dateFrom
    while tick_datetime <= dateTo:
        dt_arr_dataDB = datetime(arr_dataDB[num_rowDB][0], arr_dataDB[num_rowDB][1], arr_dataDB[num_rowDB][2], arr_dataDB[num_rowDB][3], arr_dataDB[num_rowDB][4])
        if tick_datetime == dt_arr_dataDB:
            num_rowDB += 1
            tick_datetime = tick_datetime + timedelta(minutes=30)
        elif tick_datetime < dt_arr_dataDB:
            # если в исодном массиве данных из БД нашлись непринятые 30-минутки т.е. возникли "пробелы"
            # вставим в "пробелы" пустые строки с отсутвтующими datetime-ами и с данными= 0
            #  
            # подготовим строку для вставки
            date_tuple = tick_datetime.timetuple()
            # поскольку неизвестно сколько счетчиков и групп выбрано - возьмем обычную строку из БД и на ее базе сделаем пустую
            arr_data = arr_dataDB[0,:]
            arr_insert = np.full(shape=(np.shape(arr_data)),fill_value=0)
            arr_insert[0] = date_tuple[0]
            arr_insert[1] = date_tuple[1]
            arr_insert[2] = date_tuple[2]
            arr_insert[3] = date_tuple[3]
            arr_insert[4] = date_tuple[4]
            #
            arr_dataDB = np.insert(arr_dataDB, num_rowDB, arr_insert, axis=0)
        elif tick_datetime > dt_arr_dataDB:
            # защита от дубликатов записей (с одинаковыми datetime). В конечном массиве остается первый дубликат
            arr_dataDB = np.delete(arr_dataDB, num_rowDB, 0)
    return arr_dataDB

def create_full_datetime_FromTo(de_dateFrom: QDate, de_dateTo: QDate):
    """ подготавливаем даты От и До
    как для выбранного пользователем диапазона,
    так и полного диапазона - там где ОТ: от первого числа месяца, - там где ДО: до последнего числа месяца (для вычисления суммы "ВСЕГО")
    In:
    de_dateFrom: QDate, de_dateTo: QDate - данные из QDateEdit приложения/окна/виджета
    Out:
    dateFrom, dateTo :datetime - даты От и До для выбранного пользователем диапазона в формате datetime
    full_date_From, full_date_To: datetime - даты От и До для полного диапазона в формате datetime
    """
    full_date_From = None
    full_date_To =None
    date_From = None
    date_To = None
    # преобразуем составне части в формат datetime
    date_From = de_dateFrom.dateTime().toPyDateTime()
    #конечную дату дополним часами до конца дня, до 23.30
    date_To = de_dateTo.dateTime().toPyDateTime().replace(hour=23,  minute = 30)
    # вычисляем полные полные месяца
    full_date_From = de_dateFrom.dateTime().toPyDateTime().replace(day =1 , hour=0,  minute = 0)
    selected_date = date_To
    if selected_date.month == 12: # December
        last_day_selected_month = date(selected_date.year, selected_date.month, 31)
    else:
        last_day_selected_month = date(selected_date.year, selected_date.month + 1, 1) - timedelta(days=1)
    full_date_To = selected_date.replace(day=last_day_selected_month.day , hour=23,  minute = 30)
    return full_date_From, full_date_To, date_From, date_To

def create_Array_TimeAxis(dateFrom_full, dateTo_full):
    """ создаем массив временной оси (массив с датами времени) для таблицы профиля мощности
    """
    rezult = False
    arr_TimeAxis = None
    try:
        lst_datetime_step30_full, lstsu_full, rezult = createLstIntervalDateTime(dateFrom=dateFrom_full, dateTo=dateTo_full, stepTime=30)
        arr_TimeAxis = np.array(lstsu_full)
        rezult = True
    except:
        rezult = False
    return arr_TimeAxis, rezult