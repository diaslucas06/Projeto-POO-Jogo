import pygame
import os

class Musica():
    def __init__(self, arquivo):
        
        self.caminho = os.path.join(os.path.dirname(__file__), "..", "data", "sounds", arquivo)
        
    def play(self):
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.load(self.caminho)
        pygame.mixer.music.play(-1)
        
    def parar(self):
        pygame.mixer.music.stop()
        
class Som():
    def __init__(self, som):
        self.caminho = os.path.join(os.path.dirname(__file__), "..", "data", "sounds", som)
        self.som = pygame.mixer.Sound(self.caminho)
        
    def play(self):
        self.som.play()
        
