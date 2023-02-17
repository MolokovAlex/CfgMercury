# moduleConfigApp
# autor: MolokovAlex
# coding: utf-8

# модуль окна Настройки и параметры программы

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import modulVM.config as cfg
import modulVM.moduleLogging as ml
import modulVM.moduleGeneral as mg
# import modulVM.moduleAppGUIQt as magqt

class SetSettingsConnectionDialog(QDialog):
    """
    класс окна Настройки и параметры программы
    """
    def __init__(self):
        super().__init__()

        self.setMinimumSize(QSize(400, 600))         # Устанавливаем размеры
        self.setWindowTitle("Настройки соединения") # Устанавливаем заголовок окна
        ml.logger.debug("Открытие окна Настройки соединения")
        layout = QGridLayout()
        self.setLayout(layout)

        self.gb_IPtoServer = QGroupBox("Связь по TCP/IP, подключение к серверу")
        self.gb_IPtoServer.setCheckable(True)
        # self.gb_IPtoServer.setChecked(cfg.modeIPtoServer)
        self.gb_IPtoServer.clicked.connect(self.clickGroupBoxIPtoServer)
        layout.addWidget(self.gb_IPtoServer, 0, 0,1, 2)
        vbox_IPServer = QVBoxLayout()
        self.gb_IPtoServer.setLayout(vbox_IPServer)
        vbox_IPServer.addWidget(QLabel("IP-адрес", self))#, 0, 0)
        ipRange = "(?:[0-1]?[0-9]?[0-9]|2[0-4][0-9]|25[0-5])"   # Часть регулярного выржение
        # Само регулярное выражение
        ipRegex = QRegExp("^" + ipRange + "\\." + ipRange + "\\." + ipRange + "\\." + ipRange + "$")
        ipValidator = QRegExpValidator(ipRegex, self)   # Валидатор для QLineEdit
        self.le_ipAdress = QLineEdit()
        self.le_ipAdress.setValidator(ipValidator)      # Устанавливаем валидатор
        vbox_IPServer.addWidget(self.le_ipAdress)
        self.le_ipAdress.setText(cfg.host_IP)
        # self.le_ipAdress.adjustSize()
        vbox_IPServer.addWidget(QLabel("Порт", self))#, 0, 0)
        netPortRegex = QRegExp("\d{1,5}$")
        portValidator = QRegExpValidator(netPortRegex, self)   # Валидатор для QLineEdit
        self.le_netPort = QLineEdit()
        self.le_netPort.setValidator(portValidator)      # Устанавливаем валидатор
        vbox_IPServer.addWidget(self.le_netPort)
        self.le_netPort.setText(cfg.port_IP)

        self.gb_IPtoClient = QGroupBox("Связь по TCP/IP, подключение к клиенту")
        self.gb_IPtoClient.setCheckable(True)
        # self.gb_IPtoClient.setChecked(cfg.modeIPtoClient)
        self.gb_IPtoClient.clicked.connect(self.clickGroupBoxIPtoClient)
        layout.addWidget(self.gb_IPtoClient, 1,0,1,2)
        vbox_IPClient = QVBoxLayout()
        self.gb_IPtoClient.setLayout(vbox_IPClient)
        vbox_IPClient.addWidget(QLabel("Порт", self))#, 0, 0)
        netPortRegex = QRegExp("\d{1,5}$")
        portValidator = QRegExpValidator(netPortRegex, self)   # Валидатор для QLineEdit
        self.le_clientPort = QLineEdit()
        self.le_clientPort.setValidator(portValidator)  
        vbox_IPClient.addWidget(self.le_clientPort)
        self.le_clientPort.setText(cfg.port_IP)


        self.gb_ConnectionCOM = QGroupBox("Связь по последовательному порту")
        self.gb_ConnectionCOM.setCheckable(True)
        # self.gb_ConnectionCOM.setChecked(cfg.modeConnectionCOM)
        self.gb_ConnectionCOM.clicked.connect(self.clickGroupBoxCCOM)
        layout.addWidget(self.gb_ConnectionCOM, 2,0,1,2)
        vbox_CCOM = QVBoxLayout()
        self.gb_ConnectionCOM.setLayout(vbox_CCOM)
        vbox_CCOM.addWidget(QLabel("Порт", self))#,0,0)
        self.cb_case_com_port = QComboBox()
        lsp = mg.list_of_serial_ports()
        self.cb_case_com_port.addItems(lsp)
        vbox_CCOM.addWidget(self.cb_case_com_port)
        # cb_case_com_port.addItems(["9600", "115200"])
        vbox_CCOM.addWidget(QLabel("Скорость по RS485", self))#,0,0)
        cb_BaudrateRS485 = QComboBox()
        cb_BaudrateRS485.addItems(["9600", "115200"])
        # cb_BaudrateRS485.currentIndexChanged.connect( self.changeBaudrateRS485 )
        # pagelayout.addWidget(cb_BaudrateRS485)#,1,0)
        vbox_CCOM.addWidget(cb_BaudrateRS485)#,1,0)
        # pagelayout.addWidget(QLabel("Четность", self))#,2,0)
        vbox_CCOM.addWidget(QLabel("Четность", self))#,2,0)
        cb_parity = QComboBox()
        cb_parity.addItems(["8N1", "7N1", "8O1"])
        # cb_parity.currentIndexChanged.connect( self.changeParityRS485 )
        # pagelayout.addWidget(cb_parity)#,3,0)
        vbox_CCOM.addWidget(cb_parity)#,3,0)
        
        # gb_config_mode_canal = QGroupBox("Режимы работы канала связи")
        # layout.addWidget(gb_config_mode_canal,3,0,1,2)
        # vbox_CM = QVBoxLayout()
        # gb_config_mode_canal.setLayout(vbox_CM)
        # ckb_on_mode_echo = QCheckBox("Режим ЭХО")
        # vbox_CM.addWidget(ckb_on_mode_echo)
        
        # gb_AcsessCounters = QGroupBox("Доступ к счетчикам")
        # layout.addWidget(gb_AcsessCounters,4,0,1,2)
        # vbox_AC = QVBoxLayout()
        # gb_AcsessCounters.setLayout(vbox_AC)
        # rb_levelAcsess1 = QRadioButton("Уровнь доступа 1")
        # rb_levelAcsess1.setChecked(True)
        # # rb_levelAcsess.toggled.connect(self.onClicked)
        # # pagelayout.addWidget(rb_levelAcsess1)#, 0, 0)
        # vbox_AC.addWidget(rb_levelAcsess1)#, 0, 0)
        # rb_levelAcsess2 = QRadioButton("Уровнь доступа 2")
        # rb_levelAcsess2.setChecked(False)
        # # rb_levelAcsess.toggled.connect(self.onClicked)
        # # pagelayout.addWidget(rb_levelAcsess2)#, 0, 0)
        # vbox_AC.addWidget(rb_levelAcsess2)#, 0, 0)
        # vbox_AC.addWidget(QLabel("Пароль доступа к счетчикам", self))#, 0, 0)
        # le_countPassword = QLineEdit()
        # vbox_AC.addWidget(le_countPassword )
        
        gb_transfer_data_counters = QGroupBox("Опрос счетчиков")
        layout.addWidget(gb_transfer_data_counters,5,0,1,2)
        vbox_TD = QVBoxLayout()
        gb_transfer_data_counters.setLayout(vbox_TD)
        self.ckb_on_transfer_data_from_counter = QCheckBox("Включить опрос счетчиков")
        # self.ckb_on_transfer_data_from_counter.clicked.connect(self.click_ckb_on_transfer_data_from_counter)
        self.ckb_on_transfer_data_from_counter.setTristate(False)
        self.ckb_on_transfer_data_from_counter.setCheckState(cfg.ON_TRANSFER_DATA_COUNTER)
        vbox_TD.addWidget(self.ckb_on_transfer_data_from_counter)

        btn_OKSettings = QPushButton("Да")
        layout.addWidget(btn_OKSettings, 6, 0)
        btn_OKSettings.clicked.connect(self.acceptBtnDialogSettingsGroup)
        btn_CancelSettings = QPushButton("Отмена")
        layout.addWidget(btn_CancelSettings, 6, 1)
        btn_CancelSettings.clicked.connect(self.rejectBtnDialogSettingsGroup)

        

        # включием/выключим GroupBox-ы в зависимости от режима работы прописанного в cfg.modeConnection
        self.setVisibleGroupBox(mode=cfg.MODE_CONNECT)         
        return None
    
    def acceptBtnDialogSettingsGroup(self):
        """ Обработка нажатия на кнопку ОК
        """
        mode = cfg.MODE_CONNECT
        if mode == cfg.MODE_CONNECTION_IP_TO_SERVER:
            if (self.le_netPort.text()!= '') and (self.le_ipAdress.text()!= ''):
                cfg.host_IP = self.le_ipAdress.text()
                cfg.port_IP = self.le_netPort.text()
                # magqt.window.lbl_protokolTCP = QLabel("TCP/IP="+cfg.host_IP+"/"+cfg.port_IP+"    ")
                self.closeWindow()
            else:
                button = QMessageBox.critical(
                        self,
                        "Ошибка ввода",
                        "Недостаточно параметров или неверные параметры",
                        buttons=QMessageBox.StandardButton.Ok ,
                        defaultButton=QMessageBox.StandardButton.Ok,)
        elif mode == cfg.MODE_CONNECTION_IP_TO_CLIENT:
            if self.le_clientPort.text()!= '':
                cfg.port_IP = self.le_netPort.text()
                self.closeWindow()
            else:
                button = QMessageBox.critical(
                        self,
                        "Ошибка ввода",
                        "Недостаточно параметров или неверные параметры",
                        buttons=QMessageBox.StandardButton.Ok ,
                        defaultButton=QMessageBox.StandardButton.Ok,)
        elif mode == cfg.MODE_CONNECTION_COM:
            if self.cb_case_com_port.currentText() != '':
                cfg.port_COM = self.cb_case_com_port.currentText()
                self.closeWindow()
            else:
                button = QMessageBox.critical(
                        self,
                        "Ошибка ввода",
                        "Недостаточно параметров или неверные параметры",
                        buttons=QMessageBox.StandardButton.Ok ,
                        defaultButton=QMessageBox.StandardButton.Ok,)
        
        ml.logger.debug("Закрытие окна Настройки соединения со следующими значениями:")
        ml.logger.debug(f"cfg.modeConnection={cfg.MODE_CONNECT}")
        ml.logger.debug(f"cfg.host_IP={cfg.host_IP}")
        ml.logger.debug(f"cfg.port_IP={cfg.port_IP}")
        ml.logger.debug(f"cfg.port_COM={cfg.port_COM}")
        ml.logger.debug(f"cfg.baudrateRS485={cfg.baudrateRS485}")
        ml.logger.debug(f"cfg.parityRS485={cfg.parityRS485}")
        ml.logger.debug(f"cfg.ON_TRANSFER_DATA_COUNTER={cfg.ON_TRANSFER_DATA_COUNTER}")       
        return None
    
    def rejectBtnDialogSettingsGroup(self):
        """ Обработка нажатия на кнопку Cansel
        """
        self.hide()
        return None

    def closeWindow(self):
        """ закрытие окна
        """
        cfg.ON_TRANSFER_DATA_COUNTER = self.ckb_on_transfer_data_from_counter.isChecked()
        self.hide()
        return None


    # def changeParityRS485(self, text):
    #     cfg.parityRS485 = text
    #     return None

    # def changeBaudrateRS485(self, text):
    #     cfg.baudrateRS485 = text
    #     return None
    
    def onChanged_le_netPort(self, text):
        cfg.port_IP = self.le_netPort.text()
        return None

    def setVisibleGroupBox(self,mode):
        if mode == cfg.MODE_CONNECTION_IP_TO_SERVER:
            self.gb_IPtoServer.setChecked(True)
            self.gb_ConnectionCOM.setChecked(False)
            self.gb_IPtoClient.setChecked(False)
        elif mode == cfg.MODE_CONNECTION_IP_TO_CLIENT:
            self.gb_IPtoServer.setChecked(False)
            self.gb_ConnectionCOM.setChecked(False)
            self.gb_IPtoClient.setChecked(True)
        elif mode == cfg.MODE_CONNECTION_COM:
            self.gb_IPtoServer.setChecked(False)
            self.gb_ConnectionCOM.setChecked(True)
            self.gb_IPtoClient.setChecked(False)
        return None

    def clickGroupBoxIPtoServer(self):
        cfg.MODE_CONNECT = cfg.MODE_CONNECTION_IP_TO_SERVER
        self.setVisibleGroupBox(mode=cfg.MODE_CONNECT)        
        return None

    def clickGroupBoxIPtoClient(self):
        cfg.MODE_CONNECT = cfg.MODE_CONNECTION_IP_TO_CLIENT
        self.setVisibleGroupBox(mode=cfg.MODE_CONNECT) 
        return None

    def clickGroupBoxCCOM(self):
        cfg.MODE_CONNECT = cfg.MODE_CONNECTION_COM
        self.setVisibleGroupBox(mode=cfg.MODE_CONNECT) 
        return None
    
    # def click_ckb_on_transfer_data_from_counter(self):
    #     cfg.ON_TRANSFER_DATA_COUNTER = self.ckb_on_transfer_data_from_counter.isChecked()
    #     ml.logger.debug(f"установка галочки Вкл/выкл опроса счетчиков: {cfg.ON_TRANSFER_DATA_COUNTER}")
    #     return None

    
    