

# autor: MolokovAlex
# lisence: GPL
# coding: utf-8

import struct
import socket
import serial
import datetime


import modulVM.config as cfg
# import modulVM.moduleAppGUIQt as magqt
# import modulVM.moduleProtocolMercury as mpm
# import modulVM.moduleSQLite as msql
import modulVM.moduleLogging as ml


# codeNetAdress = 0x32
# параметры проверки канала связи = Adress+codeRequest+CRC
codeRequest_testConnectionCannal = 0x00
codeRecieve_goodTestConnectionCannal = 0x00
# запрос на 77 номер
aa=b"x4d\x00\x34\xe0"


# параметры открытие и закрытие канала связи = Adress+codeRequest+CRC
# codeRequest_openConnectionCannal_level1 = b"\x01\x01\x31\x31\x31\x31\x31\x31" # Неверно! 111111 - это в HEX!!!!
codeRequest_openConnectionCannal_level1 = b"\x01\x01\x01\x01\x01\x01\x01\x01"
codeRequest_openConnectionCannal_level2 = b"\x01\x02\x02\x02\x02\x02\x02\x02"
codeRecieve_goodOpenConnectionCannal = 0x00

codeRequest_closeConnectionCannal = 0x02
codeRecieve_goodСloseConnectionCannal = 0x00

# параметры запроса/ответа текущего времени счетчика  = Adress+codeRequest+CRC
codeRequest_DateTimeCounter = b"\x04\x00"
codeRecieve_goodDateTimeCounter = b"\x43\x14\x16\x03\x27\x02\x22\x01"  

# параметры запроса/ответа серийного номера и даты выпуска
codeRequest_ManufNumberDateCounter = b"\x08\x00"
codeRecieve_goodManufNumberDateCounter = b"\x29\x5a\x40\x43\x16\x06\x14"

# параметры запроса/ответа сетевого номера
codeRequest_NetNumberCounter = b"\x05\x00"
codeRecieve_goodNetNumberCounter = b"\x00"  #  НУЖЕН ЭКСПЕРИМЕНТ !!!!!!!!!!!!!!!!!!!!!!!!!

# параметры запроса/ответа мгновенных значений тока фазы 1
codeRequest_CurrentIstantlyFaze1 = b"\x08\x11\x21"
codeRecieve_goodCurrentIstantlyFaze1 = b"\x00"  # ?????????????

# параметры запроса/ответа мгновенных значений тока фазы 2
codeRequest_CurrentIstantlyFaze2 = b"\x08\x11\x22"
codeRecieve_goodCurrentIstantlyFaze2 = b"\x00"  # ?????????????

# параметры запроса/ответа мгновенных значений тока фазы 3
codeRequest_CurrentIstantlyFaze3 = b"\x08\x11\x23"
codeRecieve_goodCurrentIstantlyFaze3 = b"\x00"  # ?????????????

# параметры запроса/ответа мгновенного коэффициента мощности общий по фазам 
codeRequest_KoefPowerIstantlySumFaze = b"\x08\x11\x30"
codeRecieve_goodKoefPowerIstantlySumFaze = b"\x00"  # ?????????????

# параметры запроса/ответа мгновенных даты и времени фиксации 
codeRequest_IstantlyFixDateTime = b"\x08\x11\xe0"
codeRecieve_goodIstantlyFixDateTime = b"\x20\x55\x11\x01\x21\x02\x22\x01"

# параметры запроса/ответа мгновенной активной мощности по сумме фаз
codeRequest_IstantlyActivePowerSumFaze = b"\x08\x11\x00"
codeRecieve_goodIstantlyActivePowerSumFaze = b"\x20\x55\x11\x01\x21\x02\x22\x01"  # ?????????????

# параметры запроса/ответа мгновенной реактивной мощности по сумме фаз
codeRequest_IstantlyReactPowerSumFaze = b"\x08\x11\x04"
codeRecieve_goodIstantlyReactPowerSumFaze = b"\x00"  # ?????????????

# параметры запроса/ответа зафиксированная энергия сумма по всем тарифам 
codeRequest_EnergyFixSumTarif = b"\x08\x11\xf0"
codeRecieve_goodEnergyFixSumTarif = b"\x00"  # ?????????????

# # параметры запроса/ответа зафиксированная энергия по тарифу 1 
# codeRequest_EnergyFixTarif1 = b"\x08\x11\xf1"
# codeRecieve_goodEnergyFixTarif1 = b"\x00"  # ?????????????

# # параметры запроса/ответа зафиксированная энергия по тарифу 2 
# codeRequest_EnergyFixTarif2 = b"\x08\x11\xf2"
# codeRecieve_goodEnergyFixTarif2 = b"\x00"  # ?????????????

# # параметры запроса/ответа зафиксированная энергия по тарифу 3
# codeRequest_EnergyFixTarif3 = b"\x08\x11\xf3"
# codeRecieve_goodEnergyFixTarif3 = b"\x00"  # ?????????????




# чтение массивов данных, имеющих привязку ко времени
codeRequest_read_1 = 0x04
codeRequest_read_2 = 0x05
codeRequest_read_3 = 0x06

level_1_number = 0x01
level_1_PasswordH = 0x3131
level_1_PasswordM = 0x3131
level_1_PasswordL = 0x3131

numberNetAdr = 0x80

# --------------------------------------------------------------------------------------------------
# --------------------------     General    -------------------------------------------------------
# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------

def connection_to_port():
    rezult = False
    # print ("Создание подключения")
    ml.logger.debug(f'Создание подключения по cfg.MODE_CONNECT={cfg.MODE_CONNECT}')
    try:
        if cfg.MODE_CONNECT == cfg.MODE_CONNECTION_IP_TO_SERVER:
            cfg.handlerSocketConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            cfg.handlerSocketConn.connect((cfg.host_IP, int(cfg.port_IP)))
            # print("IP")
            ml.logger.debug('успешно создано подключение по MODE_CONNECTION_IP_TO_SERVER')
        elif cfg.MODE_CONNECT == cfg.MODE_CONNECTION_IP_TO_CLIENT:
            cfg.handlerSocketConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            cfg.handlerSocketConn.bind(('', cfg.port_IP))
            ml.logger.debug('успешно создано подключение по MODE_CONNECTION_IP_TO_CLIENT')
        if (cfg.handlerSerialPortConn == None) or not(cfg.handlerSerialPortConn.is_open):
            if cfg.MODE_CONNECT == cfg.MODE_CONNECTION_COM:
                if cfg.port_COM != 'Нет доступных портов':
                    cfg.handlerSerialPortConn  = serial.Serial(cfg.port_COM, baudrate=9600, 
                                bytesize=serial.EIGHTBITS, 
                                parity=serial.PARITY_NONE, 
                                stopbits=serial.STOPBITS_ONE, 
                                timeout=cfg.timeOutSerial, 
                                xonxoff=False, 
                                rtscts=False, 
                                write_timeout=None, 
                                dsrdtr=False, 
                                inter_byte_timeout=None)
                    ml.logger.debug('успешно создано подключение по MODE_CONNECTION_COM')
                    rezult = True
                else:
                    ml.logger.error("Нет доступных портов для открытия", exc_info=True)
                    rezult = False
        else:
            ml.logger.error("Handler порта СОМ не закрыт!", exc_info=True)
            rezult = False
    except:
        # print ("Ошибка создании подключения")
        ml.logger.error("Ошибка создании подключения Exception occurred", exc_info=True)
        rezult = False
    return rezult

