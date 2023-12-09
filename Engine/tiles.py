import pygame
import xml.etree.ElementTree as XML

class EngineTiles():
    def __init__(self, main, settings:dict={}):
        self.main = main
        self.settings: dict = settings
        self.tiles:    dict = {}

        self.load_tiles()

    def load_xml(self, path:str):
        
        root           = XML.parse(source=path).getroot()
        sheetname: str = root.get("name")

        # Get tile data
        sheetdata:   dict = {}
        for tile in root.findall("tile"):
            id_: str = tile.get("id")
            
            # Get tile properties
            properties: dict = {}
            for x in tile.findall("properties"):

                for prop in x.findall("property"):
                    p_name:  str = prop.get("name")
                    p_type:  str = prop.get("type")
                    p_value: str = prop.get("value")

                    if p_type == "bool":
                        if   p_value == "false": p_value = False
                        elif p_value == "true":  p_value = True
                    elif p_type == "int":   p_value:  int    = int(p_value)
                    elif p_type == "str":    p_value: str    = str(p_value)  
                    elif p_type == "float":  p_value: float  = float(p_value)  

                    # Add properties to this tile
                    properties.update({p_name: p_value})

            # Add tile data (id_ - properties) 
            sheetdata.update({id_: properties})
        return sheetname, sheetdata

    def group_sheet(self, sheetname:str, sheetdata:dict):

        tiles: dict = {0: {"surfaces": [], "properties": sheetdata["1"]}} # {id: [{ "surface": pygame.Surface, "properties": {} }]} 
        for key in sheetdata: 
            if key == "0": continue

            surface: pygame.Surface = self.get_surface(sheetname=sheetname, key=key)
            tiles[0]["surfaces"].append(surface)

        return tiles

    def disperse_sheet(self, sheetname:str, sheetdata:dict):

        tiles: dict = {} # {id: [{ "surface": pygame.Surface, "properties": {} }]}
        for key in sheetdata:
            if key == "0": continue
            texture_surface: pygame.Surface
            texture_surface = self.get_surface(sheetname=sheetname, key=key)
            surface: list = [texture_surface]
            properties: dict = sheetdata[key] 
            
            tiles.update({key: {"surfaces": surface, "properties": properties}})

        return tiles

    def get_surface(self, sheetname:str, key:str):
        return self.main.sprites.sprites[sheetname][key]
        
    def load_tiles(self):
        spritesource_paths: list = self.main.sprites.spritesource_paths

        # Get all data of the tiles 
        tiles: dict = {}
        for path in spritesource_paths:
            sheetname: str; sheetdata: dict
            sheetname, sheetdata = self.load_xml(path=path)

            # Group/Disperse sheetdata & Append to tiledata
            config_tile: dict = sheetdata["0"]
            if config_tile["is_grouped"]:
                tiles.update({sheetname: self.group_sheet(sheetname=sheetname, sheetdata=sheetdata)})
            else:
                tiles.update({sheetname: self.disperse_sheet(sheetname=sheetname, sheetdata=sheetdata)})
        self.tiles = tiles
            

    @classmethod
    def d_load_tiles(cls, func):
        def inner(self, *args, **kwargs):
            spritesource_paths: list = self.main.sprites.spritesource_paths

            # Get all data of the tiles 
            tiles: list = []
            for path in spritesource_paths:
                sheetname: str; sheetdata: dict
                sheetname, sheetdata = self.load_xml(path=path)

                # Group/Disperse sheetdata & Append to tiledata
                config_tile: dict = sheetdata["0"]
                if config_tile["is_grouped"]:
                    tiles.append(self.group_sheet(sheetname=sheetname, sheetdata=sheetdata))
                else:
                    tiles.append(self.disperse_sheet(sheetname=sheetname, sheetdata=sheetdata))

            result = func(self, *args, **kwargs)

            self.tiles = tiles

            return result

        return inner


class EngineBasicTile():
    def __init__(self, surfaces:list, polygons:list, properties:dict, pos:tuple):
        self.surfaces:   list = surfaces
        self.polygons:   None = polygons
        self.properties: dict = properties
        self.pos:        list = pos

        self.is_animating:   bool  = False 
        self.current_sprite: int   = 0
        self.sprite_inc:     float = 0
        self.image: pygame.Surface = self.surfaces[self.current_sprite]

        self.animate()

    def animate(self):
        if len(self.surfaces) > 1:
            self.is_animating = True
            self.sprite_inc = self.properties["speed"]


    def update(self):

        # Animation
        if self.is_animating:
            self.current_sprite += self.sprite_inc
        
            if self.current_sprite >= len(self.surfaces): self.current_sprite = 0
            self.image = self.surfaces[int(self.current_sprite)]

    def draw(self, surface:pygame.Surface):
        surface.blit(source=self.surfaces[0], dest=self.pos)
