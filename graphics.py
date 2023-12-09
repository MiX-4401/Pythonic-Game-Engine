from Engine.graphics import EngineGraphics

class Graphics(EngineGraphics):
    def __init__(self, main, ctx, settings:dict={}):
        super().__init__(main=main, ctx=ctx, settings=settings)

    @EngineGraphics.d_draw
    def draw(self):
        self.main.renderer.draw(frame=self.main.screen)