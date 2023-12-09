import pygame

class EngineRenderer():
    def __init__(self, main, settings:dict={}):
        self.main           = main
        self.settings: dict = settings

        self.native_resolution: tuple = main.native_resolution

        self.surfaces:   dict = {} # 0: {"surface": pygame.Surface(native_resolution, pygame.SRCALPHA), "pos": (0, 0), "static": bool}

    def register_layer(self, key:int, size:tuple=(1000,1000), static:bool=True, pos:tuple=(0, 0)):
        surface: pygame.Surface = pygame.Surface(size, pygame.SRCALPHA)
        self.surfaces[key]: dict = {
            "surface": surface,
            "pos":     pos,
            "static":  static
        }
    
    def draw_layer(self, key:int, surface:pygame.Surface):
        

        self.reset_layer(key=key)

        layer: dict = self.surfaces[key]
        layer["surface"].blit(source=surface, dest=(0,0))
    
    def reset_layer(self, key:int):
        
        layer: dict = self.surfaces[key]
        layer["surface"].fill(color=(0,0,0))

    def clear_surfaces(self):
        self.surfaces = {}


    def update(self):
        pass
    
    def draw(self, frame:pygame.Surface):

        for key in self.surfaces:
            layer:   dict  = self.surfaces[key]
            surface: pygame.Surface = layer["surface"]
            pos:     tuple = layer["pos"]
            frame.blit(source=surface, dest=pos, area=self.main.camera.camera)


    @classmethod
    def d_update(cls, func):
        def inner(self, *args, **kwargs):

            result = func(self, *args, **kwargs)

            return result
        
        return inner

    @classmethod
    def d_draw(cls, func):
        def inner(self, *args, **kwargs):

            for key in self.surfaces:
                layer:   dict  = self.surfaces[key]
                surface: pygame.Surface = layer["surface"]
                pos:     tuple = layer["pos"]

                kwargs["frame"].blit(source=surface, dest=pos, area=self.main.camera.area)
            
            result = func(self, *args, **kwargs)

            return result

        return inner
    
        
