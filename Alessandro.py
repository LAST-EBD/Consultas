import os, fiona, random
import numpy as np
from shapely.geometry import mapping, shape, Point, Polygon
from fiona.crs import from_epsg


class alessandro(object):
    '''clase para calcular los centroides de un cluster de puntos, moverlos dentro de un marco y girarlos sobre el
    centroide... Vamos, lo que viene a ser un currazo de la hostia.'''

    def __init__(self, pointshp, marco):

        '''definimos la entrada como el path al shape de puntos que contiene los datos'''
        self.pointshp = pointshp
        self.marco = marco
        self.base = os.path.split(self.pointshp)[0]
        self.moved = os.path.join(self.base, 'moved')
        if not os.path.exists(self.moved):
            os.makedirs(self.moved)
        self.moves = {0: 'NW', 1: 'NE', 2: 'SW', 3: 'SE'}
        self.ccpath = os.path.join(self.base, 'cc')
        if not os.path.exists(self.ccpath):
            os.makedirs(self.ccpath)
        self.cgpath = os.path.join(self.base, 'cg')
        if not os.path.exists(self.cgpath):
            os.makedirs(self.cgpath)
        #creamos un diccionario donde guardaremos offset de x e y, coordenadas de centroides y el angulo de rotacion de cada individuo
        self.individuos = {}
        #elegimos aleatoriamente hacia donde nos movemos
        self.rndm = random.randrange(0, 4)
        self.diffX = 0
        self.diffY = 0
        self.count = 1

        print('shape:', self.pointshp, '\nmarco: ', self.marco, '\nsalida:', self.moved)
        print('Nos movemos hacia el:', self.moves[self.rndm])

    def get_extent_shapely(self, shp):

        shp = fiona.open(shp)
        # print('zone:', self.moves[self.rndm])
        # GETTING THE GEOMETRY (COORDINATES)
        feature1 = shp.next()
        geom1 = feature1['geometry']
        a1 = Polygon(geom1['coordinates'][0])
        Oeste, Este, Norte, Sur = a1.bounds[0], a1.bounds[2], a1.bounds[3], a1.bounds[1]

        # return(Oeste, Este, Norte, Sur)
        move = {'NW': (Norte, Oeste), 'NE': (Norte, Este), 'SW': (Sur, Oeste), 'SE': (Sur, Este)}
        return move[self.moves[self.rndm]]

    def get_diff(self, tupla):

        ''' Este metodo computa la diferencia entre las coordenas del shape con respecto al marco (en la direccion aleatoria
        que haya tocado. Retorna una tupla  con valores (X, Y) con la diferencia. Por tanto get_diff[0] es la diferencia en X
        y get_diff[1] es la diferencia en Y)'''

        frameM = self.get_extent_shapely(self.marco)
        # print(frameM)
        NorteM, OesteM = frameM[0], frameM[1]
        frameS = self.get_extent_shapely(self.pointshp)
        # print(frameS)
        NorteS, OesteS = frameS[0], frameS[1]

        self.diffX = OesteM - OesteS
        self.diffY = NorteM - NorteS

        return (self.diffX, self.diffY)



    def centroids(self):


        # Abrimos el shape de puntos y hacemos un set con el id de cada grupo
        point = fiona.open(self.pointshp)
        especies = set([i['properties']['ID_progres'] for i in point.values()])
        lespecies = sorted([i for i in especies])

        # Primero creamos un diccionario con la clave de cada id y como valor un diccionario con las coordenadas x e y que rellenaremos a continuacion
        d = {}
        for k in lespecies:
            d[k] = {'x': [], 'y': []}

        # Ahora recorremos todos los puntos y segun su id_progess vamos anadiendo las coordenas a d
        for i in point.values():
            d[i['properties']['ID_progres']]['x'].append(i['geometry']['coordinates'][0])
            d[i['properties']['ID_progres']]['y'].append(i['geometry']['coordinates'][1])

        # Ya tenemos todas las coordenadas ahora vamos a crear otro diccionario con los centroides y centro de gravedad de cada id_progress
        # Hacemos lo mismo que antes y lo primero sera crear el diccionario vacio que rellenaremos posteriormente
        for k, v in d.items():
            self.individuos[k] = {'centroide': (), 'ceg': (), 'grados': 0, 'xoff': 0, 'yoff': 0}

        # Ahora pasamos a calcular el centro de gravedad y el centroide
        for k, v in d.items():
            self.individuos[k]['ceg'] = (np.mean(d[k]['x']), np.mean(d[k]['y']))
            self.individuos[k]['centroide'] = (((max(d[k]['x']) + min(d[k]['x'])) / 2), ((max(d[k]['y']) + min(d[k]['y'])) / 2))

        # Ahora vamos a anadir al diccionario un valor aleatorio para el grado de giro
        for k in lespecies:
            grados = random.randint(0,360)
            self.individuos[k]['grados'] = grados

        # Ahora anadimos los offset de x e y
        for k in lespecies:

            self.offset(k)

        # Ya tenemos un diccionario con las coordenadas x e y de los centroides, ahora debemos de crear un shape para cada id_progress
        schema = {'geometry': 'Point', 'properties': {'id': 'int'}}
        for k, v in c.items():
            shp = os.path.join(self.ccpath, str(k) + '_cc.shp')
            centroid = Point(c[k]['centroide'])
            with fiona.open(shp, 'w', crs=point.crs, driver='ESRI Shapefile', schema=schema) as cshp:
                cshp.write({
                    'geometry': mapping(centroid),
                    'properties': {'id': k}})

            shpcg = os.path.join(self.cgpath, str(k) + '_cg.shp')
            centroid = Point(c[k]['ceg'])
            with fiona.open(shpcg, 'w', crs=point.crs, driver='ESRI Shapefile', schema=schema) as cshp:
                cshp.write({
                    'geometry': mapping(centroid),
                    'properties': {'id': k}})


        print(self.individuos)

    #Aqui estaban el calcula de la distancia y el angulo entre cada punto y el centroide, siguen en el notebook
    #en principio no haran falta haciendo larotacion con shapely.affinity

    def check(self, centroid, k, offx, offy):

        '''Este metodo se usa para comprobar que el centroide cae dentro de una de las zonas en las que debe de caer'''
        centroid = Point(centroid)
        cc = affinity.translate(centroid, offx, offy)
        marco = fiona.open(self.marco)
        mc = Polygon(marco['geometry']['coordinates'])

        if mc.contains(cc):
            self.individuos[k]['xoff'], self.individuos[k]['yoff'] = offx, offy
        else:
            self.offset(k)


    def offset(self, k):

        '''Este metodo va ajustando el offset hasta que el centroide cae dentro del area'''
        distxy = self.get_diff(self.individuos[k]['ceg'])
        # hemos sacado la distancia x e y al frame, ahora cogemos un valor aleatorio entre 0 y esas distancias
        if distxy[0] < 0:
            offx = round(random.uniform(distxy[0], 0), 2)
        else:
            offx = round(random.uniform(0, distxy[0]), 2)
        if distxy[1] < 0:
            offy = round(random.uniform(distxy[1], 0), 2)
        else:
            offy = round(random.uniform(0, distxy[1]), 2)

        self.check(self.individuos[k]['ceg'], k,  offx, offy)


    def rotate_c(self):

        ''' Este metodo computa la diferencia entre las coordenas del shape con respecto al marco (en la direccion aleatoria
        que haya tocado. Retorna una tupla  con valores (X, Y) con la diferencia. Por tanto get_diff[0] es la diferencia en X
        y get_diff[1] es la diferencia en Y)'''

        # Abrimos el shape originl
        with fiona.open(self.pointshp, 'r') as input:
            # The output has the same schema
            schema = input.schema.copy()
            coords = from_epsg(25830)

            # Escribimos el nuevo shapefile con las nuevas coordenadas
            with fiona.open(os.path.join(self.moved, 'out_rpt.shp'), 'w',
                            'ESRI Shapefile', schema, coords) as output:
                for elem in input:
                    idp = elem['properties']['ID_progres']
                    p = Point(elem['geometry']['coordinates'])
                    rp = affinity.rotate(p, self.individuos[idp]['grados'], self.individuos[idp]['ceg'], use_radians=False)
                    rpt = affinity.translate(rp, self.individuos[idp]['xoff'], self.individuos[idp]['yoff'])
                    output.write({'properties': elem['properties'], 'geometry': mapping(rpt)})
