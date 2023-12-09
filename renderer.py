from Engine.renderer import EngineRenderer

class Renderer(EngineRenderer):
    def __init__(self, main, settings:dict={}):
        super().__init__(main=main, settings=settings)
