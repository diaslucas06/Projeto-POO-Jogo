import pygame 
import os

class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.andar = []
        self.andar.append(pygame.image.load(os.path.join(os.path.dirname(__file__), "data", "images", "personagens", "personagem-frente.png")))
        self.andar.append(pygame.image.load(os.path.join(os.path.dirname(__file__), "data", "images", "personagens", "personagem-andando-lado.png")))
        self.andar.append(pygame.image.load(os.path.join(os.path.dirname(__file__), "data", "images", "personagens", "personagem-andando-lado2.png")))
        self.atual = 0
        self.image = self.andar[self.atual]

        self.rect = self.image.get_rect()
        self.rect.topleft = 300, 220
        self.animar = False
        
    def andando(self):
        self.animar = True
        
    def update(self):
        if self.animar == True:
            self.atual += 0.4
            if self.atual >= len(self.andar):
                self.atual = 0
                self.animar = False
            self.image = self.andar[int(self.atual)]
            self.image = pygame.transform.scale(self.image, (200, 200))
        
