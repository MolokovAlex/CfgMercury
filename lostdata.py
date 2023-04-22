from PyQt5.QtCore import *
# from time import sleep
# from datetime import datetime
import datetime
from datetime import timedelta
# from datetime import timedelta
# import queue
import sqlite3 as sql3
import traceback
import sys
import os
import time

import modulVM.config as cfg
import modulVM.moduleLogging as ml
# import modulVM.moduleAppGUIQt as magqt
import modulVM.moduleProtocolMercury as mpm
# import modulVM.moduleGeneral as mg
# import modulVM.moduleSQLite as msql
import modulVM.moduleComThread as mct
import modulVM.mLostData as mld






if __name__ == "__main__": 
    if not os.path.isdir(cfg.absLOG_DIR): 
        os.mkdir(cfg.absLOG_DIR)
    if not os.path.isdir(cfg.absDB_DIR): 
        os.mkdir(cfg.absDB_DIR)
    ml.setup_logging(cfg.absLOG_FILE)
    # cfg.port_COM = 'COM9'
    # cfg.port_COM = 'COM3'
    # cfg.port_COM = '/dev/ttyUSB0'
    # cfg.MODE_CONNECT=2
    ml.logger.debug('---------------------------- запуск программы -------------------------------------')
    fdt = mld.FindLostDataThread(cfg.absDB_FILE)
    fdt.run()
    # cct.read_old_record_from_DBPP(77, 44, datetime.datetime.now())
    a=0