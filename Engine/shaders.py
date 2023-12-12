import moderngl as mgl
import numpy as np
import os
from Engine.graphics import Canvas, Texture, Transform
from inspect import getsourcefile

class EngineShaders():

    def __init__(self, main, ctx, settings:dict={}):
        self.main = main
        self.ctx  = ctx
        self.settings: dict = settings

        self.shader_paths:  dict = {}
        self.shader_data:   dict = {}

        self.programs:      dict = {}
        self.buffers:       dict = {}
        self.vaos:          dict = {}

        self.load_shader_paths()
        self.load_shader_data()

        self.load_buffers()
        self.load_programs()
        self.load_vaos()
        self.load_graphics()

    def load_shader_paths(self):
        paths: dict = self.get_paths(self.settings["shaders"])
        self.shader_paths = paths

    def load_shader_data(self):
        paths: dict = self.shader_paths

        shader_data: dict = {}
        for key in paths:
            vert: str = paths[key]["vert"]
            frag: str = paths[key]["frag"]
            
            if vert != None: vert = self.read_file(path=vert)
            if frag != None: frag = self.read_file(path=frag)

            shader_data[key] = {"vert": vert, "frag": frag}

        self.shader_data = shader_data

    def load_graphics(self):
        Texture.init(ctx=self.ctx, program=self.programs["blit"], vao=self.vaos["blit"])
        Canvas.init(ctx=self.ctx, program=self.programs["blit"], vao=self.vaos["blit"])
        Transform.init(
            ctx=self.ctx, 
            programs={
                "scale": self.programs["main"],
                "flip":  self.programs["flip"]
            },
            vaos={
                "scale": self.vaos["main"],
                "flip":  self.vaos["flip"]
            }
        )

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

    def read_file(self, path):
        """
        Loads the contents of a shader from file
        """
        with open(file=path, mode="r") as f:
            return f.read()

    def load_buffers(self):
        self.buffers["main"]: mgl.Buffer = self.ctx.buffer(np.array([-1.0, -1.0, 0.0, 0.0, 1.0, -1.0, 1.0, 0.0,-1.0,  1.0, 0.0, 1.0, 1.0,  1.0, 1.0, 1.0], dtype='f4'))

    def load_programs(self):
        self.programs["main"]:  mgl.Program = self.ctx.program(vertex_shader=self.shader_data["main"]["vert"], fragment_shader=self.shader_data["main"]["frag"])
        self.programs["blit"]:  mgl.Program = self.ctx.program(vertex_shader=self.shader_data["blit"]["vert"], fragment_shader=self.shader_data["main"]["frag"])
        self.programs["flip"]:  mgl.Program = self.ctx.program(vertex_shader=self.shader_data["flip"]["vert"], fragment_shader=self.shader_data["main"]["frag"])

    def load_vaos(self):
        self.vaos["main"]:  mgl.VertexArray = self.ctx.vertex_array(self.programs["main"],  [(self.buffers["main"], "2f 2f", "aPosition", "aTexCoord")])
        self.vaos["blit"]:  mgl.VertexArray = self.ctx.vertex_array(self.programs["blit"],  [(self.buffers["main"], "2f 2f", "aPosition", "aTexCoord")])
        self.vaos["flip"]:  mgl.VertexArray = self.ctx.vertex_array(self.programs["flip"],  [(self.buffers["main"], "2f 2f", "aPosition", "aTexCoord")])


    def garbage_collection(self):
        for key in self.programs:
            self.programs[key].release()
        for key in self.vaos:
            self.vaos[key].release()
        for key in self.buffers:
            self.buffers[key].release()

    @classmethod
    def d_garbage_collection(cls, func):
        def inner(self, *args, **kwargs):

            result = func(self, *args, **kwargs)

            return result

        return inner

    @classmethod
    def d_load_buffers(cls, func):
        def inner(self, *args, **kwargs):

            result = func(self, *args, **kwargs)

            return result

        return inner

    @classmethod
    def d_load_programs(cls, func):
        def inner(self, *args, **kwargs):

            result = func(self, *args, **kwargs)

            return result

        return inner

    @classmethod
    def d_load_vaos(cls, func):
        def inner(self, *args, **kwargs):

            result = func(self, *args, **kwargs)

            return result

        return inner

