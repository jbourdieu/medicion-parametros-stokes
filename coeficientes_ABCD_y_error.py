import numpy as np

def A( N , I_n ):
    a = 2 / N
    suma = 0
    I_max = np.max(I_n)
    for i in range(N):
        suma += I_n[i]/I_max
    return suma * a

def B(N , I_n , theta):
    a = 4 / N
    suma = 0
    I_max = np.max(I_n)
    for i in range(N):
        suma += I_n[i] * np.sin(2*theta[i]*np.pi/180)/I_max
    return suma * a

def C(N , I_n , theta):
    a = 4 / N
    suma = 0
    I_max = np.max(I_n)
    for i in range(N):
        suma += I_n[i] * np.cos(4*theta[i]*np.pi/180)/I_max
    return suma * a

def D(N , I_n , theta):
    a = 4 / N
    suma = 0
    I_max = np.max(I_n)
    for i in range(N):
        suma += I_n[i] * np.sin(4*theta[i]*np.pi/180)/I_max
    return suma * a
    
def A_err(N , I_n , I_err ):
    a = 2 / N
    suma1 = 0
    suma2 = 0
    I_max = np.max(I_n)
    i_max = np.argmax(I_n)
    for i in range(N):
        suma1 += ( I_err[i] / I_max )**2 
        suma2 += ( I_n[i] * I_err[i_max] / ( I_max **2 ) ) **2
    return np.sqrt( suma1 + suma2 ) * a

def B_err(N , I_n , I_err , theta , theta_err):
    a = 4 / N
    suma1 = 0
    suma2 = 0
    suma3 = 0   
    I_max = np.max(I_n)
    i_max = np.argmax(I_n)
    for i in range(N):
        suma1 += ( I_err[i] * np.sin( 2*theta[i]*np.pi/180 ) / I_max ) **2 
        suma2 += ( ( ( I_n[i] * np.sin( 2*theta[i]*np.pi/180 ) *  I_err[i_max]) ) / ( I_max**2 ) ) **2 
        suma3 += ( ( ( 2 * I_n[i] * np.cos( 2*theta[i]*np.pi/180) * theta_err[i]*np.pi/180) ) / ( I_max ) ) **2
    return np.sqrt( suma1 + suma2 + suma3 ) * a

def C_err(N , I_n , I_err , theta , theta_err):
    a = 4 / N
    suma1 = 0
    suma2 = 0
    suma3 = 0   
    I_max = np.max(I_n)
    i_max = np.argmax(I_n)
    for i in range(N):
        suma1 += ( I_err[i] * np.cos( 4*theta[i]*np.pi/180 ) / I_max ) **2 
        suma2 += ( ( ( I_n[i] * np.cos( 4*theta[i]*np.pi/180 ) *  I_err[i_max]) ) / ( I_max**2 ) ) **2 
        suma3 += ( ( ( 4 * I_n[i] * np.sin( 4*theta[i]*np.pi/180) * theta_err[i]*np.pi/180) ) / ( I_max ) ) **2
    return np.sqrt( suma1 + suma2 + suma3 ) * a

def D_err(N , I_n , I_err , theta , theta_err):
    a = 4 / N
    suma1 = 0
    suma2 = 0
    suma3 = 0
    I_max = np.max(I_n)
    i_max = np.argmax(I_n)
    for i in range(N):
        suma1 += ( I_err[i] * np.sin( 4*theta[i]*np.pi/180 ) / I_max ) **2 
        suma2 += ( ( ( I_n[i] * np.sin( 4*theta[i]*np.pi/180 ) *  I_err[i_max]) ) / ( I_max**2 ) ) **2 
        suma3 += ( ( ( 4 * I_n[i] * np.cos( 4*theta[i]*np.pi/180) * theta_err[i]*np.pi/180) ) / ( I_max ) ) **2
    return np.sqrt( suma1 + suma2 + suma3 ) * a

def S( N , I_n , I_err , theta , theta_err):
    S_0 = [ ( A(N , I_n ) - C(N , I_n , theta) ) , np.sqrt(A_err(N , I_n , I_err )**2 + C_err(N , I_n , I_err , theta , theta_err)**2) ]
    S_1 = [ 2*C(N , I_n , theta) , 2 * C_err(N , I_n , I_err , theta , theta_err) ]
    S_2 = [ 2 * D(N , I_n , theta) , 2 * D_err(N , I_n , I_err , theta , theta_err) ]
    S_3 = [ B(N , I_n , theta) , B_err(N , I_n , I_err , theta , theta_err) ]
    S = np.array([S_0[0] , S_1[0] , S_2[0] , S_3[0]])
    S_err = np.array([S_0[1] , S_1[1] , S_2[1] , S_3[1]])
    return(S,S_err)

def psi( s2 , s2_err, s1 , s1_err ):
    PSI = 0.5*np.arctan(s2/s1)
    a = (s2_err / ( ( s2 / s1 ) **2 + 1) * s1 ) **2
    b = (s2 * s1_err / ( ( s2 / s1 )**2 + 1 ) * (s1 **2) ) **2
    PSI_e = 0.5*np.sqrt(a+b)
    return(PSI,PSI_e) 
def chi( s3 , s3_err , s0 , s0_err  ):
    CHI = 0.5*np.arcsin(s3/s0)
    a = (s3_err / ( 1 - ( s3 / s0 ) **2 ) * s0 ) **2
    b = (s3 * s0_err / ( 1 - ( s3 / s0 )**2 ) * (s0 **2) ) **2
    CHI_e =  0.25*np.sqrt(a+b)
    return(CHI,CHI_e) 