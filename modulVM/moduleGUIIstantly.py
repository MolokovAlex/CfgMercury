# moduleConfigApp
# autor: MolokovAlex
# coding: utf-8

# модуль окна мгновенные значения


from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import pyqtgraph as pg
import numpy as np
from random import randint
import datetime 
from datetime import timedelta
from datetime import datetime

import modulVM.config as cfg
import modulVM.moduleSQLite as msql
import modulVM.moduleGeneral as mg
# import modulVM.moduleAppGUIQt as magqt


class InstantlyParamCountersDialog(QDialog):
    inc_progressDB = pyqtSignal(int)
    send_message_statusBar = pyqtSignal(str)
    def __init__(self, parent=None):
        # super().__init__()
        super(InstantlyParamCountersDialog, self).__init__(parent)
        self.setWindowFlags(self.windowFlags()
            | Qt.WindowMinimizeButtonHint
            | Qt.WindowMaximizeButtonHint
            )
        self.setMinimumSize(QSize(800, 600))         # Устанавливаем размеры
        self.setWindowTitle("Мгновенные параметры") # Устанавливаем заголовок окна
        layout = QGridLayout()
        
        self.lst_checkItemTree=[]
        
        lbl_empty1 = QLabel("Счетчик:")
        self.cb_InstCounter = QComboBox()
        list_CounterDB, rezult_getListOfCounterDB = msql.getListCounterDB()
        for item in list_CounterDB:
            self.cb_InstCounter.addItem(item['name_counter_full'])
        self.cb_InstCounter.setMaxVisibleItems(10)
        self.cb_InstCounter.view().setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.cb_InstCounter.currentIndexChanged.connect(self.onSelectedCount)
        self.selectedCount = self.cb_InstCounter.currentText()
        lbl_empty1.setAlignment(Qt.AlignRight)
        self.de_dateFrom = QDateEdit(self)
        self.de_dateFrom.setCalendarPopup(True) 
        self.de_dateFrom.setDate(QDate(2022, 12, 25))

        lbl_empty3 = QLabel("    ")
        self.btnRefreshGraph = QPushButton("Обновить")
        self.btnRefreshGraph.setEnabled(False)
        # ckb_cycleRefreshTableCounters = QCheckBox("циклически")
        self.tree = QTreeWidget()
        self.tree.clicked.connect(self.click_in_tree)

        layout.addWidget(lbl_empty1, 0, 0)
        layout.addWidget(self.cb_InstCounter, 0, 1)
        layout.addWidget(self.de_dateFrom, 0, 2)

        layout.addWidget(lbl_empty3, 0, 3)
        layout.addWidget(self.btnRefreshGraph, 0, 4)
        # layout.addWidget(ckb_cycleRefreshTableCounters, 0, 5)
        layout.addWidget(self.tree,1,0)
        
        # self.cb_InstParam.activated.connect(self.click_cb_InstParam)
        self.btnRefreshGraph.clicked.connect(self.click_btnRefreshGraph)
        self.renderTreePanel_IC()
       
        date_axis = TimeAxisItem(orientation='bottom')
        # date_axis.attachToPlotItem(self.graphWidget.getPlotItem())
        self.graphWidget = pg.PlotWidget(axisItems = {'bottom': date_axis})
        
        self.graphWidget.setBackground('w')
        self.graphWidget.showGrid(x=True, y=True, alpha = 1.0)
        # self.graphWidget.setXRange(0, 10, padding=0)
        self.graphWidget.setYRange(20, 55, padding=0)
        styles = {'color':'r', 'font-size':'12px'}
        self.graphWidget.setLabel('left', 'Величина', **styles)
        self.graphWidget.setLabel('bottom', 'Время', **styles)
        layout.addWidget(self.graphWidget,  1, 1, 1, 5)        
        
        layout.setColumnStretch(0, 0)
        layout.setColumnStretch(1, 2)
        layout.setColumnStretch(2, 2)
        layout.setColumnStretch(3, 2)
        layout.setColumnStretch(4, 2)
        layout.setColumnStretch(5, 2)
        self.setLayout(layout)
        self.curve = []
        self.setTitleGraph()
        self.emit_string_statusBar("Выберите счетчик и мгновенный параметр")
        return None

    def emit_string_statusBar(self, strg):
        self.send_message_statusBar.emit(strg)
        return None

    def emit_value(self, value):
        self.inc_progressDB.emit(value)
        return None

    def renderTreePanel_IC(self):
        """Создание дерева мгновенных параметров с чеками выбора
        """      
        self.tree.clear()
        for item_inst_group in cfg.dic_inst_param.keys():
            parent = QTreeWidgetItem(self.tree)
            parent.setText(0, item_inst_group)
            parent.setFlags(parent.flags() | Qt.ItemIsUserCheckable)
            parent.setCheckState(0, Qt.Unchecked)
            for item_inst_param in cfg.dic_inst_param[item_inst_group]:
                child = QTreeWidgetItem(parent)
                child.setText(0, item_inst_param)
                child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
                child.setCheckState(0, Qt.Unchecked)
                   
        self.tree.setColumnWidth(0, 30)
        self.tree.expandAll()
        # self.currentItemTree =''
        return None
    
    def click_in_tree(self):
        """
        обработка кликов в дереве мгновенных параметров
        если хотябы одна галочка стоит - кнопку Обновить активируем
        
        """
        # посмотрим, где пользователь поставиль галочки в дереве
        checked_param = False
        iterator = QTreeWidgetItemIterator(self.tree, QTreeWidgetItemIterator.Checked)
        while iterator.value():
            item = iterator.value()
            if item.text(0) :
                    checked_param = True
            iterator += 1
        # если какой то выбор сделан - разблокированить кнопку Обновить
        if checked_param:
            self.btnRefreshGraph.setEnabled(True)
        else:
            # если пользователь снял все галочки
            self.btnRefreshGraph.setEnabled(False)
        return
    

    def setTitleGraph(self):
        """Вывод названия графика
        """
        self.graphWidget.setTitle(self.cb_InstCounter.currentText(), color="b", size="14pt")
        return None
        
    
    def onSelectedCount(self, idx):
        """Выбор  comboBox  - выбор счетчика
        """
        self.selectedCount = self.cb_InstCounter.currentText()
        self.setTitleGraph()
        return None
    # def click_cb_InstParam(self):
    #     # self.graphWidget.setTitle(self.cb_InstParam.currentText()+" -- "+self.cb_InstCounter.currentText(), color="b", size="14pt")
    #     self.setTitleGraph()
    #     return None
        
    def click_btnRefreshGraph(self):
        """Обработка нажатия на кнопку "Обновить"

        """
        self.btnRefreshGraph.setEnabled(False)

        self.create_lst_checked_inst_param()
        self.emit_string_statusBar("Пожалуйста, подождите. Идут запросы в БД...")
        self.emit_value(5)

        # создает список с штампами времени типа datetime от даты dateFrom до даты dateTo с шагом
        dateFrom = self.de_dateFrom.dateTime().toPyDateTime()
        dateTo = self.de_dateFrom.dateTime().toPyDateTime() + timedelta(hours=23) + timedelta(minutes=30)
        self.emit_value(10)

        self.emit_value(20)

        # найдем id_counter того счетчика который был выбран в ComboBox и ...
        list_CounterDB, rezult_getListOfCounterDB = msql.getListCounterDB()
        if rezult_getListOfCounterDB:
            for item_counter in list_CounterDB:
                if item_counter['name_counter_full'] == self.cb_InstCounter.currentText():
                    id_counter = item_counter['id']
                    break            
            self.emit_value(25)
        #     value_progressDB = 25
        #     self.emit_value(int(value_progressDB))
            #
            rezult, dataDBIC = msql.selectItemFromDBIC_all_param_v2(id_counter, dateFrom=dateFrom, dateTo=dateTo)
            if rezult:
                arr_Table = np.array(dataDBIC)
                #
                # выделим ось времени и сделаем ее сосотоящую из тайм-штампов
                # x = arr_Table[:,0]
                arr_x = np.full(shape=np.shape(arr_Table[:,0]),fill_value=0.0)
                for item_time in range (0,np.shape(arr_Table)[0],1):
                        ts = datetime.strptime(arr_Table[item_time,0],"%Y-%m-%d %H:%M:%S")
                        arr_x[item_time] = ts.timestamp()
                # а из основног массива удалим столбец времен
                arr_Table = np.delete(arr_Table, 0 , axis = 1)
                #  преобразуем матрицу из str в float
                arr_Table= np.array(arr_Table, dtype=float)
                self.emit_value(35)
                # применим коэффициенты к разным мгн значениям
                # по всем временным меткам
                for num_arrTable, val_arrTable in enumerate(arr_Table):
                    # мгновенные токи - коэф 1000
                    arr_Table[num_arrTable][0] = val_arrTable[0]/1000
                    arr_Table[num_arrTable][1] = val_arrTable[1]/1000
                    arr_Table[num_arrTable][2] = val_arrTable[2]/1000
                    arr_Table[num_arrTable][3] = val_arrTable[3]/1000
                    # мгн мощности - коэфф 100
                    arr_Table[num_arrTable][4] = val_arrTable[4]/100
                    arr_Table[num_arrTable][5] = val_arrTable[5]/100
                    arr_Table[num_arrTable][6] = val_arrTable[6]/100
                    arr_Table[num_arrTable][7] = val_arrTable[7]/100

                    arr_Table[num_arrTable][8] = val_arrTable[8]/100
                    arr_Table[num_arrTable][9] = val_arrTable[9]/100
                    arr_Table[num_arrTable][10] = val_arrTable[10]/100
                    arr_Table[num_arrTable][11] = val_arrTable[11]/100

                    arr_Table[num_arrTable][12] = val_arrTable[12]/100
                    arr_Table[num_arrTable][13] = val_arrTable[13]/100
                    arr_Table[num_arrTable][14] = val_arrTable[14]/100
                    arr_Table[num_arrTable][15] = val_arrTable[15]/100
                    # KPowerFaze - коэф 1000
                    arr_Table[num_arrTable][16] = val_arrTable[16]/100
                    arr_Table[num_arrTable][17] = val_arrTable[17]/100
                    arr_Table[num_arrTable][18] = val_arrTable[18]/100
                    arr_Table[num_arrTable][19] = val_arrTable[19]/100

                self.emit_value(45)
                # создание списка столбцов на удаление в зависимости от выбранных параметров в cfg.dic_inst_param
                lst_todelete_column = []
                for i in range (0,np.shape(arr_Table)[1],1):
                    lst_todelete_column.append(i)
                # нулевое поле удалять нельзя - там datetime
                # lst_todelete_column.remove(0)
                if cfg.dic_inst_param["Ток"][0] in self.lst_checkItemTree:
                            lst_todelete_column.remove(0)                        
                if cfg.dic_inst_param["Ток"][1] in self.lst_checkItemTree:
                                lst_todelete_column.remove(1)
                if cfg.dic_inst_param["Ток"][2] in self.lst_checkItemTree:
                                lst_todelete_column.remove(2)
                if cfg.dic_inst_param["Ток"][3] in self.lst_checkItemTree:
                                lst_todelete_column.remove(3)
                if cfg.dic_inst_param["Мощность P"][0] in self.lst_checkItemTree:
                                lst_todelete_column.remove(4)
                if cfg.dic_inst_param["Мощность P"][1] in self.lst_checkItemTree:
                                lst_todelete_column.remove(5)
                if cfg.dic_inst_param["Мощность P"][2] in self.lst_checkItemTree:
                                lst_todelete_column.remove(6)
                if cfg.dic_inst_param["Мощность P"][3] in self.lst_checkItemTree:
                                lst_todelete_column.remove(7)
                if cfg.dic_inst_param["Мощность Q"][0] in self.lst_checkItemTree:
                                lst_todelete_column.remove(8)
                if cfg.dic_inst_param["Мощность Q"][1] in self.lst_checkItemTree:
                                lst_todelete_column.remove(9)
                if cfg.dic_inst_param["Мощность Q"][2] in self.lst_checkItemTree:
                                lst_todelete_column.remove(10)
                if cfg.dic_inst_param["Мощность Q"][3] in self.lst_checkItemTree:
                                lst_todelete_column.remove(11)
                if cfg.dic_inst_param["Мощность S"][0] in self.lst_checkItemTree:
                                lst_todelete_column.remove(12)
                if cfg.dic_inst_param["Мощность S"][1] in self.lst_checkItemTree:
                                lst_todelete_column.remove(13)
                if cfg.dic_inst_param["Мощность S"][2] in self.lst_checkItemTree:
                                lst_todelete_column.remove(14)
                if cfg.dic_inst_param["Мощность S"][3] in self.lst_checkItemTree:
                                lst_todelete_column.remove(15)
                if cfg.dic_inst_param["Коэффициента мощности"][0] in self.lst_checkItemTree:
                                lst_todelete_column.remove(16)
                if cfg.dic_inst_param["Коэффициента мощности"][1] in self.lst_checkItemTree:
                                lst_todelete_column.remove(17)
                if cfg.dic_inst_param["Коэффициента мощности"][2] in self.lst_checkItemTree:
                                lst_todelete_column.remove(18)
                if cfg.dic_inst_param["Коэффициента мощности"][3] in self.lst_checkItemTree:
                                lst_todelete_column.remove(19)
                if cfg.dic_inst_param["Мощность по тарифам"][0] in self.lst_checkItemTree:
                                lst_todelete_column.remove(21)
                if cfg.dic_inst_param["Мощность по тарифам"][1] in self.lst_checkItemTree:
                                lst_todelete_column.remove(22)
                if cfg.dic_inst_param["Мощность по тарифам"][2] in self.lst_checkItemTree:
                                lst_todelete_column.remove(23)
                if cfg.dic_inst_param["Мощность по тарифам"][3] in self.lst_checkItemTree:
                                lst_todelete_column.remove(24)
                arr_Table = np.delete(arr_Table, lst_todelete_column , axis = 1)
    
                #
                    
                self.emit_value(55)
                self.curve.clear()
                self.graphWidget.clear()
                self.graphWidget.addLegend()
                #  создание линий графиков и подкоючение данных
                for numberLineGraph, item_name_in_tree in enumerate(self.lst_checkItemTree):
                    pen1 = pg.mkPen(color=(cfg.lst_color_pen_graph[numberLineGraph]), width=2, style=Qt.SolidLine)
                    # self.curve.append(self.graphWidget.plot(name=item_name_in_tree, pen=pen1, symbol='o', symbolSize=10, symbolBrush=('r'), stepMode='right'))
                    self.curve.append(self.graphWidget.plot(name=item_name_in_tree, pen=pen1, stepMode='right'))
                    # self.curve[numberLineGraph].setData(x=lst_DataX , y=lst_DataY[numberLineGraph]) 
                    
                    arr_y= arr_Table[:,numberLineGraph]
                    #  преобразуем матрицу из str в float
                    # arr_y= np.array(arr_y, dtype=float)
                    self.curve[numberLineGraph].setData(x=arr_x , y=arr_y)
                    self.emit_value(55+2*numberLineGraph)
                self.graphWidget.enableAutoRange('xy', True)
        self.emit_value(0)
        self.emit_string_statusBar("Готово.")
        self.btnRefreshGraph.setEnabled(True)
        return None

    def create_lst_checked_inst_param(self):
        """
        создание списка выбранных пунктов в дереве мгновенных параметров
        каждый клик - формируется списко выбранных элементов заново и пееррисовывается график
        """
        # составим список элементов, где пользователь поставиль галочки в дереве
        self.lst_checkItemTree=[]
        iterator = QTreeWidgetItemIterator(self.tree, QTreeWidgetItemIterator.Checked)
        while iterator.value():
            item = iterator.value()
            # a =item.text(0)
            self.lst_checkItemTree.append(item.text(0))
            iterator += 1
        # если какой то выбор сделан - разблокированить кнопку Обновить
        if self.lst_checkItemTree:
            self.btnRefreshGraph.setEnabled(True)
        else:
            # если пользователь снял все галочки
            self.btnRefreshGraph.setEnabled(False)
        # создаем список выбранных пользователем групп и список выбранных счетчиков - все по отдельности
        # cfg.lst_checked_group, cfg.lst_checked_counter = mg.createLstCheckedCounterAndGroups(self.lst_checkItemTree) 
        # a=self.lst_checkItemTree
        return None


        
       
        
    #------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------    
    

class TimeAxisItem(pg.AxisItem):
    def __init__(self, *args, **kwargs):
        pg.AxisItem.__init__(self, *args, **kwargs)
        self._oldAxis = None
        
    # def attachToPlotItem(self, plotItem):
    #     """Add this axis to the given PlotItem
    #     :param plotItem: (PlotItem)
    #     """
    #     self.setParentItem(plotItem)
    #     viewBox = plotItem.getViewBox()
    #     self.linkToView(viewBox)
    #     self._oldAxis = plotItem.axes[self.orientation]['item']
    #     self._oldAxis.hide()
    #     plotItem.axes[self.orientation]['item'] = self
    #     pos = plotItem.axes[self.orientation]['pos']
    #     plotItem.layout.addItem(self, *pos)
    #     self.setZValue(-1000)    
        
    def tickStrings(self, values, scale, spacing):
        return [datetime.fromtimestamp(value).strftime("%m/%d/%y %H:%M") for value in values]


