# moduleEditGroupAndCounter
# autor: MolokovAlex
# coding: utf-8

# модуль окна редактирования счетчиков и групп

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from time import sleep
import re

# import modulVM.moduleConfigApp as mca
import modulVM.config as cfg
# import modulVM.moduleProtocolMercury as mpm
# import modulVM.moduleGUIProfilPower as mgpp
# import modulVM.moduleGUIIstantly as mgi
# import modulVM.moduleComThread as mct
import modulVM.moduleSQLite as msql
# import modulVM.moduleEditGroupAndCounter as megc
import modulVM.moduleLogging as ml


class EditGroupsCounterDialog (QDialog):
    def __init__(self, parent=None):
        # super().__init__()
        super(EditGroupsCounterDialog, self).__init__(parent)
        
        self.currentItemTree = ''
        
        self.setWindowFlags(self.windowFlags()
            | Qt.WindowMinimizeButtonHint
            | Qt.WindowMaximizeButtonHint
            )
        self.setMinimumSize(QSize(800, 600))         # Устанавливаем размеры
        self.setWindowTitle("Редактирование групп и счетчиков") # Устанавливаем заголовок окна
        
        # layout = QHBoxLayout()
        layout = QGridLayout()
        self.setLayout(layout)

        self.gb_IPtoServer = QGroupBox("Группы")
        layout.addWidget(self.gb_IPtoServer, 0, 0, 2, 1)
        self.tree = QTreeWidget()
        self.renderTreePanel2()
        self.tree.clicked.connect(self.onClicked)
        layout2 = QVBoxLayout()
        self.gb_IPtoServer.setLayout(layout2)
        layout2.addWidget(self.tree)

        self.gb_IPtoClient = QGroupBox("Редактирование группы")  
        # self.gb_IPtoClient.clicked.connect(self.clickGroupBoxIPtoClient)
        layout.addWidget(self.gb_IPtoClient, 0, 1)
        vbox_IPClient = QVBoxLayout()
        self.gb_IPtoClient.setLayout(vbox_IPClient)
        btn_newGroup = QPushButton("Новая группа")
        vbox_IPClient.addWidget(btn_newGroup)
        btn_newGroup.clicked.connect(self.windowDialogCreateNewGroup)
        btn_editGroup = QPushButton("Редакт. группы")
        vbox_IPClient.addWidget(btn_editGroup)
        btn_editGroup.clicked.connect(self.windowDialogEditGroup)
        btn_deleteGroup = QPushButton("Удалить группу")
        vbox_IPClient.addWidget(btn_deleteGroup)
        btn_deleteGroup.clicked.connect(self.windowDialogDeleteGroup)

        self.gb_ConnectionCOM = QGroupBox("Редактирование счетчика")
        layout.addWidget(self.gb_ConnectionCOM, 1, 1)
        vbox_2 = QVBoxLayout()
        self.gb_ConnectionCOM.setLayout(vbox_2)
        btn_newCounter = QPushButton("Новый счетчик")
        vbox_2.addWidget(btn_newCounter)
        btn_newCounter.clicked.connect(self.windowDialogNewCounter)
        btn_editCounter = QPushButton("Редакт. счетчик")
        vbox_2.addWidget(btn_editCounter)
        btn_editCounter.clicked.connect(self.windowDialogEditCounter)
        btn_copyCounter = QPushButton("Копировать/удалить групповой счетчик ")
        vbox_2.addWidget(btn_copyCounter)
        btn_copyCounter.clicked.connect(self.windowDialogCounterInGroup)        
        btn_deleteCounter = QPushButton("Удалить счетчик")
        vbox_2.addWidget(btn_deleteCounter)
        btn_deleteCounter.clicked.connect(self.windowDialogDeleteCounter)

    
    def onClicked(self):
        self.currentItemTree=self.tree.currentItem().text(0)
        return None
    
    

    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------

    def windowDialogCreateNewGroup(self):

        self.DialogNewGroup = QDialog()
        self.DialogNewGroup.setWindowTitle("Создание группы")
        self.DialogNewGroup.setWindowModality(Qt.ApplicationModal)
        self.DialogNewGroup.resize(500,80)
        layout = QGridLayout(self.DialogNewGroup)
        label1 = QLabel('Введите название новой группы:',self.DialogNewGroup)
        self.newName = QLineEdit()
        self.newName.setText(self.currentItemTree)
        layout.addWidget(label1, 1, 0, 1, 2)
        layout.addWidget(self.newName,2,0, 1, 2)
        btn_OKEditGroup = QPushButton("Да")
        layout.addWidget(btn_OKEditGroup, 3, 0)
        btn_OKEditGroup.clicked.connect(self.acceptBtnDialogNewGroup)
        btn_CancelEditGroup = QPushButton("Отмена")
        layout.addWidget(btn_CancelEditGroup, 3, 1)
        btn_CancelEditGroup.clicked.connect(self.rejectBtnDialogNewGroup)
        self.DialogNewGroup.exec_()   

    def acceptBtnDialogNewGroup(self):
        # oldNameGroup = self.currentItemTree
        newNameGroup = self.newName.text()
        list_GroupDB, rezult_getListOfGroupDB = msql.getListGroupDB()

        error_name = False
        # проверка на валидность поля полнго наименования
        flag_symbol_valid, newNameGroup = self.valid_symbol_pole(newNameGroup)
        if not(flag_symbol_valid):
            # проверка на пустоту поля нового названия 
            flag_empty_valid = self.valid_empty_pole(newNameGroup)
            if not(flag_empty_valid):
                error_name = False
            else:
                error_name = True
                newNameGroup = "Новая группа"
        else:
            error_name = True
            newNameGroup = "Новая группа"

        error = True
        if not error_name:
            #  проверка на совпадение плного названия с другими группами
            error = False
            for item in list_GroupDB:
                flag_odinak_valid = self.valid_odinak_pole(item['name_group_full'], newNameGroup)
                if not(flag_odinak_valid):
                    error = False
                else:
                    error = True
                    newNameGroup = "Новая группа"
                    break




        # error = False
        # for item in list_GroupDB:
        #     if (item['name_group_full'] == newNameGroup):
        #         button = QMessageBox.critical(
        #                 self,
        #                 "Ошибка ввода",
        #                 "Группа с такими параметрами уже существует",
        #                 buttons=QMessageBox.StandardButton.Ok ,
        #                 defaultButton=QMessageBox.StandardButton.Ok,)
        #         error = True
        #         break
        #     else:
        #         error = False
        if not error:
            msql.addNewGroupDB(newNameGroup)
            self.DialogNewGroup.hide()
        self.renderTreePanel2()
        return None
    
    def rejectBtnDialogNewGroup(self):
        # self.renderTreePanel2()
        self.DialogNewGroup.hide()
        return None
    
    
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------
    def  windowDialogEditGroup(self):
        if self.currentItemTree:
            self.DialogEditGroup = QDialog()
            self.DialogEditGroup.setWindowTitle("Редактирование название группы")
            self.DialogEditGroup.setWindowModality(Qt.ApplicationModal)
            self.DialogEditGroup.resize(500,80)
            layout = QGridLayout(self.DialogEditGroup)
            label1 = QLabel('Введите новое название группы:',self.DialogEditGroup)
            self.newName = QLineEdit()
            self.newName.setText(self.currentItemTree)
            layout.addWidget(label1, 1, 0, 1, 2)
            layout.addWidget(self.newName,2,0, 1, 2)
            btn_OKEditGroup = QPushButton("Да")
            layout.addWidget(btn_OKEditGroup, 3, 0)
            btn_OKEditGroup.clicked.connect(self.acceptBtnDialogEditGroup)
            btn_CancelEditGroup = QPushButton("Отмена")
            layout.addWidget(btn_CancelEditGroup, 3, 1)
            btn_CancelEditGroup.clicked.connect(self.rejectBtnDialogEditGroup)
            self.DialogEditGroup.exec_()   
        else:
            button = QMessageBox.critical(
            self,
            "Ошибка выбора",
            "Не выбрана Группа в дереве",
            buttons=QMessageBox.StandardButton.Ok ,
            defaultButton=QMessageBox.StandardButton.Ok,)
        
    def acceptBtnDialogEditGroup(self):
        oldNameGroup = self.currentItemTree
        newNameGroup = self.newName.text()
        
        # list_counterDB, rezult_getListOfCounterDB = msql.getListCounterDB(self)
        list_GroupDB, rezult_getListOfGroupDB = msql.getListGroupDB()

        error_name = False
        # проверка на валидность поля полнго наименования
        flag_symbol_valid, newNameGroup = self.valid_symbol_pole(newNameGroup)
        if not(flag_symbol_valid):
            # проверка на пустоту поля нового названия 
            flag_empty_valid = self.valid_empty_pole(newNameGroup)
            if not(flag_empty_valid):
                error_name = False
            else:
                error_name = True
                newNameGroup = self.currentItemTree
        else:
            error_name = True
            newNameGroup = self.currentItemTree

        error = True
        if not error_name:
            #  проверка на совпадение плного названия с другими группами
            error = False
            for item in list_GroupDB:
                flag_odinak_valid = self.valid_odinak_pole(item['name_group_full'], newNameGroup)
                if not(flag_odinak_valid):
                    error = False
                else:
                    error = True
                    newNameGroup = "Новая группа"
                    break




        # error = False
        # # проверка на пустоту поля нового названия группы
        # if (newNameGroup == ""):
        #     button = QMessageBox.critical(
        #             self,
        #             "Ошибка ввода",
        #             "Поле ввода наименования группы пусто",
        #             buttons=QMessageBox.StandardButton.Ok ,
        #             defaultButton=QMessageBox.StandardButton.Ok,)
        #     error = True
        # else:
        #     # error = False
        #     # проверка на совпадение нового названия группы с существующими
        #     for item in list_GroupDB:
        #         if (item['name_group_full'] == newNameGroup):
        #             button = QMessageBox.critical(
        #                     self,
        #                     "Ошибка ввода",
        #                     "Группа с такими параметрами уже существует",
        #                     buttons=QMessageBox.StandardButton.Ok ,
        #                     defaultButton=QMessageBox.StandardButton.Ok,)
        #             error = True
        #             break
        #         else:
        #             error = False
                
        if not error:
            rezult_getListOfGroupDB = msql.editGroupDB(oldNameGroup,newNameGroup)
            self.DialogEditGroup.hide()
        self.renderTreePanel2()
        return None
    
    def rejectBtnDialogEditGroup(self):
        self.renderTreePanel2()
        self.DialogEditGroup.hide()
        return None
    
    
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------
    def windowDialogNewCounter(self):

        self.DialogNewCounter = QDialog()
        self.DialogNewCounter.setWindowTitle("Создание нового счетчика")
        self.DialogNewCounter.setWindowModality(Qt.ApplicationModal)
        self.DialogNewCounter.resize(600,600)
            
        
        layout = QGridLayout(self.DialogNewCounter)
            # self.old_list_counterDB, rezult_getListOfCounterDB = msql.getListCounterDB(self)
        self.tableNewCounter = QTableWidget(self)  
        self.tableNewCounter.setColumnCount(2)    
        self.tableNewCounter.setHorizontalHeaderLabels(["Наименование", "Значение"])
        self.tableNewCounter.horizontalHeaderItem(0).setTextAlignment(Qt.AlignHCenter)
        self.tableNewCounter.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
        self.tableNewCounter.setRowCount(0) 

        #  запонлять значениями вторую колонку таблицы НЕ БУДЕМ и сразу
        #  разрешим только конктерные ячейки для редактирования, которые определены в cfg.lst_readOnly_poles_DBC   
        i=0
        for item5 in cfg.lst_name_poles_DBC:
                rows = self.tableNewCounter.rowCount()
                self.tableNewCounter.setRowCount(rows + 1)
                tableWItem = QTableWidgetItem()
                tableWItem.setText("")
                if cfg.lst_readOnly_poles_DBC[i]:
                    tableWItem.setFlags(tableWItem.flags() ^ Qt.ItemIsEditable)
                    tableWItem.setBackground(QColor(100,100,150))
                else:
                    tableWItem.setFlags(tableWItem.flags() | Qt.ItemIsEditable)
                self.tableNewCounter.setItem(rows, 1, tableWItem)
                i = i+1
        # заполним первую колонку названиями парамтров
        row = 0
        for item in cfg.lst_rusname_poles_DBC:
            tableWItem = QTableWidgetItem()
            tableWItem.setText(item)
            font = QFont()
            font.setBold(True)
            tableWItem.setFont(font)
            self.tableNewCounter.setItem(row, 0, tableWItem)
            row = row +1
        self.tableNewCounter.resizeColumnsToContents()
        layout.addWidget(self.tableNewCounter,0,0,1,2)

        btn_OKNewCounter = QPushButton("Да")
        layout.addWidget(btn_OKNewCounter, 3, 0)
        btn_OKNewCounter.clicked.connect(self.acceptBtnDialogNewCounter)
        btn_CancelNewCounter = QPushButton("Отмена")
        layout.addWidget(btn_CancelNewCounter, 3, 1)
        btn_CancelNewCounter.clicked.connect(self.rejectBtnDialogNewCounter)
        self.DialogNewCounter.exec_()   

        
    def acceptBtnDialogNewCounter(self):
        """ оработка нажатия на кнопку ОК при создании нового счетчика
        """
        row=0
        dict_newCounter={}
        for item5 in cfg.lst_name_poles_DBC:                
                cell  = self.tableNewCounter.item(row, 1).text()
                dict_newCounter[item5]=cell
                row = row+1
        list_counterDB, rezult_getListOfCounterDB = msql.getListCounterDB()


        error_name = False
        # проверка на валидность поля полнго наименования
        flag_symbol_valid, dict_newCounter['name_counter_full'] = self.valid_symbol_pole(dict_newCounter['name_counter_full'])
        if not(flag_symbol_valid):
            # проверка на пустоту поля нового названия 
            flag_empty_valid = self.valid_empty_pole(dict_newCounter['name_counter_full'])
            if not(flag_empty_valid):
                error_name = False
            else:
                error_name = True
                dict_newCounter['name_counter_full'] = "Новый счетчик"#self.dict_one_OldCounter['name_counter_full']
        else:
            error_name = True
            dict_newCounter['name_counter_full'] = "Новый счетчик"#self.dict_one_OldCounter['name_counter_full']

        #  проверка на валидность сетевого адреса
        error_net_adr  = self.valid_number_adr_pole(str(dict_newCounter['net_adress']))
        if error_net_adr:
            dict_newCounter['net_adress'] = 255 #int(self.dict_one_OldCounter['net_adress'])
            
        error = True
        if (not error_name) and (not error_net_adr):
            #  проверка на совпадение плного названия и сетевого адреса с другими счетчиками
            error = False
            for item in list_counterDB:
                # dic_counter = msql.getCounterDB(dict_newNameCounter['id'])
                # if item['id'] != int(dict_newCounter['id']):
                flag_odinak_valid = self.valid_odinak_pole(item['name_counter_full'], dict_newCounter['name_counter_full'])
                if not(flag_odinak_valid):
                    error = False
                else:
                    error = True
                    dict_newCounter['name_counter_full'] =  "Новый счетчик"#self.dict_one_OldCounter['name_counter_full']
                    break
                #  проверка на совпадение сетевого адреса с аналогичными
                flag_odinak_number_valid = self.valid_odinak_net_pole(int(item['net_adress']), int(dict_newCounter['net_adress']))
                if not(flag_odinak_number_valid):
                    error = False
                else:
                    error = True
                    dict_newCounter['net_adress'] = 255 #int(self.dict_one_OldCounter['net_adress'])
                    break

        if not error:
            rezult_EditCounterDB = msql.addNewCounterDB(dict_newCounter)
            self.renderTreePanel2()
            self.DialogNewCounter.hide()
        self.rendertableNewCounter(dict_newCounter)
        self.renderTreePanel2()
        return None
    
    def rejectBtnDialogNewCounter(self):
        self.renderTreePanel2()
        self.DialogNewCounter.hide()
        return None
    
    def rendertableNewCounter(self, dict_counter):
        #  запонлим значениями вторую колонку таблицы и сразу
        #  разрешим только конктерные ячейки для редактирования, которые определены в cfg.lst_readOnly_poles_DBC
        # row=0
        for row, value_lst in enumerate(cfg.lst_name_poles_DBC):
            # rows = self.tableEditCounter.rowCount()
            tableWItem = QTableWidgetItem()
            if row != 0:        #  избавляемся от отображения поля id
                valueInTable = str(dict_counter[cfg.lst_name_poles_DBC[row]])
                tableWItem.setText(valueInTable)
                if cfg.lst_readOnly_poles_DBC[row]:
                    tableWItem.setFlags(tableWItem.flags() ^ Qt.ItemIsEditable)
                    tableWItem.setBackground(QColor(100,100,150))
                else:
                    tableWItem.setFlags(tableWItem.flags() | Qt.ItemIsEditable)
                self.tableNewCounter.setItem(row, 1, tableWItem)
            # self.tableEditCounter.setItem(row, 1, QTableWidgetItem(valueInTable))
            # row += 1
        # заполним первую колонку названиями парамтров
        # row = 0
        for row, value_lst in enumerate(cfg.lst_rusname_poles_DBC):
            tableWItem = QTableWidgetItem()
            tableWItem.setText(value_lst)
            font = QFont()
            font.setBold(True)
            tableWItem.setFont(font)
            self.tableNewCounter.setItem(row, 0, tableWItem)
            # row = row +1

        return None



    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------
    def windowDialogEditCounter(self):
        if self.currentItemTree:
            self.DialogEditCounter = QDialog()
            self.DialogEditCounter.setWindowTitle("Редактирование данных счетчика")
            self.DialogEditCounter.setWindowModality(Qt.ApplicationModal)
            self.DialogEditCounter.resize(600,800)


                       
            layout = QGridLayout(self.DialogEditCounter)
            self.old_list_counterDB, rezult_getListOfCounterDB = msql.getListCounterDB()
            self.tableEditCounter = QTableWidget(self)  
            self.tableEditCounter.setColumnCount(2)    
            self.tableEditCounter.setHorizontalHeaderLabels(["Наименование", "Значение"])
            self.tableEditCounter.horizontalHeaderItem(0).setTextAlignment(Qt.AlignHCenter)
            self.tableEditCounter.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
            self.tableEditCounter.setRowCount(0) 
            # найдем в старом(не измененном еще) списке счетчиков словарь того счетчика который был выбран в дереве
            self.dict_one_OldCounter ={}
            for itemOldCounter in self.old_list_counterDB:
                if itemOldCounter['name_counter_full'] == self.currentItemTree:
                    self.dict_one_OldCounter = itemOldCounter.copy()
                    break
            #  запонлим значениями вторую колонку таблицы и сразу
            #  разрешим только конктерные ячейки для редактирования, которые определены в cfg.lst_readOnly_poles_DBC
            i=0
            for item5 in cfg.lst_name_poles_DBC:
                rows = self.tableEditCounter.rowCount()
                self.tableEditCounter.setRowCount(rows + 1)
                valueInTable = str(self.dict_one_OldCounter[cfg.lst_name_poles_DBC[rows]])
                tableWItem = QTableWidgetItem()
                tableWItem.setText(valueInTable)
                if cfg.lst_readOnly_poles_DBC[i]:
                    tableWItem.setFlags(tableWItem.flags() ^ Qt.ItemIsEditable)
                    tableWItem.setBackground(QColor(100,100,150))
                else:
                    tableWItem.setFlags(tableWItem.flags() | Qt.ItemIsEditable)
                self.tableEditCounter.setItem(rows, 1, tableWItem)
                i = i+1
            
            # заполним первую колонку названиями парамтров
            row = 0
            for item in cfg.lst_rusname_poles_DBC:
                tableWItem = QTableWidgetItem()
                tableWItem.setText(item)
                font = QFont()
                font.setBold(True)
                tableWItem.setFont(font)
                self.tableEditCounter.setItem(row, 0, tableWItem)
                row = row +1
            
            layout.addWidget(self.tableEditCounter,0,0,1,2)
            self.tableEditCounter.resizeColumnsToContents()

            btn_OKEditCounter = QPushButton("Да")
            layout.addWidget(btn_OKEditCounter, 3, 0)
            btn_OKEditCounter.clicked.connect(self.acceptBtnDialogEditCounter)
            btn_CancelEditCounter = QPushButton("Отмена")
            layout.addWidget(btn_CancelEditCounter, 3, 1)
            btn_CancelEditCounter.clicked.connect(self.rejectBtnDialogEditCounter)
            self.DialogEditCounter.exec_()   
        else:
            button = QMessageBox.critical(
            self,
            "Ошибка выбора",
            "Не выбран Счетчик в дереве",
            buttons=QMessageBox.StandardButton.Ok ,
            defaultButton=QMessageBox.StandardButton.Ok)
        
    def acceptBtnDialogEditCounter(self):
        # dict_oldNameCounter = self.old_list_counterDB

        dict_editCounter={}
        for row, value_lst in enumerate(cfg.lst_name_poles_DBC):                
                cell  = self.tableEditCounter.item(row, 1).text()
                dict_editCounter[value_lst]=cell
        list_counterDB, rezult_getListOfCounterDB = msql.getListCounterDB()
        
        error_name = False
        # проверка на валидность поля полнго наименования
        flag_symbol_valid, dict_editCounter['name_counter_full'] = self.valid_symbol_pole(dict_editCounter['name_counter_full'])
        if not(flag_symbol_valid):
            # проверка на пустоту поля нового названия 
            flag_empty_valid = self.valid_empty_pole(dict_editCounter['name_counter_full'])
            if not(flag_empty_valid):
                error_name = False
            else:
                error_name = True
                dict_editCounter['name_counter_full'] = self.dict_one_OldCounter['name_counter_full']
        else:
            error_name = True
            dict_editCounter['name_counter_full'] = self.dict_one_OldCounter['name_counter_full']

        #  проверка на валидность сетевого адреса
        error_net_adr  = self.valid_number_adr_pole(str(dict_editCounter['net_adress']))
        if error_net_adr:
            dict_editCounter['net_adress'] = int(self.dict_one_OldCounter['net_adress'])
            
        error = False
        if (not error_name) and (not error_net_adr):
            #  проверка на совпадение плного названия и сетевого адреса с другими счетчиками
            error = False
            for item in list_counterDB:
                # dic_counter = msql.getCounterDB(dict_newNameCounter['id'])
                if item['id'] != int(dict_editCounter['id']):
                    flag_odinak_valid = self.valid_odinak_pole(item['name_counter_full'], dict_editCounter['name_counter_full'])
                    if not(flag_odinak_valid):
                        error = False
                    else:
                        error = True
                        dict_editCounter['name_counter_full'] = self.dict_one_OldCounter['name_counter_full']
                        break
                    #  проверка на совпадение сетевого адреса с аналогичными
                    flag_odinak_number_valid = self.valid_odinak_net_pole(int(item['net_adress']), int(dict_editCounter['net_adress']))
                    if not(flag_odinak_number_valid):
                        error = False
                    else:
                        error = True
                        dict_editCounter['net_adress'] = int(self.dict_one_OldCounter['net_adress'])
                        break
            
            if not error:
                rezult_EditCounterDB = msql.editCounterDB(dict_editCounter)
                self.DialogEditCounter.hide()
        self.rendertableEditCounter()
        self.renderTreePanel2()
        return None
    
    def rejectBtnDialogEditCounter(self):
        self.renderTreePanel2()
        self.DialogEditCounter.hide()
        return None
    
    def rendertableEditCounter(self):
        #  запонлим значениями вторую колонку таблицы и сразу
        #  разрешим только конктерные ячейки для редактирования, которые определены в cfg.lst_readOnly_poles_DBC
        # row=0
        for row, value_lst in enumerate(cfg.lst_name_poles_DBC):
            # rows = self.tableEditCounter.rowCount()
            tableWItem = QTableWidgetItem()
            valueInTable = str(self.dict_one_OldCounter[cfg.lst_name_poles_DBC[row]])
            tableWItem.setText(valueInTable)
            if cfg.lst_readOnly_poles_DBC[row]:
                tableWItem.setFlags(tableWItem.flags() ^ Qt.ItemIsEditable)
                tableWItem.setBackground(QColor(100,100,150))
            else:
                tableWItem.setFlags(tableWItem.flags() | Qt.ItemIsEditable)
            self.tableEditCounter.setItem(row, 1, tableWItem)
            # self.tableEditCounter.setItem(row, 1, QTableWidgetItem(valueInTable))
            # row += 1
        # заполним первую колонку названиями парамтров
        # row = 0
        for row, value_lst in enumerate(cfg.lst_rusname_poles_DBC):
            tableWItem = QTableWidgetItem()
            tableWItem.setText(value_lst)
            font = QFont()
            font.setBold(True)
            tableWItem.setFont(font)
            self.tableEditCounter.setItem(row, 0, tableWItem)
            # row = row +1

        return None

    def valid_symbol_pole(self, strg):
        flag_notValid = True
        try:
            # value_str = "".join(re.findall(r'[ 0-9A-Za-zА-Яа-я+-/`")(.,#№ ]*',  strg))
            value_str = "".join(re.findall(r'[ 0-9A-Za-zА-Яа-я+-`")(.,#№ ]*',  strg))
            flag_notValid = False
        except:
            flag_notValid = True
            value_str = ' '
        if flag_notValid == True:
            button = QMessageBox.critical(
                                    self,
                                    "Ошибка ввода",
                                    "Недопустимые символы в наименовании",
                                    buttons=QMessageBox.StandardButton.Ok ,
                                    defaultButton=QMessageBox.StandardButton.Ok,)
        return flag_notValid, value_str

    # def valid_number_adr_pole(self, num):
    #     flag_notValid = True
    #     try:
    #         value_num = "".join(re.findall(r'[0-9]*',  num))
    #         flag_notValid = False
    #     except:
    #         flag_notValid = True
    #         value_num = 254
    #     if flag_notValid == True:
    #         button = QMessageBox.critical(
    #                                 self,
    #                                 "Ошибка ввода",
    #                                 "Недопустимый сетевой адрес",
    #                                 buttons=QMessageBox.StandardButton.Ok ,
    #                                 defaultButton=QMessageBox.StandardButton.Ok,)
    #     return flag_notValid, value_num

    def valid_empty_pole(self, strg):
        flag_notValid = True
        if (strg == ""):
                button = QMessageBox.critical(
                        self,
                        "Ошибка ввода",
                        "Поле ввода наименования пусто",
                        buttons=QMessageBox.StandardButton.Ok ,
                        defaultButton=QMessageBox.StandardButton.Ok,)
                flag_notValid = True
        else:
            flag_notValid = False
        return flag_notValid
    
    def valid_number_adr_pole(self, number_adr):
        error_valid = True
        # убедимся что адрес сосотит из цифр
        try:
            value_num = "".join(re.findall(r'[0-9]*',  number_adr))
            # error_valid = False
        except:
            error_valid = True
            value_num = '2540'
        if (str(value_num) != number_adr) or (int(value_num) <= 0) or (int(value_num) >=256):
                button = QMessageBox.critical(
                        self,
                        "Ошибка ввода",
                        "Недопустимый сетевой адрес",
                        buttons=QMessageBox.StandardButton.Ok ,
                        defaultButton=QMessageBox.StandardButton.Ok,)
                error_valid = True
                
        else:
            error_valid = False
        return error_valid#, int(value_num)

    def valid_odinak_pole(self, strg1, strg2):
        flag_notValid = True
        if (strg1 == strg2):
                button = QMessageBox.critical(
                        self,
                        "Ошибка ввода",
                        "Такое наименование уже существует",
                        buttons=QMessageBox.StandardButton.Ok ,
                        defaultButton=QMessageBox.StandardButton.Ok,)
                flag_notValid = True
        else:
            flag_notValid = False
        return flag_notValid
    
    def valid_odinak_net_pole(self, adr1, adr2):
        flag_notValid = True
        if (adr1 == adr2):
                button = QMessageBox.critical(
                        self,
                        "Ошибка ввода",
                        "Такой сетевой адрес уже существует",
                        buttons=QMessageBox.StandardButton.Ok ,
                        defaultButton=QMessageBox.StandardButton.Ok,)
                flag_notValid = True
        else:
            flag_notValid = False
        return flag_notValid

    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------
    def windowDialogDeleteGroup(self):
        if self.currentItemTree:
            NameGroupDeleted = self.currentItemTree
            self.DialogDeleteGroup = QDialog()
            self.DialogDeleteGroup.setWindowTitle("Удаление группы")
            self.DialogDeleteGroup.setWindowModality(Qt.ApplicationModal)
            layout = QGridLayout(self.DialogDeleteGroup)
            label1 = QLabel('Вы уверены в удалении группы :'+NameGroupDeleted,self.DialogDeleteGroup)
            # self.newName = QLineEdit()
            # self.newName.setText(self.currentItemTree)
            layout.addWidget(label1, 1, 0, 1, 2)
            # layout.addWidget(self.newName,2,0, 1, 2)
            btn_OKDeleteGroup = QPushButton("Да")
            layout.addWidget(btn_OKDeleteGroup, 2, 0)
            btn_OKDeleteGroup.clicked.connect(self.acceptBtnDialogDeleteGroup)
            btn_CancelDeleteGroup = QPushButton("Отмена")
            layout.addWidget(btn_CancelDeleteGroup, 2, 1)
            btn_CancelDeleteGroup.clicked.connect(self.rejectBtnDialogDeleteGroup)
            self.DialogDeleteGroup.exec_()
        else:
            button = QMessageBox.critical(
            self,
            "Ошибка выбора",
            "Не выбрана Группа в дереве",
            buttons=QMessageBox.StandardButton.Ok ,
            defaultButton=QMessageBox.StandardButton.Ok)
    
    def acceptBtnDialogDeleteGroup(self):
        nameGroup = self.currentItemTree
        # newNameGroup = self.newName.text()
        rezult_getListOfGroupDB = msql.deleteGroupDB(nameGroup)
        self.DialogDeleteGroup.hide()
        self.renderTreePanel2()
        return None
    
    def rejectBtnDialogDeleteGroup(self):
        self.renderTreePanel2()
        self.DialogDeleteGroup.hide()
        
        return None    
    
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------
    def windowDialogDeleteCounter(self):
        if self.currentItemTree:
            NameCounterDeleted = self.currentItemTree
            self.DialogDeleteCounter = QDialog()
            self.DialogDeleteCounter.setWindowTitle("Удаление счетчика")
            self.DialogDeleteCounter.setWindowModality(Qt.ApplicationModal)
            layout = QGridLayout(self.DialogDeleteCounter)
            label1 = QLabel('Вы уверены в удалении счетчика :'+NameCounterDeleted,self.DialogDeleteCounter)
            layout.addWidget(label1, 1, 0, 1, 2)
            btn_OKEditCounter = QPushButton("Да")
            layout.addWidget(btn_OKEditCounter, 2, 0)
            btn_OKEditCounter.clicked.connect(self.acceptBtnDialogDeleteCounter)
            btn_CancelEditCounter = QPushButton("Отмена")
            layout.addWidget(btn_CancelEditCounter, 2, 1)
            btn_CancelEditCounter.clicked.connect(self.rejectBtnDialogDeleteCounter)
            self.DialogDeleteCounter.exec_()
        else:
            button = QMessageBox.critical(
            self,
            "Ошибка выбора",
            "Не выбрана Группа в дереве",
            buttons=QMessageBox.StandardButton.Ok ,
            defaultButton=QMessageBox.StandardButton.Ok)   
    
    def acceptBtnDialogDeleteCounter(self):
        nameCounter = self.currentItemTree
        rezult_getListOfGroupDB = msql.deleteCounterDB(nameCounter)
        self.DialogDeleteCounter.hide()
        self.renderTreePanel2()
        return None
    
    def rejectBtnDialogDeleteCounter(self):
        self.renderTreePanel2()
        self.DialogDeleteCounter.hide()
        
        return None    
    
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------     
    def windowDialogCounterInGroup(self):
        self.DialogCounterInGroup = QDialog()
        self.DialogCounterInGroup.setWindowTitle("Редактирование состава счетчиков в группах")
        self.DialogCounterInGroup.setWindowModality(Qt.ApplicationModal)
        self.DialogCounterInGroup.resize(900,900)
        
        layout = QHBoxLayout()
        self.DialogCounterInGroup.setLayout(layout)

        gb_Counter = QGroupBox("Счетчики")
        layout.addWidget(gb_Counter)
        self.treeCounter = QTreeWidget()
        self.treeCounter.setHeaderHidden(True)
        # self.treeCounter.setAllColumnsShowFocus(True)
        self.treeCounter.setSelectionBehavior(QAbstractItemView.SelectItems)
        # self.treeCounter.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.renderTreePanelOnlyCounter()
        self.treeCounter.clicked.connect(self.onClickedTreeCounter)
        layout2 = QVBoxLayout()
        gb_Counter.setLayout(layout2)
        layout2.addWidget(self.treeCounter)
        
        self.gb_move = QGroupBox()  
        layout.addWidget(self.gb_move)
        vbox_button = QVBoxLayout()
        self.gb_move.setLayout(vbox_button)
        btn_CopyInGroup = QPushButton("Скопировать в Группу ->")
        vbox_button.addWidget(btn_CopyInGroup)
        btn_CopyInGroup.clicked.connect(self.clickBtn_CopyInGroup)
        btn_RemoveFromGroup = QPushButton("<- Удалить из Группы")
        vbox_button.addWidget(btn_RemoveFromGroup)
        btn_RemoveFromGroup.clicked.connect(self.clickBtn_RemoveFromGroup)

        gb_Group = QGroupBox("Группы")
        layout.addWidget(gb_Group)
        self.treeGroup = QTreeWidget()
        self.treeGroup.setHeaderHidden(True)
        self.treeGroup.setSelectionBehavior(QAbstractItemView.SelectItems)
        layout3 = QVBoxLayout()
        gb_Group.setLayout(layout3)
        layout3.addWidget(self.treeGroup)
        self.renderTreePanelOnlyGroup()
        self.treeGroup.clicked.connect(self.onClickedTreeGroup)
        
        self.DialogCounterInGroup.exec_()
        self.renderTreePanel2()
        return None
    
    def onClickedTreeCounter(self):
        """
        обработка выбора элемента в дереве Счетчики
        """
        self.currentItemTreeCounter=self.treeCounter.currentItem().text(0)
        # self.currItemTreeCounter = self.treeCounter.currentItem().setBackground(Qt.green)
        return None
    
    def onClickedTreeGroup(self):
        """
        обработка выбора элемента в дереве Групп
        """
        self.currentItemTreeGroup=self.treeGroup.currentItem().text(0)
        nameGroup =''
        nameCounter=''
        for sel in self.treeGroup.selectedIndexes():
            nameCounter = sel.data()
            while sel.parent().isValid():
                sel = sel.parent()
                nameGroup = sel.data()
        if nameGroup : self.currentItemTreeGroup_NameGroup = nameGroup
        if nameCounter: self.currentItemTreeGroup_NameCounter = nameCounter
        return None
    
    def clickBtn_RemoveFromGroup(self):
        """
        обработка нажатия кнопки "Удалить счетчик из Группы"
        """
        # проверим - в дереве групп что то выбрано?
        if self.currentItemTreeGroup:
           # узнаем id выбранного в дереве счетчика и группы
            list_GroupDB, rezult_getListOfGroupDB = msql.getListGroupDB()
            list_CounterDB, rezult_getListOfCounterDB = msql.getListCounterDB()
            list_DBGC, dic_all_DBCG, rezult_getListOfCounterDB = msql.getListDBGC()
            for itemGroup in list_GroupDB:
                if itemGroup['name_group_full'] == self.currentItemTreeGroup_NameGroup:
                    id_group = itemGroup['id']
                    break
            for itemCounter in list_CounterDB:
                if itemCounter['name_counter_full'] == self.currentItemTreeGroup_NameCounter:
                    id_counter = itemCounter['id']
                    break
            for itemDBGC in list_DBGC:
                if (itemDBGC['id_group'] == id_group) & (itemDBGC['id_counter'] == id_counter):
                    # найдено такое сочетание id_group/id_counter в DBGC
                    id_DBGC = itemDBGC['id']
                    break
            # удалим запис с сочетанием id_group/id_counter из DBGC
            rezult_delete  = msql.deleteItemDBGC(id_DBGC)
            # обновим дерево Групп
            self.renderTreePanelOnlyGroup()
        else:
            button = QMessageBox.critical(
            self,
            "Ошибка выбора",
            "Не выбран Счетчик",
            buttons=QMessageBox.StandardButton.Ok ,
            defaultButton=QMessageBox.StandardButton.Ok)
        return None
    
    
    def clickBtn_CopyInGroup(self):
        """
        обработка нажатия кнопки "Скопировать счетчик в Группу"
        """
        # убедимся что выбранный элемент дерева Группы является названием группы
        list_GroupDB, rezult_getListOfGroupDB = msql.getListGroupDB()
        list_CounterDB, rezult_getListOfCounterDB = msql.getListCounterDB()
        list_DBGC, dic_all_DBCG, rezult_getListOfCounterDB = msql.getListDBGC()
        rezult_find_verifyGroup =False
        rezult_find_verifyCounter = False
        for item in list_GroupDB:
            if item['name_group_full'] == self.currentItemTreeGroup:
                rezult_find_verifyGroup =True
                break
            else:
                rezult_find_verifyGroup = False
        for itemCounter in list_CounterDB:
            if itemCounter['name_counter_full'] == self.currentItemTreeCounter:
                rezult_find_verifyCounter =True
                break
            else:
                rezult_find_verifyCounter = False
                
        if rezult_find_verifyCounter & rezult_find_verifyGroup:
            # узнаем id выбранного в дереве счетчика и группы
            for itemGroup in list_GroupDB:
                if itemGroup['name_group_full'] == self.currentItemTreeGroup:
                    id_group = itemGroup['id']
                    break
            for itemCounter in list_CounterDB:
                if itemCounter['name_counter_full'] == self.currentItemTreeCounter:
                    id_counter = itemCounter['id']
                    break
            # перед тем как записывать в БД - проверим - может в DBGC ужже есть эта пара id_group/id_counter
            rezult_find_verifyDBGC = False
            for itemDBGC in list_DBGC:
                if (itemDBGC['id_group'] == id_group) & (itemDBGC['id_counter'] == id_counter):
                    # найдено такое сочетание id_group/id_counter в DBGC
                    rezult_find_verifyDBGC = True
                    button = QMessageBox.critical(
                        self,
                        "Ошибка выбора",
                        "Этот Счетчик уже есть в выбранной группе",
                        buttons=QMessageBox.StandardButton.Ok ,
                        defaultButton=QMessageBox.StandardButton.Ok)
                    break
            if not rezult_find_verifyDBGC:
                # запишем в DBGC эти значения
                rezult = msql.addDBGC(id_group,id_counter)
                # обновим дерево Групп
                self.renderTreePanelOnlyGroup()
        else:
            button = QMessageBox.critical(
            self,
            "Ошибка выбора",
            "Не выбран Счетчик или Группа",
            buttons=QMessageBox.StandardButton.Ok ,
            defaultButton=QMessageBox.StandardButton.Ok) 
        return None
    
    def renderTreePanelOnlyCounter(self):
        list_counterDB, rezult_getListOfCounterDB = msql.getListCounterDB()
        # list_GroupDB, rezult_getListOfGroupDB = msql.getListGroupDB(self)
        self.treeCounter.clear()
        parent = QTreeWidgetItem(self.treeCounter)
        parent.setText(0, "Все счетчики")
        # parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
        # for x in range(50):
        for item_Counter in list_counterDB:
                child = QTreeWidgetItem(parent)
                child.setText(0, item_Counter['name_counter_full'])
        self.treeCounter.expandAll()
        self.currentItemTreeCounter =''
        return None
    
    def renderTreePanelOnlyGroup(self):
        # list_counterDB, rezult_getListOfCounterDB = msql.getListCounterDB()
        list_GroupDB, rezult_getListOfGroupDB = msql.getListGroupDB()
        self.treeGroup.clear()
        for item_Group in list_GroupDB:
            # для каждой группы из списка групп
            parent = QTreeWidgetItem(self.treeGroup)
            parent.setText(0, item_Group['name_group_full'])    # задаем текст названия группы
            # и по этой группе находим какие счетчики туда входят
            list_DictGroupWithCounterDB, rezult_getlistDictGroupWithCounterDB = msql.getListCounterInGroupDB(self,item_Group['name_group_full'])
            # parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            parent.setFlags(parent.flags() | Qt.ItemIsUserCheckable)
            # если счетчиков нет в группе - значит из не показываем
            if rezult_getlistDictGroupWithCounterDB:
                for item in list_DictGroupWithCounterDB:
                    child = QTreeWidgetItem(parent)
                # child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                    child.setText(0, item['name_counter_full'])
            #     child.setCheckState(0, Qt.Unchecked)
        self.treeGroup.expandAll()
        self.currentItemTreeGroup =''
        return None
    
    
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------    
    def renderTreePanel2(self):
        list_counterDB, rezult_getListOfCounterDB = msql.getListCounterDB()
        list_GroupDB, rezult_getListOfGroupDB = msql.getListGroupDB()
        
        self.tree.clear()
        for item_Group in list_GroupDB:
            parent = QTreeWidgetItem(self.tree)
            parent.setText(0, item_Group['name_group_full'])
            list_DictGroupWithCounterDB, rezult_getListOfGroupDB = msql.getListCounterInGroupDB(self,item_Group['name_group_full'])
            # parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
            parent.setFlags(parent.flags() | Qt.ItemIsUserCheckable)
            for item in list_DictGroupWithCounterDB:
                child = QTreeWidgetItem(parent)
                # child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                child.setText(0, item['name_counter_full'])
            #     child.setCheckState(0, Qt.Unchecked)
        parent = QTreeWidgetItem(self.tree)
        parent.setText(0, "Все счетчики")
        # parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)
        # for x in range(50):
        for item_Counter in list_counterDB:
                child = QTreeWidgetItem(parent)
                child.setText(0, item_Counter['name_counter_full'])
                child.setBackground(0,QBrush(Qt.white))
                for itemNoRecieve in cfg.lst_online_Counter:
                    if itemNoRecieve == item_Counter['net_adress']: child.setBackground(0,QBrush(Qt.red))
                    
        self.tree.expandAll()
        self.currentItemTree =''
        return None