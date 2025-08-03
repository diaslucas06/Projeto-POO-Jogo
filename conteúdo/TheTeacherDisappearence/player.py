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
        
        self.agachar_direita = pygame.image.load(os.path.join(os.path.dirname(__file__), "data", "images", "personagens", "agachando-direita.png"))
        self.agachar_esquerda = pygame.image.load(os.path.join(os.path.dirname(__file__), "data", "images", "personagens", "agachando-esquerda.png"))
        
        self.animacao_atual = self.andar_direita
        self.atual = 0
        self.image = self.andar_direita[self.atual]
        self.image = pygame.transform.scale(self.image, (190, 310))
        
        self.rect = self.image.get_rect()
        self.rect.topleft = 300, 320
        
        self.andar = False
        self.coletar = False
        
        self.velocidade = 8
        
        self.ultima_direcao = "direita"
        
    def andando(self):
        self.andar = True
        
    def coletando(self):
        self.coletar = True
    
    def update(self, teclas):
        
        if self.coletar:
            
            if self.ultima_direcao == "direita":
                self.image = self.agachar_direita
            else:
                self.image = self.agachar_esquerda
            self.image = pygame.transform.scale(self.image, (190, 310))
            
        if teclas[pygame.K_d]:
            
            self.ultima_direcao = "direita"
            self.rect.x += self.velocidade
            if self.atual >= len(self.andar_direita):
                self.atual = 0
            self.animacao_atual = self.andar_direita
            self.image = self.andar_direita[int(self.atual)]
            self.andar = True
            
        elif teclas[pygame.K_a]:
            
            self.ultima_direcao = "esquerda"
            self.rect.x -= self.velocidade
            if self.atual >= len(self.andar_esquerda):
                self.atual = 0
            self.animacao_atual = self.andar_esquerda
            self.image = self.andar_esquerda[int(self.atual)]
            self.andar = True
            
        else:
            self.andar = False
            
        if self.andar:
            self.atual += 0.3
            if self.atual >= len(self.animacao_atual):
                self.atual = 0
            self.image = pygame.transform.scale(self.image, (190, 310))
            self.coletar = False
            
        else:
            self.atual = 0  
            
            
            