import pygame 
import os

class Player(pygame.sprite.Sprite):
    
    def __init__(self):
        
        pygame.sprite.Sprite.__init__(self)
        self.andar_direita = []
        self.andar_esquerda = []
        
        for i in range(1,6):
            self.andar_direita.append(pygame.image.load(os.path.join(os.path.dirname(__file__), "data", "images", "personagens", f"andando-direita{i}.png")))
            
        for i in range(1,6):
            self.andar_esquerda.append(pygame.image.load(os.path.join(os.path.dirname(__file__), "data", "images", "personagens", f"andando-esquerda{i}.png")))
        
        self.animacao_atual = self.andar_direita
        self.atual = 0
        self.image = self.andar_direita[self.atual]
        
        self.rect = self.image.get_rect()
        self.rect.topleft = 300, 320
        
        self.andar = False
        
        self.velocidade = 8
        
        self.image = pygame.transform.scale(self.image, (190, 310))
        
        
    def andando(self):
        self.andar = True
    
    def update(self, teclas):
        
        if teclas[pygame.K_d]:
            self.rect.x += self.velocidade
            if self.atual >= len(self.andar_direita):
                self.atual = 0
            self.animacao_atual = self.andar_direita
            self.image = self.andar_direita[int(self.atual)]
            
        elif teclas[pygame.K_a]:
            self.rect.x -= self.velocidade
            if self.atual >= len(self.andar_esquerda):
                self.atual = 0
            self.animacao_atual = self.andar_esquerda
            self.image = self.andar_esquerda[int(self.atual)]
            
        if self.andar == True:
            self.atual += 0.3
            if self.atual >= len(self.animacao_atual):
                self.atual = 0
            self.image = pygame.transform.scale(self.image, (190, 310))
            
        else:
            self.atual = 0  