def close_connection_to_port():
    rezult = False
    ml.logger.debug(f'Закрытие подключения по cfg.MODE_CONNECT={cfg.MODE_CONNECT}')
    try:
        # if cfg.MODE_CONNECT == cfg.MODE_CONNECTION_IP_TO_SERVER:
        #     cfg.handlerSocketConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        #     cfg.handlerSocketConn.connect((cfg.host_IP, int(cfg.port_IP)))
        #     # print("IP")
        #     ml.logger.debug('успешно создано подключение по MODE_CONNECTION_IP_TO_SERVER')
        # elif cfg.MODE_CONNECT == cfg.MODE_CONNECTION_IP_TO_CLIENT:
        #     cfg.handlerSocketConn = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        #     cfg.handlerSocketConn.bind(('', cfg.port_IP))
        #     ml.logger.debug('успешно создано подключение по MODE_CONNECTION_IP_TO_CLIENT')
        if cfg.MODE_CONNECT == cfg.MODE_CONNECTION_COM:
            if cfg.handlerSerialPortConn.is_open:
                cfg.handlerSerialPortConn.close()
                ml.logger.debug('успешно закрыто подключение по MODE_CONNECTION_COM')
                rezult = True
    except:
        # print ("Ошибка создании подключения")
        ml.logger.error("Ошибка закрытия подключения Exception occurred", exc_info=True)
        rezult = False
    return rezult

def packetInHex(packet):
    # aa = " ".join([hex(int(x)) for x in packet])
    # return aa
    return packet.hex(" ")



# def accept()-> int:
#     inData = 0    
#     return inData

# def rCRC(data:int)-> int:
#     crc = 0
#     return crc


def writePort(data):
    rezult = False
    number_of_bytes_written = 0
    ml.logger.debug(f"Отправка запроса: {packetInHex(data)}")
    try:
        if cfg.MODE_CONNECT == cfg.MODE_CONNECTION_IP_TO_SERVER:
            cfg.handlerSocketConn.sendall(data)
        elif cfg.MODE_CONNECT == cfg.MODE_CONNECTION_IP_TO_CLIENT:
            pass
        elif cfg.MODE_CONNECT == cfg.MODE_CONNECTION_COM:
            number_of_bytes_written = cfg.handlerSerialPortConn.write(data)
        rezult = True
        if number_of_bytes_written != len(data):
            rezult = False
            ml.logger.debug("Ошибка в переданных данных")
    except:
        pass
        # print ("Ошибка отправки данных")
        ml.logger.error("Ошибка отправки данных - Exception occurred", exc_info=True)
    return rezult

def recievePort(response_length):
    rezult = False
    recieveData=''
    try:
        if cfg.MODE_CONNECT == cfg.MODE_CONNECTION_IP_TO_SERVER:
            recieveData = cfg.handlerSocketConn.recv(response_length)
        elif cfg.MODE_CONNECT == cfg.MODE_CONNECTION_IP_TO_CLIENT:
            pass
        elif cfg.MODE_CONNECT == cfg.MODE_CONNECTION_COM:
            recieveData = cfg.handlerSerialPortConn.read(response_length)
        ml.logger.debug(f"прием: {packetInHex(recieveData)}")
        rezult = True
    except:
        # print ("Ошибка приема данных")
        ml.logger.error("Ошибка приема данных - Exception occurred", exc_info=True)
        rezult = False
    if recieveData == '': 
        rezult = False
        ml.logger.error("Принятый пакет - пустой")
    else:
        rezult = True
    return recieveData, rezult

def parserBytePacket(data, len)-> bool:
    """ разбор данных:
            проверка CRC
            выделение информационой части пакета (без сетевого номера и CRC)
        Arg:
        data - входные данные, тип bytes
        len - длина data вместе с сетевым номером и CRC в байтах
    """
    rezult = False
    parsed_packet = ''
    try:
        # защита от пустых данных (пустого пакета)
        if data != '': 
        #
            # защита от пакета неверной длины
            len_data = 0
            for x in data:
                len_data +=1
            if len_data == len:
            #
                # выбор варианта struct.unpack() в зависимости от длины пакета - входной параметр len
                if len == 4:
                    unpack_data = struct.unpack(">BBH", data)
                elif len == 5:
                    unpack_data = struct.unpack(">BBBH", data)
                elif len == 6:
                    unpack_data = struct.unpack(">BBBBH", data)
                elif len == 7:
                    unpack_data = struct.unpack(">BBBBBH", data)
                elif len == 8:
                    unpack_data = struct.unpack(">BBBBBBH", data)
                elif len == 9:
                    unpack_data = struct.unpack(">BBBBBBBH", data)
                elif len == 10:
                    unpack_data = struct.unpack(">BBBBBBBBH", data)
                elif len == 11:
                    unpack_data = struct.unpack(">BBBBBBBBBH", data) 
                elif len == 12:
                    unpack_data = struct.unpack(">BBBBBBBBBBH", data)  
                elif len == 13:
                    unpack_data = struct.unpack(">BBBBBBBBBBBH", data) 
                elif len == 15:
                    unpack_data = struct.unpack(">BBBBBBBBBBBBBH", data)
                elif len == 18:
                    unpack_data = struct.unpack(">BBBBBBBBBBBBBBBBH", data)    
                elif len == 19:
                    unpack_data = struct.unpack(">BBBBBBBBBBBBBBBBBH", data)       
                packet = unpack_data[:-1]   # отрежем CRC - будет пакет
                r_сrc = unpack_data[-1:]    # отрежем все кроме CRC
                crcr = r_сrc[0]
                if checkCRC(packet, crcr):
                    parsed_packet = unpack_data[1:-1]          # отрезаем сет номер и crc
                    rezult = True
                else:
                    parsed_packet = ''
                    ml.logger.error("ошибка CRC принятого пакета ")
                    rezult = False
                    # ml.logger.error(f"плохой пакет: {packetInHex(packet)}")

                    # комментирую этот блок кода, поскольку очень много принятых пакетов не подходят под этот алгоритм. Проще пакет выкинуть.
                    # # попытка исправить пакет, учитывая, то что CRC_L может оказаться первым байтом посылки
                    # packet_Hbytes = list(unpack_data[1:-1])
                    # # print(f"v: {mpm.packetInHex(packet_Hbytes)}")
                    # a = list(unpack_data[-1:])
                    # packet_Lbyte = (a[0])>>8
                    # # print(f"packet_Lbyte: {hex(packet_Lbyte)}")
                    # packet_Hbytes.append(packet_Lbyte)
                    # packet = packet_Hbytes.copy()
                    # # print(f"пакет: {mpm.packetInHex(packet)}")
                    # crc_L = list(unpack_data[:-(len_data-2)])[0]
                    # # print(f"crc_L: {hex(crc_L)}")
                    # a = list(unpack_data[-1:])[0]
                    # crc_H = a & 0x00FF
                    # crcr = (crc_H<<8) + crc_L
                    # # print(f"CRC: {hex(crcr)}")
                    # if checkCRC(packet, crcr):
                    #     # print ("разбор - ОК")
                    #     parsed_packet = packet   
                    #     print(f"исправленный пакет: {packetInHex(parsed_packet)}")
                    #     rezult = True
                    # #
                    # else:
                    #     parsed_packet = ''
                    #     ml.logger.error("ошибка CRC испрвленого пакета ")
                    #     rezult = False
            else:
                parsed_packet = ''
                ml.logger.error("ошибка длины принятого пакета ")
                rezult = False
        else:
            ml.logger.error("Принятый пакет - пустой")
            rezult = False
    except :
        # print("ошибка struct при разборе")
        ml.logger.error("ошибка struct при разборе - Exception occurred", exc_info=True)
        # ml.logger.error("ошибка struct при разборе - Exception occurred", exc_info=False)
        rezult = False
    ml.logger.debug(f"разобр пакет: {parsed_packet}")
    return parsed_packet, rezult

