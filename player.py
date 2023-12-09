from Engine.player import EnginePlayer


class Player(EnginePlayer):
    def __init__(self, main, surfaces:list, properties:dict, polygons=list, pos=list, name=str, settings:dict={}):
        super().__init__(main=main, surfaces=surfaces, properties=properties, polygons=polygons, pos=pos, name=name)
        self.main.player = self

    