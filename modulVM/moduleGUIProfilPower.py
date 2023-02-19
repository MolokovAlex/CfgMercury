# moduleConfigApp
# autor: MolokovAlex
# coding: utf-8

# модуль окна Профиля мощности

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
# from PyQt5.QtCore import QDateTime
from PyQt5.QtGui import *
from time import time
import numpy as np
import datetime # обязательно до import sqlite3 as sql3  !!!!!
from datetime import date, timedelta
from statistics import mean
import sqlite3 as sql3
from xlsxwriter.workbook import Workbook

# import modulVM.moduleConfigApp as mca
import modulVM.config as cfg
# import modulVM.moduleProtocolMercury as mpm
# import modulVM.moduleGUIProfilPower as mgpp
# import modulVM.moduleGUIIstantly as mgi
import modulVM.moduleSQLite as msql
import modulVM.moduleGeneral as mg
import modulVM.moduleLogging as ml


class TableProfilePowerDialog(QDialog):
        inc_progressDB = pyqtSignal(int)
        send_message_statusBar = pyqtSignal(str)
        def __init__(self, data=np.array([[]]), parent=None):
            # super().__init__()
            super(TableProfilePowerDialog, self).__init__(parent)
            self.setWindowFlags(self.windowFlags()
                | Qt.WindowMinimizeButtonHint
                | Qt.WindowMaximizeButtonHint
                )
            self.setMinimumSize(QSize(800, 600))         # Устанавливаем размеры
            self.setWindowTitle("Таблица профиля мощности") # Устанавливаем заголовок окна

            layout = QGridLayout()

            # флаг разрешения нажатия на кнопки Обновить и Импорт в Иксель - пока не выбраны счетчики и группы он опущен
            self.flag_caseCountersAndGroups = False
            # значение Combox периода интегрирования в окне профиля мощности
            self.period_integr = ""
            
            self.lst_checkItemTree=[]

            btn_caseCountsAndGroups = QPushButton("Выбор счетчиков и групп")
            layout.addWidget(btn_caseCountsAndGroups, 1, 0)
            btn_caseCountsAndGroups.clicked.connect(self.click_btn_caseCountsAndGroups)
            
            self.de_dateFrom = QDateEdit(self)
            layout.addWidget(self.de_dateFrom, 1, 2)
            self.de_dateFrom.setCalendarPopup(True) 
            ddatefrom = QDate.currentDate()
            # ddatefrom.currentDate()
            # self.de_dateFrom.setDate(QDate(2022, 12, 25))
            self.de_dateFrom.setDate(ddatefrom)

            lbl_empty2 = QLabel("<-интервал->")
            layout.addWidget(lbl_empty2, 1, 3)
            lbl_empty2.setAlignment(Qt.AlignCenter)

            self.de_dateTo = QDateEdit(self)
            layout.addWidget(self.de_dateTo, 1, 4)
            self.de_dateTo.setCalendarPopup(True)
            # self.de_dateTo.setDate(QDate(2022, 12, 25))
            # d = ddatefrom.addDays(2)
            # print(d)
            self.de_dateTo.setDate(ddatefrom.addDays(7))

            lbl_empty4 = QLabel("Период отображения")
            layout.addWidget(lbl_empty4, 1, 6)
            lbl_empty4.setAlignment(Qt.AlignRight)
            self.cb_interval = QComboBox()
            layout.addWidget(self.cb_interval, 1, 7)
            self.cb_interval.addItems(cfg.VALUE_PERIOD_INTEGR_POFIL)
            self.cb_interval.currentIndexChanged.connect( self.change_cb_interval )
            self.period_integr = self.cb_interval.currentText()

            self.btnRefreshTableProfilePowerCounts = QPushButton("Обновить")
            layout.addWidget(self.btnRefreshTableProfilePowerCounts, 1, 9)
            self.btnRefreshTableProfilePowerCounts.clicked.connect(self.click_btnRefreshTableProfilePowerCounts_ver2)
            if not self.flag_caseCountersAndGroups:
                self.btnRefreshTableProfilePowerCounts.setEnabled(False)
            else:
                self.btnRefreshTableProfilePowerCounts.setEnabled(True) 

            # ckb_cycleRefresh = QCheckBox("циклически")
            # layout.addWidget(ckb_cycleRefresh, 1, 10)

            lbl_empty3 = QLabel("    ")
            layout.addWidget(lbl_empty3, 1, 11)

            self.btnImportTableProfilePowerCounts = QPushButton("Импорт в Excel")
            layout.addWidget(self.btnImportTableProfilePowerCounts, 1, 12)
            self.btnImportTableProfilePowerCounts.clicked.connect(self.click_bth_ImportInExcel)
            if not self.flag_caseCountersAndGroups:
                self.btnImportTableProfilePowerCounts.setEnabled(False)
            else:
                self.btnImportTableProfilePowerCounts.setEnabled(True)    
        
            #
            self.model2 = NpModel2()
            self.tableProfilePowerCounts2 = QTableView()
            self.tableProfilePowerCounts2.setModel(self.model2)
            self.tableProfilePowerCounts2.horizontalHeader().setSectionResizeMode(0)
            # self.tableProfilePowerCounts.horizontalHeader().setSectionResizeMode(1)#,QHeaderView.ResizeToContents)
            # self.tableProfilePowerCounts.horizontalHeader().hide()
            self.tableProfilePowerCounts2.verticalHeader().hide()
            self.tableProfilePowerCounts2.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
            layout.addWidget(self.tableProfilePowerCounts2,2,0, 2, 13)
            #



            self.model = NpModel()
            self.tableProfilePowerCounts = QTableView()
            self.tableProfilePowerCounts.setModel(self.model)
            self.tableProfilePowerCounts.horizontalHeader().setSectionResizeMode(0)
            # self.tableProfilePowerCounts.horizontalHeader().setSectionResizeMode(1)#,QHeaderView.ResizeToContents)
            # self.tableProfilePowerCounts.horizontalHeader().hide()
            self.tableProfilePowerCounts.verticalHeader().hide()
            self.tableProfilePowerCounts.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
            # layout.addWidget(self.tableProfilePowerCounts,2,0, 10, 13)
            layout.addWidget(self.tableProfilePowerCounts,3,0, 10, 13)

            self.setLayout(layout)

            # self.load()
            self.tableProfilePowerCounts.resizeColumnsToContents()
            return None
        
        def emit_string_statusBar(self, strg):
            self.send_message_statusBar.emit(strg)
            return None

        def emit_value(self, value):
            self.inc_progressDB.emit(value)
            return None

        def change_cb_interval(self):
            """
            Изменение в переменной периода интергрирования - вывода на экран
            """
            self.period_integr = self.cb_interval.currentText()

        def click_btn_caseCountsAndGroups(self):
            """
                Обработка нажания кноепки Выбор счетчиков и групп
                Выводиться окно с Tree
            
            """
            self.flag_caseCountersAndGroups = False
            self.DialogCaseCounterAndGroups = QDialog()
            self.DialogCaseCounterAndGroups.setWindowTitle("Выбор счетчиков и групп")
            self.DialogCaseCounterAndGroups.setWindowModality(Qt.ApplicationModal)
            self.DialogCaseCounterAndGroups.resize(400, 600)
        
            layout = QGridLayout()
            self.DialogCaseCounterAndGroups.setLayout(layout)
            self.tree = QTreeWidget()
            self.renderTreePanel_for_ProfilPower()
            # self.tree.clicked.connect(self.click_onClickedOnItemTree)
            layout.addWidget(self.tree,0,0,2,2)
            
            btn_OKCase = QPushButton("OK")
            layout.addWidget(btn_OKCase, 2, 0)
            btn_OKCase.clicked.connect(self.click_btn_OKCase)
            btn_CancelCase = QPushButton("Cancel")
            layout.addWidget(btn_CancelCase, 2, 1)
            btn_CancelCase.clicked.connect(self.click_btn_CancelCase)

            self.DialogCaseCounterAndGroups.exec_()
            return None
        
        
        
        def click_btn_OKCase(self):
            """
            обработка нажатия клавиши ОК в окне выбора счетчиков и групп
            """
            # составим список элементов, где пользователь поставиль галочки в дереве
            self.lst_checkItemTree=[]
            iterator = QTreeWidgetItemIterator(self.tree, QTreeWidgetItemIterator.Checked)
            while iterator.value():
                item = iterator.value()
                # print (item.text(0))
                self.lst_checkItemTree.append(item.text(0))
                iterator += 1
            # если какой то выбор сделан - разблокированить кнопки Обновить и Экспорт в Иксель
            if self.lst_checkItemTree:
                self.flag_caseCountersAndGroups = True
                self.btnRefreshTableProfilePowerCounts.setEnabled(True)
                self.btnImportTableProfilePowerCounts.setEnabled(True) 
            else:
                # если пользователь снял все галочки
                self.flag_caseCountersAndGroups = False
                self.btnRefreshTableProfilePowerCounts.setEnabled(False)
                self.btnImportTableProfilePowerCounts.setEnabled(False)
            # создаем список выбранных пользователем групп и список выбранных счетчиков - все по отдельности
            cfg.lst_checked_counter_in_group, cfg.lst_checked_group, cfg.lst_checked_single_counter = mg.createLstCheckedCounterAndGroups(self.lst_checkItemTree)
            # закроем диалоговое окно
            self.DialogCaseCounterAndGroups.hide()    
            return
        
        def click_btn_CancelCase(self):
            """
            обработка нажатия клавиши Cancel в окне выбора счетчиков и групп
            """
            # закроем диалоговое окно
            self.DialogCaseCounterAndGroups.hide()
            return
        
        def create_Array_TimeAxis(self):
            """ создаем массив временной оси (массив с датами времени) для таблицы профиля мощности
            """
            rezult = False
            arr_TimeAxis = None
            dateFrom_full = None
            dateTo_full =None
            dateFrom = None
            dateTo = None
            try:
                # создает список с штампами времени типа datetime от даты dateFrom до даты dateTo с шагом
                # преобразуем составне части в формат datetime
                dateFrom = self.de_dateFrom.dateTime().toPyDateTime()
                #конечную дату дополним часами до конца дня, до 23.30
                dateTo = self.de_dateTo.dateTime().toPyDateTime().replace(hour=23,  minute = 30)
                # вычисляем полные полные месяца
                dateFrom_full = self.de_dateFrom.dateTime().toPyDateTime().replace(day =1 , hour=0,  minute = 0)
                selected_date = dateTo
                if selected_date.month == 12: # December
                    last_day_selected_month = date(selected_date.year, selected_date.month, 31)
                else:
                    last_day_selected_month = date(selected_date.year, selected_date.month + 1, 1) - timedelta(days=1)
                dateTo_full = selected_date.replace(day=last_day_selected_month.day , hour=23,  minute = 30)
                #
                lst_datetime_step30_full, lstsu_full, rezult = mg.createLstIntervalDateTime(dateFrom=dateFrom_full, dateTo=dateTo_full, stepTime=30)
                arr_TimeAxis = np.array(lstsu_full)
                rezult = True
            except:
                rezult = False

            return arr_TimeAxis, dateFrom_full, dateTo_full, dateFrom, dateTo, rezult

        def click_btnRefreshTableProfilePowerCounts_ver2(self):
            """
                нажатие на кнопку Обновить
            """
            t0 = time()
            self.emit_string_statusBar("Пожалуйста, подождите. Идут запросы в БД...")
            self.emit_value(5)

            # создаем массив временной оси (массив с датами времени) для таблицы профиля мощности
            arr_TimeAxis_full, dateFrom_full, dateTo_full, dateFrom, dateTo, rezult = self.create_Array_TimeAxis()
            #
            self.emit_value(20)
            if rezult:
                self.emit_value(25)
                #
                #  сделаем пустой массив с количеством столбцов равным количеству выбранных счетчиков и с количеством строк - количеству временных меток в массиве оси времени
                arr_data = np.full(shape=(np.shape(arr_TimeAxis_full)[0], len(cfg.lst_checked_counter_in_group + cfg.lst_checked_single_counter)),fill_value=0)

                for num_counter, item_counter in enumerate(cfg.lst_checked_counter_in_group + cfg.lst_checked_single_counter):
                    rezult, lst_data = msql.selectPandQfromDBPP(item_counter=item_counter, item_datetime=None, dateFrom=dateFrom_full, dateTo=dateTo_full)
                    if rezult:
                        arr_dataDB = np.array(lst_data)
                        # вычисление полной мощьности
                        arr_dataDB = mg.calc_full_power(arr_dataDB)
                        #
                        # защита от пустых строк в БД, коорые можно затащить в datetime header
                        num_rowDB = 0
                        for num_arrTimeAxis, val_arrTimeAxis in enumerate(arr_TimeAxis_full):
                            dt_arrTimeAxis = datetime.datetime(val_arrTimeAxis[0], val_arrTimeAxis[1], val_arrTimeAxis[2], val_arrTimeAxis[3], val_arrTimeAxis[4])
                            dt_arr_dataDB = datetime.datetime(arr_dataDB[num_rowDB][0], arr_dataDB[num_rowDB][1], arr_dataDB[num_rowDB][2], arr_dataDB[num_rowDB][3], arr_dataDB[num_rowDB][4])
                            # если даты и времена совпадают с датой и временем заголовка
                            if dt_arrTimeAxis == dt_arr_dataDB:
                                arr_data[num_arrTimeAxis][num_counter] = arr_dataDB[num_rowDB][5]
                                num_rowDB +=1
                                if num_rowDB >= np.shape(arr_dataDB)[0]: break
                            if dt_arrTimeAxis < dt_arr_dataDB:
                                pass
                            if dt_arrTimeAxis > dt_arr_dataDB:
                                arr = np.insert(arr, num_arrTimeAxis+1, arr_dataDB[num_rowDB], axis=0) # ??????????????????????????????
                                num_rowDB +=1
                                if num_rowDB >= np.shape(arr_dataDB)[0]: break

                # теперь в массиве будут храниться числа с плавающей точкой
                arr_data = np.array(arr_data, dtype=float)
                # переведем абстрактные числа из БД в реальные используя коэфф счетчика A
                arr_data = mg.kWT(arr_data, arr_TimeAxis_full, cfg.lst_checked_counter_in_group + cfg.lst_checked_single_counter)
                #
                # обрежем массив в соответвии с датами, которые выбрал пользователь
                arr_data_custom, arr_TimeAxis_custom = mg.cut_arr_custom_time(arr_data, arr_TimeAxis_full, dateFrom, dateTo)
                #
                # найдем сумму для ВСЕГО 
                arr_summ_Alltime, arr_summ_Alltime_Group =mg.summ_per_day_and_month_and_year_v2(arr_data_custom, arr_TimeAxis_custom, cfg.lst_checked_group, cfg.lst_checked_counter_in_group, cfg.lst_checked_single_counter)
                #
                # найдем сумму для ИТОГО 
                arr_summ_Alltime_custom, arr_summ_Alltime_Group_custom =mg.summ_per_day_and_month_and_year_v2(arr_data_custom, arr_TimeAxis_custom, cfg.lst_checked_group, cfg.lst_checked_counter_in_group, cfg.lst_checked_single_counter)
                #
                #  Сделаем ИТОГО за период по группе
                summGroupPeriod = np.full(shape=(len(cfg.lst_checked_group)),fill_value=0.0, dtype=float)

                # приведение к виду периода отображения
                arr_data_custom, arr_TimeAxis_custom = mg.createView_periodView(arr_data_custom, arr_TimeAxis_custom, self.period_integr)
                #
                # вставка строк/столбцов суммы как итого
                arr_data_custom, arr_TimeAxis_custom, mesto = mg.insert_summ_v2(arr_data_custom, arr_TimeAxis_custom, self.period_integr, arr_summ_Alltime, arr_summ_Alltime_Group, arr_summ_Alltime_custom, arr_summ_Alltime_Group_custom, summGroupPeriod)
                # округлим все  float в массиве до трех знаков после запятой
                arr_data_custom = np.around(arr_data_custom, 3)
                #
                # перобразовать массив из  int в str чтобы добавлять текст "итого"
                # преобразуем и дату и загоовок, а потом склеим
                arr_data_custom = np.array(arr_data_custom, dtype=str)
                #
                arr_TimeAxis_custom = np.array(arr_TimeAxis_custom, dtype='<U25')
                # добавим для временных ячеек дополнительный 0 к одиночным цифрам и подготовим дату и время к виду DD.MM.YYYY  и  HH:MM
                # по всем временным меткам
                for num_time, val in enumerate(arr_TimeAxis_custom):
                    if arr_TimeAxis_custom[num_time][0] ==   '111': 
                        arr_TimeAxis_custom[num_time][0] = 'ВСЕГО ДЕНЬ'
                        arr_TimeAxis_custom[num_time][3] = ''
                    elif arr_TimeAxis_custom[num_time][0] == '222': 
                        arr_TimeAxis_custom[num_time][0] = 'ВСЕГО ДЕНЬ ПО ГРУППЕ'
                        arr_TimeAxis_custom[num_time][3] = ''
                    elif arr_TimeAxis_custom[num_time][0] == '333': 
                        arr_TimeAxis_custom[num_time][0] = 'ВСЕГО МЕСЯЦ'
                        arr_TimeAxis_custom[num_time][3] = ''
                    elif arr_TimeAxis_custom[num_time][0] == '444': 
                        arr_TimeAxis_custom[num_time][0] = 'ВСЕГО МЕСЯЦ ПО ГРУППЕ'
                        arr_TimeAxis_custom[num_time][3] = ''
                    elif arr_TimeAxis_custom[num_time][0] == '555': 
                        arr_TimeAxis_custom[num_time][0] = 'ВСЕГО ГОД'
                        arr_TimeAxis_custom[num_time][3] = ''
                    elif arr_TimeAxis_custom[num_time][0] == '777': 
                        arr_TimeAxis_custom[num_time][0] = 'ВСЕГО ГОД ПО ГРУППЕ'
                        arr_TimeAxis_custom[num_time][3] = ''
                    elif arr_TimeAxis_custom[num_time][0] == '110': 
                        arr_TimeAxis_custom[num_time][0] = 'ИТОГО ДЕНЬ'
                        arr_TimeAxis_custom[num_time][3] = ''
                    elif arr_TimeAxis_custom[num_time][0] == '220': 
                        arr_TimeAxis_custom[num_time][0] = 'ИТОГО ДЕНЬ ПО ГРУППЕ'
                        arr_TimeAxis_custom[num_time][3] = ''
                    elif arr_TimeAxis_custom[num_time][0] == '330':
                        arr_TimeAxis_custom[num_time][0] = 'ИТОГО МЕСЯЦ'
                        arr_TimeAxis_custom[num_time][3] = ''
                    elif arr_TimeAxis_custom[num_time][0] == '440': 
                        arr_TimeAxis_custom[num_time][0] = 'ИТОГО МЕСЯЦ ПО ГРУППЕ'
                        arr_TimeAxis_custom[num_time][3] = ''
                    elif arr_TimeAxis_custom[num_time][0] == '550': 
                        arr_TimeAxis_custom[num_time][0] = 'ИТОГО ГОД'
                        arr_TimeAxis_custom[num_time][3] = ''
                    elif arr_TimeAxis_custom[num_time][0] == '770': 
                        arr_TimeAxis_custom[num_time][0] = 'ИТОГО ГОД ПО ГРУППЕ'
                        arr_TimeAxis_custom[num_time][3] = ''
                    elif arr_TimeAxis_custom[num_time][0] == '880': 
                        arr_TimeAxis_custom[num_time][0] = 'ИТОГО ПО ГРУППЕ ЗА ПЕРИОД'
                        arr_TimeAxis_custom[num_time][3] = ''    
                    else:
                        arr_TimeAxis_custom[num_time][0] = mg.appendZero(arr_TimeAxis_custom[num_time][2])+'/'+mg.appendZero(arr_TimeAxis_custom[num_time][1])+'/'+arr_TimeAxis_custom[num_time][0]
                        arr_TimeAxis_custom[num_time][3] = mg.appendZero(arr_TimeAxis_custom[num_time][3])+':'+mg.appendZero(arr_TimeAxis_custom[num_time][4])
                arr_TimeAxis_custom = np.delete(arr_TimeAxis_custom, [1,2,4] , axis = 1)  # удалим ненужные столбцы с месяцем, днем и минумами
                #
                arr_Table = np.hstack((arr_TimeAxis_custom, arr_data_custom))
                #
                # дополним списко заголовки шапки таблицы на экране названиями выбранных счетчиков
                self.model.lst_header_table = mg.create_header_table(cfg.lst_checked_counter_in_group + cfg.lst_checked_single_counter)
                #
                self.data = arr_Table
                self.model.set(self.data.copy())
                self.tableProfilePowerCounts.resizeColumnsToContents()

                # сделаем вторую таблицу, которая будет прсто шапкой над первой
                self.model2.lst_header_table = mg.create_header_table2(cfg.lst_checked_counter_in_group + cfg.lst_checked_single_counter)
                self.data2 = arr_Table
                self.model2.set(self.data2.copy())
                self.tableProfilePowerCounts2.resizeColumnsToContents()
                for num_time, val in enumerate(arr_Table):
                    self.tableProfilePowerCounts2.hideRow(num_time)

                #
                for num_colunm in range (0,np.shape(arr_Table)[1],1):
                    if self.tableProfilePowerCounts.columnWidth(num_colunm) >= self.tableProfilePowerCounts2.columnWidth(num_colunm):
                        self.tableProfilePowerCounts2.setColumnWidth(num_colunm, self.tableProfilePowerCounts.columnWidth(num_colunm))
                    else:
                        self.tableProfilePowerCounts.setColumnWidth(num_colunm, self.tableProfilePowerCounts2.columnWidth(num_colunm))
                # QTableView.columnWidth(column)¶
                # setColumnWidth(column, width)¶

                #
                cfg.running_thread1 = True
                self.emit_value(0)
                self.emit_string_statusBar("Готово.")

                # сделаем объединения ячеек для строк содержащих ИТОГО
                font = QFont()
                font.setBold(True)
                for num_time, val in enumerate(arr_Table):
                    if ('ИТОГО' in arr_Table[num_time][0]) and ('ГРУПП' in arr_Table[num_time][0]):
                        self.tableProfilePowerCounts.setSpan(num_time, 0, 1, 2)
                        for num_group, itemGroup in enumerate(cfg.lst_checked_group):
                            list_counter_in_group, rezult_get = msql.get_list_counter_in_group_DBGC(itemGroup)
                            from_mesto = mesto[num_group]+2
                            span_row = len(list_counter_in_group)
                            self.tableProfilePowerCounts.setSpan(num_time, from_mesto, 1, span_row)


            else:
                button = QMessageBox.critical(self,
                    "Ошибка выбора дат и времени",
                    "Начальная дата/время превышает конечную дату/время",
                        buttons=QMessageBox.StandardButton.Ok ,
                        defaultButton=QMessageBox.StandardButton.Ok,)
            return None

        def load(self,data=np.array([[]])):
            self.data = data
            self.model.set(data.copy())

