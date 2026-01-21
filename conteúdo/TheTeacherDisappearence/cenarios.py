import pygame
from ui.hud import Inventario, Hud, Seta
from items.keys import Key1, Key2, Key3, Key4, PenDrive, Fita, Carrinho
from characters.base import Hugo, Zelador
from ui.sounds import Som, Musica
import os
from main import player
from characters.dialogue import Dialogo_Hugo1, Dialogo_Zelador

#player
PLAYER_LARGURA = 170
PLAYER_ALTURA = 300

FPS = 60

#valores
LARGURA = 1280
ALTURA = 720

#hud
inventario = Inventario()
hud = Hud()
seta1 = Seta(40, 450, "CorredorM1")
seta2 = Seta(40, 450, "Área Externa")
seta3 = Seta(40, 450, "CorredorM4")
seta4 = Seta(40, 450, "CorredorM5")
seta5 = Seta(40, 450, "CorredorM6")
seta6 = Seta(40, 450, "CorredorM1")

#sons
pegar_item_som = Som("smw_stomp.mp3")
abrir_porta_som = Som("smw_door_opens.wav")

#itens
chave = Key1(300, 520)
chave_m5 = Key2(300, 520)
chave_coapac = Key3(300, 520)
chave_m1 = Key4(300, 520)
pendrive = PenDrive(500, 520)
fita = Fita(500, 530)
carrinho = Carrinho(50, 330)
lista_itens = []

#cores
WHITE = (255, 255, 255)

#personagens
hugo = Hugo()
zelador = Zelador()

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
        self.alarme = pygame.Rect(0,0,0,0)
        self.alarme_ativado = False
        self.trancada = False
        
        self.seta = None
        self.entrar_sala = False
        self.rect_fundo = None 
        self.fundo_salvo = None
        self.dialogo = None
        
        self.item_necessario = None
        
    def desenhar(self):
        
        self.fundo = pygame.image.load(self.caminho).convert()
        self.fundo = pygame.transform.scale(self.fundo, (LARGURA, ALTURA))
        self.teclas = pygame.key.get_pressed()
                            
        colidiu = player.update(self.teclas)
        
        #verificando a colisão
        if colidiu:
            return self.mudar_tela()
        
        self.items.update()    

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
                    for indice, item in enumerate(lista_itens):
                        nova_posicao_x = inventario.posicao_base_x + (indice * inventario.espacamento_entre_itens)
                        item.rect.topleft = (nova_posicao_x, inventario.posicao_y)
                        self.tela.blit(item.image, item.rect.topleft)
        
        #colisão com a porta para entrar em salas/laboratórios
        if player.rect.colliderect(self.porta):
            #mensagem ao colidir
            self.tela.blit(hud.entrar, (60,20))
            self.tela.blit(hud.tecla_e, (20, 20))
            if self.teclas[pygame.K_e]:
                if self.trancada == False:
                    self.entrar_sala = True
                    abrir_porta_som.play()
                    return self.mudar_tela()
                else:
                    if self.item_necessario in lista_itens:
                        self.entrar_sala = True
                        abrir_porta_som.play()
                        self.trancada = False
        
                        # Remover item usado
                        item_usado = self.item_necessario
                        item_usado.utilizado = True
                        lista_itens.remove(item_usado)
                        self.items.remove(item_usado)
                        
                        return self.mudar_tela()
                
                
        #Precisa consertar
        if player.rect.colliderect(self.alarme):
            if self.teclas[pygame.K_e]:
                som_alarme = Musica("alarm.ogg")
                som_alarme.play()
                self.alarme_ativado = True
                alarme_tempo = 20000 
                inicio_alarme = pygame.time.get_ticks()
                while self.alarme_ativado:
                    agora = pygame.time.get_ticks()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                    if agora - inicio_alarme >= alarme_tempo:
                        self.alarme_ativado = False
                        som_alarme.parar()
                    pygame.time.Clock().tick(FPS)
            
            
        #desenhando itens
        self.items.draw(self.tela)
        inventario.update()
            
        for seta in self.setas:
            #desenhando seta
            seta.clicado = False
            self.tela.blit(seta.image, seta.rect)
            if player.rect.colliderect(seta.rect):
                self.tela.blit(hud.clicar, (20, 20))
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        
                    elif event.type == pygame.KEYDOWN: 
                        if event.key == pygame.K_s:
                            seta.clicado = True
                
                if seta.clicado == True:
                    if seta.destino == "CorredorM1":
                        return CorredorM1()
                    elif seta.destino == "CorredorM4":
                        return CorredorM4() 
                    elif seta.destino == "CorredorM6":
                        return CorredorM6() 
                    elif seta.destino == "CorredorM5":
                        return CorredorM5() 
                    elif seta.destino == "Área Externa":
                        return Arquibancadas() 
        
        #desenhando itens no inventário
        for item in lista_itens:
            self.tela.blit(item.image, item.rect.topleft)
            
        #desenhando o player
        self.player_andar.draw(self.tela)
        
        #desenhando os personagens
        for character in self.characters:
            self.tela.blit(character.image, (120, 245))
            alcance_interacao = character.rect.inflate(300, 300)
            if player.rect.colliderect(alcance_interacao):
                #mensagem ao colidir
                self.tela.blit(hud.interagir, (60,20))
                self.tela.blit(hud.tecla_i, (20, 20))
                if self.teclas[pygame.K_i]:
                    self.rect_fundo = self.tela.get_rect()
                    self.fundo_salvo = self.tela.copy()
                    self.dialogo.run()
        
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
        self.item_necessario = chave
        if not chave.utilizado:
            self.trancada = True
            if chave not in self.items:
                self.items.add(chave)
        else:
            self.trancada = False
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
        self.character = zelador
        if self.character not in self.characters:
            self.characters.add(self.character)
        self.dialogo = Dialogo_Zelador(cenario=self)
            
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
        self.porta = pygame.Rect(500,200,100,340)
        self.trancada = True
        
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
            return CorredorCOAPAC2()  
        
