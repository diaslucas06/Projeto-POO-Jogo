import pygame
from pygame.locals import *
from player import Player
from ui.sounds import Musica
import sys

pygame.init()

#valores
FPS = 30

#player
player = Player()

class Game():
    def __init__(self, cenario):

        pygame.display.set_caption("The Teacher Disappearence")
        self.relogio = pygame.time.Clock()    
        self.cenario = cenario
        musica = Musica("Robert Blumenau - Suspense.mp3")
        musica.play()
        pygame.mixer.music.set_volume(0.05)

    def run(self):
        self.running = True
        while self.running:
            self.relogio.tick(FPS)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
            novo_cenario = self.cenario.desenhar()
            pygame.event.pump()
            
            if novo_cenario:
                if novo_cenario == "VOLTAR_MENU":
                    self.running = False
                else:
                    self.cenario = novo_cenario
                    if player.ultima_direcao == "esquerda":   
                        player.rect.topleft = (1100, 295)
                    elif player.ultima_direcao == "direita":
                        player.rect.topleft = (0, 295)
                        
            pygame.display.flip()
            
if __name__ == "__main__":
    from menu import Menu, História, LARGURA_TELA, ALTURA_TELA
    screen = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
    while True:
        history = História()
        menu_principal = Menu(screen)
        menu_principal.run()