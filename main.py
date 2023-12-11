#dsadsa

import pygame, moderngl as mgl
from Engine.main import EngineMain
from graphics    import Graphics
from camera      import Camera
from renderer    import Renderer
from sprites     import Sprites
from tiles       import Tiles
from levels      import Levels
from player      import Player

class Main(EngineMain):
    def __init__(self):
        super().__init__()
        pygame.init()
        
        self.player:   Player   = None # The player class is initialised when the correct level objectgroup (layer) is created 
        self.sprites:  Sprites  = Sprites(main=self, settings=self.settings["sprites"])
        self.graphics: Graphics = Graphics(main=self, ctx=self.ctx, settings=self.settings["graphics"])
        self.tiles:    Tiles    = Tiles(main=self)
        self.renderer: Renderer = Renderer(main=self)
        self.levels:   Levels   = Levels(main=self, settings=self.settings["levels"])
        self.camera:   Camera   = Camera(main=self, fixed_upon=self.player, settings=self.settings["camera"])
        

    @EngineMain.d_update
    def update(self):
        pygame.display.set_caption(title=f"GumTreeGraphicsEng {int(self.clock.get_fps())}")
        self.graphics.update()
        self.levels.update()
        self.camera.update()

    @EngineMain.d_draw
    def draw(self):
        self.graphics.vertex_arrays["main"].render(mode=mgl.TRIANGLE_STRIP)
        self.levels.draw()
        self.graphics.draw()
        
    

if __name__ == "__main__":
    game: Main = Main()
    game.run()
    