def buildPacket(netAdress: int, len: int, *args):
        """Create a ready to send modbus packet.
            len: int - длина пакета включая сетевой номер спереди, но без CRC
        """
        rezult = False
        try:
            if len == 2:
                packet = struct.pack(">BB", netAdress, *args)
            elif len == 3:
                packet = struct.pack(">BBB", netAdress, *args)
            elif len == 4:
                packet = struct.pack(">BBBB", netAdress, *args)
            elif len == 5:
                packet = struct.pack(">BBBBB", netAdress, *args)
            elif len == 6:
                packet = struct.pack(">BBBBBB", netAdress, *args)    
            elif len == 9:
                packet = struct.pack(">BBBBBBBBB", netAdress, *args)
            elif len == 11:
                packet = struct.pack(">BBBBBBBBBBB", netAdress, *args)
        # packet = struct.pack( ">BB", netAdress, param)
            rezult = True  
        except:
            # print("ошибка struct при сборке пакета")
            ml.logger.error("ошибка struct при сборке пакета - Exception occurred", exc_info=True)
            rezult = False
        packet += struct.pack(">H", computeCRC(packet))
        return packet, rezult


# --------------------------------------------------------------------------------------------------
# ------------------  CRC -------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
def __generate_crc16_table():
    """Generate a crc16 lookup table.

    .. note:: This will only be generated once
    """
    result = []
    for byte in range(256):
        crc = 0x0000
        for _ in range(8):
            if (byte ^ crc) & 0x0001:
                crc = (crc >> 1) ^ 0xA001
            else:
                crc >>= 1
            byte >>= 1
        result.append(crc)
    return result
    
__crc16_table = __generate_crc16_table()

def computeCRC(data):  # pylint: disable=invalid-name
    """Compute a crc16 on the passed in string.
    For modbus, this is only used on the binary serial protocols (in this
    case RTU).
    The difference between modbus"s crc16 and a normal crc16
    is that modbus starts the crc value out at 0xffff.

    :param data: The data to create a crc16 of
    :returns: The calculated CRC
    """
    crc = 0xFFFF
    for data_byte in data:
        idx = __crc16_table[(crc ^ int(data_byte)) & 0xFF]
        crc = ((crc >> 8) & 0xFF) ^ idx
    swapped = ((crc << 8) & 0xFF00) | ((crc >> 8) & 0x00FF)
    return swapped

def checkCRC(data, check):  # pylint: disable=invalid-name
    """Check if the data matches the passed in CRC.

    :param data: The data to create a crc16 of
    :param check: The CRC to validate
    :returns: True if matched, False otherwise
    """
    return computeCRC(data) == check


# --------------------------------------------------------------------------------------------------
# ------------------  Test, Open, Close Canal ------------------------------------------------------
# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
def fn_TestCanalConnection(numberNetAdress: int)-> bool:
    rezult = False
    len_build_packet = 2
    len_recieve_packet = 4
    packData, rezult_build = buildPacket(numberNetAdress, len_build_packet, codeRequest_testConnectionCannal)
    # ml.logger.debug(f"Запрос теста канала связи с NetAdress= {numberNetAdress}...")
    if rezult_build:
        if writePort(packData):
            packet, rezult_recieve = recievePort(len_recieve_packet)
            if rezult_recieve:
                parsed_packet, rezult_parser = parserBytePacket(packet, len_recieve_packet)
                if rezult_parser and (parsed_packet[0] == 0x00):
                    rezult = True
                    ml.logger.debug(f"Запрос теста канала связи с NetAdress= {numberNetAdress}...OK")
                else:
                    rezult = False
            else:
                rezult = False
        else:
            rezult = False
    else:
        rezult = False
    return rezult

def fn_OpenCanalConnectionLevel1(numberNetAdress: int)-> bool:
    rezult = False
    len_build_packet = 9
    len_recieve_packet = 4
    packData, rezult_build = buildPacket(numberNetAdress, len_build_packet, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01, 0x01)
    # ml.logger.debug(f"Запрос откр канала L1 с NetAdress= {numberNetAdress}...")
    if rezult_build:
        if writePort(packData):
            packet, rezult_recieve = recievePort(len_recieve_packet)
            if rezult_recieve:
                parsed_packet, rezult_parser = parserBytePacket(packet, len_recieve_packet)
                if rezult_parser and (parsed_packet[0] == 0x00):
                    rezult = True
                    ml.logger.debug(f"Запрос откр канала L1 с NetAdress= {numberNetAdress}...OK")
                else:
                    rezult = False
            else:
                rezult = False
        else:
            rezult = False
    else:
        rezult = False
    return rezult

def fn_OpenCanalConnectionLevel2(numberNetAdress: int)-> bool:
    rezult = False
    len_build_packet = 9
    len_recieve_packet = 4
    packData, rezult_build = buildPacket(numberNetAdress, len_build_packet,0x01, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02, 0x02)
    # ml.logger.debug(f"Запрос откр канала L2 с NetAdress= {numberNetAdress}...")
    if rezult_build:
        if writePort(packData):
            packet, rezult_recieve = recievePort(len_recieve_packet)
            if rezult_recieve:
                parsed_packet, rezult_parser = parserBytePacket(packet, len_recieve_packet)
                if rezult_parser and (parsed_packet[0] == 0x00):
                    rezult = True
                    ml.logger.debug(f"Запрос откр канала L2 с NetAdress= {numberNetAdress}...OK")
                else:
                    rezult = False
            else:
                rezult = False
        else:
            rezult = False
    else:
        rezult = False
    return rezult

