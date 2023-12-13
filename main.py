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
        
        self.player:  Player  = None # The player class is initialised when the correct level objectgroup (layer) is created 
        self.shaders: Shaders = Shaders(main=self, ctx=self.ctx, settings=self.settings["shaders"])
        self.canvas:  Canvas  = Canvas.load(size=self.native_resolution)
        self.sprites: Sprites = Sprites(main=self, settings=self.settings["sprites"])
        # self.tiles:    Tiles    = Tiles(main=self)
        # self.renderer: Renderer = Renderer(main=self)
        # self.levels:   Levels   = Levels(main=self, settings=self.settings["levels"])
        # self.camera:   Camera   = Camera(main=self, fixed_upon=self.player, settings=self.settings["camera"])

        print([x for x in self.sprites.sprites.keys()])
        print(self.sprites.sprites["tiles_0"])
        self.canvas.blit(source=self.sprites.sprites["tiles_0"]["0"][0])

        

    @EngineMain.d_update
    def update(self):
        pygame.display.set_caption(title=f"GumTreeGraphicsEng {int(self.clock.get_fps())}")
        # self.levels.update()
        # self.camera.update()

    def draw(self):
        
        # self.canvas.clear()
        # self.canvas.fill(colour=(25,255,255))

        self.ctx.screen.use()
        self.canvas.use(location=1)
        self.shaders.programs["main"]["sourceTexture"] = 1        
        self.shaders.vaos["main"].render(mgl.TRIANGLE_STRIP)
        
        # self.levels.draw()

        pygame.display.flip()

    @EngineMain.d_garbage_collection
    def garbage_collection(self):
        self.canvas.release()
        self.shaders.garbage_collection()
    

if __name__ == "__main__":
    game: Main = Main()
    game.run()
    