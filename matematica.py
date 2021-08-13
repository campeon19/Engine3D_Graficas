# Christian Daniel Perez De Leon 19710
# Libreria de matematica propia

# Se utiliza la libreria math unicamente para utilizar la operacion de raiz cuadrada
import math

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
    magnitud = math.sqrt(vector[0] * vector[0] + vector[1] * vector[1] + vector[2] * vector[2])
    respuesta = [vector[0] / magnitud,
                    vector[1] / magnitud,
                    vector[2] / magnitud]
    return respuesta


