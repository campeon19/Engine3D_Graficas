# Programa principal
# Christian Daniel Perez De Leon 19710

from gl import Renderer, V2

# width = 800
# height = 600

width = 940
height = 540

# width = 100
# height = 100

rend = Renderer(width, height)

Pol1=[(165, 380), (185, 360), (180, 330), (207, 345), (233, 330), (230, 360), (250, 380), (220, 385), (205, 410), (193, 383)]
Pol2=[(321, 335), (288, 286), (339, 251), (374, 302)]

Pol3=[(377, 249), (411, 197), (436, 249)]

Pol4=[(413, 177), (448, 159), (502, 88), (553, 53), (535, 36), (676, 37), (660, 52),
(750, 145), (761, 179), (672, 192), (659, 214), (615, 214), (632, 230), (580, 230),
(597, 215), (552, 214), (517, 144), (466, 180)]


Pol5=[(682, 175), (708, 120), (735, 148), (739, 170)]

rend.glDrawPolygon(Pol1)
rend.glDrawPolygon(Pol2)
rend.glDrawPolygon(Pol3)
rend.glDrawPolygon(Pol4)
rend.glDrawPolygon(Pol5)

rend.glScanLine()

rend.glLine(V2(181, 330),V2(232, 330), rend.glColor(0,0,0))
rend.glLine(V2(182, 331),V2(231, 331), rend.glColor(0,0,0))
rend.glLine(V2(412, 197),V2(543, 197), rend.glColor(0,0,0))
rend.glLine(V2(413, 198),V2(543, 198), rend.glColor(0,0,0))
rend.glLine(V2(428, 230),V2(579, 230), rend.glColor(0,0,0))
rend.glLine(V2(413, 180),V2(534, 180), rend.glColor(0,0,0))
rend.glLine(V2(533, 175),V2(761, 175), rend.glColor(1,1,1))
rend.glLine(V2(416, 175),V2(473, 175), rend.glColor(1,1,1))
rend.glLine(V2(459, 144),V2(696, 144), rend.glColor(1,1,1))
rend.glLine(V2(731, 144),V2(749, 144), rend.glColor(1,1,1))
rend.glLine(V2(182, 335),V2(189, 335), rend.glColor(1,1,1))
rend.glLine(V2(224, 335),V2(231, 335), rend.glColor(1,1,1))


rend.glFinish("Lab1.bmp")