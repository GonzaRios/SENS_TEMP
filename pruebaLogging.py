import logging
from datetime import datetime
from ClientTempAgent_hostFijo import Consulta_Temp

temp = Consulta_Temp('192.168.208.51', 1002, 'QTEMPALL')
TEMP = str(temp) + ' C°'

path = 'C:/Users/gonzalo.rios/Documents/SENSOR_TEMP/ClientTempAgent_hostFijo.txt'

with open(path, 'r+') as archivo:

    logging.basicConfig(handlers=[logging.FileHandler(filename=path, encoding='utf-8',mode='a+')],
                    format = " %(asctime)s %(name)s:%(levelname)s:%(message)s ",
                    datefmt = " %d-%m-%Y %H:%M:%S %p",
                    level = logging.DEBUG )

    logging.info('Temperatura: ' + TEMP)
