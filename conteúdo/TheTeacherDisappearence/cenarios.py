import pygame
from ui.hud import Inventario, Hud, Seta
from items.keys import Key1, Key2, Key3, Key4, CartaoAcesso, Fita, Fita2, Carrinho, PéDeCabra, Provas, Tesoura
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

#consertar posições
seta1 = Seta(40, 450, "CorredorM1")
seta2 = Seta(40, 450, "Campo")
seta3 = Seta(LARGURA//2 - 35, 450, "CorredorM4") #
seta4 = Seta(LARGURA//2 - 35, 450, "CorredorM5")
seta5 = Seta(LARGURA//2 - 35, 450, "CorredorM6")
seta6 = Seta(LARGURA//2, 450, "CorredorM1")
seta7 = Seta(LARGURA//2, 450, "CorredorNapne")

#sons
pegar_item_som = Som("smw_stomp.mp3")
abrir_porta_som = Som("smw_door_opens.wav")

#itens
chave = Key1(164, 330)
chave_m5 = Key2(300, 520)
chave_coapac = Key3(300, 520)
chave_m1 = Key4(680, 330)
chave_a38 = Key2(0, 0) # Posição 0,0 porque ela começa com o Hugo
chave_a38.nome_item = "Chave da Sala A38"
cartao_acesso = CartaoAcesso(500, 540)
fita = Fita(500, 530)
fita2 = Fita2(780, 320)
fita3 = Fita(350, 530)
carrinho = Carrinho(50, 330)
pe_de_cabra = PéDeCabra(50, 430)
provas_hugo = Provas(LARGURA//2 - 140, ALTURA//2 - 130)
tesoura = Tesoura(620, 390)
lista_itens = []

#cores
WHITE = (255, 255, 255)

#personagens
hugo = Hugo()
zelador = Zelador()

# estados: "inicio", "buscando_provas", "finalizado"
estado_missao_hugo = "inicio"

sair_sala = False

#alarme
alarme_ativo = False
tempo_inicio_alarme = 0
duracao_alarme = 10000 
som_alarme = None

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
        
        #mensagem de coleta de item
        self.mensagem_texto = ""
        self.mensagem_timer = 0
        self.exibir_mensagem = False
        self.duracao_mensagem = 3000
       
    def desenhar(self):
       
        self.fundo = pygame.image.load(self.caminho).convert()
        self.fundo = pygame.transform.scale(self.fundo, (LARGURA, ALTURA))
        self.teclas = pygame.key.get_pressed()
                            
        colidiu = player.update(self.teclas)
       
        #verificando a colisão
        if colidiu:
            return self.mudar_tela()
       
        self.items.update()    
        
        self.tela.blit(self.fundo, (0,0))
        self.tela.blit(inventario.image, (300,610))
       
        for item in self.items:
            if player.rect.colliderect(item.rect) and not item.coletado:
                self.tela.blit(hud.pegar, (60, 20))
                self.tela.blit(hud.tecla_p, (20, 20))
                if self.teclas[pygame.K_p]:
                    item.image = pygame.transform.scale(item.image, (25, 40))
                    pegar_item_som.play()
                    player.coletando()
                    lista_itens.append(item)
                    item.coletado = True
                    self.mensagem_texto = f"Voce coletou: {item.nome_item}"
                    self.exibir_mensagem = True
                    self.mensagem_timer = pygame.time.get_ticks()
                    for indice, item_inv in enumerate(lista_itens):
                        nova_posicao_x = inventario.posicao_base_x + (indice * inventario.espacamento_entre_itens)
                        item_inv.rect.topleft = (nova_posicao_x, inventario.posicao_y)
                        self.tela.blit(item_inv.image, item_inv.rect.topleft)
       
        #colisão com a porta para entrar em salas/laboratórios
        if player.rect.colliderect(self.porta):
            if self.item_necessario in lista_itens and self.trancada:
                self.tela.blit(hud.destrancar_porta, (60, 20))
                self.tela.blit(hud.tecla_e, (20, 20))
            elif self.trancada:
                self.tela.blit(hud.cadeado, (20, 20))
                self.tela.blit(hud.porta_trancada, (60, 20))
            else:
                self.tela.blit(hud.entrar, (60, 20))
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
       
                        item_usado = self.item_necessario
                        item_usado.utilizado = True
                        item_usado.coletado = True # Garante que não reapareça
                        
                        if item_usado in lista_itens:
                            lista_itens.remove(item_usado)
                        
                        return self.mudar_tela()
                    
        # Coloca o player na frente da porta ao sair de uma sala
        if player.saindo_porta:
            player.rect.centerx = self.porta.centerx
            player.rect.y = 295
            player.saindo_porta = False
               
               
        # Timer
        agora_timer = pygame.time.get_ticks() 
        global alarme_ativo, tempo_inicio_alarme, som_alarme #chama as variáveis que estão fora, não criando novas dentro da classe
        if player.rect.colliderect(self.alarme):
            self.tela.blit(hud.ativar_alarme, (90,20))
            self.tela.blit(hud.tecla_e, (50, 20))
            if self.teclas[pygame.K_e]:
                if not alarme_ativo:
                    alarme_ativo = True
                    tempo_inicio_alarme = agora_timer
                    som_alarme = Musica("alarm.ogg")
                    som_alarme.play()

        # Exibição e Contagem
        if alarme_ativo:
            tempo_passado = agora_timer - tempo_inicio_alarme
            if tempo_passado < duracao_alarme:
                #desenha o tempo que falta para o timer terminar
                segundos_restantes = (duracao_alarme - tempo_passado) // 1000
                txt_timer = hud.font.render(f"Tempo: {segundos_restantes}s", True, (255, 0, 0))
                largura_texto = txt_timer.get_width()
                self.tela.blit(txt_timer, (LARGURA // 2 - largura_texto//2, 50))
            else:
                alarme_ativo = False
                if som_alarme:
                    som_alarme.parar()
           
           
        #desenhando itens
        self.items.draw(self.tela)
        inventario.update()
           
        for seta in self.setas:
            seta.clicado = False
            self.tela.blit(seta.image, seta.rect)
            if player.rect.colliderect(seta.rect):
                self.tela.blit(hud.clicar, (60, 20))
                self.tela.blit(hud.tecla_s, (20, 20))
                if self.teclas[pygame.K_s]:
                    seta.clicado = True
               
                if seta.clicado:
                    if seta.destino == "CorredorM1":
                        return CorredorM1()
                    elif seta.destino == "CorredorM4":
                        return CorredorM4()
                    elif seta.destino == "CorredorM6":
                        return CorredorM6()
                    elif seta.destino == "CorredorM5":
                        return CorredorM5()
                    elif seta.destino == "Campo":
                        return Campo()
                    elif seta.destino == "CorredorNapne":
                        return CorredorNapne()
       
        #desenhando itens no inventário
        for item in lista_itens:
            self.tela.blit(item.image, item.rect.topleft)
               
        self.player_andar.draw(self.tela)
       
        for character in self.characters:
            character.update()
            if character == hugo:
                self.tela.blit(character.image, (120, 245))
                alcance_interacao = character.rect.inflate(300, 300)
            elif character == zelador:
                self.tela.blit(character.image, character.rect) 
                alcance_interacao = character.rect.inflate(100, 100)
                character.update()
                if character.rect.x > LARGURA + 400:
                    character.kill()
                    character.foi_embora = True
            if player.rect.colliderect(alcance_interacao):
                if self.teclas[pygame.K_i]:
                    self.fundo_salvo = self.tela.copy()
                    self.dialogo.run()
                    if character == zelador:
                        character.indo_embora = True
                        character.foi_embora = True
                    return None
                self.tela.blit(hud.interagir, (60,20))
                self.tela.blit(hud.tecla_i, (20, 20))
                
        if self.exibir_mensagem:
            agora = pygame.time.get_ticks()
            if agora - self.mensagem_timer < self.duracao_mensagem:
                texto_surf = hud.font.render(self.mensagem_texto, True, (255, 255, 255))
                # Centraliza a mensagem na tela
                largura_texto = texto_surf.get_width()
                self.tela.blit(texto_surf, (LARGURA//2 - largura_texto//2, 100))
            else:
                self.exibir_mensagem = False
       
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
        else:
            self.trancada = False

        if not chave_coapac.coletado:
            self.items.add(chave_coapac)
            
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
            
        self.item_necessario = pe_de_cabra
        self.porta = pygame.Rect(500,200,100,340)
        
        if not pe_de_cabra.utilizado:
            self.trancada = True
        else:
            self.trancada = False
        
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
       
        self.alarme = pygame.Rect(950, 200, 100, 340)
        
        if not carrinho.coletado:
            self.items.add(carrinho)
            
        self.item_necessario = chave_coapac
        if not chave_coapac.utilizado:
            self.trancada = True
        else:
            self.trancada = False
            
        self.porta = pygame.Rect(1050, 200, 100, 340)

    def mudar_tela(self):
        if self.entrar_sala:
            self.entrar_sala = False
            return COAPAC()
        if player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            return CorredorCOAPAC2()
        elif player.ultima_direcao == "direita" and player.rect.x >= LARGURA - PLAYER_LARGURA - 300:
            return CorredorCOAPAC4()

class CorredorCOAPAC4(Cenario):

    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "corredores", "CorredorCoapac4.png")
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self.item_necessario = cartao_acesso
        if not cartao_acesso.utilizado:
            self.trancada = True
        else:
            self.trancada = False
        self.porta = pygame.Rect(1100, 200, 100, 340)

        if seta7 not in self.setas:
            self.setas.add(seta7)

    def mudar_tela(self):
        if self.entrar_sala:
            self.entrar_sala = False
            return Diretoria()
        if player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            return CorredorCOAPAC3()
        elif player.ultima_direcao == "direita" and player.rect.x >= LARGURA - PLAYER_LARGURA - 300:
            return None

class Diretoria(Cenario):

    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "salas", "Diretoria.png")
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        if not pe_de_cabra.coletado:
            self.items.add(pe_de_cabra)
            
        player.ultima_direcao = "esquerda"
        player.animacao_atual = player.andar_esquerda
        player.image = player.andar_esquerda[int(player.atual)]
        player.image = pygame.transform.scale(player.image, (PLAYER_LARGURA, PLAYER_ALTURA))

    def mudar_tela(self):
        if player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            return None
        elif player.ultima_direcao == "direita" and player.rect.x >= LARGURA - PLAYER_LARGURA - 300:
            return CorredorCOAPAC4()
        
class Arquibancadas(Cenario):
    
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "Arquibancada.png")
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    def mudar_tela(self):
        if player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            return Arquibancadas2()
        elif player.ultima_direcao == "direita" and player.rect.x >= LARGURA - PLAYER_LARGURA - 300:
            return Exterior()
        
class Arquibancadas2(Cenario):
    
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "Arquibancada2.png")
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        self.nova_area = None 
        if seta2 not in self.setas:
            self.setas.add(seta2)

        if player.voltando_seta:
            player.voltando_seta = False
            player.ultima_direcao = "direita"
            player.animacao_atual = player.andar_direita
            player.image = player.andar_direita[int(player.atual)]
            player.image = pygame.transform.scale(player.image, (PLAYER_LARGURA, PLAYER_ALTURA))
            player.rect.left = 295

    def mudar_tela(self):
        if player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            return None
        elif player.ultima_direcao == "direita" and player.rect.x >= LARGURA - PLAYER_LARGURA - 300:
            return Arquibancadas() 
            
class CorredorA42(Cenario):
    
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "corredores", "CorredorA42.png")
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        if not zelador.foi_embora:
            self.zelador = zelador 
            self.zelador.rect.topleft = (320, 245)
            if self.zelador not in self.characters:
                self.characters.add(self.zelador)
            self.dialogo = Dialogo_Zelador(cenario=self)
        if seta1 not in self.setas:
            self.setas.add(seta1)
        if player.voltando_seta:
            player.voltando_seta = False
            player.ultima_direcao = "direita"
            player.animacao_atual = player.andar_direita
            player.image = player.andar_direita[int(player.atual)]
            player.image = pygame.transform.scale(player.image, (PLAYER_LARGURA, PLAYER_ALTURA))
            player.rect.left = 295
            
    
        
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
            
        if seta6.clicado:
            seta6.clicado = False
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
        self.porta = pygame.Rect(1050,200,100,340)
        
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
            self.entrar_sala = True
            return LabM6()
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
        
        if not chave_m5.coletado:
            self.items.add(chave_m5)
            
    def mudar_tela(self):
        if player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            player.saindo_porta = True
            return CorredorA36()
        elif player.ultima_direcao == "direita" and player.rect.right >= LARGURA:
            return None
        
class CorredorA38(Cenario):
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "corredores", "CorredorA38.png")
        
        self.porta = pygame.Rect(640, 200, 100, 340)
        
        self.item_necessario = chave_a38
        
        if not chave_a38.utilizado:
            self.trancada = True
        else:
            self.trancada = False

    def mudar_tela(self):
        if self.entrar_sala:
            self.entrar_sala = False
            return SalaA38()
        elif player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            return CorredorA42()
        elif player.ultima_direcao == "direita" and player.rect.right >= LARGURA:
            return CorredorA36()


class CorredorNapne(Cenario):
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "corredores", "CorredorNapne.png")
        self.porta = pygame.Rect(1100, 200, 100, 340)
        self.item_necessario = pe_de_cabra

        if not pe_de_cabra.utilizado:
            self.trancada = True
        else:
            self.trancada = False

        if seta7.clicado:
            seta7.clicado = False
            player.ultima_direcao = "direita"
            player.animacao_atual = player.andar_direita
            player.image = player.andar_direita[int(player.atual)]
            player.image = pygame.transform.scale(player.image, (PLAYER_LARGURA, PLAYER_ALTURA))


    def mudar_tela(self):
        if self.entrar_sala:
            self.entrar_sala = False
            return Exterior()
        elif player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            return CorredorCOAPAC4()
        elif player.ultima_direcao == "direita" and player.rect.right >= LARGURA:
            return None
        
class SalaA38(Cenario):
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "salas", "SalaA36.png")
        
        if not cartao_acesso.coletado and cartao_acesso not in lista_itens:
            cartao_acesso.rect.topleft = (600, 530)
            self.items.add(cartao_acesso)
        
        player.ultima_direcao = "direita"
        player.animacao_atual = player.andar_direita
        player.image = player.andar_direita[int(player.atual)]
        player.image = pygame.transform.scale(player.image, (PLAYER_LARGURA, PLAYER_ALTURA))
        
    def mudar_tela(self):
        if player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            player.saindo_porta = True
            return CorredorA38()
        return None
        
class LabM5(Cenario):
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "salas", "LabM5.png")
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        #Definimos o tamanho desejado da imagem da bolsa
        tamanho = (140, 140) 
        
        pos_x = 1000 
        pos_y = 380 
        self.bolsa_objeto = pygame.Rect(pos_x, pos_y, tamanho[0], tamanho[1]) 
        
        caminho_img = os.path.join(os.path.dirname(__file__), "data", "images", "items", "Bolsa_maíra.png")
        self.imagem_bolsa = pygame.image.load(caminho_img).convert_alpha()
        
        self.imagem_bolsa = pygame.transform.scale(self.imagem_bolsa, tamanho)
            
        player.ultima_direcao = "direita"
        
    def desenhar(self):
        super().desenhar()

        self.tela.blit(self.imagem_bolsa, (self.bolsa_objeto.x, self.bolsa_objeto.y))
        self.player_andar.draw(self.tela)
        
        if player.saindo_porta:
            player.rect.centerx = self.bolsa_objeto.centerx
            player.rect.y = 295 
            player.saindo_porta = False

        #Colisão para abrir
        if player.rect.colliderect(self.bolsa_objeto):
            self.tela.blit(hud.abrir_bolsa, (60, 20)) 
            self.tela.blit(hud.tecla_e, (20, 20))
            
            if self.teclas[pygame.K_e]:
                return InteriorBolsa()
            
        return self.mudar_tela()
        
    def mudar_tela(self):
        if player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            player.saindo_porta = True
            return CorredorM5()
        elif player.ultima_direcao == "direita" and player.rect.right >= LARGURA:
            return None

class InteriorBolsa(Cenario):
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "dentro_bolsa.png")
        info_tela = pygame.display.get_surface().get_size()
        self.image = pygame.image.load(self.caminho).convert()
        self.image = pygame.transform.scale(self.image, info_tela)

        if not chave_m1.coletado:
            self.items.add(chave_m1)

        if not fita2.coletado:
            self.items.add(fita2)

    def desenhar(self):
        self.teclas = pygame.key.get_pressed()

        self.tela.blit(self.image, (0, 0))
        self.items.draw(self.tela)
        self.tela.blit(inventario.image, (300,610))
        inventario.update()
        
        #HUD (Mensagens)
        self.tela.blit(hud.font.render("Interior da bolsa", True, (255, 255, 255)), (20, 20))
        self.tela.blit(hud.tecla_p, (20, 60))
        self.tela.blit(hud.pegar, (60, 60))
        self.tela.blit(hud.tecla_esc, (20, 100))
        self.tela.blit(hud.font.render("Pressione 'Esc' para sair", True, (255, 255, 255)), (70, 100))
        
        for i, item_inv in enumerate(lista_itens):
            nova_pos_x = inventario.posicao_base_x + (i * inventario.espacamento_entre_itens)
            self.tela.blit(item_inv.image, (nova_pos_x, inventario.posicao_y))

        nomes_coletados = []
        for item in self.items:
            if self.teclas[pygame.K_p]:
                item.image = pygame.transform.scale(item.image, (25, 40))
                pegar_item_som.play()
                lista_itens.append(item)
                item.coletado = True
                nomes_coletados.append(item.nome_item)
                for indice, item_inv in enumerate(lista_itens):
                    nova_posicao_x = inventario.posicao_base_x + (indice * inventario.espacamento_entre_itens)
                    item_inv.rect.topleft = (nova_posicao_x, inventario.posicao_y)
                    self.items.remove(item)
                    
        if nomes_coletados:
            todos_nomes = " e ".join(nomes_coletados) #o join separa os nomes colocando, nesse caso, o 'e' entre eles
            self.mensagem_texto = f"Voce coletou: {todos_nomes}"
            self.exibir_mensagem = True
            self.mensagem_timer = pygame.time.get_ticks()
            
        if self.exibir_mensagem:
            agora = pygame.time.get_ticks()
            if agora - self.mensagem_timer < self.duracao_mensagem:
                texto_surf = hud.font.render(self.mensagem_texto, True, (255, 255, 255))
                largura_texto = texto_surf.get_width()
                self.tela.blit(texto_surf, (LARGURA//2 - largura_texto//2, 100))
            else:
                self.exibir_mensagem = False

        return self.mudar_tela()

    def mudar_tela(self):
        if self.teclas[pygame.K_ESCAPE]:
            player.saindo_porta = True
            return LabM5()
        return None
    
class LabM1(Cenario):
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "salas", "LabM1.png")
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        self.character = hugo
        if self.character not in self.characters:
            self.characters.add(self.character)
            
        if not chave_m1.coletado:
            self.items.add(chave_m1)
            
        player.ultima_direcao = "esquerda"
        player.animacao_atual = player.andar_esquerda
        player.image = player.andar_esquerda[int(player.atual)]
        player.image = pygame.transform.scale(player.image, (PLAYER_LARGURA, PLAYER_ALTURA))
        
        self.definir_dialogo_atual()

    def definir_dialogo_atual(self):
        from characters.dialogue import Dialogo_Hugo1, Dialogo_Hugo2, Dialogo_Hugo_Espera
        global estado_missao_hugo
        
        if estado_missao_hugo == "inicio":
            self.dialogo = Dialogo_Hugo1(cenario=self)
        elif estado_missao_hugo == "buscando_provas":
            if provas_hugo in lista_itens:
                self.dialogo = Dialogo_Hugo2(cenario=self)
            else:
                self.dialogo = Dialogo_Hugo_Espera(cenario=self)
        else:
            self.dialogo = Dialogo_Hugo2(cenario=self)

    def desenhar(self):
        global estado_missao_hugo
        self.teclas = pygame.key.get_pressed()
        
        super().desenhar()

        alcance = self.character.rect.inflate(300, 300)
        
        if player.rect.colliderect(alcance):
            if self.teclas[pygame.K_i]:
                pygame.time.delay(150) 
                
                self.fundo_salvo = self.tela.copy()
                self.dialogo.run()
                
                #LÓGICA DE ENTREGA DA CHAVE
                if estado_missao_hugo == "buscando_provas" and provas_hugo in lista_itens:
                    lista_itens.remove(provas_hugo)
                    
                    chave_a38.image = pygame.transform.scale(chave_a38.image, (25, 40))
                    chave_a38.coletado = True
                    lista_itens.append(chave_a38)
                    
                    self.mensagem_texto = f"Voce recebeu: {chave_a38.nome_item}"
                    self.exibir_mensagem = True
                    self.mensagem_timer = pygame.time.get_ticks()
                    
                    for indice, item_inv in enumerate(lista_itens):
                        nova_x = inventario.posicao_base_x + (indice * inventario.espacamento_entre_itens)
                        item_inv.rect.topleft = (nova_x, inventario.posicao_y)
                    
                    # Muda o estado para o Hugo não dar a chave de novo
                    estado_missao_hugo = "finalizado"
                
                # Se for a primeira vez que falou com ele, inicia a busca
                elif estado_missao_hugo == "inicio":
                    estado_missao_hugo = "buscando_provas"

                self.definir_dialogo_atual()
                pygame.event.clear()

        return self.mudar_tela()

    def mudar_tela(self):
        # Garante que a colisão de saída seja verificada
        if player.ultima_direcao == "direita" and player.rect.right >= LARGURA:
            player.saindo_porta = True
            return CorredorM1()
        elif player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            return None
        
class LabM6(Cenario):
    
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "salas", "LabM6.png")
            
        tamanho = (110, 120) 
        
        pos_x = 940 
        pos_y = 470 
        self.mochila_objeto = pygame.Rect(pos_x, pos_y, tamanho[0], tamanho[1]) 
        
        caminho_img = os.path.join(os.path.dirname(__file__), "data", "images", "items", "mochila.png")
        self.imagem_mochila = pygame.image.load(caminho_img).convert_alpha()
        
        self.imagem_mochila = pygame.transform.scale(self.imagem_mochila, tamanho)
            
        player.ultima_direcao = "direita"
        player.animacao_atual = player.andar_direita
        player.image = player.andar_direita[int(player.atual)]
        player.image = pygame.transform.scale(player.image, (PLAYER_LARGURA, PLAYER_ALTURA))
        
    def desenhar(self):
        super().desenhar()

        self.tela.blit(self.imagem_mochila, (self.mochila_objeto.x, self.mochila_objeto.y))
        self.player_andar.draw(self.tela)
        
        if player.saindo_porta:
            player.rect.centerx = self.mochila_objeto.centerx
            player.rect.y = 295 
            player.saindo_porta = False

        #Colisão para abrir
        if player.rect.colliderect(self.mochila_objeto):
            self.tela.blit(hud.abrir_bolsa, (60, 20)) 
            self.tela.blit(hud.tecla_e, (20, 20))
            
            if self.teclas[pygame.K_e]:
                return InteriorMochila()
            
        return self.mudar_tela()
        
    def mudar_tela(self):
        if player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            return CorredorM6()
        elif player.ultima_direcao == "direita" and player.rect.right >= LARGURA:
            return None
        
