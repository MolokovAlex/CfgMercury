#!/bin/python3
# module
# autor: MolokovAlex
# coding: utf-8

# модуль держатель класса окна Параметры и настройки счетчика

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy as np
from time import sleep
# from PyQt5.QtSql import QSqlDatabase, QSqlQuery
# import sqlite3 as sql3

import modulVM.moduleConfigApp as mca
import modulVM.moduleAppGUIQt as magqt
# import modulVM.moduleGeneral as mg
import modulVM.config as cfg
import modulVM.moduleProtocolMercury as mpm
import modulVM.moduleGUIProfilPower as mgpp
import modulVM.moduleGUIIstantly as mgi
import modulVM.moduleComThread as mct
import modulVM.moduleSQLite as msql
import modulVM.moduleEditGroupAndCounter as megc
import modulVM.moduleLogging as ml


class ParamAndSettingDataCountersDialog (QDialog):
    """
    окно Параметры и настройки счетчика
    """
    def __init__(self, parent=None):
        # super().__init__()
        super(ParamAndSettingDataCountersDialog, self).__init__(parent)
        self.setWindowFlags(self.windowFlags()
            | Qt.WindowMinimizeButtonHint
            | Qt.WindowMaximizeButtonHint
            )
        self.setMinimumSize(QSize(800, 600))         # Устанавливаем размеры
        self.setWindowTitle("Параметры и установки") # Устанавливаем заголовок окна
        layout = QGridLayout()
        self.selectedCount = ''

        # cursorDB = cfg.sql_base_conn.cursor()
        # with cfg.sql_base_conn:
        #     cursorDB.execute("""SELECT name_counter_full FROM DBC""")
        #     b = cursorDB.fetchall()
        #     d = []
        #     for item in b:
        #         d.append(item[0])

        lbl_empty1 = QLabel("Счетчик:")
        layout.addWidget(lbl_empty1, 0, 0)
        self.cb_InstCounter = QComboBox()
        list_CounterDB, rezult_getListOfCounterDB = msql.getListCounterDB()
        for item in list_CounterDB:
            self.cb_InstCounter.addItem(item['name_counter_full'])
        # self.cb_InstCounter.addItems(d)
        self.cb_InstCounter.currentIndexChanged.connect(self.onSelectedCount)
        layout.addWidget(self.cb_InstCounter, 0, 1)
        if self.cb_InstCounter.currentText(): self.selectedCount = self.cb_InstCounter.currentText()
        else : self.selectedCount=''

        lbl_empty2 = QLabel("    ")
        layout.addWidget(lbl_empty2, 0, 2)

        lbl_empty3 = QLabel("    ")
        layout.addWidget(lbl_empty3, 0, 4)

        self.btn_save_data_in_DBC = QPushButton("Записать в БД")
        self.btn_save_data_in_DBC.clicked.connect(self.click_btn_save_data_in_DBC)
        layout.addWidget(self.btn_save_data_in_DBC, 0, 4)

        self.btnRefreshTableCounters = QPushButton("Обновить")
        self.btnRefreshTableCounters.clicked.connect(self.click_but_reviewTableParamAndSettingData)
        layout.addWidget(self.btnRefreshTableCounters, 0, 5)
        
        # self.ckb_cycleRefreshTableCounters = QCheckBox("циклически")
        # layout.addWidget(self.ckb_cycleRefreshTableCounters, 0, 6)
        
        lbl_empty4 = QLabel("    ")
        layout.addWidget(lbl_empty4, 0, 7)
        btnImportParamAndSettingCounters = QPushButton("Импорт в Excel")
        layout.addWidget(btnImportParamAndSettingCounters, 0, 8)
        
        self.model = PSDCModel()
        self.tableParamAndSettingCounts = QTableView()
        self.tableParamAndSettingCounts.setModel(self.model)
        self.reviewTableParamAndSettingData(name_full_count = self.selectedCount)
        self.tableParamAndSettingCounts.horizontalHeader().setSectionResizeMode(0)
        # self.tableProfilePowerCounts.horizontalHeader().setSectionResizeMode(1)#,QHeaderView.ResizeToContents)
        # self.tableProfilePowerCounts.horizontalHeader().hide()
        self.tableParamAndSettingCounts.verticalHeader().hide()
        self.tableParamAndSettingCounts.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        # self.tableParamAndSettingCounts.setEditTriggers(QAbstractItemView.NoEditTriggers |
        #                      QAbstractItemView.DoubleClicked)
        layout.addWidget(self.tableParamAndSettingCounts,2,0, 10, 9)
        self.setLayout(layout)
        # self.load()
        self.tableParamAndSettingCounts.resizeColumnsToContents()

        # найдем в списке счетчиков БД словарь того счетчика который был выбран в Combox
        # self.old_list_counterDB, rezult_getListOfCounterDB = msql.getListCounterDB()
        # dict_one_Counter ={}
        # for itemCounter in self.old_list_counterDB:
        #     if itemCounter['name_counter_full'] == self.selectedCount:
        #         dict_one_Counter = itemCounter.copy()
        #         break
        
        return None

    def click_btn_save_data_in_DBC(self):
        pass
        # self.tableParamAndSettingCounts.setModel(self.model)
        model_for_save = self.tableParamAndSettingCounts.model()
        # dic_counter['ku'] = data['ku']
        #             dic_counter['ki'] = data['ki']
        #             rezult_EditCounterDB = editCounterDB(dic_counter)
        return None
    
    def click_but_reviewTableParamAndSettingData(self):
        numCount = self.selectedCount
        bellTimer= False
        if numCount != "":
            self.reviewTableParamAndSettingData(name_full_count = self.selectedCount)
        return None


    def reviewTableParamAndSettingData(self , name_full_count = ''):
        """обновление таблицы параметров и установок выбраннго счетчика
        """
        if name_full_count != "":
            list_CounterDB, rezult_getListOfCounterDB = msql.getListCounterDB()
            arr_vert_header = np.array(cfg.lst_rusname_poles_DBC)
            if rezult_getListOfCounterDB:
                # найдем словарь с параметрами по выбранному счетчику
                for itemCounter in list_CounterDB:
                    if name_full_count == itemCounter['name_counter_full']:
                        result = itemCounter.items()
                        data = list(result)
                        arr_data = np.array(data)
                        arr_data = np.insert(arr_data, 0, arr_vert_header, axis=1) 
                        arr_data = np.delete(arr_data,1,axis=1)   
            self.data = arr_data
            self.model.set(self.data.copy())
            self.tableParamAndSettingCounts.resizeColumnsToContents()
        return None
    
    def onSelectedCount(self, idx):
        """ обработка выбора счетчика в ComboBox
        """
        # получим полное название счетчика
        self.selectedCount = self.cb_InstCounter.currentText()
        self.reviewTableParamAndSettingData(name_full_count = self.selectedCount)
        return None



class PSDCModel(QAbstractTableModel):
    def __init__(self, data = np.array([[]])):
        super().__init__()
        self.npdata = data
        self.lst_header_table = ['Параметр', 'Значение']
        
    def rowCount(self,index=QModelIndex()):
        return len(self.npdata)
        
    def columnCount(self,index=QModelIndex()):
        return len(self.npdata[0])
    
    def data(self,index,role):
        if not index.isValid():# or role != Qt.DisplayRole: 
            return None
        if role == Qt.DisplayRole or role == Qt.EditRole:
            val = self.npdata[index.row()][index.column()]
            return str(val)
        # if role == Qt.FontRole and (index.column() == 0 or index.column() == 1):
        #     font = QFont() 
        #     font.setBold(True)
        #     return font
    
    def setData(self, index, value, role):
        if role == Qt.EditRole:
            self.npdata[index.row(), index.column()] = value
            return True

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled | Qt.ItemIsEditable
    
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