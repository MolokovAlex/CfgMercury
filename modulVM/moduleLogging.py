
# moduleLogging
# autor: MolokovAlex
# coding: utf-8

# модуль логгирования

import logging
# import modulVM.config as cfg



def setup_logging(filename):
    # level=  DEBUG  INFO  WARNING  ERROR  CRITICAL
    # Create a custom logger
    # logger= logging.getLogger()
    logger.setLevel(logging.DEBUG) 
    consol_handler_logger = logging.StreamHandler()
    file_handler_logger = logging.FileHandler(filename, 'a', 'utf-8') 
    consol_handler_logger.setLevel(logging.INFO)
    # consol_handler_logger.setLevel(logging.WARNING)
    file_handler_logger.setLevel(logging.DEBUG)
    # file_handler_logger.setLevel(logging.INFO)
    f_format = logging.Formatter('%(name)s-%(levelname)s-%(asctime)s-%(message)s', datefmt='%d-%b-%y %H:%M:%S') 
    c_format = logging.Formatter('%(name)s-%(levelname)s-%(asctime)s-%(message)s', datefmt='%d-%b-%y %H:%M:%S')
    consol_handler_logger.setFormatter(c_format)
    file_handler_logger.setFormatter(f_format)
    logger.addHandler(consol_handler_logger)
    logger.addHandler(file_handler_logger)
    # logging.info('логирование включено')
    logger.debug('логирование включено')
    return None

logger= logging.getLogger()