import pygame
import os

INVENTARIO_ALTURA = 90
INVENTARIO_LARGURA = 700

WHITE = (255, 255, 255)


class Inventario():

    def __init__(self):
        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__), "..", "data", "images", "inventario.png"))
        self.image = pygame.transform.scale(self.image, (INVENTARIO_LARGURA, INVENTARIO_ALTURA))
        self.items = []
        self.i = 280
        
class Hud():
    
    def __init__(self):
        self.font = pygame.font.Font(os.path.join(os.path.dirname(__file__), "..", "data", "fonts", "Minecraftia-Regular.ttf"), 20)
        self.entrar = self.font.render("Pressione 'E' para entrar na porta", True, WHITE)
        self.interagir = self.font.render("Pressione 'I' para interagir com o personagem", True, WHITE)
        self.pegar = self.font.render("Pressione 'P' para pegar o item", True, WHITE)
        self.clicar = self.font.render("Pressione o botão esquerdo do mouse para trocar de corredor", True, WHITE)
        self.tecla_p = pygame.image.load(os.path.join(os.path.dirname(__file__), "..", "data", "images", "teclas", "tecla_p.png"))
        self.tecla_p = pygame.transform.scale(self.tecla_p, (30, 30))
        self.tecla_i = pygame.image.load(os.path.join(os.path.dirname(__file__), "..", "data", "images", "teclas", "tecla_i.png"))
        self.tecla_i = pygame.transform.scale(self.tecla_i, (30, 30))
        self.tecla_e = pygame.image.load(os.path.join(os.path.dirname(__file__), "..", "data", "images", "teclas", "tecla_e.png"))
        self.tecla_e = pygame.transform.scale(self.tecla_e, (30, 30))

class Seta(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__), "..", "data", "images", "seta.png"))
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.clicado = False
        self.rect = self.image.get_rect()
        self.rect.topleft = 200, 620
        
        