# Programa principal
# Christian Daniel Perez De Leon 19710

from gl import Renderer, V2
import numpy as np

width = 800
height = 600

rend = Renderer(width, height)

rend.glClearColor(0, 0, 0)
rend.glClear()

rend.glColor(1, 1, 1)

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

# Cuadrado
rend.glLine(V2(30,30), V2(30,210))
rend.glLine(V2(30,30), V2(210,30))
rend.glLine(V2(210,30), V2(210,210))
rend.glLine(V2(30,210), V2(210,210))

# Triangulo
rend.glLine(V2(30, 400),V2(120, 580))
rend.glLine(V2(30, 400),V2(210, 400))
rend.glLine(V2(120, 580),V2(210, 400))

# Pentagono
rend.glLine(V2(300, 30), V2(480, 30))
rend.glLine(V2(300, 30), V2(280, 120))
rend.glLine(V2(480, 30), V2(500, 120))
rend.glLine(V2(280, 120), V2(390, 210))
rend.glLine(V2(500, 120), V2(390, 210))

# Hexagono
rend.glLine(V2(320, 400), V2(460, 400))
rend.glLine(V2(320, 400), V2(280, 490))
rend.glLine(V2(460, 400), V2(500, 490))
rend.glLine(V2(280, 490), V2(320, 580))
rend.glLine(V2(500, 490), V2(460, 580))
rend.glLine(V2(320, 580), V2(460, 580))

# Casa
rend.glLine(V2(570, 30), V2(750, 30))
rend.glLine(V2(570, 30), V2(570, 120))
rend.glLine(V2(750, 30), V2(750, 120))
rend.glLine(V2(570, 120), V2(660, 210))
rend.glLine(V2(750, 120), V2(660, 210))
rend.glLine(V2(640, 30), V2(640, 80))
rend.glLine(V2(680, 30), V2(680, 80))
rend.glLine(V2(640, 80), V2(680, 80))
rend.glLine(V2(570, 120), V2(750, 120))

for x in range(575, 665, 5):
    
    y = x - 570
    x2 = 750 - y

    rend.glLine(V2(x, 120),V2(x, 120 + y))
    rend.glLine(V2(x2, 120), V2(x2, 120 + y))





rend.glFinish("poligonos.bmp")