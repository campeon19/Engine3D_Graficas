# Programa principal
# Christian Daniel Perez De Leon 19710

from gl import Renderer, V2, V3, _color
from obj import Texture
from shaders import *

width = 940
height = 540

rend = Renderer(width, height)


rend.active_shader = flat
rend.active_texture = Texture('Modelos/model.bmp')
modelPosition = V3(0,0,-5)

rend.glLookAt(modelPosition, V3(3,1,0))

rend.glLoadModel('Modelos/model.obj', modelPosition, V3(2,2,2), V3(-15,0,0))

rend.glFinish("Resultados/Ejercicio5.bmp")