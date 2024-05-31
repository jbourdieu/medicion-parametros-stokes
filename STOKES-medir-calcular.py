''' LIBRERIAS ''' 

#LIBRERIAS GENERALES
import numpy as np
import matplotlib.pyplot as plt
import time
from datetime import datetime

#comunicacion con puertos
import serial
import serial.tools.list_ports
#para recargar librerias, sirve para el oscilocopio
from importlib import reload 
#LIBRERIAS OSCILOSCOPIO  DEBEN ESTAR EN MISMA CARPETA QUE ESTE ARCHIVO
import scope_simple_plot as osc
#LIBRERIAS para el motor
from zaber_motion import Library
from zaber_motion.binary import Connection
from zaber_motion import Units
import zaber_motion.binary.device as dv
#calculo de parámetros de Stokes
import stokes 

Library.enable_device_db_store() 

''' LISTA DE DISPOSITIVOS '''

#Pequenas lineas para saber donde esta el motor
ports = serial.tools.list_ports.comports()
print('LISTA DE DISPOSITIVOS EN PUERTOS')
for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))
        
        
''' MODIFICAR PARÁMETROS DE ESTA CELDA '''

#chequear que sea el nombre del puerto donde está el rotador
com_rotador='COM3' 

#parametros del archivo donde guardo la medicion

num = '01' #numero de medicion: SI NO LO CAMBIO PUEDO SOBREESCRIBIR LA MEDICIÓN
fecha = datetime.now().strftime("%d%m%Y") #fecha actual
comentario = f'angulos (gr) , error_ang (gr), V (V) , V_std (V)  \n '
nombre = f'medicion_{num}_{fecha}' #archivo 

#canal del osciloscopio
canal = 'CH1' 

print(nombre)

'''
Este parte mueve al rotador cant_ang veces entre 0 y 180. Rota-> 
mide con osciloscopio -> guardo el promedio de voltaje 
en V y en V_std la desviacion estandar de esto.
Espera sleep segundos y repite. 
Guardo un txt con angulos, error angulo, voltaje y desviacion estandar lllamado nombre.
Grafico angulos vs voltajes y guardo el grafico llamandolo nombre.
'''

#parametros del codigo
cant_ang = 91 #cuantos angulos quiero moverme
paso = 2 #paso entre angulos voy moviendome cada 2 grados
sleep = 0.2 #tiempo en segundos que espero entre movimientos
angulos = np.linspace( 0 , 180 , cant_ang)
angulo_medido = np.zeros( cant_ang ) #guardo la media del angulo
error_ang =np.zeros( cant_ang )

V = np.zeros( cant_ang ) #guardo la media de voltajes de una medicion con el osciloscopio
V_std = np.zeros( cant_ang )#guardo la desviacion estandar de una medicion con el osciloscopio

with Connection.open_serial_port(com_rotador) as rotador: #el entorno with permite que se cierre el dispositivo cuando salgo
    #este primer bloque chequea que se haya conectado algo a com_rotador
    device_list_r = rotador.detect_devices()
    print("Found {} devices".format( len(device_list) ) )
    
    #guardo el dispositivo en device
    device_rotador = device_list_r[0]
    #setteo a home para mover relativo de forma correcta
    device_rotador.home() 
            
    for i in range(cant_ang):
    #el if esta para poder medir el angulo cero
    #rel es el movimiento relativo del motor
        if i == 0:
            rel = 0
        else:
            rel = i * paso - ( i - 1 ) * paso              
        device_rotador.move_relative(rel, Units.ANGLE_DEGREES)
        posicion_actual = device_rotador.get_position(unit = Units.ANGLE_DEGREES)
        angulo_medido[i] = posicion_actual
        error_ang[i] = abs(angulo_medido[i]-angulos[i])*0.5        
        #MIDO CON OSCILOSCOPIO        
        tiempo, voltaje = osc.medicion_scope( canal )
        V[i] = np.mean(voltaje)
        V_std[i] = np.std(voltaje)
        print(f'cant_ang numero {i} posicion {posicion_actual}\n') #chequeo que angulo se midio
        reload(osc)
        time.sleep(sleep) #espero antes de leer
        
        
np.savetxt(f'{nombre}-osci' , [angulos , error_ang , V , V_std ] , header = comentario)
plt.plot(angulo_medido,V,'.-')
plt.errorbar(angulo_medido, V, yerr=V_std, xerr=error_ang,fmt='none')
plt.xlabel('Angulo $\\theta$ (°)')
plt.ylabel('Voltaje medio (V)')
plt.grid()
plt.show()
plt.savefig(nombre)


'''
Con stokes.calculo_polarizacion() calculo S y los angulos de la elipse. Grafico la
esfera de poincare y la elipse de polarizacion. 
En el archivo '{nombre}-analisis' guardo [S_nor,S_nor_err,psi , psi_err, chi , chi_err] con
los ángulos en radianes y S sin unidades (normalizado).
Los graficos se guardan como {nombre}-esfera y {nombre}-elipse.
'''

theta = angulos
theta_err = error_ang
I = V
I_err = V_std 

stokes.calculo_polarizacion(theta,theta_err,I,I_err)