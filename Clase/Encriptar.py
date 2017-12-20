from modules import mydes
#Definicion de variables
My_des = mydes.MyDES()
MenBin = []; ClavBin = []
C0 = []; D0 = []; L0 = []
R0 = []; K = []
E = []; X = []; Zint = []
Zfinal = []; frK = [];
VI =  []; MenEncripFinal = []
clave   = "0123456789ABCDEF"
Mensaje = "0123456789ABCDEF"

def shift(l, n):
    return l[n:] + l[:n]

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
def ConvBin(clave,round, ClavBin, c1, d1, VI):
    del VI[:]
    #Pasamos los numeros en Hexa de la clave a binario
    if round == 0:
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





#def mApply(input,matriz):
  #  for i in range (len(matriz))
  #  result[i] = [0]*len(input)
  #  result = input[matriz[i]]

#def matrix_apply(input, matrix):
 #   output = [0] * len(matrix)
  #  for cont in range(len(matrix)):
    #    output[cont] = input[matrix[cont]]
   # return output


def OperDatos(Mensaje, L0, R0, frK):
    if round == 0:
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
        varInt= R0
        R0 = XOR(L0,frK)
        L0 = varInt

        return L0,R0

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
        Sfila = int(Zint[y]) + int(Zint[y+5])
        print "Fila", Sfila
        Scolumna = 8*int(Zint[y+1]) + 4*int(Zint[y+2]) + 2*int(Zint[y+3]) + int(Zint[y+4])
        print "Columna", Scolumna
        z3 = My_des.STablas[xs][Sfila][Scolumna]
        print "Valor Tabla", z3,"\n"
        y = y+6
        xs=xs+1
        f=bin(z3)
        f= f[2:].zfill(4)
        for i in f:
            Zfinal.append(i)
    for i in My_des.PTable:
        frK.append(Zfinal[i - 1])
    del Zfinal[:]
    return frK

def PasoFinal(L0,R0,MenEncripFinal):
    k1= R0 + L0
    for j in My_des.IP1:
        MenEncripFinal.append(k1[j - 1])
    return MenEncripFinal

c1=0
d1=0
for round in range(16):
    L0, R0 = OperDatos(Mensaje, L0, R0, frK)
    VI,c1,d1 = ConvBin(clave, round, ClavBin, c1, d1, VI)
    frK = OperDatos2(VI, R0,frK)
round = round +1
L0,R0 = OperDatos(Mensaje, L0, R0, frK)
MenEncripFinal= PasoFinal(L0,R0,MenEncripFinal)
Fin = ''.join(MenEncripFinal)
Fin = hex(int(Fin,2))
print Fin[2:]

