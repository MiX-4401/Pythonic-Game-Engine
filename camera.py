from Engine.camera import EngineCamera

class Camera(EngineCamera):
    def __init__(self, main, fixed_upon, settings:dict=dict):
        super().__init__(main=main, fixed_upon=fixed_upon, settings=settings)
    

    