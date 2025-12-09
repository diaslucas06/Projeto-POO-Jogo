import pygame
import os
import sys
from ui.sounds import Musica
from player import Player
from main import Game
from cenarios import CorredorA36

LARGURA_TELA = 1280
ALTURA_TELA = 720 
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BOX = (84, 66, 33)
BORDER = (49, 38, 19)
HIGHLIGHT = (128, 0, 32)

musica = Musica("Iron wasteland.mp3")
musica.play()

pygame.init()
pygame.display.set_caption("The Teacher Disappearence")
font_start = pygame.font.Font(os.path.join(os.path.dirname(__file__), "data", "fonts", "pristina.ttf"), 56)
font = pygame.font.Font(os.path.join(os.path.dirname(__file__), "data", "fonts", "Minecraftia-Regular.ttf"), 28)
font_aviso = pygame.font.Font(os.path.join(os.path.dirname(__file__), "data", "fonts", "Minecraftia-Regular.ttf"), 20)

class Button:
    def __init__(self, text, pos, callback):
        self.text = text
        self.callback = callback
        self.default_color = WHITE
        self.highlight_color = HIGHLIGHT
        self.label = font_start.render(self.text, True, self.default_color)
        self.rect = self.label.get_rect(center=pos)

    def draw(self, surface, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            label = font_start.render(self.text, True, self.highlight_color)
        else:
            label = self.label
        surface.blit(label, self.rect)

    def check_click(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.callback()


class Menu:
    def __init__(self, screen):
        self.screen = screen
        self.fundo = pygame.image.load(os.path.join(os.path.dirname(__file__), "data", "images", "Imagem_menu.png"))
        self.fundo = pygame.transform.scale(self.fundo, (LARGURA_TELA, ALTURA_TELA))
    
        mid_x = LARGURA_TELA // 2
        start_y = ALTURA_TELA // 2 + 75
        gap = 80

        self.buttons = [ 
            Button("Iniciar Jogo", (mid_x, start_y), self.start_game),
            Button("Opções",       (mid_x, start_y + gap), self.show_options),
            Button("Sair",         (mid_x, start_y + 2*gap), self.exit_game),
        ]
        self.running = True

    def start_game(self):
        print("Iniciando o jogo...") 
        self.running = False
        História().run()

    def show_options(self):
        print("Abrindo opções...")  

    def exit_game(self):
        pygame.quit()
        sys.exit()

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for btn in self.buttons:
                        btn.check_click(mouse_pos)

            self.screen.blit(self.fundo, (0,0))
            for btn in self.buttons:
                btn.draw(self.screen, mouse_pos)

            pygame.display.flip()
            clock.tick(FPS)

class História:
    def __init__(self):
        self.screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
        self.running = True
        self.dialog_text = [
            ["Em um dia chuvoso, você entrou na biblioteca do IF", "e começou a procurar por um livro para ler, no", "entanto, não conseguia encontrar nada que", "te agradasse..."],
            ["Até que você encontrou um livro diferente, ele se", "destacava dos outros, tinha uma aparência velha", "que te chamou atenção. Sua capa era em um couro", "simples, sem muitos detalhes..."],
            ["Ao abrir o livro, você se depara com o nome da", "professora Maíra do curso de informática, que se", "encontrava desaparecida do campus há alguns", "dias."],
            ["Além disso uma matricula estava escrita", "nas informações deixadas pela professora,", "dizendo para tomar cuidado com quem", "quer que fosse esse aluno."],
            ["Agora você precisa desvendar esse misterio e","enfrentar desafios para descobrir qual o", "segredo por trás de tudo isso..."]
            ]
        self.text_view = False
        self.y = 0
        self.player_andar = pygame.sprite.Group()
        self.player = Player()
        self.player_andar.add(self.player)
        self.aviso = font_aviso.render("ESPAÇO - adiantar a história", True, WHITE)
        self.acelerado = False
        
    def run(self):
        
        LARGURA_DIALOGO = 900
        ALTURA_DIALOGO = 190
        
        x = (LARGURA_TELA - LARGURA_DIALOGO) // 2
        y = (ALTURA_TELA - ALTURA_DIALOGO) // 2 + 200 
        
        dialog_rect = pygame.Rect(x, y, LARGURA_DIALOGO, ALTURA_DIALOGO)
        
        fundos = [
            os.path.join(os.path.dirname(__file__), "data", "images", "corredores", "biblioteca-ifrn.png"),
            os.path.join(os.path.dirname(__file__), "data", "images", "corredores", "biblioteca-ifrn.png"),
            os.path.join(os.path.dirname(__file__), "data", "images", "livro-maíra.png"),
            os.path.join(os.path.dirname(__file__), "data", "images", "livro-maíra.png"),
            os.path.join(os.path.dirname(__file__), "data", "images", "corredores", "biblioteca-ifrn.png")
        ]
        
        if self.text_view == False:
                     
            i = 0
            for bloco in self.dialog_text:
                
                self.caminho = fundos[i]
                self.fundo = pygame.image.load(self.caminho).convert()
                self.fundo = pygame.transform.scale(self.fundo, (LARGURA_TELA, ALTURA_TELA))
                self.screen.blit(self.fundo, (0,0))
                self.screen.blit(self.aviso, (100,20))
                self.space = pygame.image.load(os.path.join(os.path.dirname(__file__), "data", "images", "teclas", "space.png"))
                self.space = pygame.transform.scale(self.space, (60, 30))
                self.screen.blit(self.space, (20, 20))
                
                if "biblioteca-ifrn.png" in self.caminho:
                    self.player.rect.topleft = 30, 400
                    self.player_andar.draw(self.screen)
                        
                self.y = 0
                pygame.draw.rect(self.screen, BOX, dialog_rect)
                pygame.draw.rect(self.screen, BORDER, dialog_rect, 5)
                
                for line in bloco:
                    
                    text_final = ""
                    x_position = x + 20
                    y_position = y + 20
                    
                    for s in line:
                        teclas = pygame.key.get_pressed()
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if teclas[pygame.K_SPACE]:
                                self.acelerado = True
                                
                        text_final +=s 
                        text_surface = font.render(text_final, True, WHITE)
                        self.screen.blit(text_surface, (x_position, y_position + self.y))
                        pygame.display.flip()
                        if self.acelerado == True:
                            pygame.time.Clock().tick(0)
                        else:
                            pygame.time.Clock().tick(30)
                        
                    self.y += 35 
                    pygame.display.update()
                    
                i += 1
                pausa = True
                pausa_tempo = 1500 
                inicio_pausa = pygame.time.get_ticks()
                
                while pausa:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()    
                    agora = pygame.time.get_ticks()
                    if agora - inicio_pausa >= pausa_tempo:
                        pausa = False
                    pygame.time.Clock().tick(FPS)
                    
                self.acelerado = False

            self.text_view = True
            self.running = False
            self.game_loop()    
            
    def game_loop(self):
        
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if self.running == False:
                    musica.parar()
                    Game(cenario=CorredorA36()).run()
            
            clock.tick(FPS)
        pygame.quit()


if __name__ == "__main__":
    history = História()
    menu = Menu(history.screen)
    menu.run()