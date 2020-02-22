import pygame

def fire(x, y, surface):
    """Fires crystal at x and y by next render"""
    ammo = pygame.image.load("assets/crystal.png")
    surface.blit(ammo, x, y)
