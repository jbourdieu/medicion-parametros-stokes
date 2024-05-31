import time # std module
import pyvisa as visa # http://github.com/hgrecco/pyvisa
from numpy import array as arr
from numpy import linspace as lins

'''

Este programa está basado en el ejemplo
https://github.com/tektronix/Programmatic-Control-Examples/tree/master/Examples/Oscilloscopes/MidrangeScopes/src/SimplePlotExample

'''

"""
abre el osciloscopio, limpia la informacion que haya dando vueltas, imprime ID
"""

rm = visa.ResourceManager()#llamo a esto rm_check xq solo chequeo el nombre del instrumeto
visa_address = 'USB0::0x0699::0x0418::C022752::INSTR'
print(f'Instrumentos VISA: {rm.list_resources()}\n visa_address es {visa_address}') #para ver la id del scope
scope = rm.open_resource(visa_address)
channel='CH1'

def open_scope():
    scope.timeout = 10000 # ms
    scope.encoding = 'latin_1'
    scope.read_termination = '\n'
    scope.write_termination = None
    scope.write('*cls') # clear ESR
    print(scope.query('*idn?'))
    return(scope)

"""
reseteo, sincronizo, autoseteo, sincronizo
"""
def re_auto_set():
    scope.write('*rst') # reset
    t1 = time.perf_counter()
    r = scope.query('*opc?') # sync
    t2 = time.perf_counter()
    print('reset time: {}'.format(t2 - t1))

    scope.write('autoset EXECUTE') # autoset
    t3 = time.perf_counter()
    r = scope.query('*opc?') # sync
    t4 = time.perf_counter()
    print('autoset time: {} s'.format(t4 - t3))

"""
setteos de input output
"""
record = int(scope.query('horizontal:recordlength?'))

def io_set(channel):
    scope.write('header 0')
    scope.write('data:encdg SRIBINARY')
    scope.write(f'data:source {channel}') # channel
    scope.write('data:start 1') # first sample
    scope.write('data:stop {}'.format(record)) # last sample
    scope.write('wfmoutpre:byt_n 1') # 1 byte per sample

"""
setteos de adquisicion
"""
def acq_set():
    scope.write('acquire:state 0') # stop
    scope.write('acquire:stopafter SEQUENCE') # single
    scope.write('acquire:state 1') # run
    scope.write('TRIGger:A:MODe AUTO')
    t5 = time.perf_counter()
    r = scope.query('*opc?') # sync
    t6 = time.perf_counter()
    print('acquire time: {} s'.format(t6 - t5))

"""
adquiero la curva, y escalo los valores, devuelve el array tiempo y el array voltaje
"""
def curva():
    # data query
    t7 = time.perf_counter()
    bin_wave = scope.query_binary_values('curve?', datatype='b', container=arr)
    t8 = time.perf_counter()
    print('transfer time: {} s'.format(t8 - t7))

    # retrieve scaling factors
    tscale = float(scope.query('wfmoutpre:xincr?'))
    tstart = float(scope.query('wfmoutpre:xzero?'))
    vscale = float(scope.query('wfmoutpre:ymult?')) # volts / level
    voff = float(scope.query('wfmoutpre:yzero?')) # reference voltage
    vpos = float(scope.query('wfmoutpre:yoff?')) # reference position (level)
    
    # create scaled vectors
    # horizontal (time)
    total_time = tscale * record
    tstop = tstart + total_time
    scaled_time = lins(tstart, tstop, num=record, endpoint=False)
    # vertical (voltage)
    unscaled_wave = arr(bin_wave, dtype='double') # data type conversion
    scaled_wave = (unscaled_wave - vpos) * vscale + voff
    
    return(scaled_time,scaled_wave)

"""
chequeo de errores
"""
def error_check():
    # error checking
    r = int(scope.query('*esr?'))
    print('event status register: 0b{:08b}'.format(r))
    r = scope.query('allev?').strip()
    print('all event messages: {}'.format(r))

def close_scope():
    scope.close()
    rm.close()

def medicion_scope(channel):
    rm = visa.ResourceManager()#llamo a esto rm_check xq solo chequeo el nombre del instrumeto
    open_scope() #abro el osc.
    re_auto_set() #reset y auto set
    io_set(channel) #setteo el canal
    error_check() #antes de medir chequeo errores
    acq_set() #mido
    scaled_time,scaled_wave = curva() #escalo valores a volts
    error_check()#despues de medir chequeo errores
    #close_scope() #cierro osc.
    print('tiempo en segundos, voltaje en volts\n')
    close_scope()
    return(scaled_time,scaled_wave)