def fn_CloseCanalConnection(numberNetAdress: int)-> bool:
    rezult = False
    len_build_packet = 2
    len_recieve_packet = 4
    packData, rezult_build = buildPacket(numberNetAdress, len_build_packet, codeRequest_closeConnectionCannal)
    # ml.logger.debug(f"Запрос закрытия канала связи с NetAdress= {numberNetAdress}...")
    if rezult_build:
        if writePort(packData):
            packet, rezult_recieve = recievePort(len_recieve_packet)
            if rezult_recieve:
                parsed_packet, rezult_parser = parserBytePacket(packet, len_recieve_packet)
                if rezult_parser and (parsed_packet[0] == 0x00):
                    rezult = True
                    ml.logger.debug(f"Запрос закрытия канала связи с NetAdress= {numberNetAdress}...OK")
                else:
                    rezult = False
            else:
                rezult = False
        else:
            rezult = False
    else:
        rezult = False
    return rezult




# --------------------------------------------------------------------------------------------------
# ------------------  Read Param -------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------

def fn_ReadParam_SerND(numberNetAdress: int, dic_counter)-> bool:
    rezult = False
    # заводской номер и дата выпуска - стр 63 руководства системы команд Меркурий
    len_build_packet = 3
    len_recieve_packet = 10
    packData, rezult_build = buildPacket(numberNetAdress, len_build_packet,0x08, 0x00)
    # packData = struct.pack( ">BBB", numberNetAdress,0x08, 0x00)     # 0x4d 0x8 0x0 0xe6 0x17
    # packData += struct.pack(">H", computeCRC(packData))
    ml.logger.debug(f"Запрос параметров счетчика сет.номер {numberNetAdress} - зав ном, даты вып. и т.д.")
    if rezult_build:
        if writePort(packData):
            packet, rezult_recieve = recievePort(len_recieve_packet)
            if rezult_recieve:
                parsed_packet, rezult_parser = parserBytePacket(packet, len_recieve_packet)
                if rezult_parser:
                    # раскидаем байты пакета по назначению
                    packetManufNumber = parsed_packet[:-3]     # отрезаем дату выпуска
                    packetManufData = parsed_packet[4:]        # отрезаем зав номер
                    manufNumber = "".join([str(x) for x in packetManufNumber])
                    manufData = "-".join([str(x) for x in packetManufData])
                    dic_counter['manuf_number'] = manufNumber
                    dic_counter['manuf_data'] = manufData
                    ml.logger.debug(f"ManufNumber: {manufNumber}, ManufData: {manufData}")
                    rezult = True
                else:
                    rezult = False
            else:
                rezult = False
        else:
            rezult = False
    else:
        rezult = False
    return dic_counter, rezult
            
def fn_ReadParam_KoefUI(numberNetAdress: int, dic_counter)-> bool:
    rezult = False         
    # коффициенты трансформации по току и напряжнию - стр 64 руководства системы команд Меркурий
    len_build_packet = 3
    len_recieve_packet = 7
    packData, rezult_build = buildPacket(numberNetAdress, len_build_packet,0x08, 0x02)
    # packData = struct.pack( ">BBB", numberNetAdress,0x08, 0x02)     #  0x4d 0x8 0x2 0x67 0xd6
    # packData += struct.pack(">H", computeCRC(packData))
    ml.logger.debug(f"Запрос коэф трансф: {packetInHex(packData)}")
    if rezult_build:
        if writePort(packData):
            packet, rezult_recieve = recievePort(len_recieve_packet)
            if rezult_recieve:
                parsed_packet, rezult_parser = parserBytePacket(packet, len_recieve_packet)
                if rezult_parser:
                    packetKU = parsed_packet[:-2]     # вырезаем KU
                    packetKI = parsed_packet[2:]        # вырезаем  KI
                    kU = str((packetKU[0]<<8) + packetKU[1])
                    kI = str((packetKI[0]<<8) + packetKI[1])
                    dic_counter['ku'] = kU
                    dic_counter['ki'] = kI
                    ml.logger.debug(f"KU: {kU}, KI: {kI}")
                    rezult = True
                else:
                    rezult = False
            else:
                rezult = False
        else:
            rezult = False
    else:
        rezult = False
    return dic_counter, rezult

def fn_ReadParam_VariantNew(numberNetAdress: int, dic_counter)-> bool:
    rezult = False
    # вариант исполнения счетчика - конкретно коэф А - постоянная счетчика  - стр 77 руководства системы команд Меркурий
    len_build_packet = 4
    len_recieve_packet = 15
    packData, rezult_build = buildPacket(numberNetAdress, len_build_packet,0x08, 0x12, 0x00)
                                                                                        # запрос 0x87 0x8 0x12 0x0 0xa5 0xf2
                                                                                        # ответ  0x87 0xb6 0xe3 0xc3 0x95 0x7 0x0 0x0 0x4 0x0 0x0 0x0 0x0 0x33 0x9f

    ml.logger.debug(f"Запрос вариант исполнения счетчика: {packetInHex(packData)}")
    if rezult_build:
        if writePort(packData):
            packet, rezult_recieve = recievePort(len_recieve_packet)
            if rezult_recieve:
                parsed_packet, rezult_parser = parserBytePacket(packet, len_recieve_packet)
                if rezult_parser:
                    packet_byte2 = parsed_packet[1]     # получаем второй байт
                    packet_byte2_mask = packet_byte2 & 0x0F     # выделяем число А - постоянную счетчика 
                    if packet_byte2_mask == 0:
                        count_koefА = 5000
                    elif packet_byte2_mask == 1:
                        count_koefА = 25000
                    elif packet_byte2_mask == 2:
                        count_koefА = 1250
                    elif packet_byte2_mask == 3:
                        count_koefА = 500
                    elif packet_byte2_mask == 4:
                        count_koefА = 1000
                    elif packet_byte2_mask == 5:
                        count_koefА = 250
                    # packetKI = parsed_packet[2:]        # вырезаем  KI
                    # kU = str((packetKU[0]<<8) + packetKU[1])
                    # kI = str((packetKI[0]<<8) + packetKI[1])
                    dic_counter['koefA'] = count_koefА
                    ml.logger.debug(f"koefА: {count_koefА}")
                    rezult = True
                else:
                    rezult = False
            else:
                rezult = False
        else:
            rezult = False
    else:
        rezult = False

    
    return dic_counter, rezult