class InteriorMochila(Cenario):
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "dentro_mochila.png")
        info_tela = pygame.display.get_surface().get_size()
        self.image = pygame.image.load(self.caminho).convert()
        self.image = pygame.transform.scale(self.image, info_tela)

        if not provas_hugo.coletado:
            self.items.add(provas_hugo)

    def desenhar(self):
        self.teclas = pygame.key.get_pressed()

        self.tela.blit(self.image, (0, 0))
        self.items.draw(self.tela)
        self.tela.blit(inventario.image, (300,610))
        inventario.update()
        
        #HUD (Mensagens)
        self.tela.blit(hud.font.render("Interior da mochila", True, (255, 255, 255)), (20, 20))
        self.tela.blit(hud.tecla_p, (20, 60))
        self.tela.blit(hud.pegar, (60, 60))
        self.tela.blit(hud.tecla_esc, (20, 100))
        self.tela.blit(hud.font.render("Pressione 'Esc' para sair", True, (255, 255, 255)), (70, 100))
        
        for i, item_inv in enumerate(lista_itens):
            nova_pos_x = inventario.posicao_base_x + (i * inventario.espacamento_entre_itens)
            self.tela.blit(item_inv.image, (nova_pos_x, inventario.posicao_y))

        for item in self.items:
            if self.teclas[pygame.K_p]:
                item.image = pygame.transform.scale(item.image, (25, 40))
                pegar_item_som.play()
                lista_itens.append(item)
                item.coletado = True
                self.mensagem_texto = f"Voce coletou: {item.nome_item}"
                self.exibir_mensagem = True
                self.mensagem_timer = pygame.time.get_ticks()
                for indice, item_inv in enumerate(lista_itens):
                    nova_posicao_x = inventario.posicao_base_x + (indice * inventario.espacamento_entre_itens)
                    item_inv.rect.topleft = (nova_posicao_x, inventario.posicao_y)
                    self.items.remove(item)
            
        if self.exibir_mensagem:
            agora = pygame.time.get_ticks()
            if agora - self.mensagem_timer < self.duracao_mensagem:
                texto_surf = hud.font.render(self.mensagem_texto, True, (255, 255, 255))
                largura_texto = texto_surf.get_width()
                self.tela.blit(texto_surf, (LARGURA//2 - largura_texto//2, 100))
            else:
                self.exibir_mensagem = False

        return self.mudar_tela()

    def mudar_tela(self):
        if self.teclas[pygame.K_ESCAPE]:
            player.saindo_porta = True
            return LabM6()
        return None

class COAPAC(Cenario):

    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "salas", "COAPAC.png")
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        if not chave.coletado:
            self.items.add(chave)
            
        if not tesoura.coletado:
            self.items.add(tesoura)
            
        tamanho = (80, 70) 
        
        pos_x = 600 
        pos_y = 400 
        self.porta_lapis_objeto = pygame.Rect(pos_x, pos_y, tamanho[0], tamanho[1]) 
        
        caminho_img = os.path.join(os.path.dirname(__file__), "data", "images", "items", "porta-lapis.png")
        self.imagem_porta_lapis = pygame.image.load(caminho_img).convert_alpha()
        
        self.imagem_porta_lapis = pygame.transform.scale(self.imagem_porta_lapis, tamanho)
            
        player.ultima_direcao = "direita"
        player.animacao_atual = player.andar_direita
        player.image = player.andar_direita[int(player.atual)]
        player.image = pygame.transform.scale(player.image, (PLAYER_LARGURA, PLAYER_ALTURA))
        
    def desenhar(self):
        super().desenhar()
        self.tela.blit(self.imagem_porta_lapis, (self.porta_lapis_objeto.x, self.porta_lapis_objeto.y))
        self.player_andar.draw(self.tela)
        return self.mudar_tela()

    def mudar_tela(self):
        if player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            player.saindo_porta = True
            return CorredorCOAPAC3()
        elif player.ultima_direcao == "direita" and player.rect.right >= LARGURA:
            return None


class Exterior(Cenario):

    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "corredores", "exterior.png")
        player.ultima_direcao = "esquerda"
        player.animacao_atual = player.andar_esquerda
        player.image = player.andar_esquerda[int(player.atual)]
        player.image = pygame.transform.scale(player.image, (PLAYER_LARGURA, PLAYER_ALTURA))


    def mudar_tela(self):
        if player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            return Arquibancadas()
        elif player.ultima_direcao == "direita" and player.rect.right >= LARGURA:
            return CorredorNapne()

class Campo(Cenario):

    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "corredores", "campo.png")
        player.ultima_direcao = "esquerda"
        player.animacao_atual = player.andar_esquerda
        player.image = player.andar_esquerda[int(player.atual)]
        player.image = pygame.transform.scale(player.image, (PLAYER_LARGURA, PLAYER_ALTURA))

        if seta2.clicado:
            seta2.clicado = False
            player.ultima_direcao = "direita"
            player.animacao_atual = player.andar_direita
            player.image = player.andar_direita[int(player.atual)]
            player.image = pygame.transform.scale(player.image, (PLAYER_LARGURA, PLAYER_ALTURA))

    def mudar_tela(self):
        if player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            player.voltando_seta = True
            return Arquibancadas2()
        elif player.ultima_direcao == "direita" and player.rect.right >= LARGURA:
            return None
