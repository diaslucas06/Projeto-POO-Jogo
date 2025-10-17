import pygame 
import os

class Base_Personagem(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(self.caminho)
        self.image = pygame.transform.scale(self.image, (180, 350))
        self.rect = self.image.get_rect()
        
    def falar(self):
        return None
    
class Hugo(Base_Personagem):
    
    def __init__(self):
        self.caminho = os.path.join(os.path.dirname(__file__),"..", "data", "images", "personagens", "hugo_idle.png")
        super().__init__()
        