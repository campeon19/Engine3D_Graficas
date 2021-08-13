# Programa principal
# Christian Daniel Perez De Leon 19710

from gl import Renderer, V2, V3
from obj import Texture

# width = 800
# height = 600

width = 940
height = 540

# width = 100
# height = 100

rend = Renderer(width, height)
textura = Texture('Modelos/model.bmp')

rend.glLoadModel('Modelos/model.obj', textura, V3(width/2, height/2, 0), V3(200,200,200))

rend.glFinish("Resultados/Ejercicio4.bmp")