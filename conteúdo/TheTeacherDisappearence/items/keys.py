import pygame 
import os
from ui.hud import Inventario

inventario = Inventario()

class Item(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.caminho = os.path.join(os.path.dirname(__file__),"..", "data", "images", "items", "key.png")
        self.image = pygame.image.load(self.caminho)
        self.image = pygame.transform.scale(self.image, (25, 40))
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y
        self.coletado = False
        
    def update(self):
        if self.coletado:
            inventario.i = inventario.i + 50
            self.rect.topleft = inventario.i, 635
            self.coletado = False
            
class Key1(Item):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.caminho = os.path.join(os.path.dirname(__file__),"..", "data", "images", "items", "key.png")
        

class Fita(Item):
    
    def __init__(self, x, y):
        super().__init__(x, y)
        self.caminho = os.path.join(os.path.dirname(__file__),"..", "data", "images", "items", "Itens_do_jogador.png")
        
