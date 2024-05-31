import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
 
def esfera(s0,s1,s2,s3,**args):  
    fig = plt.figure()

    ax1 = fig.add_subplot(111, projection='3d')

    u, v = np.mgrid[0:2*np.pi:100j, 0:np.pi:100j]

    x=np.cos(u)*np.sin(v)
    y=np.sin(u)*np.sin(v)
    z=np.cos(v)
    ax1.plot_wireframe(x, y, z, rstride = 10, cstride = 10, linewidth = 1.5, color = 'm', alpha = 0.3)


    ax1.quiver(0, 0, 0, s1/s0 , s2/s0, s3/s0,color='k', linewidth=1.5) 
    ax1.set_xlabel('$S_1$')
    ax1.set_ylabel('$S_2$')
    ax1.set_zlabel('$S_3$')
    if 'titulo' in args:
        plt.title(args['titulo'])
    else:
        plt.title(f'Esfera para $S =${[round(s0,2),round(s1,2),round(s2,2),round(s3,2)]}')
    if 'save' in args:
        plt.savefig(args['save'])
    plt.show()
    
def elipse(psi, chi, **args):
    a = 1.       #radius on the x-axis
    b = a*np.tan(chi)     #radius on the y-axis

    t = np.linspace(0, 2*np.pi, 100)
    Ell = np.array([a*np.cos(t) , b*np.sin(t)])  
     #u,v removed to keep the same center location
    R_rot = np.array([[np.cos(psi) , -np.sin(psi)],[np.sin(psi) , np.cos(psi)]])  
     #2-D rotation matrix

    Ell_rot = np.zeros((2,Ell.shape[1]))
    for i in range(Ell.shape[1]):
        Ell_rot[:,i] = np.dot(R_rot,Ell[:,i])
    # use set_position
    ax = plt.gca()
    ax.spines['top'].set_color('none')
    ax.spines['left'].set_position('zero')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_position('zero')
    plt.plot( Ell_rot[0,:] , Ell_rot[1,:],'darkorange' )    #rotated ellipse
    plt.grid(color='lightgray',linestyle='--')
    plt.xlim(-1.05,1.05)
    plt.ylim(-1.05,1.05)
    plt.xticks([-1, -0.5, 0.5,1], [-1, -0.5, 0.5,1])
    plt.yticks([-1, -0.5, 0.5,1], [-1, -0.5, 0.5,1])
    if 'titulo' in args:
        plt.title(args['titulo'])
    else:
        plt.title(f'Elipse para $\psi =${round(psi,2)} y $\chi =${round(chi,2)} ')
    if 'save' in args:
        plt.savefig(args['save'])
    plt.show()
    
def esferaTODO(X,Y,Z, **args):
    #parametros para dibujar la esfera
    u, v = np.mgrid[0:2*np.pi:100j, 0:np.pi:100j]

    x=np.cos(u)*np.sin(v)
    y=np.sin(u)*np.sin(v)
    z=np.cos(v)

    #Set colours and render
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.plot_wireframe(x, y, z, rstride = 10, cstride = 10, linewidth = 1.5, color = 'm', alpha = 0.2) # superficie esfera grillada
    #ax.plot_surface(x, y, z,  rstride=1, cstride=1, color='c', alpha=0.3, linewidth=0) #superficie esfera solida 
    colores = ['b','b','g','g','c','c','m','m','y','y']

    ax.scatter(X,Y,Z,color="k",s=10)


    ax.set_xlim([-1,1])
    ax.set_ylim([-1,1])
    ax.set_zlim([-1,1])
    ax.set_aspect("auto")
    ax.set_xlabel('$S_1$')
    ax.set_ylabel('$S_2$')
    ax.set_zlabel('$S_3$')
    plt.title('Parámetros de Stokes sobre esfera de Poincaré')
    plt.tight_layout()
    plt.savefig(args['save'])
    plt.show()