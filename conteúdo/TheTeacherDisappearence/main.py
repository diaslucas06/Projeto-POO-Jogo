import pygame
import sys 

pygame.init()

LARGURA, ALTURA = 936, 512
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("The Teacher Disappearence")

fundo = pygame.image.load("conteúdo/TheTeacherDisappearence/data/images/corredores/CorredorA36.png")
player_img = pygame.image.load("conteúdo/TheTeacherDisappearence/data/images/personagens/personagem-frente.png")
player_img = pygame.transform.scale(player_img, (250, 250))

player_x = 100
player_y = 200
velocidade = 5

relogio = pygame.time.Clock()
rodando = True

while rodando:
    relogio.tick(60)
    
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
            
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        player_x -= velocidade
    if teclas[pygame.K_RIGHT]:
        player_x += velocidade
        
    tela.blit(fundo, (0, 0))
    tela.blit(player_img, (player_x, player_y))
    pygame.display.flip()
    
pygame.quit()
sys.exit()