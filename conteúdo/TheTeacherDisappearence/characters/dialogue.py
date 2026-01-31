#Diálogo da personagem com o Zelador: 

#Zelador:
 #Ei! você não devia estar aqui hoje. O campus está praticamente fechado.
#Aluna:
 #Desculpa, eu só… preciso pegar umas coisas que deixei pelo campus. Não vou demorar.
#Zelador:
 #Olha… não quero me meter na sua vida. Mas as coisas andam meio complicadas por aqui. Então tome cuidado.
#Aluna:
 #Obrigada, vou tomar cuidado e ser rápida.
#Zelador:
 #Então vai rápido. E evita falar que eu te vi, tá? A supervisão tá pegando no pé de todo mundo.
#(Neste momento, o Zelador sai e a fita vermelha caí. O persoagem pega e vai para o destino, lab de maira).


#Primeiro Diálogo da Personagem com Hugo:

#Aluna:
 #“Hugo! Que bom encontrar algum rosto conhecido por aqui.”
#Hugo:
 #“O que faz aqui a essa hora? Esse laboratório devia estar trancado.”
#Aluna:
 #“Calma, estou apenas em busca de pistas. O senhor sabe o que aconteceu com a professora Maíra?”
#Hugo:
 #“Não fale esse nome em voz alta. Desde o que aconteceu... as pessoas evitam comentar. Há câmeras, microfones... não dá pra confiar em nada aqui dentro.”
#Aluna:
 #“O senhor parece assustado. O que realmente está acontecendo? Ela desapareceu mesmo dentro do campus?”
#Hugo:
 #“Sim, ou pelo menos é o que dizem. A última vez que a vi foi... deixa eu lembrar... quinta-feira, por volta das sete da noite. Ela saiu apressada, com alguns arquivos no pendrive. Depois disso, sumiu.”
#Aluna:
 #“Sete da noite... quinta-feira... isso foi antes da queda de energia, não foi? Isso tem alguma ligação?”
#Hugo:
 #“Talvez tenha. Mas eu não posso dizer mais nada... é perigoso. Já falei demais.”
#Aluna:
 #“Se eu não entender o que está acontecendo, ninguém vai. Eu preciso de alguma pista.”
#Hugo:
 #“Certo, se quer respostas, vai ter que provar que pode lidar com elas. Vá até o Laboratório M6. Há um sistema antigo lá, algo que só quem decifra é quem é digno de alguma pista.”
#Hugo:
 #“Lá dentro há um terminal de segurança. Se conseguir resolver o código travado nele... eu te direi o resto. Só tenha cuidado!
#Aluna:
 #“Entendido. Vou até o M6 e volto assim que decifrar o código.”
#Hugo:
 #“Rápido. E... não diga a ninguém que conversou comigo. Eu não quero ser o próximo a desaparecer.”


#Seguna Parte do Diálogo com Hugo:

#Hugo:
#Você voltou! Isso é... impressionante. Confesso que achei que você não fosse conseguir.

#ALuna:
#Agora o senhor pode cumprir a promessa. O que mais sabe sobre o que aconteceu com a professora Maíra?

#Hugo:
#Maíra estava investigando algo grande, algo que envolvia o próprio sistema interno da escola. Ela guardou informações confidenciais, e me deixou responsável por uma pista. 
#Eu tenho esse pendrive que é uma parte do quebra-cabeça.

#ALuna:
#O que tem dentro dele?

#Hugo:
#Eu não sei. Só sei que Maíra me pediu pra mantê-lo seguro caso algo acontecesse com ela. E me disse que só alguém de confiança e que revolvesse o problema no M6, poderia ter acesso a ele.

#Aluna:
#Obrigada Hugo. Vou fazer o possível para descobrir o que está acontecendo. 

#Hugo:
#Espere..
#Devido o que aconteceu, todos os computadores estão bloqueados, então somente um vai te dar a resposta que vc quer, e ele não é fácil de acessar...

#ALuna:
#E como vou saber qual é esse computador?

#Hugo:
#Maíra deixou pistas espalhadas, lembra? Uma delas deve estar na sala A38. Ela passava horas lá à noite, antes de tudo acontecer. Pegue esta chave.

#Narração:
#Item obtido: Chave da sala A38.

#Hugo:
#Agora vá, antes que alguém perceba que voltou. E lembre-se, nem tudo aqui é o que parece. 

import pygame
import os

LARGURA_TELA = 1280
ALTURA_TELA = 720 
FPS = 60

BOX = (84, 66, 33)
BORDER = (49, 38, 19)
WHITE = (255, 255, 255)
font = pygame.font.Font(os.path.join(os.path.dirname(__file__), "..", "data", "fonts", "Minecraftia-Regular.ttf"), 28)

