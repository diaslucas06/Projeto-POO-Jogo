import pygame
from pygame.locals import *
from player import Player
from items.keys import Key1, Key2, Fita
from ui.sounds import Musica, Som
from ui.hud import Inventario, Hud, Seta
from characters.base import Hugo
import os

pygame.init()

#valores
LARGURA = 1280
ALTURA = 720
FPS = 30

#cores
WHITE = (255, 255, 255)

#itens
chave = Key1(300, 520)
chave_m5 = Key2(300, 520)
fita = Fita(500, 530)
lista_itens = []

#player
PLAYER_LARGURA = 170
PLAYER_ALTURA = 300
player = Player()

#hud
inventario = Inventario()
hud = Hud()
seta1 = Seta()

#sons
pegar_item_som = Som("smw_stomp.mp3")
abrir_porta_som = Som("smw_door_opens.wav")

sair_sala = False

#personagens
hugo = Hugo()

class Game():
    def __init__(self, cenario):

        pygame.display.set_caption("The Teacher Disappearence")
        self.relogio = pygame.time.Clock()    
        self.cenario = cenario
        musica = Musica("Robert Blumenau - Suspense.mp3")
        musica.play()
        pygame.mixer.music.set_volume(0.05)

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
                    player.rect.topleft = (1100, 295)
                elif player.ultima_direcao == "direita":
                    player.rect.topleft = (0, 295)
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
        self.porta = pygame.Rect(0,0,0,0)
        self.entrar_sala = False
        self.character = pygame.Rect(0,0,0,0)
        
    def desenhar(self):
        
        self.fundo = pygame.image.load(self.caminho).convert()
        self.fundo = pygame.transform.scale(self.fundo, (LARGURA, ALTURA))
        self.teclas = pygame.key.get_pressed()
                            
        colidiu = self.player.update(self.teclas)
        
        if colidiu:
            return self.mudar_tela()
        
        self.items.update(inventario)            
        self.tela.blit(self.fundo, (0,0))
        self.tela.blit(inventario.image, (300,610))
        
        for item in self.items:
            if self.player.rect.colliderect(item.rect) and not item.coletado:
                self.tela.blit(hud.pegar, (60, 20))
                self.tela.blit(hud.tecla_p, (20, 20))
                if self.teclas[pygame.K_p]:
                    pegar_item_som.play()
                    self.player.coletando()
                    lista_itens.append(item)
                    item.coletado = True
        
        if self.player.rect.colliderect(self.porta):
            self.tela.blit(hud.entrar, (60,20))
            self.tela.blit(hud.tecla_e, (20, 20))
            if self.teclas[pygame.K_e]:
                self.entrar_sala = True
                abrir_porta_som.play()
                return self.mudar_tela()
            
        if self.player.rect.colliderect(self.character):
            self.tela.blit(hud.interagir, (60,20))
            self.tela.blit(hud.tecla_i, (20, 20))
            
        if player.saindo_porta:
            player.saindo_porta = False
            player.rect.topleft = (self.porta.left, 295)
            
        self.items.draw(self.tela)
        
        for item in lista_itens:
            self.tela.blit(item.image, item.rect.topleft)
            
        self.player_andar.draw(self.tela)
        
    def mudar_tela(self):
        if self.entrar_sala:
            self.entrar_sala = False
            return None
        elif self.player.ultima_direcao == "esquerda" and self.player.rect.left <= 0:
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
        if self.entrar_sala:
            self.entrar_sala = False
            return SalaA36()
        elif self.player.ultima_direcao == "esquerda" and self.player.rect.left <= 0:
            return CorredorA38()
        elif self.player.ultima_direcao == "direita" and self.player.rect.right >= LARGURA:
            return CorredorA30()
        
class CorredorA38(Cenario):
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "corredores", "CorredorA38.png")
        self.porta = pygame.Rect(600,200,180,340)
            
    def mudar_tela(self):
        if self.entrar_sala:
            self.entrar_sala = False
            return SalaA38()
        elif self.player.ultima_direcao == "esquerda" and self.player.rect.left <= 0:
            return CorredorA42()
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
            return CorredorA26()
        
