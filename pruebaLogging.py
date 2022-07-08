import logging
import logging.handlers
from datetime import datetime
from zlib import MAX_WBITS
from ClientTempAgent_hostFijo import Consulta_Temp
from logzero import logger, logfile
import logzero


temp = Consulta_Temp('192.168.208.51', 1002, 'QTEMPALL')
TEMP = str(temp) + ' °C'
path = 'C:/Users/gonzalo.rios/Documents/SENSOR_TEMP/prueba.log'
# file = logfile(path, maxBytes= 500, backupCount=2)

with open(path, 'r+') as archivo:
        p_objeto = logging.handlers.RotatingFileHandler(path,mode='', maxBytes=1000, backupCount=3, encoding=None,delay=True, errors=None )
        logging.basicConfig(handlers=[p_objeto],
                                        format = " %(asctime)s %(name)s:%(levelname)s:%(message)s ",
                                        datefmt = " %d-%m-%Y %H:%M:%S %p",
                                        level = logging.DEBUG )
        
try:
     logging.info('Temperatura: ' + TEMP)
except:
     logging.warning('Perdida señal sensor')
   
#     mi_format = logging.basicConfig(handlers=[logging.FileHandler(filename=path, encoding='utf-8',mode='a+')],

#                         datefmt = " %d-%m-%Y %H:%M:%S %p",
#                         level = logging.DEBUG )          # #logging.Formatter(" %(asctime)s %(name)s:%(levelname)s:%(message)s ")

#     logzero.formatter(mi_format)
#     logger.info('Temperatura: ' + TEMP)

## ESTO TIENE UN PROBLEMA AL LLENAR EL TAMAÑNO DEL ARCHIVO SETEADO
# -----------------------------------------------------------------------------------------------------------------

# import logzero
# from logzero import logger, logfile
# import logging
 
# #set file path
# logfile("Prueba_con_corte.txt",  maxBytes=2000, backupCount=2)
 
# # Set a custom formatter
# my_formatter = logging.Formatter('%(filename)s - %(asctime)s - %(levelname)s: %(message)s');
# logzero.formatter(my_formatter)
 
# # Log messages
# logger.info("This log message saved in the log file")
# logger.warning("This log message saved in the log file")

#####################################################
