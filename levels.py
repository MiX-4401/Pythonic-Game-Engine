from Engine.levels import EngineLevels, EngineLevel
from objects import Ball
from player  import Player

class Levels(EngineLevels):
    def __init__(self, main, settings:dict={}):
        super().__init__(main=main, settings=settings)

    def get_levels(self):
        paths: list = self.get_paths(folders=self.settings["levels"])
        
        levels: list = []
        for path in paths:
            filename: str; layers: list; tilesets: list; size: tuple; tilesize: tuple
            filename, layers, tilesets, size, tilesize = self.load_json(path=path)

            level: Level = Level(main=self.main, name=filename, layers=layers, tilesets=tilesets, size=size, tilesize=tilesize)
            levels.append(level)

        self.levels = levels

class Level(EngineLevel):
    def __init__(self, main, name:str, layers:list, tilesets:list, size:tuple, tilesize:tuple):
        super().__init__(main=main, name=name, layers=layers, tilesets=tilesets, size=size, tilesize=tilesize)

    def create_object(self, type:str,  properties:dict, polygons:list, pos:list, name:str):
        pos:      list = [pos[0]*self.main.global_settings["scale"], pos[1]*self.main.global_settings["scale"]]
        tilesize: list = [self.tilesize[0]*self.main.global_settings["scale"], self.tilesize[1]*self.main.global_settings["scale"]]
        object: None = None
        if type == "ball":
            spritesheet: list = [x for x in self.main.sprites.sprites["animate_0"].values()]
            surfaces:    list = [x[0] for x in spritesheet[1::]]
            normals:     list = [x[1] for x in spritesheet[1::]]
            object:      Ball = Ball(main=self.main, normals=normals, surfaces=surfaces, properties=properties, polygons=polygons, pos=[pos[0], pos[1]-tilesize[1]], name=name)
        if type == "player":
            spritesheet: list = [x for x in self.main.sprites.sprites["player"].values()]
            surfaces:    list = [x for x in spritesheet[1::]]
            normals:     list = [x[1] for x in spritesheet[1::]]
            object:      Player = Player(main=self.main, normals=normals, surfaces=surfaces, properties=properties, polygons=polygons, pos=[pos[0], pos[1]-tilesize[1]*2], name=name)
    
        return object



