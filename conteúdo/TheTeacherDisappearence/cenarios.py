import pygame
from ui.hud import Inventario, Hud, Seta
from items.keys import Key1, Key2, Key3, Key4, CartaoAcesso, Fita, Fita2, Carrinho, PéDeCabra, Provas, Tesoura, Cartaz
from characters.base import Hugo, Zelador, Coordenador, Zelador, Maíra, Aluno
from ui.sounds import Som, Musica
import os
from main import player
from characters.dialogue import Dialogo_Zelador, Dialogo_Coordenador, Dialogo_Maíra, Dialogo_Aluno
import sys

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
abrir_porta_som = Som("porta_abrindo.mp3")
usar_tesoura = Som("som_tesoura.mp3")
policia = Som("police-siren.mp3")

#itens
chave = None
chave_m5 = None
chave_coapac = None
chave_m1 = None
chave_a38 = None # Posição 0,0 porque ela começa com o Hugo
cartao_acesso = None
fita = None
fita2 = None
fita3 = None
carrinho = None
pe_de_cabra = None
provas_hugo = None
cartaz = None
tesoura = None

lista_itens = []

#cores
WHITE = (255, 255, 255)

#personagens
hugo = None
zelador = None
coordenador = None
maira = None
aluno = None

# estados: "inicio", "buscando_provas", "finalizado"
estado_missao_hugo = None

sair_sala = False

#alarme
alarme_ativo = None
tempo_inicio_alarme = None
duracao_alarme = None 
som_alarme = None

#alarme final
alarme_ativo_final = None
tempo_inicio_alarme_final = None
duracao_alarme_final = None 
som_alarme_final = None
alarme_final_disparado = None
explodindo = None

fios_cortados = None
dialogo_aluno_acabou = None
dialogo_maira_acabou = None

retornar_menu = False

