from modules import mydes
import binascii
#Definicion de variables
My_des = mydes.MyDES()
MenBin = []; ClavBin = []
C0 = []; D0 = []; L0 = []
R0 = []; K = []; Z=[]
E = []; X = []; Zint = []
Zfinal = []; frK = [];
VI =  []; MenEncripFinal = []
clave   = "4B45595F54455354"
Mensaje = "de722d82b237f17f"
c1=0;H = []
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

def VectorK(clave, round, ClavBin, c1, d1, VI,H):
    for w in range (16):

        #Pasamos los numeros en Hexa de la clave a binario
        if w == 0:


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
            Shift = My_des.ShiftT[w]
            del ClavBin[:]
            #Aplicamos el shifting izquierdo a C0 y D0, consiguiendo C1y D1
            c1 = shift(C0, Shift)
            d1 = shift(D0, Shift)
            k1 = c1 + d1

            for i in My_des.PC2:
                VI.append(k1[i - 1])
            Z.append(VI)


        else:

            Shift = My_des.ShiftT[w]
            # Aplicamos el shifting izquierdo a C0 y D0, consiguiendo C1y D1
            c1 = shift(c1, Shift)
            d1 = shift(d1, Shift)
            k1 = c1 + d1
            for i in My_des.PC2:
                VI.append(k1[i - 1])
            Z.append(VI)
    H=VI
    return H






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

H= VectorK(clave, round, ClavBin, c1, d1, VI,H)
V1=H[0:48]
V2=H[48:96]
V3=H[96:144]
V4=H[144:192]
V5=H[192:240]
V6=H[240:288]
V7=H[288:336]
V8=H[336:384]
V9=H[384:432]
V10=H[432:480]
V11=H[480:528]
V12=H[528:576]
V13=H[576:624]
V14=H[624:672]
V15=H[672:720]
V16=H[720:768]
for round in range(16):
    if round == 0:
        VI= V16
    elif round == 1:
        VI= V15
    elif round == 2:
        VI= V14
    elif round == 3:
        VI= V13
    elif round == 4:
        VI= V12
    elif round == 5:
        VI= V11
    elif round == 6:
        VI = V10
    elif round == 7:
        VI = V9
    elif round == 8:
        VI = V8
    elif round == 9:
        VI = V7
    elif round == 10:
        VI = V6
    elif round == 11:
        VI = V5
    elif round == 12:
        VI = V4
    elif round == 13:
        VI = V3
    elif round == 14:
        VI = V2
    elif round == 15:
        VI = V1

    L0, R0 = OperDatos(Mensaje, L0, R0, frK)

    frK = OperDatos2(VI, R0,frK)

round = round +1
L0,R0 = OperDatos(Mensaje, L0, R0, frK)
MenEncripFinal= PasoFinal(L0,R0,MenEncripFinal)
Fin = ''.join(MenEncripFinal)
Fin = int(Fin,2)
Fin = hex(Fin).strip('L')
Fin = Fin[2:]
if len(Fin) < 16:
    Fin = Fin.zfill(16)
print "El mensaje desencriptado es:", Fin


