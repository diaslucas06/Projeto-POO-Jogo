import pygame
from pygame.locals import *
from player import Player
import os

pygame.init()

LARGURA = 1280
ALTURA = 720

player_andar = pygame.sprite.Group()
player = Player()
player_andar.add(player)

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("The Teacher Disappearence")
caminho = os.path.join(os.path.dirname(__file__), "data", "images", "corredores", "CorredorA36.png")
fundo = pygame.image.load(caminho).convert()
fundo = pygame.transform.scale(fundo, (LARGURA, ALTURA))
relogio = pygame.time.Clock()

while True:
    relogio.tick(30)
    tela.blit(fundo, (0,0))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == KEYDOWN:
            player.andando()
        
    teclas = pygame.key.get_pressed()
    player_andar.draw(tela)
    player_andar.update(teclas)
    pygame.display.flip()