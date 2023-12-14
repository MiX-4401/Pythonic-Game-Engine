import pygame, os, moderngl as mgl
from Engine.graphics import Canvas
from sys     import exit
from toml    import load
from inspect import getsourcefile
from time import time

class EngineMain:
    def __init__(self):
        self.settings: dict = {}

        self.load_settings()
        
        self.global_settings:    dict  = self.settings["global"]
        self.native_resolution:  tuple = self.global_settings["native_resolution"]

        self.delta_time: float = 0.00; self.last_time: float = time()
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.native_resolution, pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE | pygame.SRCALPHA)
        self.ctx: mgl.Context = mgl.create_context()
        pygame.display.set_caption(self.global_settings["title"])
        self.ctx.enable(mgl.BLEND)


    def load_settings(self):
        source_path: str = getsourcefile(self.__init__)

        base_dir: str = os.path.abspath(source_path).split("main")[0]

        for file in os.listdir(os.path.dirname(os.path.abspath(source_path))):
            if file.split(".")[0] == "settings":
                path: str = os.path.join(base_dir, "settings.toml")  

        self.settings: dict = load(path)

    def set_dt(self):
        self.delta_time: float = time() - self.last_time
        self.delta_time *= self.global_settings["tps"]
        self.last_time: float = time()

    def update_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.garbage_collection()
                    pygame.quit()
                    exit()

    def garbage_collection(self):
        self.canvas.release()
        self.ctx.release()

    def update(self):
        pass

    def draw(self):
        self.ctx.screen.use()
        self.canvas.clear()
        self.shaders.vaos["main"].render(mode=mgl.TRIANGLE_STRIP)
        pygame.display.flip()

    def run(self):
        while True:

            self.set_dt()
            self.update_events()
            self.update()
            self.draw()
            
            self.clock.tick(self.global_settings["fps"])


    @classmethod
    def d_load_settings(cls, func):
        def inner(self, *args, **kwargs):
            source_path: str = getsourcefile(self.__init__)
            base_dir: str = os.path.abspath(source_path).split("main")[0]

            for file in os.listdir(os.path.dirname(os.path.abspath(source_path))):
                if file.split(".")[0] == "settings":
                    path: str = os.path.join(base_dir, "settings.toml")  

            self.global_settings: dict = load(path)

            result = func(self, *args, **kwargs)

            return result

        return inner

    @classmethod
    def d_update_events(cls, func):
        def inner(self, *args, **kwargs):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.garbage_collection()
                    pygame.quit()
                    exit()

            result = func(self, *args, **kwargs)
            return result

        return inner
   
    @classmethod
    def d_garbage_collection(cls, func):
        def inner(self, *args, **kwargs):

            self.canvas.release()
            self.ctx.release()

            result = func(self, *args, **kwargs)
                
        return inner


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
            
            self.ctx.screen.use()
            # self.canvas.clear()
            # self.shaders.vaos["main"].render(mode=mgl.TRIANGLE_STRIP)

            pygame.display.flip()
            return result
            
        return inner
    
    @classmethod
    def d_run(cls, func):
        def inner(self, *args, **kwargs):

            while True:
                self.set_dt()
                self.update_events()
                self.update()
                self.draw()

                result = func(self, *args, **kwargs)
                
                self.clock.tick(self.global_settings["tps"])

        return inner


