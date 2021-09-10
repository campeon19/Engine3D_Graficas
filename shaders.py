
from itertools import count
import matematica as mate
import numpy as np
import random

def flat(render, **kwargs):
    u,v,w = kwargs['baryCoords']
    tA,tB,tC = kwargs['texCoords']
    A, B, C = kwargs['verts']
    b,g,r = kwargs['color']

    b/=255
    g/=255
    r/=255

    if render.active_texture:
        tx = tA[0] * u + tB[0] * v + tC[0] * w
        ty = tA[1] * u + tB[1] * v + tC[1] * w
        texColor = render.active_texture.getColor(tx, ty)

        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    normal = mate.productoCruz3D(mate.restaVect(B,A), mate.restaVect(C,A))
    normal = mate.normalizar3D(normal)
    intensity = mate.productoPunto(normal, render.directional_light)

    b *= intensity
    g *= intensity
    r *= intensity

    if intensity > 0:
        return r,g,b
    else:
        return 0,0,0


    return r,g,b

def gourand(render, **kwargs):
    u,v,w = kwargs['baryCoords']
    tA,tB,tC = kwargs['texCoords']
    A, B, C = kwargs['verts']
    b,g,r = kwargs['color']
    nA, nB, nC = kwargs['normals']

    b/=255
    g/=255
    r/=255

    dirLight = [render.directional_light[0],
                render.directional_light[1],
                render.directional_light[2]]
    intensityA = mate.productoPunto(nA, dirLight)
    intensityB = mate.productoPunto(nB, dirLight)
    intensityC = mate.productoPunto(nC, dirLight)

    intensity = intensityA *u + intensityB *v + intensityC *w
    b*= intensity
    g*= intensity
    r*= intensity

    if intensity > 0:
        return r, g, b
    else:
        return 0,0,0

def phong(render, **kwargs):
    
    u, v, w = kwargs['baryCoords']
    tA, tB, tC = kwargs['texCoords']
    b, g, r = kwargs['color']
    nA, nB, nC = kwargs['normals']

    b/= 255
    g/= 255
    r/= 255

    if render.active_texture:
        tx = tA[0] * u + tB[0] * v + tC[0] * w
        ty = tA[1] * u + tB[1] * v + tC[1] * w
        texColor = render.active_texture.getColor(tx, ty)
        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    nX = nA[0] * u + nB[0] * v + nC[0] * w
    nY = nA[1] * u + nB[1] * v + nC[1] * w
    nZ = nA[2] * u + nB[2] * v + nC[2] * w

    normal = (nX, nY, nZ)

    dirLight = [render.directional_light[0],
                render.directional_light[1],
                render.directional_light[2]]
    intensity = mate.productoPunto(normal, dirLight)

    if intensity > 1:
        intensity = 1

    b*= intensity
    g*= intensity
    r*= intensity

    if intensity > 0:
        return r, g, b
    else:
        return 0,0,0

