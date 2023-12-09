from Engine.objects import Object

class Ball(Object):
    def __init__(self, main, surfaces:list, properties:dict, polygons:list, pos:list, name:str):
        super().__init__(main=main, surfaces=surfaces, properties=properties, polygons=polygons, pos=pos, name=name)


