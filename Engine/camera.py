import pygame
from Engine.functions import lerp

class EngineCamera():
    def __init__(self, main, fixed_upon, settings:dict={}):
        self.main:       object = main
        self.fixed_upon: object = fixed_upon
        self.settings:   dict   = settings
        
        self.camera_options: str   = settings["camera_type"]
        self.x_speed_max:  list = settings["x_speed_max"]
        self.y_speed_max:  list = settings["y_speed_max"]
        self.x_accel_rate: int  = settings["x_accel_rate"]
        self.y_accel_rate: int  = settings["y_accel_rate"]
        self.lerp_factor: float = settings["lerp_factor"]

        self.x_vel: int = 0
        self.y_vel: int = 0
        self.camera_type: function = None

        self.camera_types: tuple = (self.camera_fixed, self.camera_abstract)
        self.camera: pygame.Rect = pygame.Rect(0, 0, self.main.current_resolution[0], self.main.current_resolution[1])

        self.load_camera()

    def camera_fixed(self):
        fixed_pos:  tuple = tuple(self.fixed_upon.pos)
        distance:   tuple = self.main.native_resolution
        self.camera.x = fixed_pos[0] - distance[0] // 2
        self.camera.y = fixed_pos[1] - distance[1] // 2

    def camera_abstract(self):
        distance:  tuple = self.main.native_resolution
        fixed_pos: tuple = (self.fixed_upon.pos[0] - int(distance[0] / 2), self.fixed_upon.pos[1] - int(distance[1] / 2))

        dx = fixed_pos[0] - self.camera.x
        dy = fixed_pos[1] - self.camera.y

        # Apply lerp
        new_camera_pos: tuple = lerp(point_1=(self.camera.x, self.camera.y), point_2=fixed_pos, factor=self.lerp_factor)
        self.camera.x = new_camera_pos[0]
        self.camera.y = new_camera_pos[1]

        # Apply acceleration
        if abs(dx) > self.x_speed_max:
            self.camera.x += self.x_speed_max if dx > 0 else -self.x_speed_max
        else:
            self.camera.x += dx * self.x_accel_rate

        if abs(dy) > self.y_speed_max:
            self.camera.y += self.y_speed_max if dy > 0 else -self.y_speed_max
        else:
            self.camera.y += dy * self.x_accel_rate

        

    def load_camera(self):
        fixed_pos:  tuple = tuple(self.fixed_upon.pos)
        distance:   tuple = self.main.native_resolution
                
        self.camera.x = fixed_pos[0] - distance[0] // 2
        self.camera.y = fixed_pos[1] - distance[1] // 2
        
        if self.camera_options   == "fixed":
            self.camera_type = self.camera_types[0]
        elif self.camera_options == "abstract": 
            self.camera_type = self.camera_types[1]

    def update(self):
        self.camera_type()

    def draw(self):
        pass


