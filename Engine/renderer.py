from Engine.graphics import Canvas

class EngineRenderer():
    def __init__(self, main, settings:dict={}):
        self.main           = main
        self.settings: dict = settings

        self.native_resolution: tuple = main.native_resolution

        self.canvases:   dict = {} # 0: {"canvas": Canvas.load(native_resolution), "pos": (0, 0), "static": bool}
        self.normals:    dict = {} # 0: {"canvas": Canvas.load(native_resolution), "pos": (0, 0), "static": bool}


    def register_layer(self, key:int, size:tuple=(1000,1000), static:bool=True, pos:tuple=(0, 0), location:str="canvases"):
        canvas: Canvas = Canvas(size=size)
        
        if location == "canvases":
            self.surfaces[key]: dict = {
                "canvas":  canvas,
                "pos":     pos,
                "static":  static
            }
        elif location == "normals":
            self.surfaces[key]: dict = {
                "canvas":  canvas,
                "pos":     pos,
                "static":  static
            }

    def draw_layer(self, key:int, canvas:Canvas, location:str="canvases"):
        
        if location == "canvases":
            self.reset_layer(key=key, location=location)

            layer: dict = self.canvases[key]
            layer["canvas"].blit(source=canvas, dest=(0,0))
        elif location == "normals":
            self.reset_layer(key=key, location=location)

            layer: dict = self.normals[key]
            layer["canvas"].blit(source=canvas, dest=(0,0))
            

    def reset_layer(self, key:int, location:str="canvases"):
        if location == "canvases":
            layer: dict = self.canvases[key]
            layer["canvas"].fill(color=(0,0,0))
        elif location == "normals":
            layer: dict = self.normals[key]
            layer["canvas"].fill(color=(0,0,0))
            

    def clear_surfaces(self, location:str="canvases"):
        if location == "canvases":
            self.canvases = {}
        elif location == "normals":
            self.normals = {}

    def update(self):
        pass
    
    def draw(self, frame:Canvas, location:str="canvases"):

        loc: int = 0 if location == "canvases" else 1 if location == "normals" else -1
        for key in [self.canvases, self.normals][loc]:
            layer:   dict  = self.canvases[key]
            canvas: Canvas = layer["canvas"]
            pos:     tuple = layer["pos"]
            frame.blit(source=canvas, dest=pos, area=self.main.camera.camera)


    @classmethod
    def d_update(cls, func):
        def inner(self, *args, **kwargs):

            result = func(self, *args, **kwargs)

            return result
        
        return inner

    @classmethod
    def d_draw(cls, func):
        def inner(self, *args, **kwargs):

            loc: int = 0 if kwargs["location"] == "canvases" else 1 if kwargs["location"] == "normals" else -1
            for key in [self.canvases, self.normals][loc]:
                layer:   dict  = self.canvases[key]
                Canvas: Canvas = layer["canvas"]
                pos:     tuple = layer["pos"]
                kwargs["frame"].blit(source=canvas, dest=pos, area=self.main.camera.camera)
            
            result = func(self, *args, **kwargs)

            return result

        return inner
    
        
