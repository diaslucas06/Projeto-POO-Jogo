import pygame
import os

INVENTARIO_ALTURA = 90
INVENTARIO_LARGURA = 700

WHITE = (255, 255, 255)


class Inventario():

    def __init__(self):
        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__), "..", "data", "images", "inventario.png"))
        self.image = pygame.transform.scale(self.image, (INVENTARIO_LARGURA, INVENTARIO_ALTURA))
        self.items = pygame.sprite.Group()
        self.posicao_base_x = 340
        self.posicao_y = 635
        self.espacamento_entre_itens = 70
        
    def update(self):
        for item in self.items:
            if item.utilizado:
                self.items.update(self)
                item.kill()
    
        
class Hud():
    
    def __init__(self):
        self.font = pygame.font.Font(os.path.join(os.path.dirname(__file__), "..", "data", "fonts", "Minecraftia-Regular.ttf"), 20)
        self.entrar = self.font.render("Pressione 'E' para entrar na porta", True, WHITE)
        self.interagir = self.font.render("Pressione 'I' para interagir com o personagem", True, WHITE)
        self.pegar = self.font.render("Pressione 'P' para pegar o item", True, WHITE)
        self.clicar = self.font.render("Pressione 'S' para mudar para o outro lado do corredor", True, WHITE)
        self.abrir_bolsa = self.font.render("Pressione 'A' para abrir a bolsa", True, WHITE)

        self.tecla_p = pygame.image.load(os.path.join(os.path.dirname(__file__), "..", "data", "images", "teclas", "tecla_p.png"))
        self.tecla_p = pygame.transform.scale(self.tecla_p, (30, 30))
        
        self.tecla_i = pygame.image.load(os.path.join(os.path.dirname(__file__), "..", "data", "images", "teclas", "tecla_i.png"))
        self.tecla_i = pygame.transform.scale(self.tecla_i, (30, 30))
        
        self.tecla_e = pygame.image.load(os.path.join(os.path.dirname(__file__), "..", "data", "images", "teclas", "tecla_e.png"))
        self.tecla_e = pygame.transform.scale(self.tecla_e, (30, 30))

        try:
            self.tecla_a = pygame.image.load(os.path.join(os.path.dirname(__file__), "..", "data", "images", "teclas", "tecla_a.png"))
            self.tecla_a = pygame.transform.scale(self.tecla_a, (30, 30))
        except:
            self.tecla_a = self.tecla_e

        self.space = pygame.image.load(os.path.join(os.path.dirname(__file__), "..", "data", "images", "teclas", "space.png"))
        self.space = pygame.transform.scale(self.space, (60, 30))

class Seta(pygame.sprite.Sprite):

    def __init__(self, x, y, destino):
        pygame.sprite.Sprite.__init__(self)
        self.destino = destino
        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__), "..", "data", "images", "seta.png"))
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.image.set_alpha(128)
        self.clicado = False
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y
        
        