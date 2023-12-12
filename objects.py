from Engine.objects import Object

class Ball(Object):
    def __init__(self, main, surfaces:list, normals:list, properties:dict, polygons:list, pos:list, name:str):
        super().__init__(main=main, surfaces=surfaces, normals=normals, properties=properties, polygons=polygons, pos=pos, name=name)