def fn_ReadParam_VariantOld(numberNetAdress: int, dic_counter)-> bool:
    """ вариант исполнения счетчика  - устаревший протокол - для счетчиков примерно до 2016 года рождения
     - конкретно коэф А - постоянная счетчика  - стр 77 руководства системы команд Меркурий
    """
    rezult = False
    
    len_build_packet = 3
    len_recieve_packet = 9
    packData, rezult_build = buildPacket(numberNetAdress, len_build_packet,0x08, 0x12)
    ml.logger.debug(f"Запрос вариант исполнения счетчика (устаревший протокол): {packetInHex(packData)}")
    if rezult_build:
        if writePort(packData):
            packet, rezult_recieve = recievePort(len_recieve_packet)
            if rezult_recieve:
                parsed_packet, rezult_parser = parserBytePacket(packet, len_recieve_packet)
                if rezult_parser:
                    packet_byte2 = parsed_packet[1]     # получаем второй байт
                    packet_byte2_mask = packet_byte2 & 0x0F     # выделяем число А - постоянную счетчика 
                    if packet_byte2_mask == 0:
                        count_koefА = 5000
                    elif packet_byte2_mask == 1:
                        count_koefА = 25000
                    elif packet_byte2_mask == 2:
                        count_koefА = 1250
                    elif packet_byte2_mask == 3:
                        count_koefА = 500
                    elif packet_byte2_mask == 4:
                        count_koefА = 1000
                    elif packet_byte2_mask == 5:
                        count_koefА = 250
                    dic_counter['koefA'] = count_koefА
                    ml.logger.debug(f"koefА: {count_koefА}")
                    rezult = True
                else:
                    rezult = False
            else:
                rezult = False
        else:
            rezult = False
    else:
        rezult = False

    
    return dic_counter, rezult

# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
# ------------------  InstantlyValue ---------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------

def fn_fixInstantlyValue(numberNetAdress: int)-> bool:
    """ фиксация мгновенных значений - без открытия канала связи 

    """
    rezult = False
    len_build_packet = 3
    len_recieve_packet = 4
    # зафиксировать мгновенные значения
    # packData = struct.pack( ">BBB", numberNetAdress,0x03, 0x08)     
    # packData += struct.pack(">H", computeCRC(packData))
    packData, rezult_build = buildPacket(numberNetAdress, len_build_packet, 0x03, 0x08)
    ml.logger.debug("Запрос фиксации мгн значений.")
    if rezult_build:
        if writePort(packData):
            packet, rezult_recieve = recievePort(len_recieve_packet)
            if rezult_recieve:
                parsed_packet, rezult_parser = parserBytePacket(packet, len_recieve_packet)
                if rezult_parser and (parsed_packet[0] == 0x00):
                    rezult = True
                else:
                    rezult = False
            else:
                rezult = False
        else:
            rezult = False
    else:
        rezult = False
    return rezult
    







def fn_ReadInstantlyValue_TimeFix(numberNetAdress: int, id_counter)-> bool:
    rezult = False
    #--- дата и время фиксации
    dic = cfg.dic_template_DBIC.copy()
    len_build_packet = 4
    len_recieve_packet = 11
    # packData = struct.pack( ">BBBB", numberNetAdress,0x08, 0x14, 0xe0)     # 0x4d 0x8 0x14 0xe0 0x98 0x2
    # packData += struct.pack(">H", computeCRC(packData))
    packData, rezult_build = buildPacket(numberNetAdress, len_build_packet, 0x08, 0x14, 0xe0)
    ml.logger.debug("Запрос дата и время фиксации.")
    if rezult_build:
        if writePort(packData):
            packet, rezult_recieve = recievePort(len_recieve_packet)
            if rezult_recieve:
                parser_packet, rezult_parser = parserBytePacket(packet, len_recieve_packet)
                if rezult_parser:
                    lst_parsed_packet = list(parser_packet)
                    packetTime = lst_parsed_packet[:-5]     # вырезаем время фиксации
                    packetTime[0],packetTime[2]=packetTime[2],packetTime[0]
                    packetDate = lst_parsed_packet[4:-1]        # вырезаем дату фиксации
                    t = [hex(int(x))[2:] for x in packetTime]
                    d = [hex(int(x))[2:] for x in packetDate]
                    for i in range (0,len(t)): 
                        if len(t[i]) == 1 : t[i] = '0'+t[i]
                    TimeFix = ":".join(t)
                    for i in range (0,len(d)):
                        if len(d[i]) == 1 : d[i] = '0'+d[i]
                    d[2]='20'+d[2]  # сделаем год с послным тысячелением (было 23, стало 2023)
                    DataFix = "-".join(d)

                    # защита
                    # прежде чем поместить в dic['datetime'] - проверим на корректность дату и время
                    #  защита от неверного года
                    if (int(d[2])>2020) and (int(d[2])<2050):
                        #  защита от неверного месяца
                        if (int(d[1])>=1) and (int(d[1])<=12):
                            #  защита от неверного дня
                            if (int(d[0])>=1) and (int(d[0])<=31):
                                #  защита от неверного часа
                                if (int(t[0])>=0) and (int(t[0])<=23):
                                    #  защита от неверного минуты
                                    if (int(t[1])>=0) and (int(t[1])<=59):
                    #
                                        dic['datetime'] = datetime.datetime(int(d[2]),int(d[1]),int(d[0]),int(t[0]),int(t[1])).strftime("%d/%m/%Y %H:%M")
                                        ml.logger.debug(f"Time: {TimeFix}, Data: {DataFix}")
                                        dic['id_counter'] = id_counter
                                        # print ("TimeFix:", TimeFix ) 
                                        # print ("DataFix:", DataFix)
                                        rezult = True
                                    else:
                                        rezult = False
                                else:
                                        rezult = False
                            else:
                                        rezult = False
                        else:
                                        rezult = False
                    else:
                                        rezult = False
                else:
                    rezult = False
            else:
                rezult = False
        else:
            rezult = False
    else:
        rezult = False
    return dic, rezult
    
        
# def fn_ReadInstantlyValue_U(numberNetAdress: int, id_counter, dic)-> bool:
#     rezult = False
#     #--- мговенные напряжения
#     # rezult = False
#     len_build_packet = 4
#     len_recieve_packet = 12
#     # packData = struct.pack( ">BBBB", numberNetAdress,0x08, 0x14, 0x11)     # 0x4d 0x8 0x14 0x11 0x59 0x86
#     # packData += struct.pack(">H", computeCRC(packData))
#     packData, rezult_build = buildPacket(numberNetAdress, len_build_packet, 0x08, 0x14, 0x11)
#     ml.logger.debug("Запрос мгн напряжения.")
#     if rezult_build:
#         if writePort(packData):
#             packet, rezult_recieve = recievePort(len_recieve_packet)
#               if rezult_recieve:            
# parser_packet, rezult_parser = parserBytePacket(packet, len_recieve_packet)
#             if rezult_parser:
#                 parsed_packet = list(parser_packet)
#                 packetUfaza1 = parsed_packet[:-6]  
#                 packetUfaza1[1],packetUfaza1[2]=packetUfaza1[2],packetUfaza1[1]
#                 packetUfaza2 = parsed_packet[3:-3]        
#                 packetUfaza2[1],packetUfaza2[2]=packetUfaza2[2],packetUfaza2[1]
#                 packetUfaza3 = parsed_packet[6:]
#                 packetUfaza3[1],packetUfaza3[2]=packetUfaza3[2],packetUfaza3[1]
#                 Ufaza1 = (packetUfaza1[0]<<16) + (packetUfaza1[1]<<8) + packetUfaza1[2]
#                 Ufaza2 = (packetUfaza2[0]<<16) + (packetUfaza2[1]<<8) + packetUfaza2[2]
#                 Ufaza3 = (packetUfaza3[0]<<16) + (packetUfaza3[1]<<8) + packetUfaza3[2]
#                 ml.logger.debug(f"FixU_faza1: {Ufaza1}, FixU_faza2: {Ufaza2}, FixU_faza3: {Ufaza3}" )
#                 rezult = True
#             else:
#                 rezult = False
#         else:
#             rezult = False
#     else:
#         rezult = False
#     return dic, rezult

