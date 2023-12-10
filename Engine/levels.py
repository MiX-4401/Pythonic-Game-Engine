import pygame, os
from json    import loads
from inspect import getsourcefile
from Engine.tiles import EngineBasicTile 

class EngineLevels():
    def __init__(self, main, settings:dict={}):
        self.main = main
        self.settings: dict = settings

        self.levels:        list = []
        self.level_index:   int  = 0
        self.get_levels()

        # DEBUGGING #
        self.current_level: EngineLevel = self.levels[self.level_index]
        self.current_level.load_level()


    def get_paths(self, folders:list):
        my_path: str = getsourcefile(self.__init__)

        # Find directory to search #
        basename: str = os.path.basename(my_path)
        basedir:  str = os.path.abspath(my_path).split(basename)[0]

        # Get spritesheet paths from directory
        level_paths: list = []
        for rel_dir_path in folders:
            abs_dir_path: str = os.path.join(basedir, rel_dir_path)

            for filename in os.listdir(abs_dir_path):
                abs_path: str = os.path.join(abs_dir_path, filename)

                extension: str = filename.split(".")[-1]
                if extension not in ["tmj"]: continue

                if extension == "tmj":
                    level_paths.append(abs_path)


        return level_paths

    def load_json(self, path):

        with open(file=path, mode="r") as file:
            data: dict = loads(file.read())

        filename: str   = os.path.basename(path).split(".")[0]
        layers:   list  = []
        tilesets: list  = []
        size:     tuple = (data["width"], data["height"])  
        tilesize: tuple = (data["tilewidth"], data["tileheight"])

        # Get layers
        for layer in data["layers"]:
            type: str = layer["type"]

            # Get properties
            properties: dict = {}
            for property in layer["properties"]:
                d_name: str = property["name"]
                d_type: str = property["type"]
                d_value     = property["value"]
                
                if d_type == "bool":
                    if   d_value == "false": d_value = False
                    elif d_value == "true":  d_value = True
                elif d_type == "int":   d_value: int   = int(d_value)
                elif d_type == "str":   d_value: str   = str(d_value)  
                elif d_type == "float": d_value: float = float(d_value)  

                properties.update({d_name: d_value})

            if type == "tilelayer":
                bitmap: list; offset: tuple
                bitmap, offset = self.get_tilelayer(layerdata=layer)
                layers.append({"bitmap": bitmap, "offset": offset, "type": type, "properties": properties})
            
            elif type == "objectgroup":
                objects: dict; offset:tuple
                objects, offset = self.get_objectlayer(layerdata=layer)
                layers.append({"objects": objects, "offset": offset, "type": type, "properties": properties})
            
            elif type == "imagelayer":
                pass

        # Get tilesets
        for tileset in data["tilesets"]:
            firstgrid: str = tileset["firstgid"]
            source:    str = tileset["source"].split("/")[-1].split(".")[0]
            tilesets.append({"firstgrid": firstgrid, "source": source})   

        return filename, layers, tilesets, size, tilesize

    def convert_1d_bitmap_to_2d(self, bitmap:list, size:tuple):

        if len(bitmap) != size[1] * size[0]:
            return "Invalid input dimensions"
        
        reshaped_array = []
        for i in range(0, len(bitmap), size[0]):
            row = bitmap[i:i+size[0]]
            reshaped_array.append(row)

        return reshaped_array


    def get_tilelayer(self, layerdata:dict):
        bitmap: list  = self.convert_1d_bitmap_to_2d(bitmap=layerdata["data"], size=(layerdata["width"], layerdata["height"]))
        offset_x: int = 0; offset_y: int = 0
        if "offsetx" in layerdata: offset_x = layerdata["offsetx"]
        if "offsety" in layerdata: offset_y = layerdata["offsety"]

        return bitmap, (offset_x, offset_y)

    def get_objectlayer(self, layerdata:dict):
        objects: list = layerdata["objects"]
        offset_x: int = 0; offset_y: int = 0
        if "offsetx" in layerdata: offset_x = layerdata["offsetx"]
        if "offsety" in layerdata: offset_y = layerdata["offsety"]
        
        return objects, (offset_x, offset_y)

    def get_levels(self):
        paths: list = self.get_paths(folders=self.settings["levels"])
        
        levels: list = []
        for path in paths:
            filename: str; layers: list; tilesets: list; size: tuple; tilesize: tuple
            filename, layers, tilesets, size, tilesize = self.load_json(path=path)

            level: EngineLevel = EngineLevel(main=self.main, name=filename, layers=layers, tilesets=tilesets, size=size, tilesize=tilesize)
            levels.append(level)

        self.levels = levels


    def update(self):
        self.current_level.update()

    def draw(self):
        self.current_level.draw()

    @classmethod
    def d_update(cls, func):
        def inner(self, *args, **kwargs):
            
            self.current_level.update()

            result = func(self, *args, **kwargs)

            return result
        
        return inner
    
    @classmethod
    def d_draw(cls, func):
        def inner(self, *args, **kwargs):
            
            self.current_level.draw()

            result = func(self, *args, **kwargs)

            return result
        
        return inner

      
    