class CorredorCOAPAC2(Cenario):
    
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "corredores", "CorredorCoapac2.png")
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self.alarme = pygame.Rect(950,200,100,340)

    def mudar_tela(self):
        if player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            return CorredorCOAPAC1()
        elif player.ultima_direcao == "direita" and player.rect.x >= LARGURA - PLAYER_LARGURA - 300:
            return CorredorCOAPAC3()    
        
class CorredorCOAPAC3(Cenario):
    
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "corredores", "CorredorCoapac3.png")
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        if carrinho not in self.items:
            self.items.add(carrinho)
        self.item_necessario = chave_coapac
        if not chave_coapac.utilizado:
            self.trancada = True
        else:
            self.trancada = False
        self.porta = pygame.Rect(1050,200,100,340)

    def mudar_tela(self):
        if player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            return CorredorCOAPAC2()
        elif player.ultima_direcao == "direita" and player.rect.x >= LARGURA - PLAYER_LARGURA - 300:
            return Arquibancadas()    
        
# Área externa - Testes
class Arquibancadas(Cenario):
    
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "Arquibancada.png")
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def mudar_tela(self):
        if player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            return CorredorCOAPAC3()
        elif player.ultima_direcao == "direita" and player.rect.x >= LARGURA - PLAYER_LARGURA - 300:
            return Arquibancadas2()   
        
class Arquibancadas2(Cenario):
    
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "Arquibancada2.png")
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self.nova_area = None #Onde o player vai entrar no centro
        if seta2 not in self.setas:
            self.setas.add(seta2)

    def mudar_tela(self):
        if player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            return Arquibancadas()
        elif player.ultima_direcao == "direita" and player.rect.x >= LARGURA - PLAYER_LARGURA - 300:
            return None   
        
class CorredorA42(Cenario):
    
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "corredores", "CorredorA42.png")
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        if seta1 not in self.setas:
            self.setas.add(seta1)
        if player.voltando_seta:
            player.voltando_seta = False
            player.ultima_direcao = "direita"
            player.animacao_atual = player.andar_direita
            player.image = player.andar_direita[int(player.atual)]
            player.image = pygame.transform.scale(player.image, (PLAYER_LARGURA, PLAYER_ALTURA))
            player.rect.left = 300
        self.character = zelador
        if chave_coapac not in self.items:
            self.items.add(chave_coapac)
        
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
        self.item_necessario = chave_m1
        if not chave_m1.utilizado:
            self.trancada = True
        else:
            self.trancada = False
        if seta3 not in self.setas:
            self.setas.add(seta3)
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
        
class CorredorM4(Cenario):
    
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "corredores", "CorredorM4.png")
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        if seta6 not in self.setas:
            self.setas.add(seta6)
        if seta3.clicado:
            seta3.clicado = False
            player.ultima_direcao = "esquerda"
            player.animacao_atual = player.andar_esquerda
            player.image = player.andar_esquerda[int(player.atual)]
            player.image = pygame.transform.scale(player.image, (PLAYER_LARGURA, PLAYER_ALTURA))

    def mudar_tela(self):
        if self.entrar_sala:
            self.entrar_sala = False
            return None
        elif player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            return CorredorM6()     
        elif player.ultima_direcao == "direita" and player.rect.x >= LARGURA - PLAYER_LARGURA - 300:
            return None       
        
class CorredorM6(Cenario):
    
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "corredores", "CorredorM6.png")
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self.porta = pygame.Rect(950,200,100,340)
        if seta4 not in self.setas:
            self.setas.add(seta4)
        if seta5.clicado:
            seta5.clicado = False
            player.ultima_direcao = "esquerda"
            player.animacao_atual = player.andar_esquerda
            player.image = player.andar_esquerda[int(player.atual)]
            player.image = pygame.transform.scale(player.image, (PLAYER_LARGURA, PLAYER_ALTURA))

    def mudar_tela(self):
        if self.entrar_sala:
            self.entrar_sala = False
            return None
        elif player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            return None
        elif player.ultima_direcao == "direita" and player.rect.x >= LARGURA - PLAYER_LARGURA - 300:
            return CorredorM4()      
        
class CorredorM5(Cenario):
    
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "corredores", "CorredorM5.png")
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self.item_necessario = chave_m5
        if not chave_m5.utilizado:
            self.trancada = True
        else:
            self.trancada = False
        self.porta = pygame.Rect(300,200,100,340)
        if seta5 not in self.setas:
            self.setas.add(seta5)
        if seta4.clicado:
            seta4.clicado = False
            player.ultima_direcao = "direita"
            player.animacao_atual = player.andar_direita
            player.image = player.andar_direita[int(player.atual)]
            player.image = pygame.transform.scale(player.image, (PLAYER_LARGURA, PLAYER_ALTURA))

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
        if chave_m1 not in self.items:
            self.items.add(chave_m1)
        if pendrive not in self.items:
            self.items.add(pendrive)
        
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
        if chave_m1 not in self.items:
            self.items.add(chave_m1)
            
        player.ultima_direcao = "esquerda"
        player.animacao_atual = player.andar_esquerda
        player.image = player.andar_esquerda[int(player.atual)]
        player.image = pygame.transform.scale(player.image, (PLAYER_LARGURA, PLAYER_ALTURA))
        self.dialogo = Dialogo_Hugo1(cenario=self)
        
    def mudar_tela(self):
        if player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            return None
        elif player.ultima_direcao == "direita" and player.rect.right >= LARGURA:
            player.saindo_porta = True
            return CorredorM1()
        