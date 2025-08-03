import pygame 
import os

class Key1(pygame.sprite.Sprite):
    
    def __init__(self):
        
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(os.path.dirname(__file__),"..", "data", "images", "items", f"key.png"))
        self.image = pygame.transform.scale(self.image, (30, 50))
        
        self.rect = self.image.get_rect()
        self.rect.topleft = 500, 520
        
        self.coletado = False
        
    def update(self):
        if self.coletado:
            self.kill()
            
