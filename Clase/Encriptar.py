from modules import mydes

My_des = mydes.MyDES()
Array = []
C0 = []
D0 = []
L0 = []
R0 = []
K = []
Key = []
E = []
clave = "0123456789ABCDEF"
Mensaje = "0123456789ABCDEF"
def shift(l, n):
    return l[n:] + l[:n]
def ConvBin(clave):
    #Pasamos los numeros en Hexa de la clave a binario
    for i in clave:
        letra = bin(int(i, 16))
        letra = letra[2:].zfill(4)
        for i in letra:
            Array.append(i)
    #Aplicamos PC1 para obtener C0 Y D0
    for i in My_des.PC1[:28]:
        C0.append(Array[i - 1])
    for i in My_des.PC1[28:]:
        D0.append(Array[i - 1])

    #Cogemos el valor del shifting que nos toca de la tabla
    Shift = My_des.ShiftT[1]

    #Aplicamos el shifting izquierdo a C0 y D0, consiguiendo C1y D1
    c1 = shift(C0, Shift)
    d1 = shift(D0, Shift)
    k1 = c1 + d1

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
    Key = L0 + R0
    return Key

def OperDatos2(K,Key,R0):
    #Expando R0
    for i in My_des.ETable:
        E.append(R0[i - 1] )
    E1 = bin(int(''.join(map(str, E)), 2) << 1)
    E1 = E1[2:].zfill(4)


    C='100010'

    D='101001'
    print int(C,2) + int(D,2)
ConvBin(clave)
OperDatos(Mensaje)
OperDatos2(K, Key, R0)




