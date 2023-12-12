import os
from PIL import Image
from inspect import getsourcefile
from math import ceil
from Engine.functions import split_list
from Engine.graphics import Canvas, Texture

class EngineSprites():

    normal_colour: tuple = (50.2, 50.2, 100)
    def __init__(self, main, settings:dict={}):
        self.main = main
        self.settings: dict = settings

        self.spritesource_paths: list = []
        self.sprites:            dict = {}

        self.backgroundsource_paths: list = []
        self.backgrounds:            dict = {}

        self.get_sprites()
        self.get_backgrounds()

    
    def get_sprites(self):

        # Get paths
        spritesheet_paths: list; spritesource_paths: list
        spritesheet_paths, spritesource_paths = self.get_paths(folders=self.settings["spritesheets"])

        # Load spritesheet surfaces
        grouped_sprites: dict = {}
        for path in spritesheet_paths:

            # Load spritesheet data
            spritesheet_name: str = os.path.basename(path).split(".")[0]
            spritesheet: pygame.Surface = self.load_spritesheet(path=path) 
            tilesize: tuple; has_normals: bool
            tilesize, has_normals = self.scan_spritesheet(path=path); 

            # Load sprites
            sprites: list; normals: list
            sprites = self.load_sprites(surface=spritesheet, tilesize=tilesize)
            
            # Get normals (if any)
            if has_normals:
                # IF normals included, split sprites and normals from spritesheet
                sprites, normals = split_list(my_list=sprites)
            else:
                # ELSE create empty normal surfaces for each sprite (using pointers)
                normals = self.load_normals(sprites=sprites)              

            # Combine normals with the sprites
            sprites: dict = self.attach_normals_with_sprites(sprites=sprites, normals=normals)

            grouped_sprites[spritesheet_name] = sprites

        self.sprites            = grouped_sprites
        self.spritesource_paths = spritesource_paths
        
    def get_backgrounds(self):
        
        # Get paths
        background_paths: list; backgroundsource_paths: list
        background_paths, backgroundsource_paths = self.get_paths(self.settings["backgrounds"])

        # Load background surfaces
        backgrounds: list = []
        for path in background_paths:
            surface: pygame.Surface = self.load_spritesheet(path=path)
            backgrounds.append(surface)

        self.backgrounds            = backgrounds
        self.backgroundsource_paths = backgroundsource_paths

    def get_paths(self, folders:list):
        my_path: str = getsourcefile(self.__init__)

        # Find directory to search #
        basename: str = os.path.basename(my_path)
        basedir:  str = os.path.abspath(my_path).split(basename)[0]

        # Get spritesheet paths from directory
        sourcesheet_paths: list = []
        spritesheet_paths: list = []
        for rel_dir_path in folders:
            abs_dir_path: str = os.path.join(basedir, rel_dir_path)

            for filename in os.listdir(abs_dir_path):
                abs_path: str = os.path.join(abs_dir_path, filename)

                extension: str = filename.split(".")[-1]
                if extension not in ["tsx", "png", "jpg"]: continue

                if extension == "tsx":
                    sourcesheet_paths.append(abs_path)
                else:
                    spritesheet_paths.append(abs_path)

        return spritesheet_paths, sourcesheet_paths

    def scan_spritesheet(self, path:str):
        
        # Open file
        spritesheet: Image.Image = Image.open(fp=path).convert("RGB")
        size: tuple = spritesheet.size
        
        # Scan for red-pixel on x-axis (255,0,0) for width
        for x in range(size[0]):
            pixel_colour: tuple = spritesheet.getpixel(xy=(x,0))
            if pixel_colour == (255, 0, 0):
                break
        
        # Scan for blue-pixel on y-axis (0,0,255) for height
        for y in range(size[1]):
            pixel_colour: tuple = spritesheet.getpixel(xy=(x,y))
            if pixel_colour == (0, 0, 255):
                break

        # Scan for green-pixel for on xy-axies (0,255,0) for normalchecks
        has_normals: bool = True if spritesheet.getpixel(xy=(1,0)) == (0,255,0) else False

        spritesheet.close()
        tilesize:     tuple = (x+1, y+1)

        return tilesize, has_normals

    def load_spritesheet(self, path:str):
        spritesheet_surface: pygame.image   = pygame.image.load(path).convert_alpha()
        return spritesheet_surface
    
    def load_sprites(self, surface:pygame.Surface, tilesize:int):
        
        sprites: list = []
                
        # Find num of iterations for sprite parsing
        spritesheet_size = surface.get_size()
        x_num_tiles = spritesheet_size[0] // tilesize[0]
        y_num_tiles = spritesheet_size[1] // tilesize[1]
        
        # Sprite segmenter loop
        #
        for y in range(y_num_tiles):
            for x in range(x_num_tiles):
 
                # Find sprite position via corners
                corners: tuple = ( 
                    x * tilesize[0],
                    y * tilesize[1],
                    x * tilesize[0] + tilesize[0],
                    y * tilesize[1] + tilesize[1]
                )

                # Load sprite
                sprite: pygame.Surface = pygame.Surface(tilesize, pygame.SRCALPHA).convert_alpha()
                sprite.blit(source=surface, dest=(0,0), area=corners)
                sprite = scale_surface(surface=sprite, scale=self.main.global_settings["scale"])
                
                sprites.append(sprite)

        return sprites

    def load_normals(self, sprites:list):

        options: dict = {}
        normals: list = []
        for sprite in sprites:

            # Get sprite size
            size: tuple = sprite.get_size()
            key:  str = f"{size[0]}x{size[1]}"
            
            # Create new empty normal surface if size is not avaliable
            if key not in options:
                options[key] = pygame.Surface(size=size)
                options[key].fill(EngineSprites.normal_colour)
            
            normals.append(options[key]) 
        
        return normals
    
    def attach_normals_with_sprites(self, sprites:list, normals:list):
        
        # Zip sprites and normals
        grouped_list: list = zip(sprites, normals)
        
        # Set sprites into preffered format: {id_: (sprites, normal)}
        sprites: dict = {}
        for i,group in enumerate(grouped_list):
            sprites[str(i)] = group
        
        return sprites

    def update(self):
        pass

    def draw(self):
        pass

    
    @classmethod
    def d_update(cls, func):
        def inner(self, *args, **kwargs):

            result = func(self, *args, **kwargs)

            return result
        
        return inner

    @classmethod
    def d_draw(cls, func):
        def inner(self, *args, **kwargs):

            result = func(self, *args, **kwargs)

            return result

        return inner
    
    
