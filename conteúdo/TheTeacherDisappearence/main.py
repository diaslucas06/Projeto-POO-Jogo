import pygame
from pygame.locals import *
from player import Player
from items.keys import Key1
import os

pygame.init()

LARGURA = 1280
ALTURA = 720
FPS = 30

player_andar = pygame.sprite.Group()
player = Player()
player_andar.add(player)

items = pygame.sprite.Group()
chave = Key1()
items.add(chave)

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("The Teacher Disappearence")
caminho = os.path.join(os.path.dirname(__file__), "data", "images", "corredores", "CorredorA36.png")
fundo = pygame.image.load(caminho).convert()
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))
relogio = pygame.time.Clock()

while True:
    
    relogio.tick(FPS)
    teclas = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == KEYDOWN:
            player.andando()
            
    for item in items:
        if player.rect.colliderect(item.rect) and not item.coletado:
            if teclas[pygame.K_e]:
                player.coletando()
                item.coletado = True
                    
    items.update()            
    player_andar.update(teclas)
    
    tela.blit(fundo, (0,0))
    items.draw(tela)
    player_andar.draw(tela)
    pygame.display.flip()