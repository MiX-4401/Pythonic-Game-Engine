import pygame, os
from PIL import Image
from inspect import getsourcefile
from Engine.functions import scale_surface

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
        sprites: dict = {}
        for path in spritesheet_paths:
            spritesheet_name: str = os.path.basename(path).split(".")[0]

            tilesize: tuple; normal_index: tuple
            tilesize, normal_index  = self.scan_spritesheet(path=path)
            surface: pygame.Surface = self.load_spritesheet(path=path)
            sheet_sprites: list     = self.load_sprites(surface=surface, tilesize=tilesize)
            sprites.update({spritesheet_name: sheet_sprites})

        self.sprites            = sprites
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

        # Scan for green-pixel for on xy-axies (0,255,0) for normal index start position
        for ii in range(y):
            
            for i in range(x - 1):
                pixel_colour = spritesheet.getpixel(xy=(i, ii))
                if pixel_colour == (0,255,0):
                    print(i, ii)
                    break

        spritesheet.close()
        tilesize:     tuple = (x+1, y+1)
        normal_index: tuple = (ii,i)
        print(normal_index)
        return tilesize, normal_index

    def load_spritesheet(self, path:str):
        spritesheet_surface: pygame.image = pygame.image.load(path).convert_alpha()
        return spritesheet_surface
    
    def load_sprites(self, surface:pygame.Surface, tilesize:int):
        
        sprites: dict = {}
                
        # Find num of iterations for sprite parsing
        sheet_resolution = surface.get_size()
        size_x = sheet_resolution[0] // tilesize[0]
        size_y = sheet_resolution[1] // tilesize[1]
        
        # Blits sections of spritesheets to new surfaces which are then scaled linearly 
        counter: int = 0
        y: int = 0
        while y < size_y:
            for x in range(size_x):
 
                # Find rect area of which to crop spritesheets
                corners: tuple = ( 
                    x * tilesize[0],
                    y * tilesize[1],
                    x * tilesize[0] + tilesize[0],
                    y * tilesize[1] + tilesize[1]
                )

                # Blit spritesheet sections to new surface; Then scale
                sprite: pygame.Surface = pygame.Surface(tilesize, pygame.SRCALPHA).convert_alpha()
                sprite.blit(source=surface, dest=(0,0), area=corners)
                sprite = scale_surface(surface=sprite, scale=self.main.global_settings["scale"])
                sprites.update({str(counter): sprite})
                counter += 1
            y+=1

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
    
    
