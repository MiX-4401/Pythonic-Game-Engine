import moderngl as mgl
import numpy as np
from PIL import Image
from typing import Union

class Texture:
    ctx: mgl.Context     = None
    program: mgl.Program = None
    vao: mgl.VertexArray = None

    def __init__(self):
        self.loaded: bool  = False
        self.synced: bool  = True
        self.size:   tuple = None
        self.channels: int = None
        self.texture:     mgl.Texture = None
        self.framebuffer: mlg.Framebuffer = None
        

    def blit(self, source, pos:tuple=(0,0), area:tuple=None):

        ctx, program, vao = Texture.get_components() 

        # Bind framebuffer and source texture
        self.framebuffer.use()
        self.framebuffer.scissor: tuple = (area[0], self.texture.size[1] - area[1] - area[3], area[2], area[3]) if area != None else None
        
        source.use(location=0)

        # Set uniforms
        program["sourceTexture"] = 0
        program["pos"]           = (pos[0] + source.size[0] / 2, pos[1] + source.size[1] / 2)
        program["textureSize"]   = self.size
        program["sourceSize"]    = source.size

        # Render
        vao.render(mode=mgl.TRIANGLE_STRIP)

        # Unbind framebuffer
        ctx.screen.use()
        
    def fill(self, colour:tuple=(0,0,0,0)):
        colour: tuple = tuple([c/225 for c in colour])
        self.framebuffer.clear(red=colour[0], green=colour[1], blue=colour[2], alpha=colour[3])
        self.synced = False



    def use(self, location:int=0):
        self.texture.use(location=location)

    def sync(self):
        pass

    def __str__(self):
        return f"Texture Object {self.size[0]}x{self.size[1]} {self.channels}"

    @classmethod
    def init(cls, ctx:mgl.Context, program:mgl.Program, vao:mgl.VertexArray):
        cls.ctx = ctx
        cls.program = program
        cls.vao = vao
        
    @classmethod
    def get_components(cls) -> (mgl.Context, mgl.Program, mgl.VertexArray):
        return cls.ctx, cls.program, cls.vao

    @staticmethod
    def load(path:str):
        ctx, program, vao = Texture.get_components() 

        image:   Image = Image.open(path).transpose(Image.FLIP_TOP_BOTTOM)
        texture: Texture = Texture()
        
        texture.size:     tuple = image.size
        texture.channels: int   = len(image.getbands())
        texture.texture:  mgl.Texture = ctx.texture(size=texture.size, components=texture.channels, data=image.tobytes())
        texture.filter:   tuple       = (mgl.NEAREST, mgl.NEAREST)
        texture.framebuffer: mgl.Framebuffer = ctx.framebuffer(color_attachments=texture.texture)

        texture.loaded = True

        return texture

    @staticmethod
    def load_blank(size:tuple, channels:int=4):
        ctx, program, vao = Texture.get_components() 

        texture: Texture = Texture()
        
        texture.size:     tuple = size
        texture.channels: int   = channels
        texture.texture:  mgl.Texture = ctx.texture(size=size, components=channels)
        texture.filter:   tuple       = (mgl.NEAREST, mgl.NEAREST)
        texture.framebuffer: mgl.Framebuffer = ctx.framebuffer(color_attachments=texture.texture)

        texture.loaded = True

        return texture