def fn_ReadInstantlyValue_I(numberNetAdress: int, id_counter, dic)-> bool:
    rezult = False
    #--- мгновенный ток
    len_build_packet = 4
    len_recieve_packet = 12
    packData, rezult_build = buildPacket(numberNetAdress, len_build_packet, 0x08, 0x14, 0x21)
    ml.logger.debug("Запрос мгн токи.")
    if rezult_build:
        if writePort(packData):
            packet, rezult_recieve = recievePort(len_recieve_packet)
            if rezult_recieve:
                parser_packet, rezult_parser = parserBytePacket(packet, len_recieve_packet)
                if rezult_parser:
                    parsed_packet = list(parser_packet)
                    packetIfaza1 = parsed_packet[:-6]  
                    packetIfaza1[1],packetIfaza1[2]=packetIfaza1[2],packetIfaza1[1]
                    packetIfaza2 = parsed_packet[3:-3]        
                    packetIfaza2[1],packetIfaza2[2]=packetIfaza2[2],packetIfaza2[1]
                    packetIfaza3 = parsed_packet[6:]
                    packetIfaza3[1],packetIfaza3[2]=packetIfaza3[2],packetIfaza3[1]
                    Ifaza1 = (packetIfaza1[0]<<16) + (packetIfaza1[1]<<8) + packetIfaza1[2]
                    Ifaza2 = (packetIfaza2[0]<<16) + (packetIfaza2[1]<<8) + packetIfaza2[2]
                    Ifaza3 = (packetIfaza3[0]<<16) + (packetIfaza3[1]<<8) + packetIfaza3[2]
                    ISumm =  (Ifaza1+Ifaza2+Ifaza3)
                    dic['CurrentFaze1'] = Ifaza1
                    dic['CurrentFaze2'] = Ifaza2
                    dic['CurrentFaze3'] = Ifaza3
                    dic['CurrentSum'] = ISumm
                    ml.logger.debug(f"FixI_faza1: {Ifaza1}, FixI_faza2: {Ifaza2}, FixI_faza3: {Ifaza3}, FixI_summ: {ISumm}" )
                    rezult = True
                else:
                    rezult = False
            else:
                rezult = False
        else:
            rezult = False
    else:
        rezult = False   
    return dic, rezult 

def fn_ReadInstantlyValue_PowerP(numberNetAdress: int, id_counter, dic)-> bool:
    rezult = False
    #--- мгновенная активная мощность
    # rezult = False
    len_build_packet = 4
    len_recieve_packet = 19
    packData, rezult_build = buildPacket(numberNetAdress, len_build_packet, 0x08, 0x14, 0x00)
    ml.logger.debug("Запрос мгн акт мощ.")
    if rezult_build:
        if writePort(packData):
            packet, rezult_recieve = recievePort(len_recieve_packet)
            if rezult_recieve:
                parser_packet, rezult_parser = parserBytePacket(packet, len_recieve_packet)
                if rezult_parser:
                    parsed_packet = list(parser_packet)
                    packetPfaza1 = parsed_packet[4:-8]  
                    packetPfaza1[1],packetPfaza1[0]=packetPfaza1[0],packetPfaza1[1]
                    packetPfaza1[2],packetPfaza1[3]=packetPfaza1[3],packetPfaza1[2]
                    packetPfaza2 = parsed_packet[8:-4]        
                    packetPfaza1[1],packetPfaza1[0]=packetPfaza1[0],packetPfaza1[1]
                    packetPfaza1[2],packetPfaza1[3]=packetPfaza1[3],packetPfaza1[2]
                    packetPfaza3 = parsed_packet[12:]
                    packetPfaza1[1],packetPfaza1[0]=packetPfaza1[0],packetPfaza1[1]
                    packetPfaza1[2],packetPfaza1[3]=packetPfaza1[3],packetPfaza1[2]
                    packetPSum = parsed_packet[:-12]
                    packetPSum[1],packetPSum[0]=packetPSum[0],packetPSum[1]
                    packetPSum[2],packetPSum[3]=packetPSum[3],packetPSum[2]
                    Pfaza1 = (packetPfaza1[1]<<16) + (packetPfaza1[2]<<8) + packetPfaza1[3]
                    Pfaza2 = (packetPfaza2[1]<<16) + (packetPfaza2[2]<<8) + packetPfaza2[3]
                    Pfaza3 = (packetPfaza3[1]<<16) + (packetPfaza3[2]<<8) + packetPfaza3[3]
                    PSumm = (packetPSum[1]<<16) + (packetPSum[2]<<8) + packetPSum[3]
                    dic['PowerPFaze1'] = Pfaza1
                    dic['PowerPFaze2'] = Pfaza2
                    dic['PowerPFaze3'] = Pfaza3
                    dic['PowerPFazeSum'] = PSumm
                    ml.logger.debug(f"FixP_faza1: {Pfaza1}, FixP_faza2: {Pfaza2}, FixP_faza3: {Pfaza3}, FixP_summ: {PSumm}")
                    rezult = True
                else:
                    rezult = False
            else:
                rezult = False
        else:
            rezult = False
    else:
        rezult = False 
    return dic, rezult
    
