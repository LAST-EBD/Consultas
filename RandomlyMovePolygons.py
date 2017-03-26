import fiona, shapely, logging, sys, os, random
from shapely import affinity, speedups
from shapely.geometry import mapping, shape, Polygon

speedups.enable()

logging.basicConfig(stream=sys.stderr, level=logging.INFO)


class randomly_move():
    
    '''Con esta clase se pretende el mover aleatoriamente una serie de poligonos dentro de un shape'''
    
    
    def __init__(self, shape, marco):

        self.shape = shape
        self.marco = marco
        self.out = os.path.join(r'O:\consultas\shapes_moved', os.path.split(self.shape)[1])
        self.moves = {0: 'NW', 1: 'NE', 2: 'SW', 3: 'SE'}

        self.rndm = random.randrange(0,4)
        
        self.diffX = 0
        self.diffY = 0
        
        self.count = 1
        
        print('shape:', self.shape, '\nmarco: ', self.marco, '\nsalida:', self.out)
        print('Nos movemos hacia el:', self.moves[self.rndm])
        
        
    def get_extent_shapely(self, shp):
        
        shp = fiona.open(shp)
        #print('zone:', self.moves[self.rndm])
        #GETTING THE GEOMETRY (COORDINATES)
        feature1 = shp.next()
        geom1 = feature1['geometry']
        a1 = Polygon(geom1['coordinates'][0])
        Oeste, Este, Norte, Sur = a1.bounds[0], a1.bounds[2], a1.bounds[3], a1.bounds[1]

        #return(Oeste, Este, Norte, Sur)
        move = {'NW': (Norte, Oeste), 'NE': (Norte, Este), 'SW': (Sur, Oeste), 'SE': (Sur, Este)}
        return move[self.moves[self.rndm]]
            
    
    def get_diff(self):
        
        ''' Este metodo computa la diferencia entre las coordenas del shape con respecto al marco (en la direccion aleatoria
        que haya tocado. Retorna una tupla  con valores (X, Y) con la diferencia. Por tanto get_diff[0] es la diferencia en X
        y get_diff[1] es la diferencia en Y)'''
        
        frameM = self.get_extent_shapely(self.marco)
        #print(frameM)
        NorteM, OesteM = frameM[0], frameM[1]
        frameS = self.get_extent_shapely(self.shape)
        #print(frameS)
        NorteS, OesteS = frameS[0], frameS[1]
        
        self.diffX = OesteM - OesteS
        self.diffY = NorteM - NorteS
        
        return(self.diffX, self.diffY)
        
    
    def new_geom(self):
        
        with fiona.open(self.shape, 'r') as source:
    
            # **source.meta is a shortcut to get the crs, driver, and schema
            # keyword arguments from the source Collection.
            with fiona.open(self.out, 'w', **source.meta) as sink:
                
                
                for f in source:
                    
                    #print(f)
            
                    try:
                    
                        feature1 = f['geometry']['coordinates'][0]
                        #geom1 = feature1['geometry']['coordinates']
                        #print(feature1)
                        #coords = geom1['coordinates'][0]
                        #CALCULAMOS UN VALOR RANDOM PARA MOVER EL SHAPE
                        X_offset = random.uniform(0.1, self.get_diff()[0])
                        Y_offset = random.uniform(0.1, self.get_diff()[1])
                        #print(X_offset, Y_offset)
                        #CREAMOS LA NUEVA LISTA DE COORDENADAS PARA EL SHAPE MOVIDO                                    
                        #geom2 = [(X_offset + i[0], Y_offset + i[1]) for i in feature1]                     
                        new_shape = Polygon(feature1)
                        
                        #PROBAMOS A GIRAR EL SHAPE
                        rotated_a = affinity.rotate(new_shape, random.randint(0, 360))
                        
                        #PROBAMOS A MOVERLO CON SHAPELY (funciona de las 2 maneras)
                        rotated_b = shapely.affinity.translate(rotated_a, X_offset, Y_offset)
                        
                        
                        #COMPROBAMOS QUE ESTE DENTRO DEL MARCO SIN INTERSECTAR
                        if self.check(rotated_b) == True:
                            
                            f['geometry'] = mapping(rotated_b)
                            sink.write(f)
                            
                        else:
                            
                            self.count += 1
                            f['geometry'] = mapping(rotated_b)
                            sink.write(f)
                            self.new_geom()
                            #print('intersecta')
                        
                    except Exception as e:
                        
                        # Writing uncleanable features to a different shapefile
                        # is another option.
                        print('error', e)
                        logging.exception("Error cleaning feature %s:", f['id'])
                
       
                
                
    def check(self, ncoords):
        
        '''En este metodo vamos a comprobar si el shape que estamos utilizando  esta incluido dentro del marco'''
                
        shape2 = fiona.open(self.marco)
        feature2 = shape2.next()
        geom2 = feature2['geometry']['coordinates'][0]
        a2 = Polygon(geom2)

        return(ncoords.within(a2))
        
        
    def run(self):
        
        
        if self.check() == True:
            print('El shape esta totalmente incluido dentro del marco. La diferencia es: ')
            print(self.get_diff())
            
        else:
            print('El shape no esta incluido dentro del marco')