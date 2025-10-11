import pygame
from pygame.locals import *
from player import Player
from items.keys import Key1, Key2
from ui.hud import Inventario
import os

pygame.init()

PLAYER_LARGURA = 170
PLAYER_ALTURA = 300

LARGURA = 1280
ALTURA = 720
FPS = 30

chave = Key1()
chave2 = Key2()
player = Player()

inventario = Inventario()
lista_itens = []

class Game():
    def __init__(self, cenario):

        pygame.display.set_caption("The Teacher Disappearence")
        self.relogio = pygame.time.Clock()    
        self.cenario = cenario

    def run(self):
    
        while True:
            
            self.relogio.tick(FPS)
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                
            novo_cenario = self.cenario.desenhar()
            if novo_cenario:
                self.cenario = novo_cenario
                if player.ultima_direcao == "esquerda":
                    player.rect.topleft = (1100, 290)
                elif player.ultima_direcao == "direita":
                    player.rect.topleft = (0, 290)
            pygame.display.flip()

class Cenario():
    def __init__(self):
        self.player_andar = pygame.sprite.Group()
        self.player = player
        self.player_andar.add(self.player)
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        self.teclas = pygame.key.get_pressed()
        self.colidiu = self.player.update(self.teclas)
        self.items = pygame.sprite.Group()
        
    def desenhar(self):
        
        self.fundo = pygame.image.load(self.caminho).convert()
        self.fundo = pygame.transform.scale(self.fundo, (LARGURA, ALTURA))
        
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            for item in self.items:
                if item.rect.collidepoint(mouse):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    if self.player.rect.colliderect(item.rect) and not item.coletado:
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.player.coletando()
                            lista_itens.append(item)
                            item.coletado = True
                else: 
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                
        colidiu = self.player.update(self.teclas)
        if colidiu:
            return self.mudar_tela()
        self.items.update()            
        self.tela.blit(self.fundo, (0,0))
        self.tela.blit(inventario.image, (300,610))
        self.items.draw(self.tela)
        for item in lista_itens:
            self.tela.blit(item.image, item.rect.topleft)
        self.player_andar.draw(self.tela)
        
    def mudar_tela(self):
        if self.player.ultima_direcao == "esquerda" and self.player.rect.left <= 0:
            return None
        elif self.player.ultima_direcao == "direita" and self.player.rect.right >= LARGURA:
            return None
            
class CorredorA36(Cenario):
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "corredores", "CorredorA36.png")
        if chave not in self.items:
            self.items.add(chave)
        self.porta = pygame.Rect(540,200,180,340)
    
    def mudar_tela(self):
        if self.player.ultima_direcao == "esquerda" and self.player.rect.left <= 0:
            return CorredorA38()
        elif self.player.ultima_direcao == "direita" and self.player.rect.right >= LARGURA:
            return CorredorA30()

class CorredorA38(Cenario):
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "corredores", "CorredorA38.png")
        if chave2 not in self.items:
            self.items.add(chave2)
            
    def mudar_tela(self):
        if self.player.ultima_direcao == "esquerda" and self.player.rect.left <= 0:
            return None
        elif self.player.ultima_direcao == "direita" and self.player.rect.right >= LARGURA:
            return CorredorA36()
        
class CorredorA30(Cenario):
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "corredores", "CorredorA28.png")
        
    def mudar_tela(self):
        if self.player.ultima_direcao == "esquerda" and self.player.rect.left <= 0:
            return CorredorA36()
        elif self.player.ultima_direcao == "direita" and self.player.rect.right >= LARGURA:
            return SalaA36()
        
class SalaA36(Cenario):
    
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "salas", "SalaA36.png")
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
    def mudar_tela(self):
        if self.player.ultima_direcao == "esquerda" and self.player.rect.left <= 0:
            return CorredorA36()
        elif self.player.ultima_direcao == "direita" and self.player.rect.right >= LARGURA:
            return None
        
        
class LabM5(Cenario):
    
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "salas", "LabM5.png")
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
    def mudar_tela(self):
        if self.player.ultima_direcao == "esquerda" and self.player.rect.left <= 0:
            return None
        elif self.player.ultima_direcao == "direita" and self.player.rect.right >= LARGURA:
            return None
        
class LabM6(Cenario):
    
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "salas", "LabM6.png")
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
    def mudar_tela(self):
        if self.player.ultima_direcao == "esquerda" and self.player.rect.left <= 0:
            return None
        elif self.player.ultima_direcao == "direita" and self.player.rect.right >= LARGURA:
            return None
    