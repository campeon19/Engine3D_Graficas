# Programa principal
from gl import Renderer

width = 500
height = 500

rend = Renderer(width, height)

rend.glClearColor(0, 0, 0)
rend.glClear()

rend.glColor(1, 1, 1)

rend.glPoint(400,400)
rend.glPoint(401,401)
rend.glPoint(400,401)
rend.glPoint(401,400)

for x in range (150):
    rend.glPoint(200 + x,200 + x)
    rend.glPoint(200 + x,200)
    rend.glPoint(200,200 + x)

for x in range (150):
    rend.glPoint(190 - x,190 - x)
    rend.glPoint(190 - x,190)
    rend.glPoint(190,190 - x)





rend.glFinish("output.bmp")