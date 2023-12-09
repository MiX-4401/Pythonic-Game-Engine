import pygame, os, moderngl as mgl
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
        self.current_resolution: tuple = self.global_settings["native_resolution"]

        self.delta_time: float = 0.00; self.last_time: float = time()
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.current_resolution, pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE | pygame.SRCALPHA)
        self.ctx: mgl.Context = mgl.create_context()
        pygame.display.set_caption(self.global_settings["title"])


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
            elif event.type == pygame.VIDEORESIZE:
                self.current_resolution: tuple = event.size
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

    def update(self):
        pass

    def draw(self):
        self.screen.fill(color=(0, 0, 0))
        
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
                    pygame.quit()
                    exit()
                elif event.type == pygame.VIDEORESIZE:
                    self.current_resolution: tuple = event.size

            result = func(self, *args, **kwargs)
            return result

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
            self.screen.fill(color=(0, 0, 0))

            result = func(self, *args, **kwargs)

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


