# Christian Daniel Perez De Leon 19710
# Libreria de matematica propia

import sys

pi = 3.14159265359

def restaVect(vec1, vec2):
    respuesta = []
    for x in range(len(vec1)):
        res = vec1[x] - vec2[x]
        respuesta.append(res)
    return respuesta

def productoPunto(vec1, vec2):
    respuesta = 0
    for x in range(len(vec1)):
        res = vec1[x] * vec2[x]
        respuesta += res
    return respuesta

def productoCruz3D(vec1, vec2):
    res = [vec1[1]*vec2[2] - vec1[2]*vec2[1],
            vec1[2]*vec2[0] - vec1[0]*vec2[2],
            vec1[0]*vec2[1] - vec1[1]*vec2[0]]
    return res

def normalizar3D(vector):  
    magnitud = raizCuadrada(vector[0] * vector[0] + vector[1] * vector[1] + vector[2] * vector[2])
    respuesta = [vector[0] / magnitud,
                    vector[1] / magnitud,
                    vector[2] / magnitud]
    return respuesta

def raizCuadrada(valor):
    resultado = valor ** 0.5
    return resultado

def gradosARadianes(val):
    resultado = val * pi / 180
    return resultado

def multMatrices3x3(matriz1, matriz2):
    
    resultado = [[0,0,0],
                 [0,0,0],
                 [0,0,0]]
    
    for i in range(len(matriz1)):    
        for j in range(len(matriz2[0])):        
            for k in range(len(matriz2)):
                resultado[i][j] += matriz1[i][k] * matriz2[k][j]    
    
    return resultado

def multMatrices4x4(matriz1, matriz2):
    
    resultado = [[0,0,0,0],
                 [0,0,0,0],
                 [0,0,0,0],
                 [0,0,0,0]]
    
    for i in range(len(matriz1)):    
        for j in range(len(matriz2[0])):        
            for k in range(len(matriz2)):
                resultado[i][j] += matriz1[i][k] * matriz2[k][j]    
    
    return resultado

def multMatrices4xVec(matriz, vector):
    resultado = []

    for i in range(4):
        res1 = 0
        for j in range(4):
            res1 += matriz[i][j] * vector[j]
        resultado.append(res1)
    return resultado


def matrizInv(matriz):
    n = len(matriz)
    m = matriz
    
    # matriz aumentada con la matriz identidad
    for i in range(n):
        for j in range(n):
            if i == j:
                m[i].append(1)
            else:
                m[i].append(0)

    # Gauss Jordan Elimination
    for i in range(n):
        if m[i][i] == 0.0:
            sys.exit('Division por cero')
        
        for j in range(n):
            if i != j:
                ratio = m[j][i]/m[i][i]

                for k in range(2*n):
                    m[j][k] = m[j][k] - ratio * m[i][k]

    # Operacion en las filas para convertir la diagonal principal en 1
    for i in range(n):
        divisor = m[i][i]
        for j in range(2*n):
            m[i][j] = m[i][j]/divisor

    # Guardar matriz

    resultado = [[] for _ in range(n)]
    for i in range(n):
        for j in range(n, 2*n):
            resultado[i].append(m[i][j])

    
    return resultado


def valAbsoluto(valor):
    if valor < 0:
        valor *= -1
        return valor
    else:
        return valor