def definir():
    global chave, chave_m5, chave_coapac, chave_m1, chave_a38, cartao_acesso, fita, fita2, fita3, carrinho, pe_de_cabra, provas_hugo, cartaz, tesoura
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
    pe_de_cabra = PéDeCabra(510, 490)
    provas_hugo = Provas(LARGURA//2 - 140, ALTURA//2 - 130)
    cartaz = Cartaz(LARGURA//2 - 140, ALTURA//2)
    tesoura = Tesoura(620, 390)
    
    global hugo, zelador, coordenador, maira, aluno
    #personagens
    hugo = Hugo()
    zelador = Zelador()
    coordenador = Coordenador()
    maira = Maíra()
    aluno = Aluno()
    
    global lista_itens
    lista_itens.clear()
    
    # estados: "inicio", "buscando_provas", "finalizado"
    global estado_missao_hugo
    estado_missao_hugo = "inicio"

    global fios_cortados, dialogo_aluno_acabou, dialogo_maira_acabou
    fios_cortados = False
    dialogo_aluno_acabou = False
    dialogo_maira_acabou = False
    
    global sair_sala
    sair_sala = False

    global alarme_ativo, tempo_inicio_alarme, duracao_alarme, som_alarme, alarme_ativo_final, tempo_inicio_alarme_final, duracao_alarme_final, som_alarme_final, alarme_final_disparado, explodindo
    #alarme
    alarme_ativo = False
    tempo_inicio_alarme = 0
    duracao_alarme = 15000 
    som_alarme = Som("alarm.ogg")

    #alarme final
    alarme_ativo_final = False
    tempo_inicio_alarme_final = 0
    duracao_alarme_final = 14000 
    som_alarme_final = Som("alarm.ogg")
    alarme_final_disparado = False
    explodindo = False

class Button():
    def __init__(self, image_path, hover_path, pos, callback):
        self.pos = pos
        self.callback = callback
        
        self.image_normal = pygame.image.load(image_path).convert_alpha()
        self.image_hover = pygame.image.load(hover_path).convert_alpha()
        
        self.image_normal = pygame.transform.scale(self.image_normal, (300, 100))
        self.image_hover = pygame.transform.scale(self.image_hover, (300, 100))
            
        self.rect = self.image_normal.get_rect(center=self.pos)

    def draw(self, screen, mouse_pos):
        # Seleciona qual imagem desenhar com base na colisão do mouse
        if self.rect.collidepoint(mouse_pos):
            self.image_atual = self.image_hover
        else:
            self.image_atual = self.image_normal
            
        screen.blit(self.image_atual, self.rect)

    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.callback()

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
        self.dialogo2 = None
       
        self.item_necessario = None
        
        #mensagem de coleta de item
        self.mensagem_texto = ""
        self.mensagem_timer = 0
        self.exibir_mensagem = False
        self.duracao_mensagem = 3000
        
        self.tempo_inicial = pygame.time.get_ticks()
        self.tempo_espera = 5000
        
        #verificar se o diálogo acabou
        self.dialogo_acabou = False
        
        #fazer checagem de cliques
        self.mouse_pressionado_anteriormente = False
       
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
                    self.mensagem_texto = f"Você coletou: {item.nome_item}"
                    self.exibir_mensagem = True
                    self.mensagem_timer = pygame.time.get_ticks()
                    for indice, item_inv in enumerate(lista_itens):
                        nova_posicao_x = inventario.posicao_base_x + (indice * inventario.espacamento_entre_itens)
                        item_inv.rect.topleft = (nova_posicao_x, inventario.posicao_y)
                        self.tela.blit(item_inv.image, item_inv.rect.topleft)
       
        #colisão com a porta para entrar em salas/laboratórios
        if player.rect.colliderect(self.porta):
            if self.item_necessario in lista_itens and self.trancada and "CorredorA28.png" not in self.caminho:
                self.tela.blit(hud.destrancar_porta, (60, 20))
                self.tela.blit(hud.tecla_e, (20, 20))
            elif self.trancada and "CorredorA28.png" not in self.caminho:
                self.tela.blit(hud.cadeado, (20, 20))
                self.tela.blit(hud.porta_trancada, (60, 20))
            elif not self.trancada and  "CorredorA28.png" not in self.caminho:
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
                            if item_usado != pe_de_cabra:
                                lista_itens.remove(item_usado)
                        
                        return self.mudar_tela()
                    
        # Coloca o player na frente da porta ao sair de uma sala
        if player.saindo_porta:
            player.rect.centerx = self.porta.centerx
            player.rect.y = 295
            player.saindo_porta = False
               
               
        # Timer
        agora_timer = pygame.time.get_ticks() 
        global alarme_ativo, tempo_inicio_alarme, som_alarme, dialogo_aluno_acabou #chama as variáveis que estão fora, não criando novas dentro da classe
        if player.rect.colliderect(self.alarme):
            self.tela.blit(hud.ativar_alarme, (60,20))
            self.tela.blit(hud.tecla_e, (20, 20))
            if self.teclas[pygame.K_e]:
                if not alarme_ativo:
                    alarme_ativo = True
                    tempo_inicio_alarme = agora_timer
                    som_alarme = Musica("alarm.ogg")
                    som_alarme.play()
            
        # Timer Final        
        agora_timer_final = pygame.time.get_ticks() 
        global alarme_ativo_final, tempo_inicio_alarme_final, som_alarme_final, alarme_final_disparado #chama as variáveis que estão fora, não criando novas dentro da classe
        if dialogo_aluno_acabou and not alarme_final_disparado:
            if not alarme_ativo_final:
                alarme_ativo_final = True
                alarme_final_disparado = True
                tempo_inicio_alarme_final = agora_timer_final
                som_alarme_final = Musica("alarm.ogg")
                som_alarme_final.play()

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
                    musica = Musica("Iron wasteland.mp3")
                    musica.play()
                    
        if alarme_ativo_final:
            tempo_passado_final = agora_timer_final - tempo_inicio_alarme_final
            if tempo_passado_final < duracao_alarme_final:
                #desenha o tempo que falta para o timer terminar
                segundos_restantes = (duracao_alarme_final - tempo_passado_final) // 1000
                txt_timer = hud.font.render(f"Tempo: {segundos_restantes}s", True, (255, 0, 0))
                largura_texto = txt_timer.get_width()
                self.tela.blit(txt_timer, (LARGURA // 2 - largura_texto//2, 50))
            elif tempo_passado_final >= duracao_alarme_final and fios_cortados:
                alarme_ativo_final = False
                if som_alarme_final:
                    som_alarme_final.parar()
                    musica = Musica("Iron wasteland.mp3")
                    musica.play()
            else:
                #explosão
                global explodindo
                if not self.explodindo:
                    explodindo = True
                    self.explodindo = True
                    self.ultimo_update_exp = pygame.time.get_ticks()
                    alarme_ativo_final = False # Para o timer
                    if som_alarme_final:
                        som_alarme_final.parar()
           
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
       
        #adicionando personagens
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
                    
            elif character == coordenador:
                som_derrota = Som("defeat.mp3")
                som_derrota.play()
                self.tela.blit(character.image, character.rect) 
                alcance_interacao = character.rect
                self.fundo_salvo = self.tela.copy()
                self.dialogo.run()
                self.dialogo_acabou = True
                
            elif character == maira:
                self.tela.blit(character.image, character.rect) 
                alcance_interacao = character.rect
                
            elif character == aluno:
                self.tela.blit(character.image, character.rect)
                alcance_interacao = character.rect
                self.fundo_salvo = self.tela.copy()
                if not dialogo_aluno_acabou:
                    self.dialogo.run()
                    self.dialogo_acabou = True
                    character.kill()
                dialogo_aluno_acabou = True
                
            if character != maira and player.rect.colliderect(alcance_interacao):
                if self.teclas[pygame.K_i]:
                    self.fundo_salvo = self.tela.copy()
                    self.dialogo.run()
                    if character == zelador:
                        character.indo_embora = True
                        character.foi_embora = True
                    return None
                self.tela.blit(hud.interagir, (60,20))
                self.tela.blit(hud.tecla_i, (20, 20))
                
            elif character == maira and player.rect.colliderect(alcance_interacao) and not maira.liberta:
                if tesoura in lista_itens:
                    if self.teclas[pygame.K_e]:
                        usar_tesoura.play()
                        maira.liberta = True
                    self.tela.blit(hud.cortar, (60, 20))
                    self.tela.blit(hud.tecla_e, (20, 20))
                else:
                    self.tela.blit(hud.cortar_falha, (20, 20))
                    
            elif character == maira and player.rect.colliderect(alcance_interacao) and maira.liberta:
                if self.teclas[pygame.K_i]:
                    self.fundo_salvo = self.tela.copy()
                    global dialogo_maira_acabou
                    if not dialogo_maira_acabou:
                        self.dialogo2.run()
                        self.dialogo_acabou = True
                        dialogo_maira_acabou = True
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
                
        if cartaz in lista_itens:
            player.velocidade = 15 #aumenta
            
    # método para os paineis
    def desenhar_timer_final(self):
        global alarme_ativo_final, tempo_inicio_alarme_final, duracao_alarme_final, explodindo, alarme_final_disparado
        
        if alarme_final_disparado:
            agora = pygame.time.get_ticks()
            tempo_passado = agora - tempo_inicio_alarme_final
            
            # verifica a explosão para aparecer assim que o tempo acabar 
            if tempo_passado >= duracao_alarme_final and not fios_cortados:
                if not explodindo:
                    explodindo = True
                    if som_alarme_final:
                        som_alarme_final.parar()

            if not fios_cortados:
                segundos_restantes = max(0, (duracao_alarme_final - tempo_passado) // 1000)
                txt_timer = hud.font.render(f"Tempo: {segundos_restantes}s", True, (255, 0, 0))
                largura_texto = txt_timer.get_width()
                self.tela.blit(txt_timer, (LARGURA // 2 - largura_texto // 2, 50))
            else:
                alarme_ativo_final = False
                if som_alarme_final:
                    som_alarme_final.parar()
                    musica = Musica("Iron wasteland.mp3")
                    musica.play()
                txt_timer = hud.font.render(f"Você impediu a explosão!", True, (255, 0, 0))
                largura_texto = txt_timer.get_width()
                self.tela.blit(txt_timer, (LARGURA // 2 - largura_texto // 2, 50))
       
    def mudar_tela(self):
        if self.entrar_sala:
            self.entrar_sala = False
            return None
        elif player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            return None
        elif player.ultima_direcao == "direita" and player.rect.right >= LARGURA:
            return None
  
  
# CENÁRIOS

# CORREDORES

# CORREDORES SALAS DE AULA

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
        if self.entrar_sala:
            self.entrar_sala = False
            return Grêmio()
        elif player.ultima_direcao == "esquerda" and player.rect.left <= 0:
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
        
        
# CORREDORES COAPAC
        
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
       
        self.alarme = pygame.Rect(1200, 200, 100, 340)
        
        self.coordenador_na_sala = True
            
        self.item_necessario = chave_coapac
        self.trancada = not chave_coapac.utilizado
            
        self.porta = pygame.Rect(920, 200, 100, 340)
    
    def mudar_tela(self):
        if self.entrar_sala:
            self.entrar_sala = False
            return COAPAC()

        elif player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            return CorredorCOAPAC2()
        elif player.ultima_direcao == "direita" and player.rect.right >= LARGURA:
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
            
        #if cartao_acesso not in self.items:
        #    self.items.add(cartao_acesso)
            
        if player.voltando_seta:
            player.rect.left = 495
            player.voltando_seta = False
            
    def mudar_tela(self):
        if self.entrar_sala:
            self.entrar_sala = False
            return Diretoria()
        if player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            return CorredorCOAPAC3()
        elif player.ultima_direcao == "direita" and player.rect.x >= LARGURA - PLAYER_LARGURA - 300:
            return None
        
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
            
        if player.saindo_porta:
            player.ultima_direcao = "esquerda"
            player.animacao_atual = player.andar_esquerda
            player.image = player.andar_esquerda[int(player.atual)]
            player.image = pygame.transform.scale(player.image, (PLAYER_LARGURA, PLAYER_ALTURA))
            player.saindo_porta = False

    def mudar_tela(self):
        if self.entrar_sala:
            self.entrar_sala = True
            return Exterior()
        elif player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            player.voltando_seta = True
            return CorredorCOAPAC4()
        elif player.ultima_direcao == "direita" and player.rect.right >= LARGURA:
            return None        
        
        
# CORREDORES LABORATÓRIOS
        
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
        elif player.ultima_direcao == "direita" and player.rect.x >= LARGURA - PLAYER_LARGURA:
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
        

# SALAS DE AULA

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
        
# OUTRAS SALAS        

class Diretoria(Cenario):

    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "salas", "Diretoria.png")
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        self.computador = pygame.Rect(70, 360, 60, 60)
        if not pe_de_cabra.coletado:
            self.items.add(pe_de_cabra)
            
        player.ultima_direcao = "esquerda"
        player.animacao_atual = player.andar_esquerda
        player.image = player.andar_esquerda[int(player.atual)]
        player.image = pygame.transform.scale(player.image, (PLAYER_LARGURA, PLAYER_ALTURA))
        
    def desenhar(self):
        super().desenhar()
        self.player_andar.draw(self.tela)
        
        if player.saindo_item:
            player.rect.left = 250
            player.rect.y = 295 
            player.saindo_item = False
            
        if player.rect.colliderect(self.computador):
            self.tela.blit(hud.acessar_computador, (60, 20)) 
            self.tela.blit(hud.tecla_e, (20, 20))
            
            if self.teclas[pygame.K_e]:
                return Computador()
            
        return self.mudar_tela()

    def mudar_tela(self):
        if player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            return None
        elif player.ultima_direcao == "direita" and player.rect.x >= LARGURA - PLAYER_LARGURA:
            player.saindo_porta = True
            return CorredorCOAPAC4()
        
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
        self.imagem_porta_lapis = pygame.image.load(caminho_img)
        
        self.imagem_porta_lapis = pygame.transform.scale(self.imagem_porta_lapis, tamanho)
            
        player.ultima_direcao = "direita"
        player.animacao_atual = player.andar_direita
        player.image = player.andar_direita[int(player.atual)]
        player.image = pygame.transform.scale(player.image, (PLAYER_LARGURA, PLAYER_ALTURA))
        self.dialogo = Dialogo_Coordenador(cenario=self)
        
    def desenhar(self):
        super().desenhar()
        if not alarme_ativo:
            if coordenador not in self.characters:
                self.characters.add(coordenador)
        self.tela.blit(self.imagem_porta_lapis, (self.porta_lapis_objeto.x, self.porta_lapis_objeto.y))
        self.player_andar.draw(self.tela) #corrigir problema com o porta lápis sumindo
        return self.mudar_tela()

    def mudar_tela(self):
        if self.dialogo_acabou:
            self.dialogo_acabou = False
            player.saindo_porta = True
            return CorredorA36()
        elif player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            player.saindo_porta = True
            return CorredorCOAPAC3()
        elif player.ultima_direcao == "direita" and player.rect.right >= LARGURA:
            return None
        
class Grêmio(Cenario):
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "salas", "Grêmio.png")
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            
        self.armario = pygame.Rect(230, 200, 100, 200)
        player.ultima_direcao = "esquerda"
        player.animacao_atual = player.andar_esquerda
        player.image = player.andar_esquerda[int(player.atual)]
        player.image = pygame.transform.scale(player.image, (PLAYER_LARGURA, PLAYER_ALTURA))

    def desenhar(self):
        super().desenhar()
        
        if player.saindo_item:
            player.rect.left = 250
            player.rect.y = 295 
            player.saindo_item = False
            
        if player.rect.colliderect(self.armario):
            if self.teclas[pygame.K_e]:
                return InteriorArmario()
            
        return self.mudar_tela()

    def mudar_tela(self):
        if player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            return None
        elif player.ultima_direcao == "direita" and player.rect.x >= LARGURA - PLAYER_LARGURA:
            player.saindo_porta = True
            return CorredorA30()
        
        
# LABORATÓRIOS        

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
        
        
# INTERIORES DE BOLSAS

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
    
class InteriorArmario(Cenario):
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "interior_armário.png") 
        info_tela = pygame.display.get_surface().get_size()
        self.image = pygame.image.load(self.caminho).convert()
        self.image = pygame.transform.scale(self.image, info_tela)
        
        if cartaz not in self.items:
            self.items.add(cartaz)

    def desenhar(self):
        self.teclas = pygame.key.get_pressed()

        self.tela.blit(self.image, (0, 0))
        self.items.draw(self.tela)
        self.tela.blit(inventario.image, (300,610))
        inventario.update()
        
        #HUD (Mensagens)
        self.tela.blit(hud.font.render("Interior do armário", True, (255, 255, 255)), (20, 20))
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
            player.saindo_item = True
            return Grêmio()
        return None
    
class PainelComFios(Cenario):
    
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "painel_com_fios.png")
        info_tela = pygame.display.get_surface().get_size()
        self.image = pygame.image.load(self.caminho).convert()
        self.image = pygame.transform.scale(self.image, info_tela)

    def desenhar(self):
        self.teclas = pygame.key.get_pressed()

        self.tela.blit(self.image, (0, 0))
        self.items.draw(self.tela)
        self.tela.blit(inventario.image, (300,610))
        inventario.update()
        
        #HUD (Mensagens)
        self.tela.blit(hud.font.render("Interior do painel", True, (255, 255, 255)), (20, 20))
        self.tela.blit(hud.tecla_esc, (20, 100))
        self.tela.blit(hud.font.render("Pressione 'Esc' para sair", True, (255, 255, 255)), (70, 100))
        self.tela.blit(hud.tecla_e, (20, 60))
        self.tela.blit(hud.font.render("Pressione 'E' para cortar os fios", True, (255, 255, 255)), (60, 60))
        
        for i, item_inv in enumerate(lista_itens):
            nova_pos_x = inventario.posicao_base_x + (i * inventario.espacamento_entre_itens)
            self.tela.blit(item_inv.image, (nova_pos_x, inventario.posicao_y))
            
        if explodindo:
            return Subterraneo()
            
        self.desenhar_timer_final()

        return self.mudar_tela()

    def mudar_tela(self):
        global fios_cortados
        if self.teclas[pygame.K_ESCAPE]:
            player.saindo_item = True
            return Subterraneo()
        if self.teclas[pygame.K_e]:
            if tesoura in lista_itens:
                fios_cortados = True
                usar_tesoura.play()
                return PainelSemFios()
        return None

class PainelSemFios(Cenario):
    
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "painel_sem_fios.png")
        info_tela = pygame.display.get_surface().get_size()
        self.image = pygame.image.load(self.caminho).convert()
        self.image = pygame.transform.scale(self.image, info_tela)

    def desenhar(self):
        self.teclas = pygame.key.get_pressed()

        self.tela.blit(self.image, (0, 0))
        self.items.draw(self.tela)
        self.tela.blit(inventario.image, (300,610))
        inventario.update()
        
        #HUD (Mensagens)
        self.tela.blit(hud.font.render("Interior do painel", True, (255, 255, 255)), (20, 20))
        self.tela.blit(hud.tecla_esc, (20, 60))
        self.tela.blit(hud.font.render("Pressione 'Esc' para sair", True, (255, 255, 255)), (70, 60))
        self.tela.blit(hud.tecla_e, (20, 60))
        self.tela.blit(hud.font.render("Pressione 'E' para cortar os fios", True, (255, 255, 255)), (60, 60))
        
        for i, item_inv in enumerate(lista_itens):
            nova_pos_x = inventario.posicao_base_x + (i * inventario.espacamento_entre_itens)
            self.tela.blit(item_inv.image, (nova_pos_x, inventario.posicao_y))
            
        self.desenhar_timer_final()
        
        if explodindo:
            return Subterraneo()   

        return self.mudar_tela()

    def mudar_tela(self):
        global fios_cortados
        if explodindo:
            return Subterraneo()
        if self.teclas[pygame.K_ESCAPE]:
            player.saindo_item = True
            return Subterraneo()
        return None
    
# EXTERIOR

class Exterior(Cenario):

    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "corredores", "exterior.png")
        
        if player.saindo_porta:
            player.ultima_direcao = "direita"
            player.animacao_atual = player.andar_direita
            player.image = player.andar_direita[int(player.atual)]
            player.image = pygame.transform.scale(player.image, (PLAYER_LARGURA, PLAYER_ALTURA))
            player.saindo_porta = False
        else:
            player.ultima_direcao = "esquerda"
            player.animacao_atual = player.andar_esquerda
            player.image = player.andar_esquerda[int(player.atual)]
            player.image = pygame.transform.scale(player.image, (PLAYER_LARGURA, PLAYER_ALTURA))

    def mudar_tela(self):
        if player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            player.saindo_porta = True
            return Arquibancadas()
        elif player.ultima_direcao == "direita" and player.rect.right >= LARGURA:
            player.saindo_porta = True
            return CorredorNapne()

class Arquibancadas(Cenario):
    
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "Arquibancada.png")
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        
        if player.saindo_porta:
            player.ultima_direcao = "esquerda"
            player.animacao_atual = player.andar_esquerda
            player.image = player.andar_esquerda[int(player.atual)]
            player.image = pygame.transform.scale(player.image, (PLAYER_LARGURA, PLAYER_ALTURA))
            player.saindo_porta = False
            
    def mudar_tela(self):
        if player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            return Arquibancadas2()
        elif player.ultima_direcao == "direita" and player.rect.x >= LARGURA - PLAYER_LARGURA - 300:
            player.saindo_porta = True
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
        
#adicionar porta (alçapão)
class Campo(Cenario):

    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "corredores", "campo.png") 
        player.ultima_direcao = "esquerda"
        player.animacao_atual = player.andar_esquerda
        player.image = player.andar_esquerda[int(player.atual)]
        player.image = pygame.transform.scale(player.image, (PLAYER_LARGURA, PLAYER_ALTURA))
        self.porta = pygame.Rect(950,200,20,340)
        
        #apenas para testes
        #if tesoura not in self.items:
        #    self.items.add(tesoura)
            
        #if pe_de_cabra not in self.items:
        #    self.items.add(pe_de_cabra)
            
        if seta2.clicado:
            seta2.clicado = False
            player.ultima_direcao = "direita"
            player.animacao_atual = player.andar_direita
            player.image = player.andar_direita[int(player.atual)]
            player.image = pygame.transform.scale(player.image, (PLAYER_LARGURA, PLAYER_ALTURA))

    def mudar_tela(self):
        if self.entrar_sala:
            self.entrar_sala = False
            return Subterraneo()
        elif player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            player.voltando_seta = True
            return Arquibancadas2()
        elif player.ultima_direcao == "direita" and player.rect.right >= LARGURA:
            return None
        
# SUBTERRÂNEO
        
class Subterraneo(Cenario):

    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "salas", "Subterrâneo.png") 
        
        player.ultima_direcao = "esquerda"
        player.animacao_atual = player.andar_esquerda
        player.image = player.andar_esquerda[int(player.atual)]
        player.image = pygame.transform.scale(player.image, (PLAYER_LARGURA, PLAYER_ALTURA))
        
        self.painel = pygame.Rect(270, 300, 100, 200)
        
        if player.saindo_porta:
            player.rect.centerx = self.painel.centerx
            player.rect.y = 295 
            player.saindo_porta = False
        
        if maira not in self.characters:
            self.characters.add(maira)
        
        global dialogo_aluno_acabou
        if not dialogo_aluno_acabou:
            if aluno not in self.characters:
                self.characters.add(aluno)
            self.dialogo = Dialogo_Aluno(cenario=self)
            
        
        global dialogo_maira_acabou
        if not dialogo_maira_acabou:
            self.dialogo2 = Dialogo_Maíra(cenario=self)

        # Aumentar tamanho da explosão
        fator_escala = 3
        fator_escala2 = 4.5
        nova_largura = int(LARGURA * fator_escala)
        nova_altura = int(ALTURA * fator_escala2)
    
        # Variáveis da Explosão
        self.explodindo = False
        self.frame_explosao = 0
        self.lista_frames = []
        self.ultimo_update_exp = 0
        
        for i in range(1, 6):
            img = pygame.image.load(os.path.join(os.path.dirname(__file__), "data", "images", "explosão", f"Nuclear_explosion{i}.png"))
            self.lista_frames.append(pygame.transform.scale(img, (nova_largura, nova_altura)))
        
    def desenhar(self):
        super().desenhar() #adicionar todas as funcionalidades restantes
        
        if player.saindo_item:
            player.rect.centerx = self.painel.centerx
            player.rect.y = 295 
            player.saindo_item = False
            
        if player.rect.colliderect(self.painel):
            self.tela.blit(hud.acessar_painel, (60, 20)) 
            self.tela.blit(hud.tecla_e, (20, 20))
            
            global fios_cortados
            if self.teclas[pygame.K_e]:
                if pe_de_cabra in lista_itens:
                    if fios_cortados:
                        return PainelSemFios() 
                    else:
                        return PainelComFios()
                return None   
            
        if self.explodindo:
            agora = pygame.time.get_ticks()
            
            img_atual = self.lista_frames[self.frame_explosao]
            pos_x = (LARGURA // 2) - (img_atual.get_width() // 2)
            pos_y = (ALTURA // 2) - (img_atual.get_height() // 2 - 50)
            self.tela.blit(img_atual, (pos_x, pos_y))
            
            # Controle de tempo da animação
            if agora - self.ultimo_update_exp > 100: 
                self.frame_explosao += 1
                self.ultimo_update_exp = agora
            
            if self.frame_explosao >= len(self.lista_frames):
                self.explodindo = False
                return IfExplodindo()
            
        return self.mudar_tela()
                
            
        #adicionar funcionalidade do tempo para realizar as ações

    def mudar_tela(self):
        global dialogo_maira_acabou
        
        if dialogo_maira_acabou: 
            return Prisão()
            
        if player.ultima_direcao == "esquerda" and player.rect.left <= 0:
            return None
        elif player.ultima_direcao == "direita" and player.rect.right >= LARGURA:
            return None
            
        return None

class Prisão(Cenario):
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images",  "Prisão.png") 
        self.tempo_inicial = pygame.time.get_ticks()
        self.exibir_botao = False
        self.delay_botao = 4000 
        info_tela = pygame.display.get_surface().get_size()
        self.image = pygame.image.load(self.caminho).convert()
        self.image = pygame.transform.scale(self.image, info_tela)
        self.clicou_no_frame_anterior = False
        
        policia.play()
        
        mid_x = LARGURA // 2
        mid_y = ALTURA // 2 + 250
        
        img_btn1 = os.path.join(os.path.dirname(__file__), "data", "images", "botões", "botão_retry.png")
        img_hover1 = os.path.join(os.path.dirname(__file__), "data", "images", "botões", "botão_retry_hover.png")
        img_btn2 = os.path.join(os.path.dirname(__file__), "data", "images", "botões", "botão_exit.png")
        img_hover2 = os.path.join(os.path.dirname(__file__), "data", "images", "botões", "botão_exit_hover.png")

        self.btn_jogar = Button(img_btn1, img_hover1, (mid_x - 200, mid_y), self.clicou_jogar)
        self.btn_sair = Button(img_btn2, img_hover2, (mid_x + 200, mid_y), self.clicou_sair)
        self.foi_clicado = False
        self.foi_clicado_sair = False

    def clicou_jogar(self):
        self.foi_clicado = True
    
    def clicou_sair(self):
        print("Saindo do jogo...")
        pygame.quit()
        sys.exit()

    def desenhar(self):
        self.tela.blit(self.image, (0, 0))
        agora = pygame.time.get_ticks()
        mouse_pos = pygame.mouse.get_pos()
        
        texto = hud.font.render("Alguns dias depois, na prisão...", True, (255, 255, 255))
        self.tela.blit(texto, (20, 20))
        
        if agora - self.tempo_inicial > self.delay_botao:
            self.exibir_botao = True
            
        if self.exibir_botao:
            self.btn_jogar.draw(self.tela, mouse_pos)
            self.btn_sair.draw(self.tela, mouse_pos)
            
            clique_atual, _, _ = pygame.mouse.get_pressed()
            
            if clique_atual and not self.clicou_no_frame_anterior:
                if self.btn_jogar.rect.collidepoint(mouse_pos):
                    self.clicou_jogar()
                elif self.btn_sair.rect.collidepoint(mouse_pos):
                    self.clicou_sair()
            
            # Atualiza o estado para o próximo frame
            self.clicou_no_frame_anterior = clique_atual           
            
        # consertar ambos
        if self.foi_clicado:
            return "VOLTAR_MENU"
        
        if self.foi_clicado_sair:
            pygame.quit()
            quit()

    def mudar_tela(self):
        return None
        
class Computador(Cenario):
    
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "computador.png")
        info_tela = pygame.display.get_surface().get_size()
        self.image = pygame.image.load(self.caminho).convert()
        self.image = pygame.transform.scale(self.image, info_tela)
        self.aba = pygame.Rect(445, 45, 80, 13)

    def desenhar(self):
        self.teclas = pygame.key.get_pressed()

        self.tela.blit(self.image, (0, 0))
        self.items.draw(self.tela)
        self.tela.blit(inventario.image, (300,610))
        inventario.update()
        
        #HUD (Mensagens)
        self.tela.blit(hud.font.render("Computador da Diretoria", True, (255, 255, 255)), (20, 20))
        self.tela.blit(hud.tecla_esc, (20, 60))
        self.tela.blit(hud.font.render("Pressione 'Esc'", True, (255, 255, 255)), (70, 60))
        self.tela.blit(hud.font.render("para sair", True, (255, 255, 255)), (70, 90))
        
        for i, item_inv in enumerate(lista_itens):
            nova_pos_x = inventario.posicao_base_x + (i * inventario.espacamento_entre_itens)
            self.tela.blit(item_inv.image, (nova_pos_x, inventario.posicao_y))

        mouse_pos = pygame.mouse.get_pos()
        mouse_atualmente_pressionado = pygame.mouse.get_pressed()[0] #botão esquerdo
        
        if mouse_atualmente_pressionado and not self.mouse_pressionado_anteriormente:
            if self.aba.collidepoint(mouse_pos):
                return Computador2()
                    
        return self.mudar_tela()

    def mudar_tela(self):
        if self.teclas[pygame.K_ESCAPE]:
            player.saindo_item = True
            return Diretoria()
        return None
    
class Computador2(Cenario):
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "computador2.png")
        info_tela = pygame.display.get_surface().get_size()
        self.image = pygame.image.load(self.caminho).convert()
        self.image = pygame.transform.scale(self.image, info_tela)
        self.aba = pygame.Rect(385, 45, 80, 13)

    def desenhar(self):
        self.teclas = pygame.key.get_pressed()

        self.tela.blit(self.image, (0, 0))
        self.items.draw(self.tela)
        self.tela.blit(inventario.image, (300,610))
        inventario.update()
        
        #HUD (Mensagens)
        self.tela.blit(hud.font.render("Computador da Diretoria", True, (255, 255, 255)), (20, 20))
        self.tela.blit(hud.tecla_esc, (20, 60))
        self.tela.blit(hud.font.render("Pressione 'Esc'", True, (255, 255, 255)), (70, 60))
        self.tela.blit(hud.font.render("para sair", True, (255, 255, 255)), (70, 90))
        
        for i, item_inv in enumerate(lista_itens):
            nova_pos_x = inventario.posicao_base_x + (i * inventario.espacamento_entre_itens)
            self.tela.blit(item_inv.image, (nova_pos_x, inventario.posicao_y))
        
        mouse_pos = pygame.mouse.get_pos()
        mouse_atualmente_pressionado = pygame.mouse.get_pressed()[0]

        
        if mouse_atualmente_pressionado and not self.mouse_pressionado_anteriormente:
            if self.aba.collidepoint(mouse_pos):
                return Computador()
            

        return self.mudar_tela()

    def mudar_tela(self):
        if self.teclas[pygame.K_ESCAPE]:
            player.saindo_item = True
            return Diretoria()
        return None
    
