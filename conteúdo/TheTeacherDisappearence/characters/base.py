import pygame 
import os
from main import player

class Base_Personagem(pygame.sprite.Sprite):
    
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(self.caminho)
        
    def update(self):
        return None
    
class Hugo(Base_Personagem):
    
    def __init__(self):
        self.caminho = os.path.join(os.path.dirname(__file__),"..", "data", "images", "personagens", "hugo_idle.png")
        super().__init__()
        self.image = pygame.transform.scale(self.image, (150, 350))
        self.rect = self.image.get_rect()

class Zelador(Base_Personagem):
    
    def __init__(self):
        self.caminho = os.path.join(os.path.dirname(__file__),"..", "data", "images", "personagens", "zelador_idle.png")
        super().__init__()        
        self.image = pygame.transform.scale(self.image, (350, 350))
        self.rect = self.image.get_rect()
        self.rect.topleft = (370, 245) 
        self.indo_embora = False
        self.foi_embora = False
        self.velocidade = 5
        self.frames_andar = []
        self.index_animacao = 0.0  
        self.velocidade_animacao = 0.15
        for i in range(1,8):
            img_path = os.path.join(os.path.dirname(__file__), "..", "data", "images", "personagens", "zelador_andando", f"zelador_andando{i}.png")
            img = pygame.image.load(img_path)
            img = pygame.transform.scale(img, (350, 350))
            self.frames_andar.append(img)

    def update(self):
        if self.indo_embora:
            self.rect.x += self.velocidade
            self.index_animacao += self.velocidade_animacao
            
            if self.index_animacao >= len(self.frames_andar):
                self.index_animacao = 0
            
            self.image = self.frames_andar[int(self.index_animacao)]
            
class Aluno(Base_Personagem):
    
    def __init__(self):
        self.caminho = os.path.join(os.path.dirname(__file__),"..", "data", "images", "personagens", "aluno_idle.png")
        super().__init__()
        self.image = pygame.transform.scale(self.image, (150, 350))
        self.rect = self.image.get_rect()
        self.rect.topleft = (550, 245)

class Coordenador(Base_Personagem):
    def __init__(self):
        
        pos_x_inicial = 320
        
        self.caminho = os.path.join(os.path.dirname(__file__), "..", "data", "images", "personagens", "coordenador", "coordenador_idle_esquerda.png")
        
        super().__init__()
        
        self.image = pygame.transform.scale(self.image, (150, 350))
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x_inicial, 245) 

    def update(self):
        
        if self.rect.x > player.rect.x:
            img_nome = "coordenador_idle_esquerda.png"
        else:
            img_nome = "coordenador_idle_direita.png"
            
        # Muda a direção que o coordenador olha
        novo_caminho = os.path.join(os.path.dirname(__file__), "..", "data", "images", "personagens", "coordenador", img_nome)
        if self.caminho != novo_caminho:
            self.caminho = novo_caminho
            self.image = pygame.image.load(self.caminho)
            self.image = pygame.transform.scale(self.image, (150, 350))
    
class Maíra(Base_Personagem):
    def __init__(self):
        
        self.caminho = os.path.join(os.path.dirname(__file__), "..", "data", "images", "personagens", "maíra_presa.png")
        super().__init__()
        
        self.image = pygame.transform.scale(self.image, (250, 420))
        self.rect = self.image.get_rect()
        self.rect.topleft = (90, 175) 
        self.liberta = False

    def update(self):   
        if self.liberta:
            novo_caminho = os.path.join(os.path.dirname(__file__), "..", "data", "images", "personagens", "maíra_solta.png") 
            if self.caminho != novo_caminho:
                self.caminho = novo_caminho
                self.image = pygame.image.load(self.caminho)
                self.image = pygame.transform.scale(self.image, (250, 420))