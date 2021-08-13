# Christian Daniel Perez De Leon 19710

import struct
from collections import namedtuple
from obj import Obj
import numpy as np
import matematica as mate

V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])



def char(c):
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    return struct.pack('=h', w)

def dword(d):
    return struct.pack('=l', d)

def _color(r, g, b):
    return bytes([ int(b * 255), int(g* 255), int(r* 255)])

def baryCoords(A, B, C, P):
    # u es para A, v es para B, w es para C
    try:
        #PCB/ABC
        u = (((B.y - C.y) * (P.x - C.x) + (C.x - B.x) * (P.y - C.y)) /
            ((B.y - C.y) * (A.x - C.x) + (C.x - B.x) * (A.y - C.y)))

        #PCA/ABC
        v = (((C.y - A.y) * (P.x - C.x) + (A.x - C.x) * (P.y - C.y)) /
            ((B.y - C.y) * (A.x - C.x) + (C.x - B.x) * (A.y - C.y)))

        w = 1 - u - v
    except:
        return -1, -1, -1

    return u, v, w

BLACK = _color(0,0,0)
WHITE = _color(1,1,1)


class Renderer(object):
    def __init__(self, width, height):
        self.curr_color = WHITE
        self.clear_color = BLACK
        self.glCreateWindow(width, height)

    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
        self.glClear()
        self.glViewport(0,0, width, height)

    def glViewport(self, x, y, width, height):
        self.vpX = x
        self.vpY = y
        self.vpWidth = width
        self.vpHeight = height


    def glClearColor(self, r, g, b):
        self.clear_color = _color(r, g, b)

    def glClear(self):
        self.pixels = [[ self.clear_color for y in range(self.height)] for x in range(self.width)]

        self.zbuffer = [[ -float('inf') for y in range(self.height)] for x in range(self.width)]


    def glColor(self, r, g, b):
        self.curr_color = _color(r,g,b)


    def glPoint(self, x, y, color = None):
        if x < self.vpX or x >= self.vpX + self.vpWidth or y < self.vpY or y >= self.vpY + self.vpHeight:
            return

        if (0 < x < self.width) and (0 < y < self.height):
            self.pixels[int(x)][int(y)] = color or self.curr_color
    
    def glVertex(self, x, y, color = None):
        if x < -1 or x > 1:
            return
        if y < -1 or y > 1:
            return
        
        pixelX = (x+1) * (self.vpWidth / 2) + self.vpX
        pixelY = (y+1) * (self.vpHeight / 2) + self.vpY

        if (0 < x < self.width) and (0 < y < self.height):
            self.pixels[int(x)][int(y)] = color or self.curr_color


    def glLine(self, v0, v1, color = None):
        points = []
        x0 = v0.x
        x1 = v1.x
        y0 = v0.y
        y1 = v1.y

        if x0 == x1 and y0 == y1:
            self.glPoint(x0,y1, color)
            return points

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        offset = 0
        limit = 0.5
        m = dy/dx
        y = y0

        for x in range(x0, x1 + 1):
            if steep:
                self.glPoint(y, x, color)
            else:
                self.glPoint(x, y, color)

            offset += m
            if offset >= limit:
                y += 1 if y0 < y1 else -1
                limit += 1

    def glLoadModel(self, filename, texture = None, transalate = V3(0.0,0.0,0.0), scale = V3(1,1,1)):

        model = Obj(filename)

        light = V3(0,0,1)
        
        for cara in model.caras:
            vertCount = len(cara)

            vert0 = model.vertices[cara[0][0] - 1]
            vert1 = model.vertices[cara[1][0] - 1]
            vert2 = model.vertices[cara[2][0] - 1]

            vt0 = model.texturacoordenadas[cara[0][1] - 1]
            vt1 = model.texturacoordenadas[cara[1][1] - 1]
            vt2 = model.texturacoordenadas[cara[2][1] - 1]

            a = self.glTransform(vert0, transalate, scale)
            b = self.glTransform(vert1, transalate, scale)
            c = self.glTransform(vert2, transalate, scale)

            
            if vertCount == 4:
                vert3 = model.vertices[cara[3][0] - 1]
                vt3 = model.texturacoordenadas[cara[3][1] - 1]
                d = self.glTransform(vert3, transalate, scale)
            
            # normal = np.cross(np.subtract(vert1,vert0), np.subtract(vert2,vert0))
            # normal = normal / np.linalg.norm(normal)
            # intensity = np.dot(normal, light)

            normal = mate.productoCruz3D(mate.restaVect(vert1,vert0), mate.restaVect(vert2,vert0))
            normal = mate.normalizar3D(normal)
            intensity = mate.productoPunto(normal, light)

            if intensity > 1:
                intensity = 1
            elif intensity < 0:
                intensity = 0
            elif intensity != intensity:
                intensity = 0


            self.glTriangle_bc(a,b,c, texCoords=(vt0,vt1,vt2), texture=texture, intensity = intensity)
            if vertCount == 4:
                self.glTriangle_bc(a,c,d,texCoords=(vt0,vt2,vt3), texture=texture, intensity = intensity)


    def glFillTriangle(self, A, B, C, color = None):

        if A.y < B.y:
            A, B = B, A
        if A.y < C.y:
            A, C = C, A
        if B.y < C.y:
            B, C = C, B

        def flatBottomTriangle(v1, v2, v3):
            try:
                d_21 = (v2.x - v1.x) / (v2.y - v1.y)
                d_31 = (v3.x - v1.x) / (v3.y - v1.y)
            except:
                pass
            else:
                x1 = v2.x
                x2 = v3.x
                for y in range(v2.y, v1.y + 1):
                    self.glLine(V2(int(x1),y), V2(int(x2),y), color)
                    x1 += d_21
                    x2 += d_31

        def flatTopTriangle(v1, v2, v3):
            try:
                d_31 = (v3.x - v1.x) / (v3.y - v1.y)
                d_32 = (v3.x - v2.x) / (v3.y - v2.y)
            except:
                pass
            else:
                x1 = v3.x
                x2 = v3.x

                for y in range(v3.y, v1.y + 1):
                    self.glLine(V2(int(x1),y), V2(int(x2),y), color)
                    x1 += d_31
                    x2 += d_32

        if B.y == C.y:
            flatBottomTriangle(A, B, C)
        elif A.y == B.y:
            flatTopTriangle(A, B, C)
        else:
            D = V2(A.x + ((B.y - A.y) / (C.y - A.y)) * (C.x - A.x)   , B.y)
            flatBottomTriangle(A, B, D)
            flatTopTriangle(B, D, C)

    def glTriangle_bc(self, A, B, C, texCoords = (), texture = None, color = None, intensity = 1):
        minX = round(min(A.x, B.x, C.x))
        minY = round(min(A.y, B.y, C.y))
        maxX = round(max(A.x, B.x, C.x))
        maxY = round(max(A.y, B.y, C.y))

        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                u,v,w = baryCoords(A,B,C, V2(x,y))

                if u >= 0 and v >= 0 and w >= 0:

                    z = A.z * u + B.z * v + C.z * w

                    if texture:
                        tA, tB, tC = texCoords
                        tx = tA[0] * u + tB[0] * v + tC[0] * w
                        ty = tA[1] * u + tB[1] * v + tC[1] * w
                        color = texture.getColor(tx,ty)

                    if z > self.zbuffer[x][y]:

                        self.glPoint(x,y, _color( color[2] * intensity / 255,
                                                  color[1] * intensity / 255,
                                                  color[0] * intensity / 255) )
                        self.zbuffer[x][y] = z


    def glTransform(self, vertex, translate=V3(0,0,0), scale=V3(1,1,1)):
        return V3(vertex[0] * scale.x + translate.x, vertex[1] * scale.y + translate.y, vertex[2] * scale.z + translate.z)
    
    def glDrawPolygon(self, polygon):
        for i in range(len(polygon)):
            self.glLine(V2(polygon[i][0], polygon[i][1]), V2(polygon[(i+1) % len(polygon)][0], polygon[(i+1) % len(polygon)][1]))

    def glScanLine(self):
        # Basandose en el algoritmo Scan Line, se implemento el siguiente codigo
        for y in range (self.height):
            puntos = []
            puntosfiltrados = []
            for x in range (self.width):
                if self.pixels[x][y] == self.curr_color:
                    puntos.append((x,y))
            for l in range (0, len(puntos)):
                if (puntos[(l+1) % len(puntos)][0] - puntos[l][0]) != 1:
                    puntosfiltrados.append((puntos[l]))


            if len(puntosfiltrados) == 0:
                pass
            elif len(puntosfiltrados) % 2 == 0:
                for x in range(0, len(puntosfiltrados), 2):
                    self.glLine(V2(puntosfiltrados[x][0], puntosfiltrados[x][1]),V2(puntosfiltrados[(x+1) % len(puntosfiltrados)][0], puntosfiltrados[(x+1) % len(puntosfiltrados)][1]))
            elif len(puntosfiltrados) % 3 == 0:
                for x in range(0, len(puntosfiltrados), 1):
                    self.glLine(V2(puntosfiltrados[x][0], puntosfiltrados[x][1]),V2(puntosfiltrados[(x+1) % len(puntosfiltrados)][0], puntosfiltrados[(x+1) % len(puntosfiltrados)][1]))
            #print(puntos)

    def glFinish(self, filename):
        with open(filename, "wb") as file:
            # Header
            file.write(bytes('B'.encode('ascii')))
            file.write(bytes('M'.encode('ascii')))
            file.write(dword(14 + 40 + (self.width * self.height * 3)))
            file.write(dword(0))
            file.write(dword(14 + 40))

            # InfoHeader
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword(self.width * self.height * 3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            # Color Table
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.pixels[x][y])

