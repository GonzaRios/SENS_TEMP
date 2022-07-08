import collections
from tkinter import *
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ClientTempAgent_hostFijo import Consulta_Temp
from datetime import datetime
import time
from tkinter import ttk 
from numpy import array , arange
import logging
import logging.handlers

class SENSOR(tk.Frame):
    def __init__(self, parent, *args, **kwargs):                 
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        plt.style.use('dark_background')

        ##################### FRAMES PARA EL GRÁFICO #######################
        self.frame_graficas = tk.Frame(self, bg="#AAAAAA")                                                # EMPLEO FRAME PARA UTILIZAR LAS POSICIONES DE LOS OBJETOS
        self._figure, self._ax = plt.subplots()
        self._figure_canvas = FigureCanvasTkAgg(
            self._figure, master=self.frame_graficas
            )

        self.frame_graficas.grid_columnconfigure(2, weight=1, uniform="fig")    
    
        #################### FRAMES PARA LOS LABEL's #######################                       
        self.frame_label = tk.Frame(self, bg="#AAAAAA")  
        self.label1= tk.Label(self.frame_label,font=("Verdana",20), text='DATA CENTER: ',bg="#AAAAAA" )   #LUGAR DONDE SE ENCUENTRA EL SENSOR., height=1 , width= 13
        self.label1.grid(row=1,column=2)

        self.label2 = tk.Label(self.frame_label, font=("Verdana",20), text= '')                           # VISUALIZACIÓN DE TEMPERATURA EN LA GUI NI BIEN SE EJECUTA EL SCRIPT.
        self.label2.grid(row=1,column=3)

        self.label3 = tk.Label(self.frame_label, font=("Verdana",20), text=' ',bg="#AAAAAA")
        self.label3.grid(row=2,column=1)

        self._figure_canvas.get_tk_widget().grid(
            row=0, column=2, padx=(50, 50), pady=(30, 30),
            sticky="nsew"
            )                                                                                             # POSICION , con STICKY puedo definir para qué dirección se expande el gráfico al modificar el tamaño de la ventana.
                                                                                                          # En este caso Norte,Sur.Este y Oeste.

        #################### FRAMES PARA LOS BOTONES #######################
        self.frame_botones = tk.Frame(self, bg="#151515")
                                                                                                          # DEFINICION DE BOTON CON SU FUNCION ASOCIADA
        self.btn_iniciar = ttk.Button(
            self.frame_botones, 
            text="Iniciar", command=self.iniciar_animacion
            )    
                                                                                                          # DEFINICION DE BOTON CON SU FUNCION ASOCIADA
        self.btn_pausar = ttk.Button(
            self.frame_botones,  
            text="  Pausa  ", command=self.pausar_animación, state=tk.DISABLED
            )  
        self.btn_iniciar.pack(
            side="left", padx=(50, 50), pady=(50, 50),
            fill="y", expand=True
            )                                                                                             # POSICION DEL BOTON
        self.btn_pausar.pack(
            side="left", padx=(50, 50), pady=(50, 50),
            fill="y", expand=True
            )                                                                                             # POSICION DEL BOTON

        self._anim = None
 
        self.frame_botones.pack(fill="both")
        self.frame_label.pack(fill="both")                                                                # SI LO QUIERO CENTRAR DEBO DEJAR VACIO EL ARGUMENTO 
        self.frame_graficas.pack(fill="both", expand=True)

        self.lista_gl = []
        self._init_axes()  
        self.y = 0
        self.hora = 0

    #########################################################################################################
    #########################################################################################################

    after_id = None
    secs = 0
         
    def consult_sensor(self):
        ''' FUNCIÓN ENCARGADA DE HACER LA CONSULTA DE TEMPERATURA POR MEDIO DE LA LLAMADA A Consult_Temp Y CLASIFICAR POR COLORES SEGÚN EL VALOR.
            TAMBIÉN CREA UNA LISTA DONDE ALOJA TODAS LAS CONSULTAS REALIZADAS.'''
        global after_id                                                                               
        global secs       
        secs += 1     
        try:   
            if secs % 2 == 0:        
                x =  Consulta_Temp('192.168.208.51',1002,'QTEMP001')                       
                self.X = str(x)+ " °C "                     
                self.hora= time.strftime("%H:%M" )
                self.label3.config(font=("Verdana",20), text= self.hora ,bg="#AAAAAA")
                if self.X < "25 °C":
                    self.label2.config(font=("Verdana",30) ,text= self.X, foreground="green", 
                                                    borderwidth=4, anchor="e", bg="#AAAAAA")                   
                elif self.X > "27 °C":
                    self.label2.config(font=("Verdana",30),text= self.X, foreground="red" , 
                                                borderwidth=4, anchor="e", bg="#AAAAAA")
                elif "25 °C"< self.X < "27 °C":
                    self.label2.config(font=("Verdana",30) ,text= self.X, foreground="yellow", 
                                                    borderwidth=4, anchor="e", bg="#AAAAAA")
                self.lista_gl.append(x)
                
        except:
            messagebox.showinfo(message="Problemas con la VPN, por favor espere.", title="Error")         # MENSAJE DE ERROR CUANDO SE CORTA LA VPN.
            
        finally:
            after_id = self.after(10000, self.consult_sensor)                                              # CADA 10 SEGUNDOS (la función los expresa como mili s.) EL MÉTODO AFTER LLAMA A LA FUNCIÓN consult_sensor. LO QUE HACE ESTE MÉTODO ES ITERAR CADA X SEGUNDOS LA FUNCIÓN INGRESADA.                                                                                                    
        
        path = 'C:/Users/gonzalo.rios/Documents/SENSOR_TEMP/ClientTempAgent_hostFijo.txt'
        try:
            with open(path, 'r+') as archivo:
                p_objeto = logging.handlers.RotatingFileHandler(path,mode='', maxBytes=100000, backupCount=5, encoding=None,delay=True, errors=None )
                logging.basicConfig(handlers=[p_objeto],
                                            format = " %(asctime)s %(name)s:%(levelname)s:%(message)s ",
                                            datefmt = " %d-%m-%Y %H:%M:%S %p",
                                            level = logging.DEBUG )
        finally:
            pass
        try:
            logging.info('Temperatura: ' + self.X)
        except:
            logging.warning('Perdida señal sensor')
        return self.lista_gl       

    def start(self):
        ''' FUNCIÓN QUE LLAMA A INICIAR A LA FUNCIÓN consult_sensor'''
        global secs
        secs = 0 
        self.consult_sensor()                                                                           

    def stop(self):
        ''' FUNCIÓN QUE LLAMA A PARAR AL MÉTODO AFTER Y POR LO TANTO A LAS CONSULTAS AL SENSOR Y GRÁFICO'''
        global after_id
        if after_id:
            self.after_cancel(after_id)
            after_id = None
    
    ######################################### PROPIEDADES DEL GRAFICO ######################################
    def _init_axes(self):
        self._ax.set_title('SEÑAL SENSOR')
        self._ax.set_xlabel("HORA [m]")
        self._ax.set_ylabel("TEMPERATURA [°C]")
        self._ax.set_xticks(array([0, 15, 30, 45, 60]))
        self._ax.set_yticks(array([10,15,20,25,30]))
        self._ax.set_xlim(0, 60)
        self._ax.set_ylim(0,30)  
        self._ax.set_axis_on()
    #########################################################################################################
       
    def iniciar_animacion(self):
        ''' LLAMA A GENERAR LAS CONSULTAS AL SENSOR Y GRAFICAR CON LOS DATOS DE DICHA CONSULTA '''
        self.start()

        def animacion(values):
            value = values
            data.append(value)
            l_data= arange(len(data))
            linea.set_data(l_data, data)
            return linea

        def data_gen():                                                                                   # FUNCIÓN GENERADORA  
            try:
                inicio=0                     
                for k in range(50):
                    inicio= inicio+0.1                   
                    self.y =  self.lista_gl.pop()                                                         # EXTRAE EL ÚLTIMO ELEMENTO DE LA LISTA self.lista_gl              
                    yield self.y                                                                          # GENERADOR  
               
            except:
                pass
                   
        if self._anim is None:
            linea = self._ax.plot([], [], color='#80FF00')[0]      
            data = collections.deque([0] , maxlen= 60)
            self._anim = animation.FuncAnimation(self._figure, animacion, frames=data_gen, interval=3)    # DATA PARA LA GRÁFICA. Espacio de figura=self.figure / Funcion graficadora=animacion / frame=data_gen Data del origen para pasar, en este caso el generador, y cada cuadro de animaciones / inter=3 cantidadd en milisegundos con la que se muestra cada frame a graficar. 
            self._figure_canvas.draw()                                                                    # MÉTODO PARA GRAFICAR. 
            self.btn_pausar.configure(state=tk.NORMAL)
            self.btn_iniciar.configure(text="Detener")
        else:
            self._ax.linea = []
            self.btn_pausar.configure(state=tk.DISABLED, text="  Pausa  ")
            self.btn_iniciar.configure(text="Iniciar")
            self._anim = None        
    
    def pausar_animación(self):     
        if self.btn_pausar["text"] == "  Pausa  ":
            self.stop()
            self._anim.event_source.stop()          
            self.btn_pausar.configure(text="Continuar")
            
        else:
            self.start()
            self._anim.event_source.start()
            self.btn_pausar.configure(text="  Pausa  ")

if __name__ == "__main__":
    root = tk.Tk()
    root.title('SENSOR TEMPERATURA ')
    SENSOR(root).pack(side="top", fill="both", expand=True)
    root.mainloop()