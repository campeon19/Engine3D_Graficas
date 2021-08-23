
import matematica as mate

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