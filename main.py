import pygame, moderngl as mgl
from Engine.main import EngineMain
from shaders     import Shaders
from camera      import Camera
from renderer    import Renderer
from sprites     import Sprites
from tiles       import Tiles
from levels      import Levels
from player      import Player
from Engine.graphics import Texture, Canvas, Transform

class Main(EngineMain):
    def __init__(self):
        super().__init__()
        pygame.init()
        
        self.player:   Player   = None # The player class is initialised when the correct level objectgroup (layer) is created 
        self.shaders:  Shaders  = Shaders(main=self, ctx=self.ctx, settings=self.settings["shaders"])
        self.canvas:   Canvas   = Canvas.load(size=self.native_resolution)
        self.sprites:  Sprites  = Sprites(main=self, settings=self.settings["sprites"])
        self.tiles:    Tiles    = Tiles(main=self)
        self.renderer: Renderer = Renderer(main=self)
        self.levels:   Levels   = Levels(main=self, settings=self.settings["levels"])
        # self.camera:   Camera   = Camera(main=self, fixed_upon=self.player, settings=self.settings["camera"])

        

    @EngineMain.d_update
    def update(self):
        pygame.display.set_caption(title=f"GumTreeGraphicsEng {int(self.clock.get_fps())}")
        self.levels.update()
        # self.camera.update()

    def draw(self):
        
        self.canvas.clear()
        self.levels.draw()
        self.renderer.draw(frame=self.renderer.canvases,      location="canvases")
        self.renderer.draw(frame=self.renderer.normal_canvas, location="normals")

        self.ctx.screen.use()
        self.canvas.use(location=1)
        self.shaders.programs["main"]["sourceTexture"] = 1        
        self.shaders.vaos["main"].render(mgl.TRIANGLE_STRIP)
        
        pygame.display.flip()

    @EngineMain.d_garbage_collection
    def garbage_collection(self):
        self.canvas.release()
        self.shaders.garbage_collection()
    

if __name__ == "__main__":
    game: Main = Main()
    game.run()
    