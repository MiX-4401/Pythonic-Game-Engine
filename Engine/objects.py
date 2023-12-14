import pygame

class Object():
    def __init__(self, main, surfaces:list, normals:list, properties:dict, polygons:list, pos:list, name:str):
        self.main = main
        self.surfaces:   list = surfaces
        self.normals:    list = normals
        self.properties: dict = properties
        self.polygons:   list = polygons 
        self.pos:        list = pos
        self.name:       str  = name

        self.is_animating:   bool  = False 
        self.current_sprite: int   = 0
        self.sprite_inc:     float = 0
        self.image: pygame.Surface = self.surfaces[self.current_sprite]

        self.animate()

    def animate(self):
        if len(self.surfaces) > 1:
            self.is_animating = True
            self.sprite_inc = self.properties["speed"]# * self.main.delta_time


    def update(self):

        # Animation
        if self.is_animating:
            self.current_sprite += self.sprite_inc
        
            if self.current_sprite >= len(self.surfaces): self.current_sprite = 0
            self.image = self.surfaces[int(self.current_sprite)]

    def draw(self, surface:pygame.Surface):
        surface.blit(source=self.image, pos=self.pos)
        

