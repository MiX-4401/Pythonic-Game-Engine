import pygame


class EnginePlayer():
    def __init__(self, main, surfaces:list, normals:list, properties:dict, polygons=list, pos=list, name=str, settings:dict={}):
        self.main = main
        self.settings:   dict = settings
        self.surfaces:   list = surfaces
        self.normals:    list = normals
        self.properties: dict = properties
        self.polygons:   list = polygons
        self.pos:        list = pos
        self.name:       list = name


        self.is_animating:   bool  = False 
        self.current_sprite: int   = 0
        self.sprite_inc:     float = 0
        #self.image: pygame.Surface = self.surfaces[self.current_sprite]
        self.image: pygame.Surface = self.surfaces[0][0]

        self.x_speed: list = self.main.settings["player"]["x_speed"]
        self.y_speed: list = self.main.settings["player"]["y_speed"]

        self.x_vel: float = 0.00
        self.y_vel: float = 0.00

    def animate(self):
        if len(self.surfaces) > 1:
            self.is_animating = True
            self.sprite_inc = self.properties["speed"]

        if self.is_animating:
            self.current_sprite += self.sprite_inc
        
            if self.current_sprite >= len(self.surfaces): self.current_sprite = 0
            self.image = self.surfaces[int(self.current_sprite)]

    def move(self):
        self.pos[0] += self.x_vel #* self.main.delta_time
        self.pos[1] += self.y_vel #* self.main.delta_time

    def reset_velocity(self):
        self.x_vel: float = 0.00
        self.y_vel: float = 0.00

    def update(self):
        self.reset_velocity()

        keys: list = pygame.key.get_pressed()
        if keys[pygame.K_w]: self.y_vel = self.x_speed[0]
        if keys[pygame.K_a]: self.x_vel = self.x_speed[0]
        if keys[pygame.K_s]: self.y_vel = self.x_speed[1]
        if keys[pygame.K_d]: self.x_vel = self.x_speed[1]

        self.move()
        self.animate()

    def draw(self, surface:pygame.Surface):
        surface.blit(source=self.image, dest=self.pos)
        

    @classmethod
    def d_update(cls, func):
        def inner(self, *args, **kwargs):
            
            # Animation
            if self.is_animating:
                self.current_sprite += self.sprite_inc
            
                if self.current_sprite >= len(self.surfaces): self.current_sprite = 0
                self.image = self.surfaces[int(self.current_sprite)]

            result = func(self, *args, **kwargs)

            return result
        
        return inner

    @classmethod
    def d_draw(cls, func):
        def inner(self, *args, **kwargs):

            kwargs["surface"].blit(source=self.image, dest=self.pos)

            result = func(self, *args, **kwargs)

            return result

        return inner



