import os

ruta = r'O:\consultas\shapes'
mc = r'O:\consultas\shapes\Irregular_Frame.shp'
shplist = []

for i in os.listdir(ruta):
    
    if i.endswith('.shp') and not i.startswith('Irregular'):
        
        shplist.append(os.path.join(ruta, i))
        

for shp in shplist:
    
    pr = randomly_move(shp, mc)
    pr.new_geom()
    print(pr.shape, 'realizado en', pr.count, 'intentos\n')