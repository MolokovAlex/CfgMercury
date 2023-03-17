#!/bin/python3
# module
# autor: MolokovAlex
# coding: utf-8

# модуль держатель класса основного окна

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import numpy as np
from time import sleep
# from PyQt5.QtSql import QSqlDatabase, QSqlQuery
import sqlite3 as sql3

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
import modulVM.moduleParamSettingDataCounter as mpsdc
import modulVM.moduleUpdate as mudp


# Подкласс QMainWindow для настройки главного окна приложения
class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        # super().__init__()
        super(MainWindow, self).__init__(parent)
        self.setWindowFlags(self.windowFlags()
            | Qt.WindowMinimizeButtonHint
            | Qt.WindowMaximizeButtonHint
            | Qt.WindowCloseButtonHint
            )

        self.setWindowTitle("Программа считывания данных со счетчиков Меркурий 230 ART версия "+ cfg.VERSION)

        # Получить размер разрешения монитора и распахнуть окно во весь монитор
        self.desktop = QApplication.desktop()
        self.screenRect = self.desktop.screenGeometry()
        self.height = self.screenRect.height()
        self.width = self.screenRect.width()
        self.resize(self.screenRect.width()-50, self.screenRect.height()-100)

        self.mdiArea = QMdiArea(self)
        self.setCentralWidget(self.mdiArea)

        self._createActions()
        self._createMenuBar()
        self._connectActions()
        self.createStatusBar()

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
            # sql3.viewCodeError (error_sql)

        # вызовем функцию Update программы
        mudp.createUpdate()

        #  создание  watchdog  сторожевого таймера для потока
        self.timer = QTimer()
        self.timer.timeout.connect(self.on_watchdog_timeout)

        # включение потока
        # if not self.thread:
        ml.logger.debug('старт потока')
        self.thread = mct.CommunicationCounterThread()
        self.thread.signal_progressRS.connect(self.onChangeProgressRS)
        self.thread.signal_error_open_connect_port.connect(self.openWindows_error_open_connect_port)
        self.thread.signal_error_connect_to_DB.connect(self.openWindows_error_connect_to_DB)
        self.thread.signal_watchdog_thread.connect(self.on_change_watchdog_timer)
        self.thread.finished.connect(self.on_finished_thread)
        self.thread.start()
        ml.logger.debug('включение watchdog')
        self.timer.start(cfg.time_watchdog_thread)

        # self.connect(self.thread, SIGNAL("mysignal(QString"), self.onChangeProgressRS, Qt.QueuedConnection)
        return None

    def open_window_wait(self):
        self.window2 = QWidget()
        self.window2.label = QLabel()
        self.window2.label.resize(600, 400)
        self.window2.label.move(100, 100)
        self.window2.label.setText("Пожалуйства, подождите")
        self.window2.label.show()
        return None

    def openWindows_error_connect_to_DB(self):
        """если порт не открылся - обработка сигнала в основную программу на вывод окна про ошибку
        """
        button = QMessageBox.critical(
                        self,
                        "Ошибка ввода-вывода",
                        "Ошибка доступа к БД",
                        buttons=QMessageBox.StandardButton.Ok ,
                        defaultButton=QMessageBox.StandardButton.Ok,)

        return None

    def openWindows_error_open_connect_port(self):
        """если порт не открылся - обработка сигнала в основную программу на вывод окна про ошибку
        """
        button = QMessageBox.critical(
                        self,
                        "Ошибка ввода-вывода",
                        "Ошибка открытия порта",
                        buttons=QMessageBox.StandardButton.Ok ,
                        defaultButton=QMessageBox.StandardButton.Ok,)

        return None
    
    
    def closeEvent(self, event):
        """
        закрытие основного главного окна программы
        """
        result = QMessageBox.question(self,
                "Подтверждение закрытия окна",
                "Вы действительно хотите закрыть окно?",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No)
        if result == QMessageBox.Yes:
            ml.logger.debug('закрытие главного окна')
            self.on_finished_thread()

            event.accept()
            # если открыта БД - закрыть
            if(cfg.sql_base_conn):
                cfg.sql_base_conn.close()
            QWidget.closeEvent(self, event)
        else:
            event.ignore()
    
    def on_watchdog_timeout(self):
        """
        функция обработки срабатывания watchdog сторожевого таймера
        """
        ml.logger.error('срабатывание watchdog потока')
        # остановим таймер
        self.timer.stop()

        # перезапустим поток опроса счетчиков
        # 1.закроем/финишируем поток 
        self.on_finished_thread()
        mpm.close_connection_to_port()
        # 2.заново запустим поток
        cfg.ON_TRANSFER_DATA_COUNTER = True
        ml.logger.debug('старт потока')
        self.thread = mct.CommunicationCounterThread()
        self.thread.signal_progressRS.connect(self.onChangeProgressRS)
        self.thread.signal_error_open_connect_port.connect(self.openWindows_error_open_connect_port)
        self.thread.signal_error_connect_to_DB.connect(self.openWindows_error_connect_to_DB)
        self.thread.signal_watchdog_thread.connect(self.on_change_watchdog_timer)
        self.thread.finished.connect(self.on_finished_thread)
        self.thread.start()
        # 3.и запустим таймер снова
        ml.logger.debug('включение watchdog')
        self.timer.start(cfg.time_watchdog_thread)

        return None

    def on_change_watchdog_timer(self):
        """
        Обработка прихода сигнала signal_watchdog_thread из потока опроса счетчиков
        приход сигнала означает что закончился 3-минутный цикл опроса счетчиков и поток жив
        """
        ml.logger.debug('приход из потока сигнала signal_watchdog_thread')
        # остановим таймер
        ml.logger.debug('остановка watchdog')
        self.timer.stop()
        # и запустим его снова
        ml.logger.debug('включение watchdog')
        self.timer.start(cfg.time_watchdog_thread)
        return None

    def onChangeProgressDB(self, value):
        self.progressDB.setValue(value)
        return None
            
    def onChangeProgressRS(self, s):
        progressrs485 = s
        if progressrs485 < 100:
                self.progressRS.setValue(progressrs485)
                self.progressRS.setFormat(f"Serial {progressrs485}%")
                
    def onChangeMessageStatusBar(self, strng):
        self.statusbar.showMessage(strng, msecs=6000)
        return None
                
    def on_finished_thread(self):
        ml.logger.debug('закрытие потока...')
        self.thread.signal_progressRS.disconnect(self.onChangeProgressRS)
        self.thread.finished.disconnect(self.on_finished_thread)
        self.thread = None
        ml.logger.debug('закрытие потока...ОК')

    def createStatusBar(self):
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage("Ready", msecs=3000)
        if (cfg.MODE_CONNECT == cfg.MODE_CONNECTION_IP_TO_SERVER):
            # self.lbl_protokolTCP = QLabel("TCP/IP="+cfg.host_IP+"/"+cfg.port_IP+"    ")
            self.lbl_protokolTCP = QLabel("")
            self.statusbar.addPermanentWidget(self.lbl_protokolTCP)
        
        self.lbl_protokolRS485 = QLabel("Serial=(9600 8N1)"+"    ")
        self.statusbar.addPermanentWidget(self.lbl_protokolRS485)
        # self.lbl_TxD = QLabel("TxD->")
        # self.lbl_TxD.setStyleSheet("background-color: yellow; border: 1px solid black;")
        # self.statusbar.addPermanentWidget(self.lbl_TxD)
        # lbl_empty = QLabel("TCP/IP")
        # self.statusbar.addPermanentWidget(lbl_empty)
        # self.lbl_RxD = QLabel("->RxD")
        # self.lbl_RxD.setStyleSheet("background-color: red; border: 1px solid black;")
        # self.statusbar.addPermanentWidget(self.lbl_RxD)
        self.progressRS = QProgressBar(self)
        # self.progress.setGeometry(0, 0, 300, 25)
        self.progressRS.setMaximum(100)
        self.progressRS.setFormat("Serial")
        # self.value_progress_DB = 5
        # self.progressRS.setValue(self.value_progress_DB)
        self.progressRS.setAlignment(Qt.AlignCenter)
        self.statusbar.addPermanentWidget(self.progressRS)
        # self.lbl_TxD_DB = QLabel("TxD->")
        # self.lbl_TxD_DB.setStyleSheet("background-color: red;")
        # self.statusbar.addPermanentWidget(self.lbl_TxD_DB)
        # lbl_empty2 = QLabel("DataBase")
        # self.statusbar.addPermanentWidget(lbl_empty2)
        # self.lbl_RxD_DB = QLabel("->RxD")
        # self.lbl_RxD_DB.setStyleSheet("background-color: green;")
        # self.statusbar.addPermanentWidget(self.lbl_RxD_DB)
        self.progressDB = QProgressBar(self)
        # self.progress.setGeometry(0, 0, 300, 25)
        self.progressDB.setMaximum(100)
        self.progressDB.setFormat("DataBase")
        self.progressDB.setValue(0)
        self.progressDB.setAlignment(Qt.AlignCenter)
        self.statusbar.addPermanentWidget(self.progressDB)
        

        return None

    

    def _connectActions(self):
        """# Connect Connection actions
        """
        # self.IPConnectionAction.triggered.connect(self.SetIPConnection)
        # self.RS485ConnectionAction.triggered.connect(self.SetRS485Connection)
        self.SettingsConnectionAction.triggered.connect(self.SetSettingsConnection)
        # self.FieldCountsAction.triggered.connect(self.RenderFieldCountsWindow)
        # self.openTableCountersAction.triggered.connect(self.openTableCountersWindow)
        self.openParamAndSettingDataCountersAction.triggered.connect(self.openParamAndSettingDataCounterWindow)
        self.EditGroupsCounterAction.triggered.connect(self.EditGroupsCounterWindow)
        # self.EditCounterAction.triggered.connect(self.EditCounterWindow)
        self.openTableProfilePowerAction.triggered.connect(self.TableProfilePowerWindow)
        self.openInstantlyParamCounterAction.triggered.connect(self.InstantlyParamCountersWindow)
        # Connect Help actions
        # self.helpContentAction.triggered.connect(self.helpContent)
        # self.aboutAction.triggered.connect(self.about)
        # Connect Demo actions
        # self.demoAction.triggered.connect(self.demo)

    def _createActions(self):
        # self.CreateConnAction = QAction("Create connection", self)
        # self.IPConnectionAction = QAction("Setting IP", self)
        # self.RS485ConnectionAction = QAction("Setting net RS485", self)
        self.SettingsConnectionAction = QAction("Настройки соединения", self)
        # self.FieldCountsAction =  QAction("Field counts", self)
        # self.openTableCountersAction =  QAction("Таблица", self)
        self.openParamAndSettingDataCountersAction = QAction("Параметры и установки", self)
        self.EditGroupsCounterAction =  QAction("Редактирование Групп, Счетчиков", self)
        # self.EditCounterAction =  QAction("Редактирование Счетчиков", self)

        self.openTableProfilePowerAction =  QAction("Профиль мощности", self)
        openTableProfilePowerTip = "Таблица профиля мощности"
        self.openTableProfilePowerAction.setStatusTip(openTableProfilePowerTip)
        self.openTableProfilePowerAction.setToolTip(openTableProfilePowerTip)

        self.openInstantlyParamCounterAction =  QAction("Мгновенные значения", self)
        openInstantlyParamCounterTip = "Мгновенные значения"
        self.openInstantlyParamCounterAction.setStatusTip(openInstantlyParamCounterTip)
        self.openInstantlyParamCounterAction.setToolTip(openInstantlyParamCounterTip)

        # self.helpContentAction = QAction("Help Content", self)
        # self.aboutAction = QAction("About", self)
        # self.demotAction = QAction("Demo", self)


    def _createMenuBar(self):

        menuBar = QMenuBar(self)
        self.setMenuBar(menuBar)
        menuBar = self.menuBar()

        connectMenu = menuBar.addMenu("Настройки")
        menuBar.addMenu(connectMenu)
        connectMenu.addAction(self.SettingsConnectionAction)

        countsMenu = menuBar.addMenu("Счетчики")
        menuBar.addMenu(countsMenu)
        # countsMenu.addAction(self.openTableCountersAction)   
        countsMenu.addAction(self.openParamAndSettingDataCountersAction)
        countsMenu.addAction(self.EditGroupsCounterAction)
        # countsMenu.addAction(self.EditCounterAction)
        
        profilePowerMenu = menuBar.addMenu("Профиль мощности")
        menuBar.addMenu(profilePowerMenu)
        profilePowerMenu.addAction(self.openTableProfilePowerAction)   
        # ProfilePowerMenu.addAction(self.EditGroupsCounterAction)

        instantlyParamMenu = menuBar.addMenu("Мгновенные значения")
        menuBar.addMenu(instantlyParamMenu)
        instantlyParamMenu.addAction(self.openInstantlyParamCounterAction)

        return None


    def onMyToolBarButtonClick(self, s):
        print("click", s) 

    def SetSettingsConnection(self)-> None:
        """
        открытие окна ввода настроек соединения
        """
        self.windowSetSettingsConnection = mca.SetSettingsConnectionDialog()
        # self.windowSetSettingsConnection.signal_error_open_connect_port.connect(self.magqt.click_ckb_on_transfer_data_from_counter)
        self.windowSetSettingsConnection.exec()

        return None
    
    def openParamAndSettingDataCounterWindow(self):
        """
        открытие окна Параметры и настройки счетчика
        """
        ml.logger.debug('открытие окна Параметры и настройки счетчика')
        windowInfoDataCounters=mpsdc.ParamAndSettingDataCountersDialog()
        self.mdiArea.addSubWindow(windowInfoDataCounters)
        windowInfoDataCounters.show()
        return None
       
    def EditGroupsCounterWindow(self):
        """
        открытие окна редактирования счетчиков и групп
        """
        ml.logger.debug('открытие окна редактирования счетчиков и групп')
        windowEditGroupsCounter=megc.EditGroupsCounterDialog()
        self.mdiArea.addSubWindow(windowEditGroupsCounter)
        windowEditGroupsCounter.show()
        return None


    def InstantlyParamCountersWindow(self):
        """
        открытие окна просмотра мгновенных значений
        """
        ml.logger.debug('открытие окна просмотра мгновенных значений')
        WindowInstantlyParamCounters = mgi.InstantlyParamCountersDialog()
        self.mdiArea.addSubWindow(WindowInstantlyParamCounters)
        WindowInstantlyParamCounters.inc_progressDB.connect(self.onChangeProgressDB)
        WindowInstantlyParamCounters.send_message_statusBar.connect(self.onChangeMessageStatusBar)
        WindowInstantlyParamCounters.show()
        return None 

    def TableProfilePowerWindow(self):
        """
        открытие окна вывода таблицы профиля мощности
        """     
        ml.logger.debug(' открытие окна вывода таблицы профиля мощности')
        WindowTableProfilePower = mgpp.TableProfilePowerDialog()
        self.mdiArea.addSubWindow(WindowTableProfilePower)
        WindowTableProfilePower.inc_progressDB.connect(self.onChangeProgressDB)
        WindowTableProfilePower.send_message_statusBar.connect(self.onChangeMessageStatusBar)
        WindowTableProfilePower.show()
        return None 

    def helpContent(self):
        # Logic for launching help goes here...
        self.centralWidget.setText("<b>Help > Help Content...</b> clicked")

    def about(self):
        # Logic for showing an about dialog content goes here...
        self.centralWidget.setText("<b>Help > About...</b> clicked")  



    





    