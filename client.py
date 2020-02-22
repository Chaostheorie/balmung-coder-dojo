#!/usr/bin/env python3
import pygame
import os
import logging
import sys
from json import load
from pygame.locals import *


def fire(x, y):
    """Fires crystal at x and y by next render"""
    ammo = pygame.image.load("assets/crystal.png")
    surface.blit(ammo, x, y)


# Load config from config.json
if not os.path.exists("config.json"):
    raise EnvironmentError("Config.json not found")
with open("config.json") as f:
    config = load(f)

# Initilaze pygame
pygame.init()
fpsClock = pygame.time.Clock()
surface = pygame.display.set_mode((config["display-width"],
                                   config["display-height"]))
pygame.font.init()


# Load graphics
distance_wall = config["distance_wall"]
distance_width = config["display-width"] - distance_wall
distance_height = config["display-height"] - distance_wall
image = pygame.image.load("assets/canvas.png")
meeple1 = pygame.image.load("assets/eyelander.png")
player1_x = 100
player1_y = 100
meeple2 = pygame.image.load("assets/Snake.png")
player2_x = distance_width
player2_y = distance_height
background = pygame.Color(100, 149, 237)
myfont = pygame.font.SysFont("arial", 25)

steps_player1 = 0
steps_player2 = 0


while True:
    surface.fill(background)
    surface.blit(image, (0, 0))
    surface.blit(meeple1, (player1_x, player1_y))
    surface.blit(meeple2, (player2_x, player2_y))
    textsurface_1 = myfont.render(f"Highscore 1: {steps_player1}",
                                  False, (0, 0, 0))
    textsurface_2 = myfont.render(f"Highscore 2: {steps_player2}",
                                  False, (0, 0, 0))
    surface.blit(textsurface_1, (0, 0))
    surface.blit(textsurface_2, (0, 20))
    for event in pygame.event.get():
        # print(player1_x, player1_y)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player1_x = 0
                player1_y = 0
            elif event.key == pygame.K_RIGHT and player1_x < distance_width:
                player1_x += 100
                steps_player1 += 100
            elif event.key == pygame.K_LEFT and player1_x > distance_wall:
                player1_x -= 100
                steps_player1 += 100
            elif event.key == pygame.K_DOWN and player1_y < distance_height:
                player1_y += 100
                steps_player1 += 100
            elif event.key == pygame.K_UP and player1_y > distance_wall:
                player1_y -= 100
                steps_player1 += 100
            if event.key == pygame.K_d and player2_x < distance_width:
                player2_x += 100
                steps_player2 += 100
            elif event.key == pygame.K_a and player2_x > distance_wall:
                player2_x -= 100
                steps_player2 += 100
            elif event.key == pygame.K_s and player2_y < distance_height:
                player2_y += 100
                steps_player2 += 100
            elif event.key == pygame.K_w and player2_y > distance_wall:
                player2_y -= 100
                steps_player2 += 100
            elif event.key == pygame.K_f:
                # fire(player1_x, player1_y)
                ammo = pygame.image.load("assets/crystal_th.png")
                ammo_x = player1_x
                ammo_y = player1_y
                surface.blit(ammo, (ammo_x, ammo_y))
                for y in range(ammo_y, 0, -10):
                    surface.blit(ammo, (ammo_x, ammo_y))
                    pygame.display.update()
                    pygame.time.delay(10)
            env_player1 = ((player1_x-100, player1_y-100), (player1_x, player1_y-100), (player1_x, player1_y+100), (player1_x-100, player1_y))
            env_player2 = ((player2_x-100, player2_y-100), (player2_x, player2_y-100), (player2_x, player2_y+100), (player2_x-100, player2_y))
            for touch in env_player1:
                if touch in env_player2:
                    steps_player1 = 0
                    steps_player2 = 0

            logging.debug(env_player1)
            logging.debug(env_player2)
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    fpsClock.tick(30)