# -----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------
        def click_bth_ImportInExcel(self):
            """
                нажатие на кнопку Экспорт в Иксель
            """
            try:
                fileName, ok = QFileDialog.getSaveFileName(self,"Сохранить файл",".","All Files(*.xlsx)")
                if not fileName:   return 
                _list = []
                model = self.tableProfilePowerCounts.model()

                # дополним списк заголовки шапки таблицы
                lst_header_table = mg.create_header_table(cfg.lst_checked_counter_in_group + cfg.lst_checked_single_counter)
                _list.append(lst_header_table)

                for row in range(model.rowCount()):
                    _r = []
                    for column in range(model.columnCount()):
                        _r.append("{}".format(model.index(row, column).data() or ""))
                    _list.append(_r)

                bold_row = []
                for r, row in enumerate(_list):
                    # for c, col in enumerate(row):
                    if 'ИТОГО' in row[0]:
                        bold_row.append(r)

                workbook = Workbook(fileName)
                worksheet = workbook.add_worksheet() 

                for r, row in enumerate(_list):
                    for c, col in enumerate(row):
                        worksheet.write(r, c, col)  

                cell_format = workbook.add_format()
                cell_format.set_bold()
                cell_format.set_font_color('green')
                cell_format.set_border(1)
                worksheet.set_column(0, 0, 20, cell_format) # Установка стиля для столбца A и ширины 20  

                cell_format = workbook.add_format()
                cell_format.set_bold()
                cell_format.set_bg_color('silver')
                cell_format.set_bottom(1)
                cell_format.set_align('center')
                cell_format.set_align('vcenter')
                worksheet.set_row(0, 18, cell_format) # Установка стиля для строки 2 и высоты 11
                for r in bold_row:
                    worksheet.set_row(r, 18, cell_format)
                workbook.close()  
                msg = QMessageBox.information(
                    self, 
                    "Success!", 
                    f"Данные сохранены в файле: \n{fileName}"
                    ) 
            except:
                ml.logger.error("Ошибка обработки записи в Excel", exc_info=True)
                msg = QMessageBox.information(
                    self, 
                    "Ошибка!", 
                    "Ошибка обработки записи в Excel"
                    )
                


    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------    
        def renderTreePanel_for_ProfilPower(self):
            
            list_counterDB, rezult_getListOfCounterDB = msql.getListCounterDB()
            list_GroupDB, rezult_getListOfGroupDB = msql.getListGroupDB()
            self.tree.clear()
            for item_Group in list_GroupDB:
                parent = QTreeWidgetItem(self.tree)
                parent.setText(0, item_Group['name_group_full'])
                list_DictGroupWithCounterDB, rezult_getListOfGroupDB = msql.getListCounterInGroupDB(self,item_Group['name_group_full'])
                parent.setFlags(parent.flags() | Qt.ItemIsUserCheckable)
                parent.setCheckState(0, Qt.Unchecked)
                for itemChek in cfg.lst_checked_group:
                    if itemChek == item_Group['id']:
                        parent.setCheckState(0, Qt.Checked)
                        break
                for item in list_DictGroupWithCounterDB:
                    child = QTreeWidgetItem(parent)
                    child.setText(0, item['name_counter_full'])
            parent = QTreeWidgetItem(self.tree)
            parent.setText(0, "Все счетчики")
            for item_Counter in list_counterDB:
                    child = QTreeWidgetItem(parent)
                    child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                    child.setCheckState(0, Qt.Unchecked)
                    child.setText(0, item_Counter['name_counter_full'])
                    # for itemChek in (cfg.lst_checked_counter_in_group + cfg.lst_checked_single_counter):
                    for itemChek in (cfg.lst_checked_single_counter):    
                        if itemChek == item_Counter['id']:
                            child.setCheckState(0, Qt.Checked)
                            break
            self.tree.expandAll()
            return None


