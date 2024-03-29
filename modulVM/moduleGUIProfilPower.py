# moduleConfigApp
# autor: MolokovAlex
# coding: utf-8

# модуль окна Профиля мощности

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
# from PyQt5.QtCore import QDateTime
from PyQt5.QtGui import *
# from time import time
import numpy as np
import datetime # обязательно до import sqlite3 as sql3  !!!!!
from datetime import date, timedelta
# from statistics import mean
# import sqlite3 as sql3
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
        # def __init2__(self, data=np.array([[]]), parent=None):
        #     # super().__init__()
        #     super(TableProfilePowerDialog, self).__init__(parent)
        #     self.setWindowFlags(self.windowFlags()
        #         | Qt.WindowMinimizeButtonHint
        #         | Qt.WindowMaximizeButtonHint
        #         )
        #     self.setMinimumSize(QSize(800, 400))         # Устанавливаем размеры
        #     self.setWindowTitle("Таблица профиля мощности") # Устанавливаем заголовок окна

        #     layout = QGridLayout()
        #     layout.setSpacing(1)
            
        #     # флаг разрешения нажатия на кнопки Обновить и Импорт в Иксель - пока не выбраны счетчики и группы он опущен
        #     self.flag_caseCountersAndGroups = False
        #     # значение Combox периода интегрирования в окне профиля мощности
        #     self.period_integr = ""
            
        #     self.lst_checkItemTree=[]

        #     btn_caseCountsAndGroups = QPushButton("Выбор счетчиков и групп")
        #     layout.addWidget(btn_caseCountsAndGroups, 0, 0)
        #     btn_caseCountsAndGroups.clicked.connect(self.click_btn_caseCountsAndGroups)
            
        #     self.de_dateFrom = QDateEdit(self)
        #     layout.addWidget(self.de_dateFrom, 0, 2)
        #     self.de_dateFrom.setCalendarPopup(True) 

        #     # от первого дня месяца
        #     ddate_from = QDate(QDate.currentDate().year(), QDate.currentDate().month(), 1)
        #     # до текущей даты
        #     ddate_to = QDate.currentDate()

        #     lbl_empty2 = QLabel("<-интервал->")
        #     layout.addWidget(lbl_empty2, 0, 3)
        #     lbl_empty2.setAlignment(Qt.AlignCenter)

        #     self.de_dateTo = QDateEdit(self)
        #     layout.addWidget(self.de_dateTo, 0, 4)
        #     self.de_dateTo.setCalendarPopup(True)
        #     # self.de_dateTo.setDate(QDate(2022, 12, 25))
        #     # d = ddatefrom.addDays(2)
        #     # print(d)
        #     self.de_dateFrom.setDate(ddate_from)
        #     self.de_dateTo.setDate(ddate_to)

        #     lbl_empty4 = QLabel("Период отображения")
        #     layout.addWidget(lbl_empty4, 0, 6)
        #     lbl_empty4.setAlignment(Qt.AlignRight)
        #     self.cb_interval = QComboBox()
        #     layout.addWidget(self.cb_interval, 0, 7)
        #     self.cb_interval.addItems(cfg.VALUE_PERIOD_INTEGR_POFIL)
        #     self.cb_interval.currentIndexChanged.connect( self.change_cb_interval )
        #     self.period_integr = self.cb_interval.currentText()

        #     self.cbox = QCheckBox("применить kU и kI")
        #     self.cbox.setChecked(False)
        #     self.cbox.toggled.connect(self.onClicked_cbox) 
        #     layout.addWidget(self.cbox, 0, 8)

        #     self.btnRefreshTableProfilePowerCounts = QPushButton("Обновить")
        #     layout.addWidget(self.btnRefreshTableProfilePowerCounts, 0, 9)
        #     self.btnRefreshTableProfilePowerCounts.clicked.connect(self.click_btnRefreshTableProfilePowerCounts_ver2)
        #     if not self.flag_caseCountersAndGroups:
        #         self.btnRefreshTableProfilePowerCounts.setEnabled(False)
        #     else:
        #         self.btnRefreshTableProfilePowerCounts.setEnabled(True) 

        #     # ckb_cycleRefresh = QCheckBox("циклически")
        #     # layout.addWidget(ckb_cycleRefresh, 1, 10)

        #     lbl_empty3 = QLabel("    ")
        #     layout.addWidget(lbl_empty3, 0, 11)

        #     self.btnImportTableProfilePowerCounts = QPushButton("Импорт в Excel")
        #     layout.addWidget(self.btnImportTableProfilePowerCounts, 0, 12)
        #     self.btnImportTableProfilePowerCounts.clicked.connect(self.click_bth_ImportInExcel)
        #     if not self.flag_caseCountersAndGroups:
        #         self.btnImportTableProfilePowerCounts.setEnabled(False)
        #     else:
        #         self.btnImportTableProfilePowerCounts.setEnabled(True)    
        
        #     #
        #     # self.model2 = NpModel2()
        #     # self.tableProfilePowerCounts2 = QTableView()
        #     # self.tableProfilePowerCounts2.setModel(self.model2)
        #     # self.tableProfilePowerCounts2.horizontalHeader().setSectionResizeMode(0)
        #     # # self.tableProfilePowerCounts.horizontalHeader().setSectionResizeMode(1)#,QHeaderView.ResizeToContents)
        #     # # self.tableProfilePowerCounts.horizontalHeader().hide()
        #     # self.tableProfilePowerCounts2.verticalHeader().hide()
        #     # # self.tableProfilePowerCounts2.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        #     # layout.addWidget(self.tableProfilePowerCounts2, 1, 0, 1, 13, alignment=Qt.AlignmentFlag.AlignBottom)
            
        #     #


        #     self.model = NpModel()
        #     self.tableProfilePowerCounts = QTableView()
        #     self.tableProfilePowerCounts.setModel(self.model)
        #     self.tableProfilePowerCounts.horizontalHeader().setSectionResizeMode(0)
        #     # self.tableProfilePowerCounts.horizontalHeader().setSectionResizeMode(1)#,QHeaderView.ResizeToContents)
        #     # self.tableProfilePowerCounts.horizontalHeader().hide()
        #     self.tableProfilePowerCounts.verticalHeader().hide()
        #     self.tableProfilePowerCounts.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        #     # layout.addWidget(self.tableProfilePowerCounts,2,0, 10, 13)
        #     # layout.addWidget(self.tableProfilePowerCounts,2,0, 2, 13, alignment=Qt.AlignmentFlag.AlignTop)
        #     layout.addWidget(self.tableProfilePowerCounts,2,0, 2, 13, alignment=Qt.AlignmentFlag.AlignTop)

        #     # layout.setRowStretch(0, 0)
        #     # layout.setRowStretch(1, 0)
        #     # layout.setRowStretch(2, 0)
        #     self.setLayout(layout)

        #     # self.load()
        #     self.tableProfilePowerCounts.resizeColumnsToContents()

        #     return None
        
        def __init__(self, data=np.array([[]]), parent=None):
            # super().__init__()
            super(TableProfilePowerDialog, self).__init__(parent)
            self.setWindowFlags(self.windowFlags()
                | Qt.WindowMinimizeButtonHint
                | Qt.WindowMaximizeButtonHint
                )
            self.setMinimumSize(QSize(800, 400))         # Устанавливаем размеры
            self.setWindowTitle("Таблица профиля мощности") # Устанавливаем заголовок окна


            hbox = QHBoxLayout(self)
            self.leftFrame = QFrame(self)       
            self.leftFrame.setFrameShape(QFrame.StyledPanel)
            self.leftLayout = QGridLayout(self.leftFrame)
            self.treeCount = QTreeWidget()
            self.treeCount.itemClicked.connect(self.onItemClicked)
            self.renderTreePanel_for_ProfilPower2()
            # self.treeCount.clicked.connect(self.click_in_tree)
            self.leftLayout.addWidget(self.treeCount,0,0)
            
            
            self.rightFrame = QFrame(self)
            self.rightFrame.setFrameShape(QFrame.StyledPanel)
            self.rightLayout = QGridLayout(self.rightFrame)
            self.rightLayout.setSpacing(1)
            
            # флаг разрешения нажатия на кнопки Обновить и Импорт в Иксель - пока не выбраны счетчики и группы он опущен
            self.flag_caseCountersAndGroups = False
            # значение Combox периода интегрирования в окне профиля мощности
            self.period_integr = ""
            
            self.lst_checkItemTree=[]

            # btn_caseCountsAndGroups = QPushButton("Выбор счетчиков и групп")
            # self.rightLayout.addWidget(btn_caseCountsAndGroups, 0, 0)
            # btn_caseCountsAndGroups.clicked.connect(self.click_btn_caseCountsAndGroups)
            
            self.de_dateFrom = QDateEdit(self)
            self.rightLayout.addWidget(self.de_dateFrom, 0, 0)
            self.de_dateFrom.setCalendarPopup(True) 

            # от первого дня месяца
            ddate_from = QDate(QDate.currentDate().year(), QDate.currentDate().month(), 1)
            # до текущей даты
            ddate_to = QDate.currentDate()

            lbl_empty2 = QLabel("<-интервал->")
            self.rightLayout.addWidget(lbl_empty2, 0, 1)
            lbl_empty2.setAlignment(Qt.AlignCenter)

            self.de_dateTo = QDateEdit(self)
            self.rightLayout.addWidget(self.de_dateTo, 0, 2)
            self.de_dateTo.setCalendarPopup(True)
            # self.de_dateTo.setDate(QDate(2022, 12, 25))
            # d = ddatefrom.addDays(2)
            # print(d)
            self.de_dateFrom.setDate(ddate_from)
            self.de_dateTo.setDate(ddate_to)

            lbl_empty4 = QLabel("Период отображения")
            self.rightLayout.addWidget(lbl_empty4, 0, 4)
            lbl_empty4.setAlignment(Qt.AlignRight)
            self.cb_interval = QComboBox()
            self.rightLayout.addWidget(self.cb_interval, 0, 5)
            self.cb_interval.addItems(cfg.VALUE_PERIOD_INTEGR_POFIL)
            self.cb_interval.currentIndexChanged.connect( self.change_cb_interval )
            self.period_integr = self.cb_interval.currentText()

            self.cbox = QCheckBox("применить kU и kI")
            self.cbox.setChecked(False)
            self.cbox.toggled.connect(self.onClicked_cbox) 
            self.rightLayout.addWidget(self.cbox, 0, 6)

            self.btnRefreshTableProfilePowerCounts = QPushButton("Обновить")
            self.rightLayout.addWidget(self.btnRefreshTableProfilePowerCounts, 0, 8)
            self.btnRefreshTableProfilePowerCounts.clicked.connect(self.click_btnRefreshTableProfilePowerCounts_ver2)
            if not self.flag_caseCountersAndGroups:
                self.btnRefreshTableProfilePowerCounts.setEnabled(False)
            else:
                self.btnRefreshTableProfilePowerCounts.setEnabled(True) 

            # ckb_cycleRefresh = QCheckBox("циклически")
            # layout.addWidget(ckb_cycleRefresh, 1, 10)

            lbl_empty3 = QLabel("    ")
            self.rightLayout.addWidget(lbl_empty3, 0, 11)

            self.btnImportTableProfilePowerCounts = QPushButton("Импорт в Excel")
            self.rightLayout.addWidget(self.btnImportTableProfilePowerCounts, 0, 12)
            self.btnImportTableProfilePowerCounts.clicked.connect(self.click_bth_ImportInExcel)
            if not self.flag_caseCountersAndGroups:
                self.btnImportTableProfilePowerCounts.setEnabled(False)
            else:
                self.btnImportTableProfilePowerCounts.setEnabled(True)    
        
            #
            # self.model2 = NpModel2()
            # self.tableProfilePowerCounts2 = QTableView()
            # self.tableProfilePowerCounts2.setModel(self.model2)
            # self.tableProfilePowerCounts2.horizontalHeader().setSectionResizeMode(0)
            # # self.tableProfilePowerCounts.horizontalHeader().setSectionResizeMode(1)#,QHeaderView.ResizeToContents)
            # # self.tableProfilePowerCounts.horizontalHeader().hide()
            # self.tableProfilePowerCounts2.verticalHeader().hide()
            # # self.tableProfilePowerCounts2.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
            # layout.addWidget(self.tableProfilePowerCounts2, 1, 0, 1, 13, alignment=Qt.AlignmentFlag.AlignBottom)
            
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
            # layout.addWidget(self.tableProfilePowerCounts,2,0, 2, 13, alignment=Qt.AlignmentFlag.AlignTop)
            self.rightLayout.addWidget(self.tableProfilePowerCounts,2,0, 2, 13, alignment=Qt.AlignmentFlag.AlignTop)

            # layout.setRowStretch(0, 0)
            # layout.setRowStretch(1, 0)
            # layout.setRowStretch(2, 0)

            # self.setLayout(layout)
            splitter = QSplitter(Qt.Horizontal)
            splitter.addWidget(self.leftFrame)
            splitter.addWidget(self.rightFrame)
            splitter.setStretchFactor(1, 1)
            splitter.setSizes([125, 150])
            hbox.addWidget(splitter)
            self.setLayout(hbox)

            # self.load()
            self.tableProfilePowerCounts.resizeColumnsToContents()

            return None
        
        def onClicked_cbox(self):
            cbutton = self.sender()
            if self.cbox.isChecked():
                cfg.check_KU_KI = True
            else:
                cfg.check_KU_KI = False
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

        # def click_btn_caseCountsAndGroups(self):
        #     """
        #         Обработка нажания кноепки Выбор счетчиков и групп
        #         Выводиться окно с Tree
            
        #     """
        #     self.flag_caseCountersAndGroups = False
        #     self.DialogCaseCounterAndGroups = QDialog()
        #     self.DialogCaseCounterAndGroups.setWindowTitle("Выбор счетчиков и групп")
        #     self.DialogCaseCounterAndGroups.setWindowModality(Qt.ApplicationModal)
        #     self.DialogCaseCounterAndGroups.resize(800, 800)
        
        #     layout = QGridLayout()
        #     self.DialogCaseCounterAndGroups.setLayout(layout)
        #     self.treeCount = QTreeWidget()
        #     # self.tree.setColumnCount(2)
        #     # self.tree.setHeaderLabels(['Наименование', 'Сетевой адрес'])
        #     self.treeCount.setColumnCount(1)
        #     self.treeCount.setHeaderLabels(['Наименование'])
        #     self.renderTreePanel_for_ProfilPower()
        #     # self.tree.clicked.connect(self.click_onClickedOnItemTree)
        #     # self.tree.selectionModel().selectionChanged.connect(self.onSelectionChanged)      # QItemSelectionModel
        #     # self.tree.itemChanged.connect(self.onChangeCheckBox)
        #     # self.tree.doubleClicked.connect(self.click_onClickedOnItemTree)
        #     self.treeCount.itemClicked.connect(self.onItemClicked)
        #     layout.addWidget(self.treeCount,0,0,2,2)
            
        #     btn_OKCase = QPushButton("OK")
        #     layout.addWidget(btn_OKCase, 2, 0)
        #     btn_OKCase.clicked.connect(self.click_btn_OKCase)
        #     btn_CancelCase = QPushButton("Cancel")
        #     layout.addWidget(btn_CancelCase, 2, 1)
        #     btn_CancelCase.clicked.connect(self.click_btn_CancelCase)

        #     self.DialogCaseCounterAndGroups.exec_()
        #     return None
        
        

        # def onChangeCheckBox(self, item):
        #     a=0
        #     run_inSelectionChange= cfg.run_inSelectionChange
        #     run_onChangeCheckBox = cfg.run_onChangeCheckBox
        #     if cfg.run_onChangeCheckBox == 1: return None
        #     if cfg.run_inSelectionChange == 1: return None
        #     cfg.run_onChangeCheckBox = 1
        #     run_onChangeCheckBox = cfg.run_onChangeCheckBox
        #     # item.setSelected(True)
        #     # self.onSelectionChanged(item)
        #     # item.setSelected(True)
        #     self.onItemClicked(item, 0)
        #     # self.onSelectionChanged(item)
        #     # cfg.run_inSelectionChange = 0
        #     run_inSelectionChange= cfg.run_inSelectionChange
        #     # item.setSelected(False)

        #     # if cfg.flag_callonChangeCheckBox == 0:
        #     #     self.onSelectionChanged(item)
                
        #     # cfg.flag_callonChangeCheckBox = 0
        #     # flag_callonChangeCheckBox= cfg.flag_callonChangeCheckBox
        #     cfg.run_onChangeCheckBox = 0
        #     run_onChangeCheckBox = cfg.run_onChangeCheckBox
        #     return None
        
        def onItemClicked(self, it, col):
            a=0
            if cfg.run_onChangeCheckBox == 1: return None
            if cfg.run_inSelectionChange == 1: return None
            # print(it, col, it.text(col))
            it.setSelected(True)
            self.onSelectionChanged()
            return None

        def onSelectionChanged(self):#, item):
            """ Обработка клики мышкой в дереве на группе или одиночном счетчике
            """
            run_inSelectionChange= cfg.run_inSelectionChange
            run_onChangeCheckBox = cfg.run_onChangeCheckBox
            # if cfg.run_onChangeCheckBox == 1: return None
            if cfg.run_inSelectionChange == 1: return None
            rezult_get_id_group = False
            cfg.run_inSelectionChange = 1
            run_inSelectionChange = cfg.run_inSelectionChange
            id_group = 0
            list_id_counter_in_group = []
            rezult_get_id_counter_in_group = False
            id_counter = 0 
            rezult_get_id_counter = False
            
            lst_id_checked_group = cfg.lst_id_checked_group.copy()
            lst_id_checked_single_counter = cfg.lst_id_checked_single_counter.copy()
            lst_id_checked_counter_in_group = cfg.lst_id_checked_counter_in_group.copy()
            for sel in self.treeCount.selectedIndexes():
                selected_idgetItem = self.treeCount.itemFromIndex(sel)
                val = sel.data()
                try:
                # если название предположительно - название группы - по названию получим  id группы
                    id_group, rezult_get_id_group =  msql.get_id_group_DBG(sel.data())
                    #  если это группа - найдем какие счетчики есть в этой группу и начнем заполнять список счетчиками группы
                    if rezult_get_id_group:
                        list_id_counter_in_group, rezult_get_id_counter_in_group = msql.get_list_counter_in_group_DBGC(id_group)
                except:
                    a=0

                
                try:
                    # если название предположительно - название одиноч счетчика - по названию получим  id счтечика
                    id_counter, rezult_get_id_counter =  msql.get_id_counter_DBC(sel.data())
                except:
                    a=0
                

                # если нет родителя (это название группы) и это не "Все счетчики"
                if not(sel.parent().isValid()) and sel.data() != "Все счетчики":
                    # если галочка в checkbox-е установлена (checkState(0) = 2)
                    if cfg.run_onChangeCheckBox == 0:
                        if selected_idgetItem.checkState(0) == Qt.Checked:
                        # print (widgetItem.checkState(0))
                        # if widgetItem.isChecked():
                            # получаем id группы и проверяем есть ли этот id в списке lst_id_checked_group
                            # id_group, rezult =  msql.get_id_group_DBG(sel.data())
                            if rezult_get_id_group and (id_group in lst_id_checked_group): 
                                # if id_group in lst_id_checked_group:
                                    # если есть в списке - удаляем из списка
                                    lst_id_checked_group.remove(id_group)
                                    # заполним/уберем  id  из списка lst_id_checked_counter_in_group
                                    if rezult_get_id_counter_in_group:
                                        for item_list in list_id_counter_in_group:
                                            lst_id_checked_counter_in_group.remove(item_list)
                        # если галочка в checkbox-е НЕустановлена
                        else:
                            # id_group, rezult =  msql.get_id_group_DBG(sel.data())
                            if rezult_get_id_group and not(id_group in lst_id_checked_group): 
                                # if not(id_group in lst_id_checked_group):
                                    lst_id_checked_group.append(id_group)
                                    # заполним/уберем  id  из списка lst_id_checked_counter_in_group
                                    if rezult_get_id_counter_in_group:
                                        for item_list in list_id_counter_in_group:
                                            lst_id_checked_counter_in_group.append(item_list)
                    if cfg.run_onChangeCheckBox == 1:
                        if selected_idgetItem.checkState(0) == Qt.Checked:
                            if rezult_get_id_group and not(id_group in lst_id_checked_group): 
                                    lst_id_checked_group.append(id_group)
                                    # заполним/уберем  id  из списка lst_id_checked_counter_in_group
                                    if rezult_get_id_counter_in_group:
                                        for item_list in list_id_counter_in_group:
                                            lst_id_checked_counter_in_group.append(item_list)
                        # если галочка в checkbox-е НЕустановлена
                        else:
                            if rezult_get_id_group and (id_group in lst_id_checked_group): 
                                    # если есть в списке - удаляем из списка
                                    lst_id_checked_group.remove(id_group)
                                    # заполним/уберем  id  из списка lst_id_checked_counter_in_group
                                    if rezult_get_id_counter_in_group:
                                        for item_list in list_id_counter_in_group:
                                            lst_id_checked_counter_in_group.remove(item_list)
                            

                # если есть родитель и он называется "Все счетчики" - это название одиночного счетчика
                # - снимаем или ставим галочку на названии счетчика
                # если этот одинокий счетчик есть в cfg.lst_checked_single_counter - удаляем его из списка
                # и наоборот
                if sel.parent().isValid() and sel.parent().data()=="Все счетчики":
                    
                    if cfg.run_onChangeCheckBox == 0:
                        if selected_idgetItem.checkState(0) == Qt.Checked:
                            if rezult_get_id_counter and (id_counter in lst_id_checked_single_counter):
                                lst_id_checked_single_counter.remove(id_counter)
                        else:
                            if rezult_get_id_counter and not(id_counter in lst_id_checked_single_counter):
                                lst_id_checked_single_counter.append(id_counter)
                    if cfg.run_onChangeCheckBox == 1:
                        if selected_idgetItem.checkState(0) == Qt.Checked:
                            if rezult_get_id_counter and not(id_counter in lst_id_checked_single_counter):
                                lst_id_checked_single_counter.append(id_counter)
                        else:
                            if rezult_get_id_counter and (id_counter in lst_id_checked_single_counter):
                                lst_id_checked_single_counter.remove(id_counter)

                
                # если галочка в checkbox-е установлена (checkState(0) = 2) - снимаем или ставим галочку на названии группы/счетчика
                if cfg.run_onChangeCheckBox == 0:
                    if selected_idgetItem.checkState(0) == 2:
                        # cfg.run_inSelectionChange = 1
                        # b= cfg.run_inSelectionChange
                        selected_idgetItem.setCheckState(0, Qt.Unchecked)
                        # selected_idgetItem.setForeground(0, Qt.darkBlue)
                    else:
                        # cfg.run_inSelectionChange = 1
                        # b= cfg.run_inSelectionChange
                        selected_idgetItem.setCheckState(0, Qt.Checked)
                        # selected_idgetItem.setForeground(0, Qt.red)
                    # selected_idgetItem.setSelected(False)
                if cfg.run_onChangeCheckBox == 1:
                    if selected_idgetItem.checkState(0) == 2:
                        selected_idgetItem.setCheckState(0, Qt.Checked)
                    else:
                        selected_idgetItem.setCheckState(0, Qt.Unchecked)
                selected_idgetItem.setSelected(False)
            # self.tree.clearSelection()  # QItemSelectionModel

            cfg.lst_id_checked_group = lst_id_checked_group.copy()
            cfg.lst_id_checked_single_counter = lst_id_checked_single_counter.copy()
            cfg.lst_id_checked_counter_in_group = lst_id_checked_counter_in_group.copy()
                # cfg.run_inSelectionChange = 0
                # b= cfg.run_inSelectionChange
            cfg.run_inSelectionChange = 0
            run_inSelectionChange = cfg.run_inSelectionChange
                # selected_idgetItem.setSelected(False)
            if cfg.lst_id_checked_group or cfg.lst_id_checked_single_counter:
                self.flag_caseCountersAndGroups = True
                self.btnRefreshTableProfilePowerCounts.setEnabled(True)
                self.btnImportTableProfilePowerCounts.setEnabled(True) 
            else:
                # если пользователь снял все галочки
                self.flag_caseCountersAndGroups = False
                self.btnRefreshTableProfilePowerCounts.setEnabled(False)
                self.btnImportTableProfilePowerCounts.setEnabled(False)
            return None
        
        # def click_onClickedOnItemTree(self , sel:QModelIndex):
        #     a=0
        #     # parentItem = self.tree.item(sel.parent().row(), sel.parent.column())
        #     # item = parentItem.child(sel.row(), sel.column)
        #     # print(item.data())
        #     b = self.tree.selectedItems()
        #     return None
        
        
        # def click_btn_OKCase(self):
        #     """
        #     обработка нажатия клавиши ОК в окне выбора счетчиков и групп
        #     """
        #     # составим список элементов, где пользователь поставиль галочки в дереве
        #     # self.lst_checkItemTree=[]
        #     # iterator = QTreeWidgetItemIterator(self.tree, QTreeWidgetItemIterator.Checked)
        #     # while iterator.value():
        #     #     item = iterator.value()
        #     #     print (item.text(0))
        #     #     self.lst_checkItemTree.append(item.text(0))
        #     #     iterator += 1
        #     # если какой то выбор сделан - разблокированить кнопки Обновить и Экспорт в Иксель
        #     # if self.lst_checkItemTree:
        #     if cfg.lst_id_checked_group or cfg.lst_id_checked_single_counter:
        #         self.flag_caseCountersAndGroups = True
        #         self.btnRefreshTableProfilePowerCounts.setEnabled(True)
        #         self.btnImportTableProfilePowerCounts.setEnabled(True) 
        #     else:
        #         # если пользователь снял все галочки
        #         self.flag_caseCountersAndGroups = False
        #         self.btnRefreshTableProfilePowerCounts.setEnabled(False)
        #         self.btnImportTableProfilePowerCounts.setEnabled(False)
        #     # создаем список выбранных пользователем групп и список выбранных счетчиков - все по отдельности
        #     # cfg.lst_checked_counter_in_group, cfg.lst_checked_group, cfg.lst_checked_single_counter = mg.createLstCheckedCounterAndGroups(self.lst_checkItemTree)
        #     # cfg.lst_id_checked_counter_in_group, cfg.lst_id_checked_group, cfg.lst_id_checked_single_counter = mg.create_id_LstCheckedCounterAndGroups()
        #     # закроем диалоговое окно
        #     self.DialogCaseCounterAndGroups.hide() 
        #     # lst_id_checked_group = cfg.lst_id_checked_group.copy()
        #     # lst_id_checked_single_counter = cfg.lst_id_checked_single_counter.copy()
        #     # lst_id_checked_counter_in_group = cfg.lst_id_checked_counter_in_group.copy() 
        #     cfg.run_inSelectionChange = 0  
        #     return
        
        # def click_btn_CancelCase(self):
        #     """
        #     обработка нажатия клавиши Cancel в окне выбора счетчиков и групп
        #     """
        #     # закроем диалоговое окно
        #     self.DialogCaseCounterAndGroups.hide()
        #     return
        
        
        # def click_btnRefreshTableProfilePowerCounts_ver3(self):
        #     """
        #         нажатие на кнопку Обновить
        #     """
        #     # t0 = time()
        #     self.emit_string_statusBar("Пожалуйста, подождите. Идут запросы в БД...")
        #     self.emit_value(5)
        #     self.model.set()
        #     # подготавливаем даты От и До
        #     # как для выбранного пользователем диапазона,
        #     # так и полного диапазона - там где ОТ: от первого числа месяца, - там где ДО: до последнего числа месяца (для вычисления суммы "ВСЕГО")
        #     # dateFrom_full, dateTo_full, dateFrom, dateTo = mg.create_full_datetime_FromTo(self.de_dateFrom, self.de_dateTo)
        #     dateFrom_custom, dateTo_custom = mg.create_datetimeFromTo_custom(self.de_dateFrom, self.de_dateTo)
        #     dateFrom_full, dateTo_full = mg.create_full_datetimeFromTo(dateFrom_custom, dateTo_custom)
        #     # создаем массив временной оси (массив с датами времени) для таблицы профиля мощности
        #     # arr_TimeAxis_full, dateFrom_full, dateTo_full, dateFrom, dateTo, rezult = self.create_Array_TimeAxis()
        #     arr_TimeAxis_full, rezult = mg.create_Array_TimeAxis(dateFrom_full, dateTo_full)
        #     #
        #     self.emit_value(20)
        #     arr_data = np.full(shape=(np.shape(arr_TimeAxis_full)[0], len(cfg.lst_id_checked_counter_in_group + cfg.lst_id_checked_single_counter)),fill_value=0)
        #     if True:
        #         self.emit_value(25)
        #         #
        #         for num_arrTimeAxis, val_arrTimeAxis in enumerate(arr_TimeAxis_full):
        #             for num_counter, item_counter in enumerate(cfg.lst_id_checked_counter_in_group + cfg.lst_id_checked_single_counter):
        #                 dt_arrTimeAxis = datetime.datetime(val_arrTimeAxis[0], val_arrTimeAxis[1], val_arrTimeAxis[2], val_arrTimeAxis[3], val_arrTimeAxis[4])
        #                 rezult, dict_one_data, lst_data = msql.select_one_PandQ_from_DBPP(item_counter=item_counter, dateTime=dt_arrTimeAxis)
        #                 # если по конктреному datetime получили числа - заносим их в таблицу
        #                 # если записи в БД нет - заносим нули
        #                 if rezult:
        #                     a=0
        #                 else:
        #                     lst_data = [0,0,0,0,0]
        #                 arr_dataDB = np.array(lst_data)
        #                 arr_dataDB = np.delete(arr_dataDB, [0] , axis = 0)
        #                 arr_dataDB = np.array(arr_dataDB, dtype=float)
        #                 # вычисление полной мощьности
        #                 arr_dataDB[0] = arr_dataDB[0]-arr_dataDB[1]
        #                 # удалим лишние столбцы
        #                 arr_dataDB = np.delete(arr_dataDB, [1,2,3] , axis = 0)
        #                 arr_data[num_arrTimeAxis][num_counter] = arr_dataDB[0]
        #             arr_data_custom = np.array(arr_data, dtype=str)
        #             # arr_data_custom = np.array(arr_data_custom, dtype=str)
        #             # arr_Table = np.hstack((arr_TimeAxis_custom, arr_data_custom))
        #             self.data = arr_data_custom
        #             self.model.set(self.data.copy())
        #             self.tableProfilePowerCounts.resizeColumnsToContents()
                        
        #     return None



        def click_btnRefreshTableProfilePowerCounts_ver2(self):
            """
                нажатие на кнопку Обновить
            """
            # t0 = time()
            self.emit_string_statusBar("Пожалуйста, подождите. Идут запросы в БД...")
            self.emit_value(5)
            self.model.set()
            # подготавливаем даты От и До
            # как для выбранного пользователем диапазона,
            # так и полного диапазона - там где ОТ: от первого числа месяца, - там где ДО: до последнего числа месяца (для вычисления суммы "ВСЕГО")
            # dateFrom_full, dateTo_full, dateFrom, dateTo = mg.create_full_datetime_FromTo(self.de_dateFrom, self.de_dateTo)
            dateFrom_custom, dateTo_custom = mg.create_datetimeFromTo_custom(self.de_dateFrom, self.de_dateTo)
            dateFrom_full, dateTo_full = mg.create_full_datetimeFromTo(dateFrom_custom, dateTo_custom)
            # создаем массив временной оси (массив с датами времени) для таблицы профиля мощности
            # arr_TimeAxis_full, dateFrom_full, dateTo_full, dateFrom, dateTo, rezult = self.create_Array_TimeAxis()
            arr_TimeAxis_full, rezult = mg.create_Array_TimeAxis(dateFrom_full, dateTo_full)
            #
            self.emit_value(20)
            arr_data = np.full(shape=(np.shape(arr_TimeAxis_full)[0], len(cfg.lst_id_checked_counter_in_group + cfg.lst_id_checked_single_counter)),fill_value=0)
            if True:
                self.emit_value(25)
                #
                for num_counter, item_counter in enumerate(cfg.lst_id_checked_counter_in_group + cfg.lst_id_checked_single_counter):
                    rezult, lst_data = msql.selectPandQfromDBPP(item_counter=item_counter, dateFrom=dateFrom_full, dateTo=dateTo_full)
                    if rezult:
                        arr_dataDB = np.array(lst_data)
                        # корректировка данных профиля мощности  полученных из БД - добавление пустых пропущенных/напринятых профилей 30-минуток
                        # arr_dataDB = mg.korrekt_dataDB(arr_dataDB, dateFrom_full, dateTo_full)
                        #
                        # вычисление полной мощьности
                        arr_dataDB = mg.calc_full_power(arr_dataDB)
                        #
                        # выделение временной оси в отдельный массив
                        # arr_TimeAxis_full = arr_dataDB[:,0:5]
                        #
                        # выделим только данные
                        # if num_counter == 0: 
                        #     arr_data = arr_dataDB[:,5:]
                        # else:
                        #     arr_data = np.hstack((arr_data, arr_dataDB[:,5:]))
                        # защита от пустых строк в БД, коорые можно затащить в datetime header
                        num_rowDB = 0
                        for num_arrTimeAxis, val_arrTimeAxis in enumerate(arr_TimeAxis_full):
                            dt_arrTimeAxis = datetime.datetime(val_arrTimeAxis[0], val_arrTimeAxis[1], val_arrTimeAxis[2], val_arrTimeAxis[3], val_arrTimeAxis[4])
                            dt_arr_dataDB = datetime.datetime(arr_dataDB[num_rowDB][0], arr_dataDB[num_rowDB][1], arr_dataDB[num_rowDB][2], arr_dataDB[num_rowDB][3], arr_dataDB[num_rowDB][4])

                            if dt_arrTimeAxis < dt_arr_dataDB:
                                # сюда приходим при пропуске в данных БД записи с каким-то временем
                                pass
                            if dt_arrTimeAxis > dt_arr_dataDB:
                                # сюда приходим при появлении дубликата записи из БД
                                # перебираем записи с одинаковыми дата-штампами пока они не закончаться
                                # запоминаем время дубликата
                                dt_arr_dataDB_prev = dt_arr_dataDB
                                while dt_arr_dataDB_prev == dt_arr_dataDB:
                                    # dt_arr_dataDB_prev = dt_arr_dataDB
                                    num_rowDB +=1
                                    if num_rowDB >= np.shape(arr_dataDB)[0]: break
                                    dt_arr_dataDB = datetime.datetime(arr_dataDB[num_rowDB][0], arr_dataDB[num_rowDB][1], arr_dataDB[num_rowDB][2], arr_dataDB[num_rowDB][3], arr_dataDB[num_rowDB][4])
                                if num_rowDB >= np.shape(arr_dataDB)[0]: break    
                            # если даты и времена совпадают с датой и временем заголовка
                            if dt_arrTimeAxis == dt_arr_dataDB:
                                arr_data[num_arrTimeAxis][num_counter] = arr_dataDB[num_rowDB][5]
                                num_rowDB +=1
                                if num_rowDB >= np.shape(arr_dataDB)[0]: break

                self.emit_value(30)
                # теперь в массиве будут храниться числа с плавающей точкой
                arr_data = np.array(arr_data, dtype=float)
                # переведем абстрактные числа из БД в реальные используя коэфф счетчика A
                arr_data = mg.kWT(arr_data, arr_TimeAxis_full, cfg.lst_id_checked_counter_in_group + cfg.lst_id_checked_single_counter)
                #
                self.emit_value(35)
                # обрежем массив в соответвии с датами, которые выбрал пользователь
                arr_data_custom, arr_TimeAxis_custom = mg.cut_arr_custom_time(arr_data, arr_TimeAxis_full, dateFrom_custom, dateTo_custom)
                #
                self.emit_value(40)
                # приведение к виду периода отображения
                arr_data_custom, arr_TimeAxis_custom = mg.createView_periodView(arr_data_custom, arr_TimeAxis_custom, self.period_integr)
                # найдем сумму для ВСЕГО 
                arr_summ_Alltime, arr_summ_Alltime_Group =mg.summ_per_day_and_month_and_year_v2(arr_data_custom, arr_TimeAxis_custom, cfg.lst_id_checked_group, cfg.lst_id_checked_counter_in_group, cfg.lst_id_checked_single_counter)
                #
                # найдем сумму для ИТОГО 
                arr_summ_Alltime_custom, arr_summ_Alltime_Group_custom =mg.summ_per_day_and_month_and_year_v2(arr_data_custom, arr_TimeAxis_custom, cfg.lst_id_checked_group, cfg.lst_id_checked_counter_in_group, cfg.lst_id_checked_single_counter)
                #
                #  Сделаем ИТОГО за период по группе
                summGroupPeriod = np.full(shape=(len(cfg.lst_id_checked_group)),fill_value=0.0, dtype=float)
                self.emit_value(50)
                # # приведение к виду периода отображения
                # arr_data_custom, arr_TimeAxis_custom = mg.createView_periodView(arr_data_custom, arr_TimeAxis_custom, self.period_integr)
                #
                # вставка строк/столбцов суммы как итого
                arr_data_custom, arr_TimeAxis_custom, mesto = mg.insert_summ_v2(arr_data_custom, arr_TimeAxis_custom, self.period_integr, arr_summ_Alltime, arr_summ_Alltime_Group, arr_summ_Alltime_custom, arr_summ_Alltime_Group_custom, summGroupPeriod)
                # округлим все  float в массиве до трех знаков после запятой
                arr_data_custom = np.around(arr_data_custom, 4)
                #
                self.emit_value(60)
                # перобразовать массив из  int в str чтобы добавлять текст "итого"
                # преобразуем и дату и загоовок, а потом склеим
                arr_data_custom = np.array(arr_data_custom, dtype=str)
                #
                arr_TimeAxis_custom = np.array(arr_TimeAxis_custom, dtype='<U45')
                # добавим для временных ячеек дополнительный 0 к одиночным цифрам и подготовим дату и время к виду DD.MM.YYYY  и  HH:MM
                # по всем временным меткам
                for num_time, val in enumerate(arr_TimeAxis_custom):
                    if arr_TimeAxis_custom[num_time][0] ==   '111': 
                        arr_TimeAxis_custom[num_time][0] = 'ВСЕГО ДЕНЬ по счетчику'
                        arr_TimeAxis_custom[num_time][3] = ''
                    elif arr_TimeAxis_custom[num_time][0] == '222': 
                        arr_TimeAxis_custom[num_time][0] = 'ВСЕГО ДЕНЬ по группе'
                        arr_TimeAxis_custom[num_time][3] = ''
                    elif arr_TimeAxis_custom[num_time][0] == '333': 
                        arr_TimeAxis_custom[num_time][0] = 'ВСЕГО МЕСЯЦ по счетчику'
                        arr_TimeAxis_custom[num_time][3] = ''
                    elif arr_TimeAxis_custom[num_time][0] == '444': 
                        arr_TimeAxis_custom[num_time][0] = 'ВСЕГО МЕСЯЦ по группе'
                        arr_TimeAxis_custom[num_time][3] = ''
                    elif arr_TimeAxis_custom[num_time][0] == '555': 
                        arr_TimeAxis_custom[num_time][0] = 'ВСЕГО ГОД по счетчику'
                        arr_TimeAxis_custom[num_time][3] = ''
                    elif arr_TimeAxis_custom[num_time][0] == '777': 
                        arr_TimeAxis_custom[num_time][0] = 'ВСЕГО ГОД по группе'
                        arr_TimeAxis_custom[num_time][3] = ''

                    elif arr_TimeAxis_custom[num_time][0] == '110': 
                        # arr_TimeAxis_custom[num_time][0] = 'ИТОГО ДЕНЬ'
                        arr_TimeAxis_custom[num_time][0] = 'ИТОГО ДЕНЬ по счетчику'
                        arr_TimeAxis_custom[num_time][3] = ''
                    elif arr_TimeAxis_custom[num_time][0] == '220': 
                        arr_TimeAxis_custom[num_time][0] = 'ИТОГО ДЕНЬ по группе'
                        arr_TimeAxis_custom[num_time][3] = ''
                    elif arr_TimeAxis_custom[num_time][0] == '330':
                        # arr_TimeAxis_custom[num_time][0] = 'ИТОГО МЕСЯЦ'
                        # arr_TimeAxis_custom[num_time][0] = 'ИТОГО ЗА запрошенный ИНТЕРВАЛ'
                        arr_TimeAxis_custom[num_time][0] = 'ИТОГО МЕСЯЦ по счетчику'
                        arr_TimeAxis_custom[num_time][3] = ''
                    elif arr_TimeAxis_custom[num_time][0] == '440': 
                        arr_TimeAxis_custom[num_time][0] = 'ИТОГО МЕСЯЦ по группе'
                        arr_TimeAxis_custom[num_time][3] = ''
                    elif arr_TimeAxis_custom[num_time][0] == '550': 
                        arr_TimeAxis_custom[num_time][0] = 'ИТОГО ГОД по счетчику'
                        # arr_TimeAxis_custom[num_time][0] = 'ИТОГО ЗА запрошенный ИНТЕРВАЛ'
                        arr_TimeAxis_custom[num_time][3] = ''
                    elif arr_TimeAxis_custom[num_time][0] == '770': 
                        arr_TimeAxis_custom[num_time][0] = 'ИТОГО ГОД по группе'
                        arr_TimeAxis_custom[num_time][3] = ''
                    elif arr_TimeAxis_custom[num_time][0] == '880': 
                        # arr_TimeAxis_custom[num_time][0] = 'ИТОГО по группе \nЗА ПЕРИОД'
                        arr_TimeAxis_custom[num_time][0] = 'ИТОГО по группе \nза запрошенный ИНТЕРВАЛ'
                        arr_TimeAxis_custom[num_time][3] = ''    
                    elif arr_TimeAxis_custom[num_time][0] == '990': 
                        # arr_TimeAxis_custom[num_time][0] = 'ИТОГО по счетчику \nЗА ПЕРИОД'
                        arr_TimeAxis_custom[num_time][0] = 'ИТОГО по счетчику \nза запрошенный ИНТЕРВАЛ'
                        arr_TimeAxis_custom[num_time][3] = ''
                    else:
                        arr_TimeAxis_custom[num_time][0] = mg.appendZero(arr_TimeAxis_custom[num_time][2])+'/'+mg.appendZero(arr_TimeAxis_custom[num_time][1])+'/'+arr_TimeAxis_custom[num_time][0]
                        arr_TimeAxis_custom[num_time][3] = mg.appendZero(arr_TimeAxis_custom[num_time][3])+':'+mg.appendZero(arr_TimeAxis_custom[num_time][4])
                arr_TimeAxis_custom = np.delete(arr_TimeAxis_custom, [1,2,4] , axis = 1)  # удалим ненужные столбцы с месяцем, днем и минумами
                #
                arr_Table = np.hstack((arr_TimeAxis_custom, arr_data_custom))
                #
                self.emit_value(70)
                # # добавим в конец таблицы еще пустых строк (нужно для визуализации первой таблицы групп заголовков)
                # leng = np.shape(arr_Table)[0]
                # for i in range (0,30,1):
                #     arr_Table = np.insert(arr_Table, leng+i, "", axis=0)
                # дополним списко заголовки шапки таблицы на экране названиями выбранных счетчиков
                self.model.lst_header_table, self.model.lst_backgroundcolor_group = mg.create_header_table(cfg.lst_id_checked_counter_in_group + cfg.lst_id_checked_single_counter)
                #
                self.data = arr_Table
                self.model.set(self.data.copy())
                self.tableProfilePowerCounts.resizeColumnsToContents()
                
                self.emit_value(90)
                # # сделаем вторую таблицу, которая будет прсто шапкой над первой
                # self.model2.lst_header_table = mg.create_header_table2(cfg.lst_checked_counter_in_group + cfg.lst_checked_single_counter)
                # self.data2 = arr_Table
                # self.model2.set(self.data2.copy())
                # self.tableProfilePowerCounts2.resizeColumnsToContents()
                # for num_time, val in enumerate(arr_Table):
                #     self.tableProfilePowerCounts2.setRowHeight(num_time, 1)
                #     # self.tableProfilePowerCounts2.hideRow(num_time)
                #     self.tableProfilePowerCounts2.setRowHidden(num_time, True)
                    
                # # выравниваем ширину столбцов у двух таблиц исходя из максимальной ширины
                # for num_colunm in range (0,np.shape(arr_Table)[1],1):
                #     if self.tableProfilePowerCounts.columnWidth(num_colunm) >= self.tableProfilePowerCounts2.columnWidth(num_colunm):
                #         self.tableProfilePowerCounts2.setColumnWidth(num_colunm, self.tableProfilePowerCounts.columnWidth(num_colunm))
                #     else:
                #         self.tableProfilePowerCounts.setColumnWidth(num_colunm, self.tableProfilePowerCounts2.columnWidth(num_colunm))

                # #  запретим пользователю изменять ширину столбцов
                # self.tableProfilePowerCounts.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)#,QHeaderView.ResizeToContents)
                # self.tableProfilePowerCounts2.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)#,QHeaderView.ResizeToContents)

                #
                cfg.running_thread1 = True
                self.emit_value(0)
                self.emit_string_statusBar("Готово.")

                # сделаем объединения ячеек для строк содержащих ИТОГО
                font = QFont()
                font.setBold(True)
                for num_time, val in enumerate(arr_Table):
                    if ('итого' in arr_Table[num_time][0].lower()) and ('счетчик' in arr_Table[num_time][0].lower()):
                        # setSpan(row, column, rowSpan, columnSpan)
                        self.tableProfilePowerCounts.setSpan(num_time, 0, 1, 2)
                        # setRowHeight(row, height)
                        # self.tableProfilePowerCounts.setRowHeight(num_time, 50)
                for num_time, val in enumerate(arr_Table):
                    if ('ИТОГО' in arr_Table[num_time][0].upper()) and ('ГРУПП' in arr_Table[num_time][0].upper()):
                        # setSpan(row, column, rowSpan, columnSpan)
                        self.tableProfilePowerCounts.setSpan(num_time, 0, 1, 2)
                        # self.tableProfilePowerCounts.setRowHeight(num_time, 50)
                        for num_group, itemGroup in enumerate(cfg.lst_id_checked_group):
                            list_counter_in_group, rezult_get = msql.get_list_counter_in_group_DBGC(itemGroup)
                            from_mesto = mesto[num_group]+2
                            span_row = len(list_counter_in_group)
                            self.tableProfilePowerCounts.setSpan(num_time, from_mesto, 1, span_row)
                self.tableProfilePowerCounts.resizeRowsToContents()

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
                # lst_header_table2 = mg.create_header_table2(cfg.lst_checked_counter_in_group + cfg.lst_checked_single_counter)
                lst_header_table,lst_backgroundcolor_group = mg.create_header_table(cfg.lst_id_checked_counter_in_group + cfg.lst_id_checked_single_counter)
                # _list.append(lst_header_table2)
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
                        # worksheet.write(r, c, col)
                        # сделаем так, чтобы в иксель числа сохранялись как числа, а не строки
                        # все числа типа float имеют разделитель ','
                        if ',' in col:
                            col = col.replace(',', '.' )
                            col = float(col)
                            worksheet.write(r, c, col)  
                        else:
                            # если это не число
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
                worksheet.set_row(0, 18, cell_format) # Установка стиля для строки 
                #worksheet.set_row(1, 18, cell_format) # Установка стиля для строки 
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
        def renderTreePanel_for_ProfilPower2(self):
            
            list_counterDB, rezult_getListOfCounterDB = msql.getListCounterDB()
            list_GroupDB, rezult_getListOfGroupDB = msql.getListGroupDB()
            self.treeCount.clear()
            for item_Group in list_GroupDB:
                parent = QTreeWidgetItem(self.treeCount)
                parent.setText(0, item_Group['name_group_full'])
                list_DictGroupWithCounterDB, rezult_getListOfGroupDB = msql.getListCounterInGroupDB(self,item_Group['name_group_full'])
                parent.setFlags(parent.flags() | Qt.ItemIsUserCheckable)
                parent.setCheckState(0, Qt.Unchecked)
                for itemChek in cfg.lst_id_checked_group:
                    if itemChek == item_Group['id']:
                        parent.setCheckState(0, Qt.Checked)
                        break
                for item in list_DictGroupWithCounterDB:
                    child = QTreeWidgetItem(parent)
                    child.setForeground(0, Qt.darkBlue)
                    child.setText(0, "    " + item['name_counter_full'])
                    # child.setText(1, item['net_adress'])
            parent = QTreeWidgetItem(self.treeCount)
            parent.setText(0, "Все счетчики")
            for item_Counter in list_counterDB:
                    child = QTreeWidgetItem(parent)
                    child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                    child.setCheckState(0, Qt.Unchecked)
                    child.setForeground(0, Qt.darkBlue)
                    child.setText(0, item_Counter['name_counter_full'])
                    # child.setText(1, item_Counter['net_adress'])
                    # for itemChek in (cfg.lst_checked_counter_in_group + cfg.lst_checked_single_counter):
                    for itemChek in (cfg.lst_id_checked_single_counter):    
                        if itemChek == item_Counter['id']:
                            child.setCheckState(0, Qt.Checked)
                            break
            self.treeCount.expandAll()
            self.treeCount.resizeColumnToContents(0)
            # self.tree.resizeColumnToContents(1)
            return None

    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------    
        def renderTreePanel_for_ProfilPower(self):
            
            list_counterDB, rezult_getListOfCounterDB = msql.getListCounterDB()
            list_GroupDB, rezult_getListOfGroupDB = msql.getListGroupDB()
            self.treeCount.clear()
            for item_Group in list_GroupDB:
                parent = QTreeWidgetItem(self.treeCount)
                parent.setText(0, item_Group['name_group_full'])
                list_DictGroupWithCounterDB, rezult_getListOfGroupDB = msql.getListCounterInGroupDB(self,item_Group['name_group_full'])
                parent.setFlags(parent.flags() | Qt.ItemIsUserCheckable)
                parent.setCheckState(0, Qt.Unchecked)
                for itemChek in cfg.lst_id_checked_group:
                    if itemChek == item_Group['id']:
                        parent.setCheckState(0, Qt.Checked)
                        break
                for item in list_DictGroupWithCounterDB:
                    child = QTreeWidgetItem(parent)
                    child.setForeground(0, Qt.darkBlue)
                    child.setText(0, "    " + item['name_counter_full'])
                    # child.setText(1, item['net_adress'])
            parent = QTreeWidgetItem(self.treeCount)
            parent.setText(0, "Все счетчики")
            for item_Counter in list_counterDB:
                    child = QTreeWidgetItem(parent)
                    child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                    child.setCheckState(0, Qt.Unchecked)
                    child.setForeground(0, Qt.darkBlue)
                    child.setText(0, item_Counter['name_counter_full'])
                    # child.setText(1, item_Counter['net_adress'])
                    # for itemChek in (cfg.lst_checked_counter_in_group + cfg.lst_checked_single_counter):
                    for itemChek in (cfg.lst_id_checked_single_counter):    
                        if itemChek == item_Counter['id']:
                            child.setCheckState(0, Qt.Checked)
                            break
            self.treeCount.expandAll()
            self.treeCount.resizeColumnToContents(0)
            # self.tree.resizeColumnToContents(1)
            return None


