import pygame
import os

INVENTARIO_ALTURA = 90
INVENTARIO_LARGURA = 1000

class Inventario(pygame.sprite.Sprite):

    def __init__(self):
        self.imagem = pygame.image.load(os.path.join(os.path.dirname(__file__), "data", "images", "inventario.png"))
        self.imagem = pygame.transform.scale(self.imagem, (INVENTARIO_LARGURA, INVENTARIO_ALTURA))