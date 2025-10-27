import pygame
from ui.hud import Inventario, Hud, Seta
from items.keys import Key1, Key2, Fita
from characters.base import Hugo
from ui.sounds import Som
import os
from main import player

#player
PLAYER_LARGURA = 170
PLAYER_ALTURA = 300

#valores
LARGURA = 1280
ALTURA = 720

#hud
inventario = Inventario()
hud = Hud()
seta1 = Seta()

#sons
pegar_item_som = Som("smw_stomp.mp3")
abrir_porta_som = Som("smw_door_opens.wav")

#itens
chave = Key1(300, 520)
chave_m5 = Key2(300, 520)
fita = Fita(500, 530)
lista_itens = []

#cores
WHITE = (255, 255, 255)

#personagens
hugo = Hugo()

sair_sala = False

class Cenario():
    
    def __init__(self):
        
        self.player_andar = pygame.sprite.Group()
        self.player_andar.add(player)
        
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        self.teclas = pygame.key.get_pressed()
        
        self.colidiu = player.update(self.teclas)
        
        self.items = pygame.sprite.Group()
        self.characters = pygame.sprite.Group()
        self.setas = pygame.sprite.Group()
        
        self.porta = pygame.Rect(0,0,0,0)
        
        self.seta = None
        self.entrar_sala = False
        
    def desenhar(self):
        
        self.fundo = pygame.image.load(self.caminho).convert()
        self.fundo = pygame.transform.scale(self.fundo, (LARGURA, ALTURA))
        self.teclas = pygame.key.get_pressed()
                            
        colidiu = player.update(self.teclas)
        
        #verificando a colisão
        if colidiu:
            return self.mudar_tela()
        
        self.items.update(inventario)    
        #desenhando o fundo        
        self.tela.blit(self.fundo, (0,0))
        #desenhando o inventário
        self.tela.blit(inventario.image, (300,610))
        
        #pegar itens e colocá-los no inventário
        for item in self.items:
            if player.rect.colliderect(item.rect) and not item.coletado:
                #mensagem ao colidir
                self.tela.blit(hud.pegar, (60, 20))
                self.tela.blit(hud.tecla_p, (20, 20))
                if self.teclas[pygame.K_p]:
                    pegar_item_som.play()
                    player.coletando()
                    lista_itens.append(item)
                    item.coletado = True
        
        #colisão com a porta para entrar em salas/laboratórios
        if player.rect.colliderect(self.porta):
            #mensagem ao colidir
            self.tela.blit(hud.entrar, (60,20))
            self.tela.blit(hud.tecla_e, (20, 20))
            if self.teclas[pygame.K_e]:
                self.entrar_sala = True
                abrir_porta_som.play()
                return self.mudar_tela()
            
        if player.saindo_porta:
            player.saindo_porta = False
            player.rect.topleft = (self.porta.left, 295)
            
        #desenhando itens
        self.items.draw(self.tela)
        
        #desenhando os personagens
        for character in self.characters:
            if player.rect.colliderect(character):
                #mensagem ao colidir
                self.tela.blit(hud.interagir, (60,20))
                self.tela.blit(hud.tecla_i, (20, 20))
            self.tela.blit(character.image, (120, 245))
            
        for seta in self.setas:
            #desenhando seta
            self.tela.blit(seta.image, seta.rect)
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif seta.rect.collidepoint(mouse_pos):
                    self.tela.blit(hud.clicar, (20, 20))
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        seta.clicado = True
                        return CorredorM1()
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        #desenhando itens no inventário
        for item in lista_itens:
            self.tela.blit(item.image, item.rect.topleft)
            
        #desenhando o player
        self.player_andar.draw(self.tela)
        
    def mudar_tela(self):
        if self.entrar_sala:
            self.entrar_sala = False
            return None
        elif player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            return None
        elif player.ultima_direcao == "direita" and player.rect.right >= LARGURA:
            return None
  
class CorredorA36(Cenario):
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "corredores", "CorredorA36.png")
        if chave not in self.items:
            self.items.add(chave)
        self.porta = pygame.Rect(550,200,100,340)
    
    def mudar_tela(self):
        if self.entrar_sala:
            self.entrar_sala = False
            return SalaA36()
        elif player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            return CorredorA38()
        elif player.ultima_direcao == "direita" and player.rect.right >= LARGURA:
            return CorredorA30()
        
class CorredorA38(Cenario):
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "corredores", "CorredorA38.png")
        self.porta = pygame.Rect(640,200,100,340)
            
    def mudar_tela(self):
        if self.entrar_sala:
            self.entrar_sala = False
            return SalaA38()
        elif player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            return CorredorA42()
        elif player.ultima_direcao == "direita" and player.rect.right >= LARGURA:
            return CorredorA36()
        
