from modules import mydes
#Definicion de variables
My_des = mydes.MyDES()
Array = []
C0 = []; D0 = []; L0 = []
R0 = []; K = []
E = []; X = []; Zint = []
Zfinal = []; MenEncr = []
clave = "0123456789ABCDEF"
Mensaje = "0123456789ABCDEF"
def shift(l, n):
    return l[n:] + l[:n]
def ConvBin(clave,round, Array):
    #Pasamos los numeros en Hexa de la clave a binario
    if round == 0:
        for i in clave:
            letra = bin(int(i, 16))
            letra = letra[2:].zfill(4)
            for j in letra:
                Array.append(j)
        for i in My_des.PC1[:28]:
            C0.append(Array[i - 1])
        for i in My_des.PC1[28:]:
            D0.append(Array[i - 1])
    else:
        print Array
        print C0
        print D0
        del Array[:]
        Array = C0 + D0
        del C0[:]; del D0[:]
        #Aplicamos PC1 para obtener C0 Y D0


    #Cogemos el valor del shifting que nos toca de la tabla
    Shift = My_des.ShiftT[round]

    #Aplicamos el shifting izquierdo a C0 y D0, consiguiendo C1y D1
    c1 = shift(C0, Shift)
    d1 = shift(D0, Shift)
    k1 = c1 + d1
    print C0
    for i in My_des.PC2:
        K.append(k1[i - 1])
    return K

def OperDatos(Mensaje):
    # Pasamos los numeros en Hexa deL mensaje a binario
    for i in Mensaje:
        letra = bin(int(i, 16))
        letra = letra[2:].zfill(4)
        for i in letra:
            Array.append(i)
    #Tras pasarlo a binario y ponerlo en un Array, aploicamos IP
    for i in My_des.IP[:32]:
        L0.append(Array[i - 1])
    for i in My_des.IP[32:]:
        R0.append(Array[i - 1])

def OperDatos2(K,R0):
    #Expando R0
    for i in My_des.ETable:
        E.append(R0[i - 1] )
    #Suma XOR de R0 Expandido y K
    for x in range(0, len(E)):
        num = int(E[x]) + int(K[x])
        if num==0 or num ==2:
            X.append(0)
        elif num==1:
            X.append(1)
    y=0
    xs=0
    while xs <8:
        for x in range (y,y+6):
            Zint.append(X[x])
        z1 = int(Zint[y]) + int(Zint[y+5])
        z2 = 8*int(Zint[y+1]) + 4*int(Zint[y+2]) + 2*int(Zint[y+3]) + int(Zint[y+4])
        z3 = My_des.STablas[xs][z1][z2]
        y = y+6
        xs=xs+1
        f=bin(z3)
        f= f[2:].zfill(4)
        for i in f:
            Zfinal.append(i)
    for i in My_des.PTable:
        MenEncr.append(Zfinal[i - 1])


def vaciarVariables():
    del L0[:]; del R0[:]; del Array[:]
    del K[:]; del X[:]; del Zint[:]
    del E[:]


for round in range(16):
    ConvBin(clave,round, Array)
    OperDatos(Mensaje)
    OperDatos2(K, R0)
    vaciarVariables()


