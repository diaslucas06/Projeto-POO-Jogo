import pygame
from pygame.locals import *
from player import Player
from items.keys import Key1
import os

pygame.init()

LARGURA = 1280
ALTURA = 720
FPS = 30

class Game():
    def __init__(self, cenario):

        pygame.display.set_caption("The Teacher Disappearence")
        self.relogio = pygame.time.Clock()
        self.cenario = cenario

    def run(self):
    
        while True:
            
            self.relogio.tick(FPS)
            self.items = pygame.sprite.Group()
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                
            self.cenario.desenhar()
            pygame.display.flip()

class Cenario():
    def __init__(self):
        self.player_andar = pygame.sprite.Group()
        self.player = Player()
        self.player_andar.add(self.player)
        
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        
        self.items = pygame.sprite.Group()
        
    def desenhar(self):
        
        self.fundo = pygame.image.load(self.caminho).convert()
        self.fundo = pygame.transform.scale(self.fundo, (LARGURA, ALTURA))
        self.teclas = pygame.key.get_pressed()
        colidiu = "Não"
        
        for event in pygame.event.get():
            if event.type == KEYDOWN:
               colidiu = self.player.andando()
               print(colidiu)

                
            for item in self.items:
                if self.player.rect.colliderect(item.rect) and not item.coletado:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.player.coletando()
                        item.coletado = True
                
        colidiu = self.player.update(self.teclas)
        if colidiu:
            Game(cenario=Cenario2()).run()      
        self.items.update()            
        self.tela.blit(self.fundo, (0,0))
        self.items.draw(self.tela)
        self.player_andar.draw(self.tela)
            
class Cenario1(Cenario):
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "corredores", "CorredorA36.png")
        self.chave = Key1()
        self.items.add(self.chave)
        
class Cenario2(Cenario):
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "corredores", "CorredorA38.png")