class IfExplodindo(Cenario):
    def __init__(self):
        super().__init__()
        self.caminho = os.path.join(os.path.dirname(__file__), "data", "images", "ifrn_explosion.png")
        self.caminho_final = os.path.join(os.path.dirname(__file__), "data", "images", "Perdeu.png")  
        
        info_tela = pygame.display.get_surface().get_size()
        self.image = pygame.image.load(self.caminho).convert()
        self.image = pygame.transform.scale(self.image, info_tela)
        
        self.img_fundo_final = pygame.image.load(self.caminho_final).convert()
        self.img_fundo_final = pygame.transform.scale(self.img_fundo_final, info_tela)

        self.explodindo = False
        self.frame_explosao = 0
        self.lista_frames = []
        self.ultimo_update_exp = 0
        self.animacao_finalizada = False
        
        fator_escala = 2.5
        fator_escala2 = 3.5
        nova_largura = int(LARGURA * fator_escala)
        nova_altura = int(ALTURA * fator_escala2)
    
        for i in range(1, 10):
            img = pygame.image.load(os.path.join(os.path.dirname(__file__), "data", "images", "explosão", f"Nuclear_explosion{i}.png"))
            self.lista_frames.append(pygame.transform.scale(img, (nova_largura, nova_altura)))

        self.tempo_finalizacao = 0
        self.exibir_botao = False
        self.delay_botao = 4000 
        self.clicou_no_frame_anterior = False
        
        mid_x = LARGURA // 2
        mid_y = ALTURA // 2 + 250
        
        img_btn1 = os.path.join(os.path.dirname(__file__), "data", "images", "botões", "botão_retry.png")
        img_hover1 = os.path.join(os.path.dirname(__file__), "data", "images", "botões", "botão_retry_hover.png")
        img_btn2 = os.path.join(os.path.dirname(__file__), "data", "images", "botões", "botão_exit.png")
        img_hover2 = os.path.join(os.path.dirname(__file__), "data", "images", "botões", "botão_exit_hover.png")

        self.btn_jogar = Button(img_btn1, img_hover1, (mid_x - 200, mid_y), self.clicou_jogar)
        self.btn_sair = Button(img_btn2, img_hover2, (mid_x + 200, mid_y), self.clicou_sair)
        self.foi_clicado = False

    def clicou_jogar(self):
        self.foi_clicado = True
    
    def clicou_sair(self):
        pygame.quit()
        sys.exit()

    def desenhar(self):
        agora = pygame.time.get_ticks()
        mouse_pos = pygame.mouse.get_pos()

        if not self.animacao_finalizada:
            self.tela.blit(self.image, (0, 0))
            img_atual = self.lista_frames[self.frame_explosao]
            pos_x = (LARGURA // 2) - (img_atual.get_width() // 2)
            pos_y = (ALTURA // 2) - (img_atual.get_height() // 2 - 50)
            self.tela.blit(img_atual, (pos_x, pos_y))
            
            if agora - self.ultimo_update_exp > 100: 
                self.frame_explosao += 1
                self.ultimo_update_exp = agora
            
            if self.frame_explosao >= len(self.lista_frames):
                self.animacao_finalizada = True
                self.tempo_finalizacao = agora
        else:
            self.tela.blit(self.img_fundo_final, (0, 0))
            texto = hud.font.render("Alguns dias depois da explosão, na casa do aluno...", True, (255, 255, 255))
            self.tela.blit(texto, (20, 20))
            
            if agora - self.tempo_finalizacao > self.delay_botao:
                self.exibir_botao = True
                
            if self.exibir_botao:
                self.btn_jogar.draw(self.tela, mouse_pos)
                self.btn_sair.draw(self.tela, mouse_pos)
                
                clique_atual, _, _ = pygame.mouse.get_pressed()
                
                if clique_atual and not self.clicou_no_frame_anterior:
                    if self.btn_jogar.rect.collidepoint(mouse_pos):
                        self.clicou_jogar()
                    elif self.btn_sair.rect.collidepoint(mouse_pos):
                        self.clicou_sair()
                
                self.clicou_no_frame_anterior = clique_atual
                
        if self.foi_clicado:
            return "VOLTAR_MENU"

    def mudar_tela(self):
        return None