# Programa principal
# Christian Daniel Perez De Leon 19710

from gl import Renderer, V2
import numpy as np

# width = 800
# height = 600

width = 940
height = 540

rend = Renderer(width, height)

Pol1=[(165, 380), (185, 360), (180, 330), (207, 345), (233, 330), (230, 360), (250, 380), (220, 385), (205, 410), (193, 383)]
Pol2=[(321, 335), (288, 286), (339, 251), (374, 302)]

Pol3=[(377, 249), (411, 197), (436, 249)]

Pol4=[(413, 177), (448, 159), (502, 88), (553, 53), (535, 36), (676, 37), (660, 52),
(750, 145), (761, 179), (672, 192), (659, 214), (615, 214), (632, 230), (580, 230),
(597, 215), (552, 214), (517, 144), (466, 180)]


Pol5=[(682, 175), (708, 120), (735, 148), (739, 170)]

for i in range(len(Pol1)):
    rend.glLine(V2(Pol1[i][0], Pol1[i][1]), V2(Pol1[(i+1) % len(Pol1)][0], Pol1[(i+1) % len(Pol1)][1]))

for i in range(len(Pol2)):
    rend.glLine(V2(Pol2[i][0], Pol2[i][1]), V2(Pol2[(i+1) % len(Pol2)][0], Pol2[(i+1) % len(Pol2)][1]))

# for i in range(len(Pol3)):
#     rend.glLine(V2(Pol3[i][0], Pol3[i][1]), V2(Pol3[(i+1) % len(Pol3)][0], Pol3[(i+1) % len(Pol3)][1]))

for i in range(len(Pol4)):
    rend.glLine(V2(Pol4[i][0], Pol4[i][1]), V2(Pol4[(i+1) % len(Pol4)][0], Pol4[(i+1) % len(Pol4)][1]))

for i in range(len(Pol5)):
    rend.glLine(V2(Pol5[i][0], Pol5[i][1]), V2(Pol5[(i+1) % len(Pol5)][0], Pol5[(i+1) % len(Pol5)][1]))

rend.glFillTriangleInv(V2(377, 249), V2(436, 249), V2(411, 197))




# for x in range(Pol3[0][0], Pol3[1][0]):
#     y = x - Pol3[0][0]
#     x2 = Pol3[2][0] - y
#     rend.glLine(V2(x,Pol3[0][1]), V2(x, Pol3[0][1] - y))


#y = x - 570
#     x2 = 750 - y

#     rend.glLine(V2(x, 120),V2(x, 120 + y))
#     rend.glLine(V2(x2, 120), V2(x2, 120 + y))


# rend.glClearColor(0, 0, 0)
# rend.glClear()

# rend.glColor(1, 1, 1)

# rend.glPoint(400,400)
# rend.glPoint(401,401)
# rend.glPoint(400,401)
# rend.glPoint(401,400)

# for x in range (150):
#     rend.glPoint(200 + x,200 + x)
#     rend.glPoint(200 + x,200)
#     rend.glPoint(200,200 + x)

# for x in range (150):
#     rend.glPoint(190 - x,190 - x)
#     rend.glPoint(190 - x,190)
#     rend.glPoint(190,190 - x)

# for x in range(0, width, 40):
#     rend.glLine(V2(0,0), V2(x,height))
#     rend.glLine(V2(0,height), V2(x,0))

#     rend.glLine(V2(width,0), V2(width - x,height))
#     rend.glLine(V2(width,height), V2(width - x,0))

# # Cuadrado
# rend.glLine(V2(30,30), V2(30,210))
# rend.glLine(V2(30,30), V2(210,30))
# rend.glLine(V2(210,30), V2(210,210))
# rend.glLine(V2(30,210), V2(210,210))

# # Triangulo
# rend.glLine(V2(30, 400),V2(120, 580))
# rend.glLine(V2(30, 400),V2(210, 400))
# rend.glLine(V2(120, 580),V2(210, 400))

# # Pentagono
# rend.glLine(V2(300, 30), V2(480, 30))
# rend.glLine(V2(300, 30), V2(280, 120))
# rend.glLine(V2(480, 30), V2(500, 120))
# rend.glLine(V2(280, 120), V2(390, 210))
# rend.glLine(V2(500, 120), V2(390, 210))

# # Hexagono
# rend.glLine(V2(320, 400), V2(460, 400))
# rend.glLine(V2(320, 400), V2(280, 490))
# rend.glLine(V2(460, 400), V2(500, 490))
# rend.glLine(V2(280, 490), V2(320, 580))
# rend.glLine(V2(500, 490), V2(460, 580))
# rend.glLine(V2(320, 580), V2(460, 580))

# # Casa
# rend.glLine(V2(570, 30), V2(750, 30))
# rend.glLine(V2(570, 30), V2(570, 120))
# rend.glLine(V2(750, 30), V2(750, 120))
# rend.glLine(V2(570, 120), V2(660, 210))
# rend.glLine(V2(750, 120), V2(660, 210))
# rend.glLine(V2(640, 30), V2(640, 80))
# rend.glLine(V2(680, 30), V2(680, 80))
# rend.glLine(V2(640, 80), V2(680, 80))
# rend.glLine(V2(570, 120), V2(750, 120))

# for x in range(575, 665, 5):
    
#     y = x - 570
#     x2 = 750 - y

#     rend.glLine(V2(x, 120),V2(x, 120 + y))
#     rend.glLine(V2(x2, 120), V2(x2, 120 + y))

# rend.glLoadModel('guitar.obj', V2(width/2, height/3), V2(100, 100))



rend.glFinish("Lab1.bmp")