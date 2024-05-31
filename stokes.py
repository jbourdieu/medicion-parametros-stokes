import numpy as np
import os
import coeficientes_ABCD_y_error as coef
import EsferaElipse as pol

import matplotlib.pyplot as plt
#from matplotlib import style

'''
En S_todo guardo los parametros relevantes a calcular: [S/S0 , S/S0_err , 
psi , psi_err, chi , chi_err] para la medicion y luego se guarda en el archivo
'{nombre}-analisis'.

Calculo S, los angulos de la elipse y los errores. 
Ademas se imprime y guardan los graficos. 

SNormErr(Si:parametro S_i, Sier: error parametro S_i, S0: parametros S_0,
        S0er: error parametros S_0) calcula el error del parametro S_i al normalizarlo por S0
'''


S_todo = {}
S_todo['cometario']='[S/S0,S/S0_err,psi , psi_err, chi , chi_err] angulos en radianes, S sin unidades'

def SNormErr(Si, Sier, S0, S0er):
     return np.sqrt( (Sier/S0)**2 + (Si*S0er/(S0**2))**2 )
    
    
def calculo_polarizacion(theta,theta_err,I,I_err, nombre):
    datos = [theta,theta_err,I,I_err]

    S , S_err  = coef.S(len(datos[0]) , datos[2] , datos[3], datos[0] , datos[1] )
    S_nor = S/S[0] #vector de stokes normalizado
    S_nor_err = np.array([np.sqrt(2)*S_err[0]/S[0] , 
                 SNormErr(S[1], S_err[1], S[0], S_err[0]) ,
                 SNormErr(S[2], S_err[2], S[0], S_err[0]) ,
                 SNormErr(S[3], S_err[3], S[0], S_err[0]) ])
    print('S/S0 = ', S_nor , '\n' ,'S/S0_err= ', S_nor_err , '\n')
    psi , psi_err = coef.psi(S[2] , S_err[2], S[1], S_err[1])
    chi , chi_err = coef.chi(S[3] , S_err[3], S[0], S_err[0])
    print('psi = ', psi, '\n', 'psi_err = ', psi_err,'\n')
    print('psi = ', chi, '\n', 'psi_err = ', chi_err,'\n')
    pol.esfera(S[0],S[1],S[2],S[3], save=f'{nombre}-esfera', titulo = nombre)
    pol.elipse(psi,abs(chi), save=f'{nombre}-elipse', titulo = nombre )

    S_todo[f'{nombre}'] = [S_nor,S_nor_err,psi , psi_err, chi , chi_err] 
    f = open(f'{nombre}-analisis',"w")
    f.write( str(S_todo) )
    f.close()
    