class NpModel(QAbstractTableModel):
    def __init__(self, data = np.array([[]])):
        super().__init__()
        self.npdata = data
        self.lst_header_table = []
        # self.lst_Qt_color = [Qt.white, Qt.gray, Qt.lightGray, Qt.yellow, Qt.red,  Qt.green, Qt.blue, Qt.magenta, Qt.cyan]
        self.lst_Qt_color = [Qt.white, Qt.yellow, Qt.green, Qt.blue, Qt.red, Qt.magenta, Qt.cyan]
        self.lst_backgroundcolor_group = []
        
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
            if ('ИТОГО' in self.npdata[index.row()][0]):# and ('ГРУПП' in self.npdata[index.row()][0]):
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
        if role == Qt.BackgroundRole:
            index_background_color = self.lst_backgroundcolor_group[section]
            # background_color = QVariant(QColor(Qt.green))
            if index_background_color >= len(self.lst_Qt_color)-1: index_background_color = index_background_color - (len(self.lst_Qt_color)-2) 
            background_color = self.lst_Qt_color[index_background_color]
            return QVariant(QColor(background_color))
 
    def set(self,arr=np.array([[]])):
        self.beginResetModel()
        self.npdata = arr
        self.endResetModel()
        self.layoutChanged.emit()
    
    def get(self):
        return self.npdata



# class NpModel2(QAbstractTableModel):
#     def __init__(self, data = np.array([[]])):
#         super().__init__()
#         self.npdata = data
#         self.lst_header_table = []
        
#     def rowCount(self,index=QModelIndex()):
#         return len(self.npdata)
        
#     def columnCount(self,index=QModelIndex()):
#         return len(self.npdata[0])
    
#     def data(self,index,role):
#         return None
   
#     def headerData(self,section,orientation,role):
#         # if role != Qt.DisplayRole: 
#         #     return None
#         if role == Qt.DisplayRole:
#             if orientation == Qt.Vertical:
#                 ret = 'Строка ' + str(section)
#                 return ret
#             if orientation == Qt.Horizontal:
#                 # ret = 'Столбец ' + str(section)
#                 ret = self.lst_header_table[section]
#                 return ret
#         if role == Qt.FontRole:
#             font = QFont()
#             font.setBold(True)
#             # font.setPointSize(10)
#             return font
 
#     def set(self,arr=np.array([[]])):
#         self.beginResetModel()
#         self.npdata = arr
#         self.endResetModel()
#         self.layoutChanged.emit()
    
#     def get(self):
#         return self.npdata