class CorredorA30(Cenario):
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "corredores", "CorredorA28.png")
        
    def mudar_tela(self):
        if player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            return CorredorA36()
        elif player.ultima_direcao == "direita" and player.rect.right >= LARGURA:
            return CorredorA26()
        
class CorredorA26(Cenario):
    
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "corredores", "CorredorA26.png")
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
    def mudar_tela(self):
        if player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            return CorredorA30()
        elif player.ultima_direcao == "direita" and player.rect.x >= LARGURA - PLAYER_LARGURA - 300:
            return CorredorCOAPAC1()
        
class CorredorCOAPAC1(Cenario):
    
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "corredores", "CorredorCoapac1.png")
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def mudar_tela(self):
        if player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            return CorredorA26()
        elif player.ultima_direcao == "direita" and player.rect.x >= LARGURA - PLAYER_LARGURA - 300:
            return None   
        
class CorredorA42(Cenario):
    
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "corredores", "CorredorA42.png")
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self.seta = seta1
        if self.seta not in self.setas:
            self.setas.add(self.seta)
        if player.voltando_seta:
            player.voltando_seta = False
            player.ultima_direcao = "direita"
            player.animacao_atual = player.andar_direita
            player.image = player.andar_direita[int(player.atual)]
            player.image = pygame.transform.scale(player.image, (PLAYER_LARGURA, PLAYER_ALTURA))
            player.rect.left = 300
        
    def mudar_tela(self):
        if player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            return None
        elif player.ultima_direcao == "direita" and player.rect.right >= LARGURA:
            return CorredorA38()
        
class CorredorM1(Cenario):
    
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "corredores", "CorredorM1.png")
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self.porta = pygame.Rect(900,200,100,340)
        if seta1.clicado:
            seta1.clicado = False
            player.ultima_direcao = "direita"
            player.animacao_atual = player.andar_direita
            player.image = player.andar_direita[int(player.atual)]
            player.image = pygame.transform.scale(player.image, (PLAYER_LARGURA, PLAYER_ALTURA))
        
    def mudar_tela(self):
        if self.entrar_sala:
            self.entrar_sala = False
            return LabM1()
        elif player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            player.voltando_seta = True
            return CorredorA42()
        elif player.ultima_direcao == "direita" and player.rect.x >= LARGURA - PLAYER_LARGURA - 300:
            return CorredorM5()
        
class CorredorM5(Cenario):
    
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "corredores", "CorredorM5.png")
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self.porta = pygame.Rect(300,200,100,340)

    def mudar_tela(self):
        if self.entrar_sala:
            self.entrar_sala = False
            return LabM5()
        elif player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            return CorredorM1()
        elif player.ultima_direcao == "direita" and player.rect.x >= LARGURA - PLAYER_LARGURA - 300:
            return None
        
class SalaA36(Cenario):
    
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "salas", "SalaA36.png")
        player.ultima_direcao = "direita"
        player.animacao_atual = player.andar_direita
        player.image = player.andar_direita[int(player.atual)]
        player.image = pygame.transform.scale(player.image, (PLAYER_LARGURA, PLAYER_ALTURA))
        
        if chave_m5 not in self.items:
            self.items.add(chave_m5)
            
    def mudar_tela(self):
        if player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            player.saindo_porta = True
            return CorredorA36()
        elif player.ultima_direcao == "direita" and player.rect.right >= LARGURA:
            return None
        
class SalaA38(Cenario):
    
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "salas", "SalaA36.png")
        player.ultima_direcao = "direita"
        player.animacao_atual = player.andar_direita
        player.image = player.andar_direita[int(player.atual)]
        player.image = pygame.transform.scale(player.image, (PLAYER_LARGURA, PLAYER_ALTURA))
        
        if fita not in self.items:
            self.items.add(fita)
        
    def mudar_tela(self):
        if player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            player.saindo_porta = True
            return CorredorA38()
        elif player.ultima_direcao == "direita" and player.rect.right >= LARGURA:
            return None
        
class LabM5(Cenario):
    
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "salas", "LabM5.png")
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
    def mudar_tela(self):
        if player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            player.saindo_porta = True
            return CorredorM5()
        elif player.ultima_direcao == "direita" and player.rect.right >= LARGURA:
            return None
        
class LabM1(Cenario):
    
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "salas", "LabM6.png")
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self.character = hugo
        if self.character not in self.characters:
            self.characters.add(self.character)
            
        player.ultima_direcao = "esquerda"
        player.animacao_atual = player.andar_esquerda
        player.image = player.andar_esquerda[int(player.atual)]
        player.image = pygame.transform.scale(player.image, (PLAYER_LARGURA, PLAYER_ALTURA))
        
    def mudar_tela(self):
        if player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            return None
        elif player.ultima_direcao == "direita" and player.rect.right >= LARGURA:
            player.saindo_porta = True
            return CorredorM1()
        