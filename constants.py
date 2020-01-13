"""
Global constants
"""
import pygame
from pygame import freetype

pygame.font.init()
pygame.freetype.init()
pygame.mixer.pre_init(44100, -16, 1, 512)
pygame.mixer.init()

# Colors
BLUE = (0, 0, 255)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

GREY = (200, 200, 200)

RED = (200, 0, 0)
LIGHT_RED = (255, 0, 0)

YELLOW = (200, 200, 0)
LIGHT_YELLOW = (255, 255, 0)

GREEN = (0, 155, 0)
LIGHT_GREEN = (0, 255, 0)

with open("config/graphics.ini", "r") as f:
    lines = f.read().splitlines()
    lines = list(map(lambda s: s.split("#")[0], lines))
    TITLE = lines[0]
    WIDTH, HEIGHT = tuple(map(int, lines[1].split()))
    FPS = int(lines[2])

# Different text sizes for in menus
minecraft_font = pygame.freetype.Font("assets/fonts/Minecraft.ttf", 25)
small_font = pygame.freetype.SysFont(pygame.font.get_default_font(), 25)
medium_font = pygame.freetype.SysFont(pygame.font.get_default_font(), 50)
large_font = pygame.freetype.SysFont(pygame.font.get_default_font(), 80)

small_font_old = pygame.font.SysFont("arial", 25)
medium_font_old = pygame.font.SysFont("arial", 50)
large_font_old = pygame.font.SysFont("arial", 80)
