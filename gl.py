# Christian Daniel Perez De Leon 19710

import struct
from collections import namedtuple
from obj import Obj
import numpy as np
from numpy import sin, cos, tan
import matematica as mate

V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])
V4 = namedtuple('Point4', ['x', 'y', 'z', 'w'])



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
        self.glViewMatrix()
        self.glCreateWindow(width, height)

        self.active_texture = None
        self.normal_map = None

        self.background = None

        self.active_shader = None
        self.directional_light = V3(0,0,1)
        

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

        self.viewportMatrix = np.matrix([[width/2, 0, 0, x + width/2],
                                         [0, height/2, 0, y + height/2],
                                         [0, 0, 0.5, 0.5],
                                         [0, 0, 0, 1]])
        self.glProjectionMatrix()

    def glClearColor(self, r, g, b):
        self.clear_color = _color(r, g, b)

    def glClear(self):
        self.pixels = [[ self.clear_color for y in range(self.height)] for x in range(self.width)]

        self.zbuffer = [[ float('inf') for y in range(self.height)] for x in range(self.width)]

    def glClearBackground(self):

        if self.background:
            for x in range(self.vpX, self.vpX + self.vpWidth):
                for y in range(self.vpY, self.vpY + self.vpHeight):
                    
                    tx = (x - self.vpX) / self.vpWidth
                    ty = (y - self.vpY) / self.vpHeight

                    self.glPoint(x, y, self.background.getColor(tx, ty))
                
            
    def glViewportClear(self, color = None):
        for x in range(self.vpX, self.vpX + self.vpWidth):
            for y in range(self.vpY, self.vpY + self.vpHeight):
                self.glPoint(x, y, color)

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

    def glLoadModel(self, filename, transalate = V3(0.0,0.0,0.0), scale = V3(1,1,1), rotation = V3(0,0,0)):

        model = Obj(filename)

        modelMatrix = self.glCreateObjectMatrix(transalate, scale, rotation)
        rotationMatrix = self.glCreateRotationMatrix(rotation)
        
        for cara in model.caras:
            vertCount = len(cara)

            vert0 = model.vertices[cara[0][0] - 1]
            vert1 = model.vertices[cara[1][0] - 1]
            vert2 = model.vertices[cara[2][0] - 1]

            vt0 = model.texturacoordenadas[cara[0][1] - 1]
            vt1 = model.texturacoordenadas[cara[1][1] - 1]
            vt2 = model.texturacoordenadas[cara[2][1] - 1]

            vn0 = self.glDirTransform(model.normales[cara[0][2] - 1], rotationMatrix)
            vn1 = self.glDirTransform(model.normales[cara[1][2] - 1], rotationMatrix)
            vn2 = self.glDirTransform(model.normales[cara[2][2] - 1], rotationMatrix)

            if vertCount == 4:
                vn3 = self.glDirTransform(model.normales[cara[3][2] - 1], rotationMatrix)

            vert0 = self.glTransform(vert0, modelMatrix)
            vert1 = self.glTransform(vert1, modelMatrix)
            vert2 = self.glTransform(vert2, modelMatrix)

            
            if vertCount == 4:
                vert3 = model.vertices[cara[3][0] - 1]
                vt3 = model.texturacoordenadas[cara[3][1] - 1]
                vert3 = self.glTransform(vert3, modelMatrix)

            a = self.glCamTransform(vert0)
            b = self.glCamTransform(vert1)
            c = self.glCamTransform(vert2)
            if vertCount == 4:
                d = self.glCamTransform(vert3)

            self.glTriangle_bc(a,b,c, texCoords=(vt0,vt1,vt2), normals = (vn0, vn1, vn2), verts=(vert0, vert1, vert2) )
            if vertCount == 4:
                self.glTriangle_bc(a,c,d,texCoords=(vt0,vt2,vt3), normals = (vn0, vn2, vn3), verts=(vert0, vert2, vert3))

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

    def glTriangle_bc(self, A, B, C, texCoords = (), normals = (), verts = (), color = None):
        minX = round(min(A.x, B.x, C.x))
        minY = round(min(A.y, B.y, C.y))
        maxX = round(max(A.x, B.x, C.x))
        maxY = round(max(A.y, B.y, C.y))

        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                u,v,w = baryCoords(A,B,C, V2(x,y))

                if u >= 0 and v >= 0 and w >= 0:

                    z = A.z * u + B.z * v + C.z * w

                    if 0<=x<self.width and 0<=y<self.height:

                        if z < self.zbuffer[x][y] and z<=1 and z >= -1:

                            if self.active_shader:
                                
                                r,g,b = self.active_shader(self, verts = verts , baryCoords = (u,v,w), texCoords = texCoords, normals = normals, color = color or self.curr_color)

                            else:
                                b,g,r = color or self.curr_color
                                b/=255
                                g/=255
                                r/=255


                            self.glPoint(x,y, _color(r, g, b))
                            self.zbuffer[x][y] = z

    def glTransform(self, vertex, vMatrix):
        augVertex = V4(vertex[0], vertex[1], vertex[2], 1)
        # transVertex = vMatrix @ augVertex
        transVertex = mate.multMatrices4xVec(vMatrix, augVertex)
        # transVertex = transVertex.tolist()[0]

        transVertex = V3(transVertex[0] / transVertex[3],
                         transVertex[1] / transVertex[3],
                         transVertex[2] / transVertex[3])
        
        return transVertex

    def glDirTransform(self, dirVector, vMatrix):
        augVertex = V4(dirVector[0], dirVector[1], dirVector[2], 0)
        # transVertex = vMatrix @ augVertex
        # transVertex = transVertex.tolist()[0]
        transVertex = mate.multMatrices4xVec(vMatrix, augVertex)

        transVertex = V3(transVertex[0],
                         transVertex[1],
                         transVertex[2])

        return transVertex

    def glCamTransform( self, vertex ):
        augVertex = V4(vertex[0], vertex[1], vertex[2], 1)
        transVertex = self.viewportMatrix @ self.projectionMatrix @ self.viewMatrix @ augVertex
        # res1 = mate.multMatrices4x4(self.viewportMatrix, self.projectionMatrix)
        # res2 = mate.multMatrices4x4(res1, self.viewMatrix)
        # transVertex = mate.multMatrices4xVec(res2, augVertex)
        
        transVertex = transVertex.tolist()[0]

        transVertex = V3(transVertex[0] / transVertex[3],
                         transVertex[1] / transVertex[3],
                         transVertex[2] / transVertex[3])

        return transVertex
    
    def glCreateRotationMatrix(self, rotate=V3(0,0,0)):
        # pitch = np.deg2rad(rotate.x)
        # yaw = np.deg2rad(rotate.y)
        # roll = np.deg2rad(rotate.z)

        pitch = mate.gradosARadianes(rotate.x)
        yaw = mate.gradosARadianes(rotate.y)
        roll = mate.gradosARadianes(rotate.z)

        # rotationX = np.matrix([[1,0,0,0],
        #                        [0,cos(pitch),-sin(pitch),0],
        #                        [0,sin(pitch),cos(pitch),0],
        #                        [0,0,0,1]])

        # rotationY = np.matrix([[cos(yaw),0,sin(yaw),0],
        #                        [0,1,0,0],
        #                        [-sin(yaw),0,cos(yaw),0],
        #                        [0,0,0,1]])

        # rotationZ = np.matrix([[cos(roll),-sin(roll),0,0],
        #                        [sin(roll),cos(roll),0,0],
        #                        [0,0,1,0],
        #                        [0,0,0,1]])

        # return rotationX * rotationY * rotationZ

        rotationX = [[1,0,0,0],
                     [0,cos(pitch),-sin(pitch),0],
                     [0,sin(pitch),cos(pitch),0],
                     [0,0,0,1]]

        rotationY = [[cos(yaw),0,sin(yaw),0],
                     [0,1,0,0],
                     [-sin(yaw),0,cos(yaw),0],
                     [0,0,0,1]]

        rotationZ = [[cos(roll),-sin(roll),0,0],
                     [sin(roll),cos(roll),0,0],
                     [0,0,1,0],
                     [0,0,0,1]]
        res1 = mate.multMatrices4x4(rotationX, rotationY)
        res2 = mate.multMatrices4x4(res1, rotationZ)

        return res2

    def glCreateObjectMatrix(self, translate = V3(0,0,0), scale=V3(1,1,1), rotate = V3(0,0,0)):
        # translateMatrix = np.matrix([[1,0,0, translate.x],
        #                              [0,1,0, translate.y],
        #                              [0,0,1, translate.z],
        #                              [0,0,0,1]])

        # scaleMatrix = np.matrix([[scale.x,0,0,0],
        #                          [0,scale.y,0,0],
        #                          [0,0,scale.z,0],
        #                          [0,0,0,1]])
        
        # rotationMatrix = self.glCreateRotationMatrix(rotate)

        # return translateMatrix * rotationMatrix * scaleMatrix

        translateMatrix=[[1,0,0, translate.x],
                         [0,1,0, translate.y],
                         [0,0,1, translate.z],
                         [0,0,0,1]]

        scaleMatrix=[[scale.x,0,0,0],
                     [0,scale.y,0,0],
                     [0,0,scale.z,0],
                     [0,0,0,1]]
        
        rotationMatrix = self.glCreateRotationMatrix(rotate)

        res1 = mate.multMatrices4x4(translateMatrix, rotationMatrix)
        res2 = mate.multMatrices4x4(res1, scaleMatrix)

        return res2

    def glViewMatrix(self, translate = V3(0,0,0), rotate = V3(0,0,0)):
        self.camMatrix = self.glCreateObjectMatrix(translate,V3(1,1,1),rotate)
        self.viewMatrix = np.linalg.inv(self.camMatrix)

    def glLookAt(self, eye, camPosition = V3(0,0,0)):
        # forward = np.subtract(camPosition, eye)
        # forward = forward / np.linalg.norm(forward)

        # right = np.cross(V3(0,1,0), forward)
        # right = right / np.linalg.norm(right)

        # up = np.cross(forward, right)
        # up = up / np.linalg.norm(up)

        forward = mate.restaVect(camPosition, eye)
        forward = mate.normalizar3D(forward)

        right = mate.productoCruz3D(V3(0,1,0), forward)
        right = mate.normalizar3D(right)

        up = mate.productoCruz3D(forward, right)
        up = mate.normalizar3D(up)

        camMatrix = np.matrix([[right[0],up[0],forward[0],camPosition.x],
                               [right[1],up[1],forward[1],camPosition.y],
                               [right[2],up[2],forward[2],camPosition.z],
                               [0,0,0,1]])

        self.viewMatrix = np.linalg.inv(camMatrix)

    def glProjectionMatrix(self, n = 0.1, f = 1000, fov = 60 ):
        # aspectRatio = self.vpWidth / self.vpHeight

        t = tan((fov * mate.pi / 180) / 2) * n
        r = t * self.vpWidth / self.vpHeight

        self.projectionMatrix = np.matrix([[n/r, 0, 0, 0],
                                           [0, n/t, 0, 0],
                                           [0, 0, -(f+n)/(f-n), -(2*f*n)/(f-n)],
                                           [0, 0, -1, 0]])
        
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