def fn_ReadInstantlyValue_PowerQ(numberNetAdress: int, id_counter, dic)-> bool:
    rezult = False
    #--- мгновенная реактивная мощность
    len_build_packet = 4
    len_recieve_packet = 19
    packData, rezult_build = buildPacket(numberNetAdress, len_build_packet, 0x08, 0x14, 0x04)
    ml.logger.debug("Запрос мгн реакт мощ.")
    if rezult_build:
        if writePort(packData):
            packet, rezult_recieve = recievePort(len_recieve_packet)
            if rezult_recieve:
                parser_packet, rezult_parser = parserBytePacket(packet, len_recieve_packet)
                if rezult_parser:
                    parsed_packet = list(parser_packet)
                    packetQfaza1 = parsed_packet[4:-8]  
                    packetQfaza1[1],packetQfaza1[0]=packetQfaza1[0],packetQfaza1[1]
                    packetQfaza1[2],packetQfaza1[3]=packetQfaza1[3],packetQfaza1[2]
                    packetQfaza2 = parsed_packet[8:-4]        
                    packetQfaza1[1],packetQfaza1[0]=packetQfaza1[0],packetQfaza1[1]
                    packetQfaza1[2],packetQfaza1[3]=packetQfaza1[3],packetQfaza1[2]
                    packetQfaza3 = parsed_packet[12:]
                    packetQfaza1[1],packetQfaza1[0]=packetQfaza1[0],packetQfaza1[1]
                    packetQfaza1[2],packetQfaza1[3]=packetQfaza1[3],packetQfaza1[2]
                    packetQSum = parsed_packet[:-12]
                    packetQSum[1],packetQSum[0]=packetQSum[0],packetQSum[1]
                    packetQSum[2],packetQSum[3]=packetQSum[3],packetQSum[2]
                    Qfaza1 = (packetQfaza1[1]<<16) + (packetQfaza1[2]<<8) + packetQfaza1[3]
                    Qfaza2 = (packetQfaza2[1]<<16) + (packetQfaza2[2]<<8) + packetQfaza2[3]
                    Qfaza3 = (packetQfaza3[1]<<16) + (packetQfaza3[2]<<8) + packetQfaza3[3]
                    QSumm = (packetQSum[1]<<16) + (packetQSum[2]<<8) + packetQSum[3]
                    dic['PowerQFaze1'] = Qfaza1
                    dic['PowerQFaze2'] = Qfaza2
                    dic['PowerQFaze3'] = Qfaza3
                    dic['PowerQFazeSum'] = QSumm
                    ml.logger.debug(f"FixQ_faza1: {Qfaza1}, FixQ_faza2: {Qfaza2}, FixQ_faza3: {Qfaza3}, FixQ_summ: {QSumm}" )
                    rezult = True
                else:
                    rezult = False
            else:
                rezult = False
        else:
            rezult = False
    else:
        rezult = False 
    return dic, rezult
    
def fn_ReadInstantlyValue_Cos(numberNetAdress: int, id_counter, dic)-> bool:
    rezult = False
    #--- мгновенный коэфф мощности
    # rezult = False
    len_build_packet = 4
    len_recieve_packet = 15
    packData, rezult_build = buildPacket(numberNetAdress, len_build_packet, 0x08, 0x14, 0x30)
                                                                            #запрос 87 08 14 30 a6 46
                                                                            # ответ 87 40 fa 01 00 00 00 00 00 00 40 fa 01 07 f8

    ml.logger.debug("Запрос мгн коэфф мощности.")
    if rezult_build:
        if writePort(packData):
            packet, rezult_recieve = recievePort(len_recieve_packet)
            if rezult_recieve:
                parser_packet, rezult_parser = parserBytePacket(packet, len_recieve_packet)
                if rezult_parser:
                    parsed_packet = list(parser_packet)
                    packetKPowerFazeSum = parsed_packet[:-9]  
                    packetKPowerFazeSum[1],packetKPowerFazeSum[2]=packetKPowerFazeSum[2],packetKPowerFazeSum[1]
                    packetKPowerFaze1 = parsed_packet[3:6]  
                    packetKPowerFaze1[1],packetKPowerFaze1[2]=packetKPowerFaze1[2],packetKPowerFaze1[1]
                    packetKPowerFaze2 = parsed_packet[6:9]  
                    packetKPowerFaze2[1],packetKPowerFaze2[2]=packetKPowerFaze2[2],packetKPowerFaze2[1]
                    packetKPowerFaze3 = parsed_packet[9:12]  
                    packetKPowerFaze3[1],packetKPowerFaze3[2]=packetKPowerFaze3[2],packetKPowerFaze3[1]
                    KPowerFaze1 = (packetKPowerFaze1[1]<<8) + packetKPowerFaze1[2]
                    KPowerFaze2 = (packetKPowerFaze2[1]<<8) + packetKPowerFaze2[2]
                    KPowerFaze3 = (packetKPowerFaze3[1]<<8) + packetKPowerFaze3[2]
                    KPowerFazeSum = (packetKPowerFazeSum[1]<<8) + packetKPowerFazeSum[2]
                    dic['KPowerFaze1'] = KPowerFaze1
                    dic['KPowerFaze2'] = KPowerFaze2
                    dic['KPowerFaze3'] = KPowerFaze3
                    dic['KPowerFazeSum'] = KPowerFazeSum
                    ml.logger.debug(f"KPowerFaze1: {KPowerFaze1},KPowerFaze2: {KPowerFaze2},KPowerFaze3: {KPowerFaze3}, FixCosSum: {KPowerFazeSum}" )
                    rezult = True
                else:
                    rezult = False
            else:
                rezult = False
        else:
            rezult = False
    else:
        rezult = False 
    return dic, rezult
    
    





# --------------------------------------------------------------------------------------------------
# ------------------  Profil Power -------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------
def fn_InitMassPofilPower(numberNetAdress: int)-> bool:
    """ Инициализация массива средних мощностей

    """
    rezult = False
    #  запрос доступа уровня 2
    if fn_OpenCanalConnectionLevel2(numberNetAdress):
        len_build_packet = 5
        len_recieve_packet = 4
        packData, rezult_build = buildPacket(numberNetAdress, len_build_packet, 0x03, 0x00, 0x1e, 0x01)
        print ("Запрос иниц массива профиля.")
        if rezult_build:
            if writePort(packData):
                packet, rezult_recieve = recievePort(len_recieve_packet)
                if rezult_recieve:
                    parsed_packet, rezult_parser = parserBytePacket(packet, len_recieve_packet)
                    if rezult_parser:
                        rezult = True
                    else:
                        rezult = False
                else:
                    rezult = False
            else:
                rezult = False
        else:
            rezult = False
    return rezult
                
                