class SalaA36(Cenario):
    
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "salas", "SalaA36.png")
        self.player.ultima_direcao = "direita"
        self.player.animacao_atual = self.player.andar_direita
        self.player.image = self.player.andar_direita[int(self.player.atual)]
        self.player.image = pygame.transform.scale(self.player.image, (PLAYER_LARGURA, PLAYER_ALTURA))
        
        if chave_m5 not in self.items:
            self.items.add(chave_m5)
            
    def mudar_tela(self):
        if self.player.ultima_direcao == "esquerda" and self.player.rect.left <= 0:
            player.saindo_porta = True
            return CorredorA36()
        elif self.player.ultima_direcao == "direita" and self.player.rect.right >= LARGURA:
            return None
            
        
class SalaA38(Cenario):
    
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "salas", "SalaA36.png")
        self.player.ultima_direcao = "direita"
        self.player.animacao_atual = self.player.andar_direita
        self.player.image = self.player.andar_direita[int(self.player.atual)]
        self.player.image = pygame.transform.scale(self.player.image, (PLAYER_LARGURA, PLAYER_ALTURA))
        
        if fita not in self.items:
            self.items.add(fita)
        
    def mudar_tela(self):
        if self.player.ultima_direcao == "esquerda" and self.player.rect.left <= 0:
            player.saindo_porta = True
            return CorredorA38()
        elif self.player.ultima_direcao == "direita" and self.player.rect.right >= LARGURA:
            return None
        
class LabM5(Cenario):
    
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "salas", "LabM5.png")
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
    def mudar_tela(self):
        if self.player.ultima_direcao == "esquerda" and self.player.rect.left <= 0:
            player.saindo_porta = True
            return CorredorM5()
        elif self.player.ultima_direcao == "direita" and self.player.rect.right >= LARGURA:
            return None
        
class LabM1(Cenario):
    
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "salas", "LabM6.png")
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self.player.ultima_direcao = "direita"
        self.player.animacao_atual = self.player.andar_esquerda
        self.player.image = self.player.andar_esquerda[int(self.player.atual)]
        self.player.image = pygame.transform.scale(self.player.image, (PLAYER_LARGURA, PLAYER_ALTURA))
        self.character = hugo
        
    def mudar_tela(self):
        if self.player.ultima_direcao == "esquerda" and self.player.rect.left <= 0:
            player.saindo_porta = True
            return CorredorM()
        elif self.player.ultima_direcao == "direita" and self.player.rect.right >= LARGURA:
            return None
        
    def desenhar(self):
        super().desenhar()
        self.tela.blit(self.character.image, (120, 245))
        
class CorredorA42(Cenario):
    
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "corredores", "CorredorA42.png")
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self.seta = seta1

    def desenhar(self):
        super().desenhar()
        self.tela.blit(seta1.image, seta1.rect)
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif seta1.rect.collidepoint(mouse_pos):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return CorredorM()
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
    def mudar_tela(self):
        if self.player.ultima_direcao == "esquerda" and self.player.rect.left <= 0:
            return None
        elif self.player.ultima_direcao == "direita" and self.player.rect.right >= LARGURA:
            return CorredorA38()

class CorredorA26(Cenario):
    
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "corredores", "CorredorA26.png")
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
    def mudar_tela(self):
        if self.player.ultima_direcao == "esquerda" and self.player.rect.left <= 0:
            return CorredorA30()
        elif self.player.ultima_direcao == "direita" and self.player.rect.x >= LARGURA - PLAYER_LARGURA - 300:
            return None
        
class CorredorM(Cenario):
    
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "corredores", "CorredorM1.png")
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self.porta = pygame.Rect(600,200,180,340)
        self.player.ultima_direcao = "direita"
        self.player.animacao_atual = self.player.andar_direita
        self.player.image = self.player.andar_direita[int(self.player.atual)]
        self.player.image = pygame.transform.scale(self.player.image, (PLAYER_LARGURA, PLAYER_ALTURA))
        
    def mudar_tela(self):
        if self.entrar_sala:
            self.entrar_sala = False
            return LabM1()
        elif self.player.ultima_direcao == "esquerda" and self.player.rect.left <= 0:
            return CorredorA42()
        elif self.player.ultima_direcao == "direita" and self.player.rect.x >= LARGURA - PLAYER_LARGURA - 300:
            return CorredorM5()
        
class CorredorM5(Cenario):
    
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "corredores", "CorredorM5.png")
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self.porta = pygame.Rect(600,200,180,340)

    def mudar_tela(self):
        if self.entrar_sala:
            self.entrar_sala = False
            return LabM5()
        elif self.player.ultima_direcao == "esquerda" and self.player.rect.left <= 0:
            return CorredorM()
        elif self.player.ultima_direcao == "direita" and self.player.rect.x >= LARGURA - PLAYER_LARGURA - 300:
            return None
    