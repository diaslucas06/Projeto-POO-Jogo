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
    def __init__(self):
        self.player_andar = pygame.sprite.Group()
        self.player = Player()
        self.player_andar.add(self.player)

        self.items = pygame.sprite.Group()
        self.chave = Key1()
        self.items.add(self.chave)

        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("The Teacher Disappearence")
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "corredores", "CorredorA36.png")
        self.fundo = pygame.image.load(self.caminho).convert()
        self.fundo = pygame.transform.scale(self.fundo, (LARGURA, ALTURA))
        self.relogio = pygame.time.Clock()

    def run(self):
    
        while True:
            
            self.relogio.tick(FPS)
            
            self.teclas = pygame.key.get_pressed()
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                elif event.type == KEYDOWN:
                    self.player.andando()
                    
            for item in self.items:
                if self.player.rect.colliderect(item.rect) and not item.coletado:
                    if self.teclas[pygame.K_e]:
                        self.player.coletando()
                        item.coletado = True
                            
            self.items.update()            
            self.player_andar.update(self.teclas)
            
            self.tela.blit(self.fundo, (0,0))
            self.items.draw(self.tela)
            self.player_andar.draw(self.tela)
            pygame.display.flip()