def fn_ReadLastRecordMassProfilPower(numberNetAdress: int):
    """ чтение параметров последней записи массива средних профилей мощности  - стр. 78
    """
    rezult = False
    # dic = cfg.dic_template_DBPP.copy()
    # чтение последней записи массива профиля мощности:
    adress = 0x0010         # примем по умолчанию
    len_build_packet = 3
    len_recieve_packet = 12
    packData, rezult_build = buildPacket(numberNetAdress, len_build_packet, 0x08, 0x13)
    ml.logger.debug("Запрос последней записи массива профиля.")
    if rezult_build:
        if writePort(packData):
            packet, rezult_recieve = recievePort(len_recieve_packet)            # 0x4d 0x0 0x10 0x1a 0x13 0x0 0x28 0x12 0x22 0x1e 0x6a 0x4a
            if rezult_recieve:
                parser_packet, rezult_parser = parserBytePacket(packet, len_recieve_packet)
                if rezult_parser:
                    parsed_packet = list(parser_packet)
                    # dic['period_int'] = str(parsed_packet[8:][0]) 
                    # year = parsed_packet[7:-1]
                    # mounth = parsed_packet[6:-2]
                    # day = parsed_packet[5:-3]
                    # minute=parsed_packet[4:-4]
                    # hour = parsed_packet[3:-5]
                    # packetTime = parsed_packet[3:-4]
                    # packetDate = parsed_packet[5:-1]
                    # t = [hex(int(x))[2:] for x in packetTime]
                    # d = [hex(int(x))[2:] for x in packetDate]
                    # for i in range (0,len(t)): 
                        # if len(t[i]) == 1 : t[i] = '0'+t[i]
                    # TimeFix = ":".join(t)
                    # for i in range (0,len(d)):
                        # if len(d[i]) == 1 : d[i] = '0'+d[i]
                    # d[2]='20'+d[2]  # сделаем год с послным тысячелением (было 23, стало 2023)
                    # DataFix = "-".join(d)
                    # dic['datetime'] = datetime.datetime(int(d[2]),int(d[1]),int(d[0]),int(t[0]),int(t[1]))
                    # ml.logger.debug(f"Time: {TimeFix}, Data: {DataFix}")
                    # byte_status = parsed_packet[2:-6]
                    # bytes_adress  =parsed_packet[:-7]
                    # bytes_adress[0], bytes_adress[1] = bytes_adress[1], bytes_adress[0]
                    # adress = (bytes_adress[0]<<8) + bytes_adress[1]
                    # dic['id_counter'] = id_counter
                    bytes_adress  =parsed_packet[:-7]
                    adress = (bytes_adress[0]<<8) + bytes_adress[1]
                    ml.logger.debug(f"запись: adress: {hex(adress)}" )
                    # защита от корректности вычисления адреса
                    if (adress >= 0x010) and (adress <= 0xffef):
                        rezult = True
                    else:
                        ml.logger.error(f"ошибка - adress не в интервале 0x010...0xffef" )
                        rezult = False
                else:
                    rezult = False
            else:
                rezult = False
        else:
            rezult = False
    else:
        rezult = False 
    return adress, rezult

def fn_ReadRecordMassProfilPower(numberNetAdress: int, adress:int, id_counter)-> bool:
    rezult = False
    dic = cfg.dic_template_DBPP.copy()
    adrH = adress >> 8
    adrL = adress & 0xFF
    # чтение последней записи массива профиля мощности:
    len_build_packet = 6
    len_recieve_packet = 18
    packData, rezult_build = buildPacket(numberNetAdress, len_build_packet, 0x06, 0x03, adrH, adrL, 0x0F)
    ml.logger.debug("Запрос записи массива профиля.")
    if rezult_build:
        if writePort(packData):
            packet, rezult_parser = recievePort(18)                        
            if rezult_parser:
                parser_pasket, rezult_parser = parserBytePacket(packet, len_recieve_packet)
                if rezult_parser:
                    lst_parsed_packet = list(parser_pasket)
                    # byte_status = parsed_packet[:-14] 
                    packetTime = lst_parsed_packet[1:-12]
                    packetDate = lst_parsed_packet[3:-9]
                    t = [hex(int(x))[2:] for x in packetTime]
                    d = [hex(int(x))[2:] for x in packetDate]
                    for i in range (0,len(t)): 
                        if len(t[i]) == 1 : t[i] = '0'+t[i]
                    TimeFix = ":".join(t)
                    for i in range (0,len(d)):
                        if len(d[i]) == 1 : d[i] = '0'+d[i]
                    d[2]='20'+d[2]  # сделаем год с послным тысячелением (было 23, стало 2023)
                    DataFix = "-".join(d)
                    ml.logger.debug(f"Time: {TimeFix}, Data: {DataFix}")
                    # защита
                    # прежде чем поместить в dic['datetime'] - проверим на корректность дату и время
                    #  защита от неверного года
                    if (int(d[2])>2020) and (int(d[2])<2050):
                        #  защита от неверного месяца
                        if (int(d[1])>=1) and (int(d[1])<=12):
                            #  защита от неверного дня
                            if (int(d[0])>=1) and (int(d[0])<=31):
                                #  защита от неверного часа
                                if (int(t[0])>=0) and (int(t[0])<=23):
                                    #  защита от неверного минуты
                                    if (int(t[1])>=0) and (int(t[1])<=59):
                    #
                                        dic['datetime'] = datetime.datetime(int(d[2]),int(d[1]),int(d[0]),int(t[0]),int(t[1])).strftime("%d/%m/%Y %H:%M")
                                        dic['period_int'] = str(lst_parsed_packet[6:-8][0]) 
                                        A_plus = lst_parsed_packet[7:-6]
                                        A_plus[0], A_plus[1] = A_plus[1], A_plus[0]
                                        dic['P_plus'] = (A_plus[0]<<8) + A_plus[1]
                                        # когда нет данных - оба байта 255 (0xFF) - тогда просто обнулим значения
                                        if dic['P_plus'] == 65535 : dic['P_plus'] = 0
                                        A_minus = lst_parsed_packet[9:-4]
                                        A_minus[0], A_minus[1] = A_minus[1], A_minus[0]
                                        dic['P_minus'] = (A_minus[0]<<8) + A_minus[1]
                                        if dic['P_minus'] == 65535 : dic['P_minus'] = 0
                                        Q_plus = lst_parsed_packet[11:-2]
                                        Q_plus[0], Q_plus[1] = Q_plus[1], Q_plus[0]
                                        dic['Q_plus'] = (Q_plus[0]<<8) + Q_plus[1]
                                        if dic['Q_plus'] == 65535 : dic['Q_plus'] = 0
                                        Q_minus = lst_parsed_packet[13:]
                                        Q_minus[0], Q_minus[1] = Q_minus[1], Q_minus[0]
                                        dic['Q_minus'] = (Q_minus[0]<<8) + Q_minus[1]
                                        if dic['Q_minus'] == 65535 : dic['Q_minus'] = 0
                                        # byte_status = parsed_packet[2:-6]
                                        # bytes_adress  =parsed_packet[:-8]
                                        # dic['datetime'] = datetime.datetime(year[0],mounth[0],day[0],hour[0],minute[0])
                                        # adress = bytes_adress[1]*256 + bytes_adress[2]*1
                                        dic['id_counter'] = id_counter
                                        ml.logger.debug(f"запись:  значения {dic}" )
                                        # print ("запись:", "значения", dic )
                                        rezult = True
                                    else:
                                        rezult = False
                                else:
                                        rezult = False
                            else:
                                        rezult = False
                        else:
                                        rezult = False
                    else:
                                        rezult = False
                else:
                    rezult = False
            else:
                rezult = False
        else:
            rezult = False
    else:
        rezult = False 
    return dic, rezult




