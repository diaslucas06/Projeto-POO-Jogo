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
        self.caminho = os.path.join(os.path.dirname(__file__),"..", "data", "images", "items", "chaves", "chave_a36.png")
        super().__init__(x, y)
        self.image = pygame.transform.scale(self.image, (25, 40))
        self.nome_item = "Chave da sala A36"
        
class Key2(Item):

    def __init__(self, x, y):
        self.caminho = os.path.join(os.path.dirname(__file__),"..", "data", "images", "items", "chaves", "chave_m5.png")
        super().__init__(x, y)
        self.image = pygame.transform.scale(self.image, (25, 40))
        self.nome_item = "Chave da sala M5"
        
class Key3(Item):

    def __init__(self, x, y):
        self.caminho = os.path.join(os.path.dirname(__file__),"..", "data", "images", "items", "chaves", "chave_coapac.png")
        super().__init__(x, y)
        self.image = pygame.transform.scale(self.image, (25, 40))
        self.nome_item = "Chave da COAPAC"
        
class Key4(Item):

    def __init__(self, x, y):
        self.caminho = os.path.join(os.path.dirname(__file__),"..", "data", "images", "items", "chaves", "chave_m1.png")
        super().__init__(x, y)
        self.image = pygame.transform.scale(self.image, (80, 140))
        self.nome_item = "Chave da sala M1"
        
class Key5(Item):

    def __init__(self, x, y):
        self.caminho = os.path.join(os.path.dirname(__file__),"..", "data", "images", "items", "chaves", "chave_a38.png")
        super().__init__(x, y)
        self.image = pygame.transform.scale(self.image, (100, 300))
        self.nome_item = "Chave da sala A38"
        
class Fita(Item):
    
    def __init__(self, x, y):
        self.caminho = os.path.join(os.path.dirname(__file__),"..", "data", "images", "items", "fita.png")
        super().__init__(x, y)
        self.image = pygame.transform.scale(self.image, (25, 40))
        self.nome_item = "Fita"
        
class Fita2(Item):
    
    def __init__(self, x, y):
        self.caminho = os.path.join(os.path.dirname(__file__),"..", "data", "images", "items", "fita.png")
        super().__init__(x, y)
        self.image = pygame.transform.scale(self.image, (100, 200))
        self.nome_item = "Fita"

class CartaoAcesso(Item):

    def __init__(self, x, y):
        self.caminho = os.path.join(os.path.dirname(__file__),"..", "data", "images", "items", "cartaoAcesso.png")
        super().__init__(x, y)
        self.image = pygame.transform.scale(self.image, (50, 30))
        self.nome_item = "Cartão de Acesso"

class PéDeCabra(Item):

    def __init__(self, x, y):
        self.caminho = os.path.join(os.path.dirname(__file__),"..", "data", "images", "items", "pedecabra.png")
        super().__init__(x, y)
        self.image = pygame.transform.scale(self.image, (20, 100))
        self.nome_item = "Pé de Cabra"
        
class Tesoura(Item):

    def __init__(self, x, y):
        self.caminho = os.path.join(os.path.dirname(__file__),"..", "data", "images", "items", "tesoura_fechada.png")
        super().__init__(x, y)
        self.image = pygame.transform.scale(self.image, (40, 70))
        self.nome_item = "Tesoura"
        
class Provas(Item):

    def __init__(self, x, y):
        self.caminho = os.path.join(os.path.dirname(__file__),"..", "data", "images", "items", "provas_hugo.png")
        super().__init__(x, y)
        self.image = pygame.transform.scale(self.image, (280, 340))
        self.nome_item = "Provas de Hugo"
        
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
        self.nome_item = "Carrinho" #por enquanto
        
    def update(self):
        if self.coletado:
            self.coletado = False
        
