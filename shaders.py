
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

    dirLight = [render.directional_light[0],
                render.directional_light[1],
                render.directional_light[2]]

    if render.normal_map:
        texNormal = render.normal_map.getColor(tx, ty)
        texNormal = [(texNormal[2] / 255) *2 -1,
                     (texNormal[1] / 255) *2 -1,
                     (texNormal[0] / 255) *2 -1]
        texNormal = mate.normalizar3D(texNormal)

        edge1 = mate.restaVect(B,A)
        edge2 = mate.restaVect(C,A)
        deltaUV1 = np.subtract(tB,tA)
        deltaUV2 = np.subtract(tC,tA)
        f = 1 / (deltaUV1[0] * deltaUV2[1] - deltaUV2[0] * deltaUV1[1])

        tangente = [f * (deltaUV2[1] * edge1[0] - deltaUV1[1] * edge2[0]),
                    f * (deltaUV2[1] * edge1[1] - deltaUV1[1] * edge2[1]),
                    f * (deltaUV2[1] * edge1[2] - deltaUV1[1] * edge2[2])]
        
        tangente = mate.normalizar3D(tangente)

        bitangente = mate.productoCruz3D(normal, tangente)
        bitangente = mate.normalizar3D(bitangente)

        tangenteMatrix = [[tangente[0],bitangente[0],normal[0]],
                          [tangente[1],bitangente[1],normal[1]],
                          [tangente[2],bitangente[2],normal[2]]]
        
        dirLight = mate.multMatrices4xVec(tangenteMatrix, render.directional_light)
        dirLight = mate.normalizar3D(dirLight)

        intensity = mate.productoPunto(texNormal, dirLight)

    else:
        dirLight = [render.directional_light[0],
                    render.directional_light[1],
                    render.directional_light[2]]
        intensity = mate.productoPunto(normal, dirLight)


    

    b*= intensity
    g*= intensity
    r*= intensity

    if intensity > 0:
        return r, g, b
    else:
        return 0,0,0

def shader1(render, **kwargs):
    
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

    
    if intensity > 0.9:
        b*= 5/255
        g*= 255/255
        r*= 255/255
    elif intensity > 0.8:
        b*= 40/255
        g*= 225/255
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


def shader2(render, **kwargs):
    
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

    # for x in range(0, 1, 0.2):
    #     if intensity > x:



    if intensity > 0.8:
        b*= 40/255
        g*= 235/255
        r*= 255/255
    elif intensity > 0.5:
        b*= 20/255
        g*= 140/255
        r*= 255/255
    elif intensity > 0.3:
        b*= 10/255
        g*= 80/255
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