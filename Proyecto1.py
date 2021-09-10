# Programa principal
# Christian Daniel Perez De Leon 19710

from gl import Renderer, V2, V3, _color
from obj import Texture
from shaders import *

width = 1920
height = 1080

rend = Renderer(width, height)

rend.background = Texture('Proyecto 1/Modelos/Background/opcion2.bmp')
rend.glClearBackground()

# --------------------------------------------------------------------------

rend.active_shader = transparencia
# rend.active_texture = Texture('Proyecto 1/Modelos/Boo/Boo_tex.bmp')
modelPosition = V3(-4,-2,-5)



rend.glLoadModel('Proyecto 1/Modelos/Boo/Boo.obj', 
                  modelPosition, 
                  V3(0.003,0.003,0.003), 
                  V3(0,160,0))


# --------------------------------------------------------------------------

rend.active_shader = flat
rend.active_texture = Texture('Proyecto 1/Modelos/Toad/Toad_tex.bmp')
modelPosition = V3(-4.5,-2.6,-8)



rend.glLoadModel('Proyecto 1/Modelos/Toad/Toad.obj', 
                  modelPosition, 
                  V3(0.008,0.008,0.008), 
                  V3(0,180,0))

# --------------------------------------------------------------------------

rend.active_shader = phong
rend.active_texture = Texture('Proyecto 1/Modelos/luigiD.bmp')
modelPosition = V3(0,-2.5,-5)



rend.glLoadModel('Proyecto 1/Modelos/luigi.obj', 
                  modelPosition, 
                  V3(0.01,0.01,0.01), 
                  V3(0,120,0))


# --------------------------------------------------------------------------

rend.active_shader = phong
rend.active_texture = Texture('Proyecto 1/Modelos/marioD.bmp')
modelPosition = V3(-2,-2.3,-5)



rend.glLoadModel('Proyecto 1/Modelos/mario.obj', 
                  modelPosition, 
                  V3(0.01,0.01,0.01), 
                  V3(0,-180,0))


# --------------------------------------------------------------------------

rend.active_shader = flat
rend.active_texture = Texture('Proyecto 1/Modelos/Bullet_Bill/Bullet_Bill_tex.bmp')
modelPosition = V3(-2,0,-8)



rend.glLoadModel('Proyecto 1/Modelos/Bullet_Bill/Bullet_Bill.obj', 
                  modelPosition, 
                  V3(0.001,0.001,0.001), 
                  V3(0,50,20))


# --------------------------------------------------------------------------

rend.active_shader = toon
rend.active_texture = Texture('Proyecto 1/Modelos/Extra Life/Extra_Life_tex.bmp')
modelPosition = V3(2.5,-2.5,-7)



rend.glLoadModel('Proyecto 1/Modelos/Extra Life/Extra_Life.obj', 
                  modelPosition, 
                  V3(0.015,0.015,0.015), 
                  V3(0,150,0))


# --------------------------------------------------------------------------

rend.active_shader = phong
rend.active_texture = Texture('Proyecto 1/Modelos/Koopa2/textures/Koopa_tex.bmp')
modelPosition = V3(3.7,-2,-6)



rend.glLoadModel('Proyecto 1/Modelos/Koopa2/source/Koopa.obj', 
                  modelPosition, 
                  V3(0.06,0.06,0.06), 
                  V3(0,90,0))

# --------------------------------------------------------------------------

rend.active_shader = glow
rend.active_texture = None
rend.curr_color = _color(215/255, 151/255, 10/255)
modelPosition = V3(1.5,0.5,-6)



rend.glLoadModel('Proyecto 1/Modelos/Star/Star.obj', 
                  modelPosition, 
                  V3(0.0025,0.0025,0.0025), 
                  V3(0,-40,0))


# --------------------------------------------------------------------------

rend.active_shader = normalMap
rend.active_texture = Texture('Proyecto 1/Modelos/Moon/Textures/Bump_2K.bmp')
rend.normal_map = Texture('Proyecto 1/Modelos/Moon/Textures/normal_map.bmp')
rend.curr_color = _color(1,1,1)
modelPosition = V3(-3.7,2,-6)



rend.glLoadModel('Proyecto 1/Modelos/Moon/Moon_2K.obj', 
                  modelPosition, 
                  V3(0.55,0.55,0.55), 
                  V3(0,90,0))


rend.glFinish("Proyecto 1/Resultado/Proyecto1.bmp")