class EngineLevel():
    def __init__(self, main, name:str, layers:list, tilesets:list, size:tuple, tilesize:tuple):
        self.main = main
        self.name:     str   = name
        self.layers:   list  = layers
        self.tilesize: tuple = tilesize

        self.tilesets: list  = tilesets
        self.size:     tuple = (size[0], size[1]) # size * 32 is development only. Only works when the scale is factored by the average tile size after scaling
        self.tiles:    dict  = {}
        self.objects:  dict  = {}
        self.images:   dict  = {}


    def rematch_tile_ids(self, tilesets):
       
        level_tiles: list = []
        for tileset in tilesets:
            firstgrid: str = tileset["firstgrid"]
            source:    str = tileset["source"]

            global_tiles: list = self.main.tiles.tiles[source]
            for tile in global_tiles:

                level_id: int = firstgrid + int(tile) 

                level_tiles.append({"id_": level_id, "surfaces": global_tiles[tile]["surfaces"], "normals": global_tiles[tile]["normals"], "properties": global_tiles[tile]["properties"]})

        return level_tiles

    def create_object(self, type: str, properties:dict, polygons:list, pos:list, name:str):
        return None

    def load_tiles(self, level_tiles:dict, layer:dict):

            tiles: list = []
            for i,y in enumerate(layer["bitmap"]):
                for ii,id_ in enumerate(y):
                    if id_ == 0: continue

                    tile: dict = {}
                    for tiledata in level_tiles:
                        if tiledata["id_"] == id_: tile = tiledata
                    
                    surfaces:   list  = tile["surfaces"]
                    normals:    list  = tile["normals"]
                    properties: dict  = tile["properties"]
                    polygons:   None  = None # polygons:   None = tile["polygons"]
                    size:       tuple = surfaces[0].get_size() 
                    pos:        list  = [ii*size[0], i*size[1]]
                    tile:       EngineBasicTile = EngineBasicTile(surfaces=surfaces, normals=normals, polygons=polygons, properties=properties, pos=pos)
                    
                    tiles.append(tile)

            return tiles

    def load_objects(self, layer:dict): 
        objects: list = []
        for object in layer["objects"]:
            name: str   = object["name"]
            type: str   = object["type"]
            pos:  list  = [object["x"], object["y"]]
            polygons: None = []

            # Get properties
            properties: dict = {}
            for property in object["properties"]:
                d_name: str = property["name"]
                d_type: str = property["type"]
                d_value     = property["value"]
                
                if d_type == "bool":
                    if   d_value == "false": d_value = False
                    elif d_value == "true":  d_value = True
                elif d_type == "int":   d_value: int   = int(d_value)
                elif d_type == "str":   d_value: str   = str(d_value)  
                elif d_type == "float": d_value: float = float(d_value)  

                properties.update({d_name: d_value})

            # Create object
            object = self.create_object(type=type, properties=properties, polygons=polygons, pos=pos, name=name)
            if object == None: continue
            
            objects.append(object)

        return objects

    def load_level(self):
    
        # Get re-id'd tiles for this level
        level_tiles: list = self.rematch_tile_ids(tilesets=self.tilesets)

        # load tiles, objects, images from layers
        tiles:   dict = {}
        objects: dict = {}
        images:  dict = {}
        for i,layer in enumerate(self.layers):
                
            if layer["type"] == "tilelayer":
                tiles.update({i: self.load_tiles(level_tiles=level_tiles, layer=layer)})
            if layer["type"] == "objectgroup":
                objects.update({i: self.load_objects(layer=layer)})
            if layer["type"] == "imagelayer":
                pass

        self.tiles   = tiles
        self.objects = objects
        self.images  = images

        # Register surfaces
        for i,x in enumerate(self.layers):
            static: bool = x["properties"]["draw_static"]
            self.main.renderer.register_layer(key=i, pos=self.layers[i]["offset"], static=static)
        self.draw_static()

    def draw_dynamic(self):

        # Draw images -> tiles -> objects
        for i in range(len(self.layers)):
            
            layer: dict = self.main.renderer.surfaces[i]

            if layer["static"]: continue

            layer["surface"].fill(color=(0,0,0,0))

            if i in self.images:
                images:  list = self.images[i]
                for image in images:   image.draw(surface=layer["surface"])
            
            if i in self.tiles:
                tiles:   list = self.tiles[i]
                for tile in tiles:     tile.draw(surface=layer["surface"])
            
            if i in self.objects:
                objects: list = self.objects[i]
                for object in objects: object.draw(surface=layer["surface"])

    def draw_static(self):
        # Draw images -> tiles -> objects
        for i in range(len(self.layers)):
            
            layer: dict = self.main.renderer.surfaces[i]

            if not layer["static"]: continue

            layer["surface"].fill(color=(0,0,0,0))

            if i in self.images:
                images:  list = self.images[i]
                for image in images:   image.draw(surface=layer["surface"])
            
            if i in self.tiles:
                tiles:   list = self.tiles[i]
                for tile in tiles:     tile.draw(surface=layer["surface"])
            
            if i in self.objects:
                objects: list = self.objects[i]
                for object in objects: object.draw(surface=layer["surface"])


    def update(self):

        # Update objects -> tiles -> images
        for i,x in enumerate(self.layers):

            if x["properties"]["update_static"]: continue

            if i in self.tiles:
                for tile in self.tiles[i]:     tile.update()
            if i in self.objects:
                for object in self.objects[i]: object.update()
            if i in self.images:
                for image in self.images[i]:   image.update()

    def draw(self):

        self.draw_dynamic()
            

    @classmethod
    def d_update(cls, func):
        def inner(self, *args, **kwargs):
            
            # Update objects -> tiles -> images
            for i in range(len(self.layers)):
                if i in self.tiles:
                    for tile in self.tiles[i]:     tile.update
                if i in self.objects:
                    for object in self.objects[i]: object.update
                if i in self.images:
                    for image in self.images[i]:   image.update

            
            result = func(self, *args, **kwargs)

            return result
        
        return inner
    
    @classmethod
    def d_draw(cls, func):
        def inner(self, *args, **kwargs):
            
            # Draw images -> tiles -> objects
            for i in range(len(self.layers)):
                
                layer: pygame.Surface = self.main.renderer.surfaces[i]

                if i in self.images:
                    images:  list = self.images[i]
                    for image in images:   image.draw(surface=layer["surface"])
                
                if i in self.tiles:
                    tiles:   list = self.tiles[i]
                    for tile in tiles:     tile.draw(surface=layer["surface"])
                
                if i in self.objects:
                    objects: list = self.objects[i]
                    for object in objects: object.draw(surface=layer["surface"])

            result = func(self, *args, **kwargs)

            return result
        
        return inner
      




