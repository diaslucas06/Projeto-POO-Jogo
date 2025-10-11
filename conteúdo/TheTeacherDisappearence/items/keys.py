import pygame 
import os

class Key(pygame.sprite.Sprite):
    
    def __init__(self):
        
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__),"..", "data", "images", "items", f"key.png"))
        self.image = pygame.transform.scale(self.image, (30, 50))
        
        self.rect = self.image.get_rect()
        self.rect.topleft = 500, 520
        
        self.coletado = False
        self.i = 330
        
    def update(self):
        if self.coletado:
            self.image = pygame.transform.scale(self.image, (25, 40))
            self.rect.topleft = self.i, 635
            self.i += 50
            self.coletado = False
            
class Key1(Key):
    def __init__(self):
        super().__init__()
        
class Key2(Key):
    def __init__(self):
        super().__init__()