class NpModel(QAbstractTableModel):
    def __init__(self, data = np.array([[]])):
        super().__init__()
        self.npdata = data
        self.lst_header_table = []
        
    def rowCount(self,index=QModelIndex()):
        return len(self.npdata)
        
    def columnCount(self,index=QModelIndex()):
        return len(self.npdata[0])
    
    def data(self,index,role):
        if not index.isValid():# or role != Qt.DisplayRole: 
            return None
        if role == Qt.DisplayRole:
            # елси это обычное число из таблицы - поменяем разделитель с . на , (для соблюдения нац стандартов)
            # и заменим nan на отсутствие
            if (index.column() != 0 or index.column() != 1):
                val = self.npdata[index.row()][index.column()]
                val = val.replace('.', ',')
                if val == 'nan': val = ''
                return str(val)
            else:
                val = self.npdata[index.row()][index.column()]
                return str(val)
        if role == Qt.FontRole: 
            if (index.column() == 0 or index.column() == 1):
                font = QFont() 
                font.setBold(True)
                return font
            if 'ИТОГО' in self.npdata[index.row()][0]:
                font = QFont() 
                font.setBold(True)
                # font.setColor(QPen('blue'))
                return font
        if role == Qt.TextAlignmentRole:
            if ('ИТОГО' in self.npdata[index.row()][0]) and ('ГРУПП' in self.npdata[index.row()][0]):
                # font = QFont() 
                # font.setBold(True)
                return Qt.AlignCenter #QVariant(int(Qt.AlignHCenter|Qt.AlignVCenter))
    


    
    def headerData(self,section,orientation,role):
        # if role != Qt.DisplayRole: 
        #     return None
        if role == Qt.DisplayRole:
            if orientation == Qt.Vertical:
                ret = 'Строка ' + str(section)
                return ret
            if orientation == Qt.Horizontal:
                # ret = 'Столбец ' + str(section)
                ret = self.lst_header_table[section]
                return ret
        if role == Qt.FontRole:
            font = QFont()
            font.setBold(True)
            # font.setPointSize(10)
            return font
 
    def set(self,arr=np.array([[]])):
        self.beginResetModel()
        self.npdata = arr
        self.endResetModel()
        self.layoutChanged.emit()
    
    def get(self):
        return self.npdata



class NpModel2(QAbstractTableModel):
    def __init__(self, data = np.array([[]])):
        super().__init__()
        self.npdata = data
        self.lst_header_table = []
        
    def rowCount(self,index=QModelIndex()):
        return len(self.npdata)
        
    def columnCount(self,index=QModelIndex()):
        return len(self.npdata[0])
    
    # def data(self,index,role):
    #     return None
   
    def headerData(self,section,orientation,role):
        # if role != Qt.DisplayRole: 
        #     return None
        if role == Qt.DisplayRole:
            if orientation == Qt.Vertical:
                ret = 'Строка ' + str(section)
                return ret
            if orientation == Qt.Horizontal:
                # ret = 'Столбец ' + str(section)
                ret = self.lst_header_table[section]
                return ret
        if role == Qt.FontRole:
            font = QFont()
            font.setBold(True)
            # font.setPointSize(10)
            return font
 
    def set(self,arr=np.array([[]])):
        self.beginResetModel()
        self.npdata = arr
        self.endResetModel()
        self.layoutChanged.emit()
    
    def get(self):
        return self.npdata