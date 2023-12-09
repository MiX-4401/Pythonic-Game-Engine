import moderngl as mgl, numpy as np
import pygame, os
from inspect import getsourcefile

class EngineGraphics():

    def __init__(self, main, ctx, settings:dict={}):
        self.main = main
        self.ctx  = ctx
        self.settings: dict = settings
        self.surface:  pygame.Surface = pygame.Surface(main.native_resolution, pygame.SRCALPHA)

        self.shader_paths: dict = {
            "display": EngineGraphics.get_base_shaders()
        }
        self.load_shaders()

        self.programs:      dict = {}
        self.vertex_arrays: dict = {}
        self.framebuffers:  dict = {}
        self.buffers:       dict = {}
        self.textures:      dict = {}

        self.programs["main"]:      mgl.Program     = self.ctx.program(vertex_shader=self.load_shader(path=self.shader_paths["display"]["vert"]), fragment_shader=self.load_shader(path=self.shader_paths["display"]["frag"]))
        self.buffers["main"]:       mgl.Buffer      = self.ctx.buffer(np.array([-1.0, 1.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, -1.0, -1.0, 0.0, 1.0, 1.0, -1.0, 1.0, 1.0], dtype="f4")) 
        self.vertex_arrays["main"]: mgl.VertexArray = self.ctx.vertex_array(self.programs["main"], [(self.buffers["main"], "2f 2f", "aPosition", "aTexCoord")])
        self.textures["main"]:      mgl.Texture     = self.ctx.texture(size=main.native_resolution, components=4)

    def load_shaders(self):
        paths: dict = self.get_paths(self.settings["shaders"])
        self.shader_paths.update(paths)

    def get_paths(self, folders:str):
        my_path: str = getsourcefile(self.__init__)

        # Find directory to search #
        basename: str = os.path.basename(my_path)
        basedir:  str = os.path.abspath(my_path).split(basename)[0]

        # Get spritesheet paths from directory
        shader_paths: dict = {} # { <name>: {vert: <path>, <frag>: <path>} }
        for rel_dir_path in folders:
            abs_dir_path: str = os.path.join(basedir, rel_dir_path)

            for filename in os.listdir(abs_dir_path):
                abs_path: str = os.path.join(abs_dir_path, filename)

                name: str; extension: str 
                name, extension = filename.split(".")

                # Create shader group if unique path is found
                if name not in shader_paths: shader_paths[name] = {"vert": None, "frag": None}

                # Add vertex and Fragment shader to shader group
                if extension == "vert":
                    shader_paths[name]["vert"] = abs_path
                elif extension == "frag":
                    shader_paths[name]["frag"] = abs_path

        return shader_paths

    def load_shader(self, path):
        """
        Loads the contents of a shader from file
        """
        with open(file=path, mode="r") as f:
            return f.read()


    def update(self):
        self.textures["main"].write(self.main.screen.get_view("1"))
        self.textures["main"].swizzle:  str = "BGRA"
        self.textures["main"].filter: tuple = (mgl.NEAREST, mgl.NEAREST)

    def draw(self):
        self.textures["main"].use(location=0)
        self.programs["main"]["tScene"] = 0
        self.vertex_arrays["main"].render(mode=mgl.TRIANGLE_STRIP)


    def garbage_collection(self):
        self.programs["main"].release()
        self.vertex_arrays["main"].release()
        self.buffers["main"].release()
        self.textures["main"].release()

    @classmethod
    def d_garbage_collection(cls, func):
        def inner(self, *args, **kwargs):
            
            self.programs["main"].release()
            self.vertex_arrays["main"].release()
            self.buffers["main"].release()
            self.textures["main"].release()

            result = func(self, *args, **kwargs)

            return result

        return inner

    @classmethod
    def d_update(cls, func):
        def inner(self, *args, **kwargs):
            
            result = func(self, *args, **kwargs)

            self.textures["main"].write(self.surface.get_view("1"))
            self.textures["main"].swizzle: str = "BGRA"
            self.textures["main"].filter: tuple = (mgl.NEAREST, mgl.NEAREST)

            return result

        return inner
    
    @classmethod
    def d_draw(cls, func):
        def inner(self, *args, **kwargs):

            result = func(self, *args, **kwargs)

            self.textures["main"].use(location=0)
            self.programs["main"]["tScene"] = 0
            self.vertex_arrays["main"].render(mode=mgl.TRIANGLE_STRIP)

            return result

        return inner

    @classmethod
    def get_base_shaders(cls):
        my_path: str = __file__.split(os.path.basename(__file__))[0]
        my_dir:  str = f"{os.path.abspath(my_path)}\shaders"

        shader_paths: dict = {"vert": None, "frag": None}
        for x in os.listdir(f"{my_path}\shaders"):
            if x == "display.frag":
                shader_paths["frag"] = f"{my_dir}\{x}"
            elif x == "display.vert":
                shader_paths["vert"] = f"{my_dir}\{x}"
        
        return shader_paths

    