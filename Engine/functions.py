from math import ceil
import pygame

def lerp(point_1, point_2, factor):
    
    x: float = point_1[0] + factor * (point_2[0] - point_1[0])
    y: float = point_1[1] + factor * (point_2[1] - point_1[1])

    return (x, y)

def scale_surface(surface:pygame.Surface, scale:int):
    resolution: tuple = surface.get_size()
    scaled_res: tuple = (
        resolution[0] * scale,
        resolution[1] * scale
    )
    return pygame.transform.scale(surface=surface, size=scaled_res)

def split_list(my_list:list):
    length: int = len(my_list)
    middle: int = ceil(length / 2)
    first_half:  list = my_list[0:middle:]
    second_half: list = my_list[middle:]

    return first_half, second_half
