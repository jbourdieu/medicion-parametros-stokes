##STOKES-medir-calcular.py
Para medir el estado de polarización de un haz polarizado, es necesario propagar el haz a través de una lámina de cuarto de onda rotante, luego a través de un polarizador y, por último, adquirir la intensidad del haz a la salida del polarizador en función de la posición angular de la lámina de cuarto de onda. Para obtener información completa sobre la polarización, la lámina de cuarto de onda debe rotarse un total de 180º.
El programa STOKES-medir-calcular.py, desarrollado en Python, está diseñado para medir el estado de polarización de un haz polarizado de manera completamente automatizada. Este programa se encarga de rotar una lámina de cuarto de onda desde 0º hasta 180º con pasos de 2º montada sobre un motor rotador Zaber. En cada ángulo de rotación, registra la intensidad de la señal a través de un osciloscopio Tektronix utilizando el programa auxiliar scope_simple_plot.py de autoría propia. El programa devuelve un archivo de texto llamado {nombre}-osci, que contiene la posición angular de la lámina con su error, el voltaje medio registrado en el osciloscopio y la desviación estándar del voltaje medio. Luego, se obtiene el estado de polarización calculando los parámetros de Stokes y los parámetros de la elipse de polarización con sus respectivos errores y guarda la información en un archivo de texto llamado {nombre}-analisis. Para esto, se utiliza los programas auxiliares stokes.py, coeficientes_ABCD_y_error.py y EsferaElipse.py de autoría propia. Además, se generan y se guardan los gráficos de la elipse de polarización y la esfera de Poincaré.

Los archivos medicion_PRUEBA01_27032023.png, medicion_PRUEBA01_27032023-analisis, medicion_PRUEBA01_27032023-elipse.png, medicion_PRUEBA01_27032023-esfera.png y medicion_PRUEBA01_27032023-osci son un ejemplo de los archivos que devuelve el programa. 

##RECOMENDACIONES IMPORTANTES PARA EL USO DEL PROGRAMA

El archivo del progrma siempre debe estar en la misma carpeta que coeficientes_ABCD_y_error.py, EsferaElipse.py, scope_simple_plot.py y stokes.py. 

SIEMPRE ANTES DE USARLO modificar el siguiente bloque de código: 
    
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
            