def unlit(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    tA, tB, tC = kwargs['texCoords']
    b, g, r = kwargs['color']

    b/= 255
    g/= 255
    r/= 255

    if render.active_texture:
        tx = tA[0] * u + tB[0] * v + tC[0] * w
        ty = tA[1] * u + tB[1] * v + tC[1] * w
        texColor = render.active_texture.getColor(tx, ty)
        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    return r, g, b

def toon(render, **kwargs):
    u, v, w = kwargs['baryCoords']
    tA, tB, tC = kwargs['texCoords']
    b, g, r = kwargs['color']
    nA, nB, nC = kwargs['normals']

    b/= 255
    g/= 255
    r/= 255

    if render.active_texture:
        tx = tA[0] * u + tB[0] * v + tC[0] * w
        ty = tA[1] * u + tB[1] * v + tC[1] * w
        texColor = render.active_texture.getColor(tx, ty)
        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    nX = nA[0] * u + nB[0] * v + nC[0] * w
    nY = nA[1] * u + nB[1] * v + nC[1] * w
    nZ = nA[2] * u + nB[2] * v + nC[2] * w

    normal = (nX, nY, nZ)

    dirLight = [render.directional_light[0],
                render.directional_light[1],
                render.directional_light[2]]
    intensity = mate.productoPunto(normal, dirLight)

    if intensity > 0.7:
        intensity = 1
    elif intensity > 0.3:
        intensity = 0.5
    else:
        intensity = 0.05


    b*= intensity
    g*= intensity
    r*= intensity

    if intensity > 0:
        return r, g, b
    else:
        return 0,0,0

def textureBlend(render, **kwargs):

    u, v, w = kwargs['baryCoords']
    tA, tB, tC = kwargs['texCoords']
    b, g, r = kwargs['color']
    nA, nB, nC = kwargs['normals']

    b/= 255
    g/= 255
    r/= 255

    if render.active_texture:
        tx = tA[0] * u + tB[0] * v + tC[0] * w
        ty = tA[1] * u + tB[1] * v + tC[1] * w
        texColor = render.active_texture.getColor(tx, ty)
        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    nX = nA[0] * u + nB[0] * v + nC[0] * w
    nY = nA[1] * u + nB[1] * v + nC[1] * w
    nZ = nA[2] * u + nB[2] * v + nC[2] * w

    normal = (nX, nY, nZ)

    dirLight = [-render.directional_light[0],
                -render.directional_light[1],
                -render.directional_light[2]]
    intensity = mate.productoPunto(normal, dirLight)

    if intensity < 0:
        intensity = 0

    b*= intensity
    g*= intensity
    r*= intensity

    if render.active_texture2:
        texColor = render.active_texture2.getColor(tx, ty)
        b += (texColor[0] / 255) * (1 - intensity)
        g += (texColor[1] / 255) * (1 - intensity)
        r += (texColor[2] / 255) * (1 - intensity)


    return r, g, b

def normalMap(render, **kwargs):
    A, B, C = kwargs['verts']
    u, v, w = kwargs['baryCoords']
    tA, tB, tC = kwargs['texCoords']
    b, g, r = kwargs['color']
    nA, nB, nC = kwargs['normals']

    b/= 255
    g/= 255
    r/= 255

    if render.active_texture:
        tx = tA[0] * u + tB[0] * v + tC[0] * w
        ty = tA[1] * u + tB[1] * v + tC[1] * w
        texColor = render.active_texture.getColor(tx, ty)
        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    nX = nA[0] * u + nB[0] * v + nC[0] * w
    nY = nA[1] * u + nB[1] * v + nC[1] * w
    nZ = nA[2] * u + nB[2] * v + nC[2] * w
    normal = (nX, nY, nZ)

    dirLight = np.array(render.directional_light)
    

    if render.normal_map:
        texNormal = render.normal_map.getColor(tx, ty)
        texNormal = [(texNormal[2] / 255) * 2 - 1,
                     (texNormal[1] / 255) * 2 - 1,
                     (texNormal[0] / 255) * 2 - 1]

        texNormal = texNormal / np.linalg.norm(texNormal)

        edge1 = np.subtract(B, A)
        edge2 = np.subtract(C, A)
        deltaUV1 = np.subtract(tB, tA)
        deltaUV2 = np.subtract(tC, tA)

        f = 1 / (deltaUV1[0] * deltaUV2[1] - deltaUV2[0] * deltaUV1[1])

        tangent = [f * (deltaUV2[1] * edge1[0] - deltaUV1[1] * edge2[0]),
                   f * (deltaUV2[1] * edge1[1] - deltaUV1[1] * edge2[1]),
                   f * (deltaUV2[1] * edge1[2] - deltaUV1[1] * edge2[2])]
        tangent = tangent / np.linalg.norm(tangent)
        tangent = np.subtract(tangent, np.multiply(np.dot(tangent, normal), normal))
        tangent = tangent / np.linalg.norm(tangent)

        bitangent = np.cross(normal, tangent)
        bitangent = bitangent / np.linalg.norm(bitangent)

        tangentMatrix = np.matrix([[tangent[0],  bitangent[0],  normal[0]],
                                   [tangent[1],  bitangent[1],  normal[1]],
                                   [tangent[2],  bitangent[2],  normal[2]]])

        texNormal = tangentMatrix @ texNormal
        texNormal = texNormal.tolist()[0]
        texNormal = texNormal / np.linalg.norm(texNormal)
        intensity = np.dot(texNormal, dirLight)
    else:
        intensity = np.dot(normal, dirLight)

    b*= intensity
    g*= intensity
    r*= intensity

    if intensity > 0:
        return r, g, b
    else:
        return 0,0,0

def shader1(render, **kwargs):

    # Inversion de colores
    
    u, v, w = kwargs['baryCoords']
    tA, tB, tC = kwargs['texCoords']
    b, g, r = kwargs['color']
    nA, nB, nC = kwargs['normals']

    b/= 255
    g/= 255
    r/= 255

    if render.active_texture:
        tx = tA[0] * u + tB[0] * v + tC[0] * w
        ty = tA[1] * u + tB[1] * v + tC[1] * w
        texColor = render.active_texture.getColor(tx, ty)
        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    nX = nA[0] * u + nB[0] * v + nC[0] * w
    nY = nA[1] * u + nB[1] * v + nC[1] * w
    nZ = nA[2] * u + nB[2] * v + nC[2] * w

    normal = (nX, nY, nZ)

    dirLight = [render.directional_light[0],
                render.directional_light[1],
                render.directional_light[2]]
    intensity = mate.productoPunto(normal, dirLight)

    b = mate.valAbsoluto(b - 1)
    g = mate.valAbsoluto(g - 1)
    r = mate.valAbsoluto(r - 1)

    b*= intensity
    g*= intensity
    r*= intensity

    if intensity > 0:
        return r, g, b
    else:
        return 0,0,0

def shader2(render, **kwargs):
    
    # Degradacion de color utilizando las coordenadas baricentricas

    A, B, C = kwargs['verts']
    u, v, w = kwargs['baryCoords']
    tA, tB, tC = kwargs['texCoords']
    b, g, r = kwargs['color']
    nA, nB, nC = kwargs['normals']

    b/= 255
    g/= 255
    r/= 255

    nX = nA[0] * u + nB[0] * v + nC[0] * w
    nY = nA[1] * u + nB[1] * v + nC[1] * w
    nZ = nA[2] * u + nB[2] * v + nC[2] * w

    normal = (nX, nY, nZ)

    dirLight = [render.directional_light[0],
                render.directional_light[1],
                render.directional_light[2]]
    intensity = mate.productoPunto(normal, dirLight)

    b*= u
    g*= v
    r*= w
    
    b*= intensity
    g*= intensity
    r*= intensity

    if intensity > 0:
        return r, g, b
    else:
        return 0,0,0

def shader3(render, **kwargs):
    
    # Randomizando colores utilizando la coordenada baricentrica u para dar un toque tipo roca

    u, v, w = kwargs['baryCoords']
    tA, tB, tC = kwargs['texCoords']
    b, g, r = kwargs['color']
    nA, nB, nC = kwargs['normals']

    b/= 255
    g/= 255
    r/= 255

    nX = nA[0] * u + nB[0] * v + nC[0] * w
    nY = nA[1] * u + nB[1] * v + nC[1] * w
    nZ = nA[2] * u + nB[2] * v + nC[2] * w

    normal = (nX, nY, nZ)

    dirLight = [render.directional_light[0],
                render.directional_light[1],
                render.directional_light[2]]
    intensity = mate.productoPunto(normal, dirLight)

    b*= random.random() * u
    g*= random.random() * u
    r*= random.random() * u

    b*= intensity
    g*= intensity
    r*= intensity

    if intensity > 0:
        return r, g, b
    else:
        return 0,0,0


    
    A, B, C = kwargs['verts']
    u, v, w = kwargs['baryCoords']
    tA, tB, tC = kwargs['texCoords']
    b, g, r = kwargs['color']
    nA, nB, nC = kwargs['normals']

    b/= 255
    g/= 255
    r/= 255

    if render.active_texture:
        tx = tA[0] * u + tB[0] * v + tC[0] * w
        ty = tA[1] * u + tB[1] * v + tC[1] * w
        texColor = render.active_texture.getColor(tx, ty)
        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    nX = nA[0] * u + nB[0] * v + nC[0] * w
    nY = nA[1] * u + nB[1] * v + nC[1] * w
    nZ = nA[2] * u + nB[2] * v + nC[2] * w

    normal = (nX, nY, nZ)

    dirLight = [render.directional_light[0],
                render.directional_light[1],
                render.directional_light[2]]
    intensity = mate.productoPunto(normal, dirLight)

    # numero = random.randint(0,10)

    # if numero > 5:
    #     b*=0
    #     g*=0
    #     r*=0

     

    b*= intensity
    g*= intensity
    r*= intensity

    if intensity > 0:
        return r, g, b
    else:
        return 0,0,0

def glow(render, **kwargs):
    
    u, v, w = kwargs['baryCoords']
    tA, tB, tC = kwargs['texCoords']
    b, g, r = kwargs['color']
    nA, nB, nC = kwargs['normals']

    b/= 255
    g/= 255
    r/= 255

    if render.active_texture:
        tx = tA[0] * u + tB[0] * v + tC[0] * w
        ty = tA[1] * u + tB[1] * v + tC[1] * w
        texColor = render.active_texture.getColor(tx, ty)
        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    nX = nA[0] * u + nB[0] * v + nC[0] * w
    nY = nA[1] * u + nB[1] * v + nC[1] * w
    nZ = nA[2] * u + nB[2] * v + nC[2] * w

    normal = (nX, nY, nZ)

    dirLight = [render.directional_light[0],
                render.directional_light[1],
                render.directional_light[2]]
    intensity = mate.productoPunto(normal, dirLight)

    if intensity <= 0:
        intensity = 0

    b*= intensity
    g*= intensity
    r*= intensity

    camForward = [render.camMatrix[0][2],
                  render.camMatrix[1][2],
                  render.camMatrix[2][2]]

    glowAmount = 1 - mate.productoPunto(normal, camForward)
    glowColor = [1,1,0]

    r += glowColor[0] * glowAmount
    g += glowColor[1] * glowAmount
    b += glowColor[2] * glowAmount

    if r > 1: r=1
    if g > 1: g=1
    if b > 1: b=1



    return r, g, b

def shader4(render, **kwargs):
    
    u, v, w = kwargs['baryCoords']
    tA, tB, tC = kwargs['texCoords']
    b, g, r = kwargs['color']
    nA, nB, nC = kwargs['normals']

    b/= 255
    g/= 255
    r/= 255

    nX = nA[0] * u + nB[0] * v + nC[0] * w
    nY = nA[1] * u + nB[1] * v + nC[1] * w
    nZ = nA[2] * u + nB[2] * v + nC[2] * w

    normal = (nX, nY, nZ)

    dirLight = [render.directional_light[0],
                render.directional_light[1],
                render.directional_light[2]]
    intensity = mate.productoPunto(normal, dirLight)

    if intensity > 0.95:
        b*= 0/255
        g*= 255/255
        r*= 255/255
    elif intensity > 0.94:
        b*= 1/255
        g*= 254/255
        r*= 255/255
    elif intensity > 0.93:
        b*= 2/255
        g*= 253/255
        r*= 255/255
    elif intensity > 0.92:
        b*= 3/255
        g*= 252/255
        r*= 255/255
    elif intensity > 0.91:
        b*= 4/255
        g*= 251/255
        r*= 255/255
    elif intensity > 0.9:
        b*= 5/255
        g*= 250/255
        r*= 255/255
    elif intensity > 0.85:
        b*= 10/255
        g*= 245/255
        r*= 255/255
    elif intensity > 0.8:
        b*= 20/255
        g*= 235/255
        r*= 255/255
    elif intensity > 0.65:
        b*= 25/255
        g*= 180/255
        r*= 255/255
    elif intensity > 0.5:
        b*= 20/255
        g*= 140/255
        r*= 255/255
    elif intensity > 0.4:
        b*= 15/255
        g*= 100/255
        r*= 255/255
    elif intensity > 0.3:
        b*= 10/255
        g*= 80/255
        r*= 255/255
    elif intensity > 0.25:
        b*= 9/255
        g*= 70/255
        r*= 255/255
    elif intensity > 0.2:
        b*= 8/255
        g*= 60/255
        r*= 255/255
    elif intensity > 0.15:
        b*= 7/255
        g*= 30/255
        r*= 255/255
    elif intensity > 0.1:
        b*= 6/255
        g*= 20/255
        r*= 255/255
    else:
        b*= 3/255
        g*= 10/255
        r*= 255/255

    b*= intensity
    g*= intensity
    r*= intensity

    if intensity > 0:
        return r, g, b
    else:
        return 0,0,0

def koopa(render, **kwargs):
    
    u, v, w = kwargs['baryCoords']
    tA, tB, tC = kwargs['texCoords']
    b, g, r = kwargs['color']
    nA, nB, nC = kwargs['normals']

    b/= 255
    g/= 255
    r/= 255

    if render.active_texture:
        tx = tA[0] * u + tB[0] * v + tC[0] * w
        ty = tA[1] * u + tB[1] * v + tC[1] * w
        texColor = render.active_texture.getColor(tx, ty)
        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    nX = nA[0] * u + nB[0] * v + nC[0] * w
    nY = nA[1] * u + nB[1] * v + nC[1] * w
    nZ = nA[2] * u + nB[2] * v + nC[2] * w

    normal = (nX, nY, nZ)

    dirLight = [render.directional_light[0],
                render.directional_light[1],
                render.directional_light[2]]
    intensity = mate.productoPunto(normal, dirLight)

    if intensity > 1:
        intensity = 1

    if intensity > 0.95:
        r*= 183/255
        g*= 129/255
        b*= 6/255
    elif intensity > 0.94:
        r*= 180/255
        g*= 125/255
        b*= 6/255
    elif intensity > 0.93:
        r*= 175/255
        g*= 120/255
        b*= 6/255
    elif intensity > 0.92:
        r*= 173/255
        g*= 118/255
        b*= 6/255
    elif intensity > 0.91:
        r*= 170/255
        g*= 115/255
        b*= 6/255
    elif intensity > 0.9:
        r*= 165/255
        g*= 110/255
        b*= 6/255
    elif intensity > 0.85:
        r*= 160/255
        g*= 105/255
        b*= 6/255
    elif intensity > 0.8:
        r*= 155/255
        g*= 100/255
        b*= 6/255
    elif intensity > 0.65:
        r*= 155/255
        g*= 10/255
        b*= 6/255
    elif intensity > 0.5:
        r*= 20/255
        g*= 140/255
        b*= 255/255
    elif intensity > 0.4:
        r*= 15/255
        g*= 100/255
        b*= 255/255
    elif intensity > 0.3:
        r*= 10/255
        g*= 80/255
        b*= 255/255
    elif intensity > 0.25:
        r*= 9/255
        g*= 70/255
        b*= 255/255
    elif intensity > 0.2:
        r*= 8/255
        g*= 60/255
        b*= 255/255
    else:
        r*= 0/255
        g*= 91/255
        b*= 11/255

    # r = 0.7176
    # g = 0.5059
    # b = 0.03

    b*= intensity
    g*= intensity
    r*= intensity

    if intensity > 0:
        return r, g, b
    else:
        return 0,0,0

def transparencia(render, **kwargs):
    
    u, v, w = kwargs['baryCoords']
    tA, tB, tC = kwargs['texCoords']
    b, g, r = kwargs['color']
    nA, nB, nC = kwargs['normals']
    maxY, minY, y = kwargs['heightY']

    b/= 255
    g/= 255
    r/= 255

    if render.active_texture:
        tx = tA[0] * u + tB[0] * v + tC[0] * w
        ty = tA[1] * u + tB[1] * v + tC[1] * w
        texColor = render.active_texture.getColor(tx, ty)
        b *= texColor[0] / 255
        g *= texColor[1] / 255
        r *= texColor[2] / 255

    nX = nA[0] * u + nB[0] * v + nC[0] * w
    nY = nA[1] * u + nB[1] * v + nC[1] * w
    nZ = nA[2] * u + nB[2] * v + nC[2] * w

    normal = (nX, nY, nZ)

    dirLight = [render.directional_light[0],
                render.directional_light[1],
                render.directional_light[2]]
    intensity = mate.productoPunto(normal, dirLight)

    if intensity > 1:
        intensity = 1

    for x in range(minY, maxY, 2):
        if y % 2 != 0:
                b = 0
                g = 0
                r = 0

    b*= intensity
    g*= intensity
    r*= intensity

    if intensity > 0:
        return r, g, b
    else:
        return 0,0,0


