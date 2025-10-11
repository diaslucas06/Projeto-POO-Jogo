import pygame
import os

INVENTARIO_ALTURA = 90
INVENTARIO_LARGURA = 1000

class Inventario():

    def __init__(self):
        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__), "..", "data", "images", "inventario.png"))
        self.image = pygame.transform.scale(self.image, (INVENTARIO_LARGURA, INVENTARIO_ALTURA))