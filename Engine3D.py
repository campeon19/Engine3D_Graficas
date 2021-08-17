# Programa principal
# Christian Daniel Perez De Leon 19710

from gl import Renderer, V2, V3
from obj import Texture

width = 940
height = 540

rend = Renderer(width, height)
textura = Texture('Modelos/model.bmp')
modelPosition = V3(0,0,-5)

rend.glLookAt(modelPosition, V3(3,1,0))

rend.glLoadModel('Modelos/model.obj', textura, modelPosition, V3(2,2,2), V3(-15,0,0))

rend.glFinish("Resultados/Ejercicio5.bmp")