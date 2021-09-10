# Programa principal
# Christian Daniel Perez De Leon 19710

from gl import Renderer, V2, V3, _color
from obj import Texture
from shaders import *

width = 940
height = 540

rend = Renderer(width, height)

# rend.background = Texture('Fondos/fondo.bmp')
# rend.glClearBackground()

# rend.active_shader = shader1
# rend.active_texture = Texture('Modelos/model.bmp')
# modelPosition = V3(-3,1.3,-5)



# rend.glLoadModel('Modelos/model.obj', 
#                   modelPosition, 
#                   V3(1.2,1.2,1.2), 
#                   V3(0,0,0))

# rend.active_shader = toon
# rend.active_texture = Texture('Modelos/model.bmp')
# modelPosition = V3(0,1.3,-5)



# rend.glLoadModel('Modelos/model.obj', 
#                   modelPosition, 
#                   V3(1.2,1.2,1.2), 
#                   V3(0,0,0))

# rend.active_shader = shader2
# rend.active_texture = Texture('Modelos/model.bmp')
# modelPosition = V3(3,1.3,-5)



# rend.glLoadModel('Modelos/model.obj', 
#                   modelPosition, 
#                   V3(1.2,1.2,1.2), 
#                   V3(0,0,0))

# rend.active_shader = shader3
# rend.active_texture = Texture('Modelos/model.bmp')
# modelPosition = V3(-3,-1.2,-5)



# rend.glLoadModel('Modelos/model.obj', 
#                   modelPosition, 
#                   V3(1.2,1.2,1.2), 
#                   V3(0,0,0))

# rend.active_shader = glow
# rend.active_texture = Texture('Modelos/model.bmp')
# modelPosition = V3(0,-1.2,-5)



# rend.glLoadModel('Modelos/model.obj', 
#                   modelPosition, 
#                   V3(1.2,1.2,1.2), 
#                   V3(0,0,0))

# rend.active_shader = shader4
# rend.active_texture = Texture('Modelos/model.bmp')
# modelPosition = V3(3,-1.2,-5)



# rend.glLoadModel('Modelos/model.obj', 
#                   modelPosition, 
#                   V3(1.2,1.2,1.2), 
#                   V3(0,0,0))


rend.active_shader = transparencia
rend.active_texture = Texture('Modelos/model.bmp')
modelPosition = V3(0,0,-5)



rend.glLoadModel('Modelos/model.obj', 
                  modelPosition, 
                  V3(2.5,2.5,2.5), 
                  V3(0,0,0))


# rend.glLookAt(modelPosition, V3(0,4,2))

# rend.active_shader = phong
# # rend.active_texture = Texture('Modelos/New_Albedo.bmp')
# rend.active_texture = Texture('Modelos/New_AmbientOcclusion.bmp')
# modelPosition = V3(0,0,-4)
# # rend.directional_light = V3(0,0,0)

# rend.glLookAt(modelPosition, V3(0,5,0))

# rend.glLoadModel('Modelos/laptop.obj', modelPosition, V3(7,7,7), V3(20,35,0))

rend.glFinish("Resultados/Pruebas2.bmp")