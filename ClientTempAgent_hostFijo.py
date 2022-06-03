import socket
import time
import sys

#Tiempo de espera de la respuesta desde el server
MSG_TIMEOUT     = 7     # Lo defino en T/2 para salir antes de enviar otro nuevo mensaje
# Cantidad de bytes esperados en la respuesta
EXPECTED_BYTES  = 10
BUFSIZE = 16
DEBUG_VERSION = False


    

def Consulta_Temp(host, port, msg):
    server_address = (host, port)
    try:
        socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
        if DEBUG_VERSION:
            print( time.strftime("%H:%M:%S") + " --> " +'Conectando a {} puerto {}'.format(*server_address))
        socket_tcp.connect(server_address)
        
        # Datos a enviar
        message = msg.encode("ascii")
        #print( time.strftime("%H:%M:%S") + " --> " + "Envio: {}".format(message) )
        socket_tcp.settimeout(MSG_TIMEOUT)
        socket_tcp.sendall(message)
        
        # Cantidad de bytes para esperar
        bytes_recibidos = 0
        bytes_esperados = EXPECTED_BYTES
        received_msg= ""
        while bytes_recibidos < bytes_esperados:
            data = socket_tcp.recv(BUFSIZE)
            bytes_recibidos += len(data)
            received_msg = received_msg + data.decode("ascii")

        socket_tcp.settimeout(None)
        if "T01" in received_msg:
            if DEBUG_VERSION:
                print( time.strftime("%H:%M:%S") + " --> " + "Recibo: " + received_msg)
            indice = received_msg.find('+') +1
            temp_value = float(received_msg[indice: indice+4])
            print(temp_value)
        else:
            if DEBUG_VERSION:
                print("Error de recepcion")
    except:
        if DEBUG_VERSION:
            print( time.strftime("%H:%M:%S") + " --> " + "Cierro socket")
        socket_tcp.close()
    finally:
        if DEBUG_VERSION:
            print( time.strftime("%H:%M:%S") + " --> " + "Cierro socket")
        socket_tcp.close()
    return temp_value
    
#host = '192.168.208.51'
#port = 1002
#msg = 'QTEMPALL'

#Consulta_Temp(host, port, msg)