class Dialogo():
    def __init__(self, cenario):
        self.running = True
        self.dialog_text = None
        self.text_view = False
        self.y = 0
        self.cenario = cenario
        self.tela = self.cenario.tela
        self.largura_dialogo = 1000
        self.altura_dialogo = 190
        
    def run(self):
        
        if self.text_view == False:
            
            x = (LARGURA_TELA - self.largura_dialogo) // 2
            y = (ALTURA_TELA - self.altura_dialogo) // 2 + 250 
            dialog_rect = pygame.Rect(x, y, self.largura_dialogo, self.altura_dialogo)    
            i = 0
            
            for bloco in self.dialog_text:
                
                if "Aluna" in bloco: #cor muda baseado em quem está falando
                    BOX = (126, 140, 84)
                    BORDER = (47, 69, 56)
                elif "Maíra Faria" in bloco:
                    BOX = (172, 50, 87)
                    BORDER = (102, 2, 33)
                else:
                    BOX = (84, 105, 140)
                    BORDER = (47, 54, 69)
                        
                self.y = 0
                self.tela.blit(self.cenario.fundo_salvo, (0, 0))
                pygame.draw.rect(self.tela, BOX, dialog_rect)
                pygame.draw.rect(self.tela, BORDER, dialog_rect, 5)
                
                for line in bloco:
                    
                    text_final = ""
                    x_position = x + 50
                    y_position = y + 20
                    
                    for s in line:
                                
                        text_final +=s 
                        text_surface = font.render(text_final, True, WHITE)
                        self.tela.blit(text_surface, (x_position, y_position + self.y))
                        pygame.display.flip()
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
                           
                    agora = pygame.time.get_ticks()
                    if agora - inicio_pausa >= pausa_tempo:
                        pausa = False
                    pygame.time.Clock().tick(FPS)

            self.text_view = True
            self.running = False
            
            pygame.event.pump()
            
class Dialogo_Hugo1(Dialogo):
    def __init__(self, cenario):
        super().__init__(cenario)
        self.dialog_text = [
            ["Aluna", "Hugo! Que bom encontrar algum rosto conhecido", "por aqui."],
            ["Hugo", "O que faz aqui a essa hora? Esse laboratório devia", "estar trancado."],
            ["Aluna", "Calma, estou apenas em busca de pistas. O senhor", "sabe o que aconteceu com a professora Maíra?"],
            ["Hugo", "Não fale esse nome em voz alta. Desde o que", "aconteceu... as pessoas evitam comentar. Há câ-", "meras, microfones..."],
            ["Hugo", "Não dá pra confiar em nada aqui dentro."],
            ["Aluna","O senhor parece assustado. O que realmente está", "acontecendo? Ela desapareceu mesmo dentro do", "campus?"],
            ["Hugo", "Sim, ou pelo menos é o que dizem. A última vez", "que a vi foi... deixa eu lembrar... quinta-feira,", "por volta das sete da noite. Ela saiu apressada,"],
            ["Hugo", "com alguns arquivos no pendrive. Depois disso,", "sumiu."],
            ["Aluna", "Sete da noite... quinta-feira... isso foi antes", "da queda de energia, não foi? Isso tem alguma", "ligação?"],
            ["Hugo", "Talvez tenha. Mas eu não posso dizer mais nada...", "é perigoso. Já falei demais."],
            ["Aluna", "Se eu não entender o que está acontecendo,", "ninguém vai. Eu preciso de alguma pista."],
            ["Hugo", "Certo, se quer respostas.. vai precisar me ajudar,", "os alunos estão quase me sequestrando junto", "por não corrigir as provas.."],
            ["Hugo", "Vá lá no Laboratório M6.", "Traga minhas provas e eu te darei uma pista!"],
            ["Aluna", "Entendido. Vou até o M6 e volto assim que", "pegar suas provas."],
            ["Hugo", "Rápido. E... não diga a ninguém que conversou", "comigo. Eu não quero ser o próximo a desaparecer..."]
        ]
        
class Dialogo_Hugo_Espera(Dialogo):
    def __init__(self, cenario):
        super().__init__(cenario)
        self.dialog_text = [
            ["Hugo", "Ainda aqui? Eu fui bem claro.", "Vá até o Laboratório M6 e traga minhas provas!"],
            ["Hugo", "Não volte aqui sem elas se quiser a sua pista."]
        ]

class Dialogo_Hugo2(Dialogo):
    def __init__(self, cenario):
        super().__init__(cenario)
        self.dialog_text = [
            ["Aluna", "Hugo, aqui estão as provas que você pediu.", "Consegui pegá-las no M6."],
            ["Hugo", "Top! Finalmente poderei corrigir isso.", "Os alunos já estavam perdendo a paciência."],
            ["Hugo", "Como prometido, aqui está o que você precisa.", "Está chave abre a sala A38."],
            ["Hugo", "Tome cuidado. O que tem lá dentro pode ser", "pior do que você imagina."]
        ]
        
class Dialogo_Zelador(Dialogo):
    def __init__(self, cenario):
        super().__init__(cenario)
        self.dialog_text = [
            ["Zelador", "Ei! você não devia estar aqui hoje. O campus está", "praticamente fechado."],
            ["Aluna", "Desculpa, eu só… preciso pegar umas coisas que deixei", "pelo campus."],
            ["Zelador", "Olha… não quero me meter na sua vida. Mas as coisas", "andam meio complicadas por aqui. Então tome cuidado."],
            ["Aluna", "Obrigada, vou tomar cuidado e ser rápida."],
            ["Zelador", "Então vai rápido. E evita falar que eu te vi, tá?", "A supervisão tá pegando no pé de todo mundo."],
        ]
        
class Dialogo_Coordenador(Dialogo):
    def __init__(self, cenario):
        super().__init__(cenario)
        self.dialog_text = [
            ["Coordenador", "O que você está fazendo aqui? Alunos não estão", "permitidos nesse campus durante a noite!", "Vá embora!"],
        ]
        
class Dialogo_Maíra(Dialogo):
    def __init__(self, cenario):
        super().__init__(cenario)
        self.dialog_text = [
            ["Maíra Faria", "O que você está fazendo aqui? Alunos não estão", "permitidos nesse campus durante a noite!", "Vá embora!"],
        ]        