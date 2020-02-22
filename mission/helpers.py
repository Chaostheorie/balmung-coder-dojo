import pygame
from mission.config import load_config


def fire(x, y, surface):
    """Fires crystal at x and y by next render"""
    ammo = pygame.image.load("assets/crystal.png")
    surface.blit(ammo, x, y)


class AssetHelper:
    def __init__(self):
        self.config = load_config(instance="helper")

    def get_asset(self, asset):
        """Gets path for asset as str"""
        return f"{self.config['path']}/{asset}"
