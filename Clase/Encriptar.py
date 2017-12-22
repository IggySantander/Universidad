from modules import mydes
#Definicion de variables
My_des = mydes.MyDES()
MenBin = []; ClavBin = []
C0 = []; D0 = []; L0 = []
R0 = []; K = []
E = []; X = []; Zint = []
Zfinal = []; frK = [];
VI =  []; MenEncripFinal = []
clave   = "123456ABCD789EF0"
Mensaje = "123456ABCD789EF0"
c1=0
d1=0


#Hace el shifting
def shift(l, n):
    return l[n:] + l[:n]


#Funcion que hace la XOR de dos arrays
def XOR(Array1, Array2):
    Array3 = []
    del Array3[:]
    for x in range(0, len(Array1)):
        num = int(Array1[x]) + int(Array2[x])
        if num == 0 or num == 2:
            Array3.append('0')
        elif num == 1:
            Array3.append('1')
    return Array3


#Funcion que nos da la KI en cada iteraccion
def ConvBin(clave,round, ClavBin, c1, d1, VI):
    del VI[:]
    #Pasamos los numeros en Hexa de la clave a binario
    if round == 0:
        #Rellenamos con ceros si la clave no llega a 16 elementos
        clave= clave.zfill(16)
        for i in clave:
            letra = bin(int(i, 16))
            letra = letra[2:].zfill(4)
            for j in letra:
                ClavBin.append(j)
        # Aplicamos PC1 para obtener C0 Y D0
        for i in My_des.PC1[:28]:
            C0.append(ClavBin[i - 1])
        for i in My_des.PC1[28:]:
            D0.append(ClavBin[i - 1])
        #Cogemos el valor del shifting que nos toca de la tabla/
        Shift = My_des.ShiftT[round]
        del ClavBin[:]
        #Aplicamos el shifting izquierdo a C0 y D0, consiguiendo C1y D1
        c1 = shift(C0, Shift)
        d1 = shift(D0, Shift)
        k1 = c1 + d1

        for i in My_des.PC2:
            VI.append(k1[i - 1])
        return VI,c1,d1
    else:

        Shift = My_des.ShiftT[round]
        # Aplicamos el shifting izquierdo a C0 y D0, consiguiendo C1y D1
        c1 = shift(c1, Shift)
        d1 = shift(d1, Shift)
        k1 = c1 + d1
        for i in My_des.PC2:
            VI.append(k1[i - 1])
        return VI,c1,d1

#Funcion que nos da L0 Y R0 en cada iteraccion
def OperDatos(Mensaje, L0, R0, frK):
    if round == 0:
        #Rellenamos con ceros si el mensaje no tiene 16 elementos
        Mensaje = Mensaje.zfill(16)
        # Pasamos los numeros en Hexa deL mensaje a binario
        for i in Mensaje:
            letra = bin(int(i, 16))
            letra = letra[2:].zfill(4)
            for j in letra:
                MenBin.append(j)
        #Tras pasarlo a binario y ponerlo en un Array, aploicamos IP
        for i in My_des.IP[:32]:
            L0.append(MenBin[i - 1])
        for i in My_des.IP[32:]:
            R0.append(MenBin[i - 1])
        del MenBin[:]

        return L0,R0

    else:
        #Conseguir L0 y R0 despues de la primera iteraccion
        varInt= R0
        R0 = XOR(L0,frK)
        L0 = varInt

        return L0,R0

#Funcion que nos da frK en cada iteraccion, para luego sumarselo a la XOR

def OperDatos2(VI,R0, frK):
    #Expando R0
    del frK[:]
    del Zfinal[:]
    del Zint[:]
    del E[:]
    for i in My_des.ETable:
        E.append(R0[i - 1] )
    #Suma XOR de R0 Expandido y K
    X = XOR(E,VI)
    y=0
    xs=0
    while xs <8:
        for x in range (y,y+6):
            Zint.append(X[x])
        Sfila = 2*int(Zint[y]) + int(Zint[y+5])
        #Calcula la fila que toca
        Scolumna = 8*int(Zint[y+1]) + 4*int(Zint[y+2]) + 2*int(Zint[y+3]) + int(Zint[y+4])
        #Calcula la columna que toca
        z3 = My_des.STablas[xs][Sfila][Scolumna]
        #Coge el valor, de la tabla, fila y columna correspondiente
        y = y+6
        xs=xs+1
        f=bin(z3)
        f= f[2:].zfill(4)
        #Convierte a binario
        for i in f:
            Zfinal.append(i)
        #Pone todos los resultados de las puertas S en binario en el array Zfina
    for i in My_des.PTable:
        frK.append(Zfinal[i - 1])
    #Aplico permutacion a Zfinal,y consigo frk
    del Zfinal[:]
    return frK

#Cojo el vector final y lo permuto
def PasoFinal(L0,R0,MenEncripFinal):
    k1= R0 + L0
    for j in My_des.IP1:
        MenEncripFinal.append(k1[j - 1])
    return MenEncripFinal



##############################################
#
#
#       Programa principal
#
#
##############################################


for round in range(16):
    L0, R0 = OperDatos(Mensaje, L0, R0, frK)
    VI,c1,d1 = ConvBin(clave, round, ClavBin, c1, d1, VI)
    frK = OperDatos2(VI, R0,frK)

round = round +1
L0,R0 = OperDatos(Mensaje, L0, R0, frK)
MenEncripFinal= PasoFinal(L0,R0,MenEncripFinal)
Fin = ''.join(MenEncripFinal)
Fin = hex(int(Fin,2))
print "El resultado final encriptado es: ", Fin[2:]

