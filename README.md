El programa STOKES-medir-calcular mide la polarización de un haz polarizado y calcula los parámetros de stokes 
y de la esfera de Poincaré.

Para medir la polarización se debe propagar el haz, primero, a través de una lámina de cuarto de onda rotante, luego a traves de un polarizador analizador.
Finalmente, se adquiere la intensidad del haz a la salida del polarizador en función de la posición angular de la lámina de cuarto de onda. 
Para alinear el polarizador se debe quitar la lámina de cuarto de onda y luego rotar al analizador hasta que se tenga la máxima transmisión posible. 
Para obtener la información completa de la polarización es necesario que la lámina de onda se rote un total 180 grados.

El programa se encarga de rotar la lámina de cuarto de onda desde 0 a 180 grados con pasos de 2 grados y, por cada ángulo que rota, de medir la intensidad de la señal a través del osciloscopio.
Por un lado, el programa devuelve un archivo de texto llamado {nombre} con: el valor de los ángulos, el error en la posicion del angulo, el voltaje medio leído en el osciloscopio y la desviasión estándar del voltaje medio. También, genera y guarda el gráfico de la intensidad de la señal en funcion del ángulo de la lámina de onda. 
Por el otro lado, el programa calcula los parámetros de Stokes y los ángulos de elipticidad (chi) y de orientación (psi) de la elipse con sus respectivos errores. Esta información seguarda en un archivo de texto llamado {nombre}-analisis y también se generan y guardan los graficos de la elipse de polarización y la esfera de Poincaré. 

RECOMENDACIONES IMPORTANTES PARA EL USO DEL PROGRAMA

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
            