class Canvas:
    ctx: mgl.Context     = None
    program: mgl.Program = None
    vao: mgl.VertexArray = None

    def __init__(self):
        self.loaded: bool  = False
        self.synced: bool  = False
        self.size:   tuple = None
        self.channels: int = None
        self.renderbuffer: mgl.Renderbuffer = None
        self.framebuffer:  mgl.Framebuffer  = None
        self.texture:      mgl.Texture      = None
        

    def blit(self, source, pos:tuple=(0,0), area:tuple=None):

        ctx, program, vao = Canvas.get_components() 

        # Bind framebuffer and source texture
        self.framebuffer.use()
        self.framebuffer.scissor: tuple = (area[0], self.texture.size[1] - area[1] - area[3], area[2], area[3]) if area != None else None

        source.use(location=0)

        # Set uniforms
        program["sourceTexture"] = 0
        program["pos"]           = (pos[0] + source.size[0] / 2, pos[1] + source.size[1] / 2)
        program["textureSize"]   = self.size
        program["sourceSize"]    = source.size

        # Render
        vao.render(mode=mgl.TRIANGLE_STRIP)

        self.synced = False

        # Unbind framebuffer
        ctx.screen.use()

    def fill(self, colour:tuple=(0,0,0,0)):
        colour: tuple = tuple([c/225 for c in colour])
        self.framebuffer.clear(red=colour[0], green=colour[1], blue=colour[2], alpha=colour[3])
        self.synced = False

    def clear(self):
        self.framebuffer.clear(red=0.0, green=0.0, blue=0.0, alpha=1.0)
        self.synced = False

    def use(self, location:int=0):
        self.sync()
        self.texture.use(location=location)

    def sync(self):
        if not self.synced:
            self.texture.write(data=self.framebuffer.read(components=self.channels, attachment=0))
            self.synced = True

    def __str__(self):
        return f"Canvas Object {self.size[0]}x{self.size[1]} {self.channels}"

    @classmethod
    def init(cls, ctx:mgl.Context, program:mgl.Program, vao:mgl.VertexArray):
        cls.ctx = ctx
        cls.program = program
        cls.vao = vao
        
    @classmethod
    def get_components(cls) -> (mgl.Context, mgl.Program, mgl.VertexArray):
        return cls.ctx, cls.program, cls.vao

    @staticmethod
    def load(size:tuple, channels:int=4):
        ctx, program, vao = Canvas.get_components() 

        canvas: Canvas = Canvas()
        canvas.size:   tuple = size
        canvas.channels: int = channels
        canvas.renderbuffer: mgl.Renderbuffer = ctx.renderbuffer(size=canvas.size, components=canvas.channels)
        canvas.framebuffer:  mgl.Framebuffer  = ctx.framebuffer(color_attachments=canvas.renderbuffer)
        canvas.texture:      mgl.Texture      = ctx.texture(size=canvas.size, components=canvas.channels)
        canvas.texture.filter: tuple          = (mgl.NEAREST, mgl.NEAREST)
        
        canvas.loaded = True

        return canvas

class Transform:
    
    ctx: mgl.Context = None
    programs: dict   = None
    vaos:     dict   = None

    @staticmethod
    def scale(surface:Union[Texture, Canvas], size:tuple) -> Union[Texture, Canvas]:
        ctx, programs, vaos = Transform.get_components()
        
        if type(surface) == Texture:
            scaled_surface: Texture = Texture.load_blank(size=size, channels=surface.channels)
        elif type(surface) == Canvas:
            scaled_surface: Canvas = Canvas.load(size=size, channels=surface.channels)

        # Bind framebuffer and source texture
        scaled_surface.framebuffer.use()
        surface.use(location=0)

        # Set uniforms
        programs["scale"]["sourceTexture"] = 0

        # Render
        vaos["scale"].render(mgl.TRIANGLE_STRIP)

        scaled_surface.synced = False

        # Unbind
        ctx.screen.use()

        return scaled_surface

    @staticmethod
    def flip(surface:Union[Texture, Canvas], x_flip:bool=False, y_flip:bool=False) -> Union[Texture, Canvas]:
        ctx, programs, vaos = Transform.get_components()
        
        if type(surface) == Texture:
            new_surface: Texture = Texture.load_blank(size=surface.size, channels=surface.channels)
        elif type(surface) == Canvas:
            new_surface: Canvas = Canvas.load(size=surface.size, channels=surface.channels)

        # Bind framebuffer and source texture
        new_surface.framebuffer.use()
        surface.use(location=0)

        # Set uniforms
        programs["flip"]["xFlip"] = x_flip
        programs["flip"]["yFlip"] = y_flip

        # Render
        vaos["flip"].render(mgl.TRIANGLE_STRIP)

        new_surface.synced = False

        # Unbind
        ctx.screen.use()

        return new_surface

    @classmethod
    def init(cls, ctx:mgl.Context, programs:list, vaos:list):
        cls.ctx = ctx
        cls.programs = programs
        cls.vaos = vaos
     
    @classmethod
    def get_components(cls):
        return cls.ctx, cls.programs, cls.vaos

