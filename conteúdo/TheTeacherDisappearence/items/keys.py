import pygame 
import os

#consertar a função de pegar item, item reaparecendo
class Item(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(self.caminho)
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y
        self.coletado = False
        self.utilizado = False
        
    def update(self):
        if self.coletado:
            self.coletado = False
            
class Key1(Item):

    def __init__(self, x, y):
        self.caminho = os.path.join(os.path.dirname(__file__),"..", "data", "images", "items", "key.png")
        super().__init__(x, y)
        self.image = pygame.transform.scale(self.image, (25, 40))
        
class Key2(Item):

    def __init__(self, x, y):
        self.caminho = os.path.join(os.path.dirname(__file__),"..", "data", "images", "items", "key.png")
        super().__init__(x, y)
        self.image = pygame.transform.scale(self.image, (25, 40))
        
class Key3(Item):

    def __init__(self, x, y):
        self.caminho = os.path.join(os.path.dirname(__file__),"..", "data", "images", "items", "key.png")
        super().__init__(x, y)
        self.image = pygame.transform.scale(self.image, (25, 40))
        
class Key4(Item):

    def __init__(self, x, y):
        self.caminho = os.path.join(os.path.dirname(__file__),"..", "data", "images", "items", "key.png")
        super().__init__(x, y)
        self.image = pygame.transform.scale(self.image, (25, 40))
        
class Fita(Item):
    
    def __init__(self, x, y):
        self.caminho = os.path.join(os.path.dirname(__file__),"..", "data", "images", "items", "fita.png")
        super().__init__(x, y)
        self.image = pygame.transform.scale(self.image, (25, 40))

#consertar problema com o cartão reaparecendo
class CartaoAcesso(Item):

    def __init__(self, x, y):
        self.caminho = os.path.join(os.path.dirname(__file__),"..", "data", "images", "items", "cartaoAcesso.png")
        super().__init__(x, y)
        self.image = pygame.transform.scale(self.image, (50, 30))

class PéDeCabra(Item):

    def __init__(self, x, y):
        self.caminho = os.path.join(os.path.dirname(__file__),"..", "data", "images", "items", "pedecabra.png")
        super().__init__(x, y)
        self.image = pygame.transform.scale(self.image, (20, 60))
        
class Carrinho(pygame.sprite.Sprite):
    
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.caminho = os.path.join(os.path.dirname(__file__),"..", "data", "images", "Carrinho_limpeza.png")
        self.image = pygame.image.load(self.caminho)
        self.image = pygame.transform.scale(self.image, (350, 250))
        self.rect = self.image.get_rect()
        self.rect.topleft = x, y
        self.coletado = False
        self.utilizado = False
        
    def update(self):
        if self.coletado:
            self.coletado = False
        
