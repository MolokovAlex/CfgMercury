#!/bin/python3
# autor: MolokovAlex
# lisence: 
# coding: utf-8

import sys
import os

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import *
# from time import sleep
import modulVM.moduleAppGUIQt as magqt
import modulVM.config as cfg
# import modulVM.moduleSQLite as msql
# import modulVM.moduleProtocolMercury as mpm
# import modulVM.moduleComThread as mct
import modulVM.moduleLogging as ml
# import modulVM.moduleGeneral as mg
# import modulVM.moduleParamSettingDataCounter as mpsdc



def main():
    # создаем графический оконный интерфейс
    # global window
    app = QApplication(sys.argv)
    # app = QApplication()
    app.setStyle('Windows')
    if True:     
        ml.logger.debug('создание главного окна')
        window = magqt.MainWindow()
        window.show()
        app.exec()
    return None

if __name__ == "__main__": 
    if not os.path.isdir(cfg.absLOG_DIR): 
        os.mkdir(cfg.absLOG_DIR)
    if not os.path.isdir(cfg.absDB_DIR): 
        os.mkdir(cfg.absDB_DIR)
    ml.setup_logging(cfg.absLOG_FILE)
    ml.logger.debug('---------------------------- запуск программы -------------------------------------')
    main()


    
              
    


