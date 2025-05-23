
# Documentação do Projeto: The Teacher Disappearence
## 1. Visão Geral  
**Tecnologia Utilizada:** Python + Pygame  
**Descrição:** Jogo 2D de suspense investigativo com ambientação no Instituto Federal do Rio Grande do Norte, Campus Caicó, utilizando a biblioteca Pygame para renderização gráfica e lógica do jogo.  
**Objetivo:** Criar um jogo cativante no qual o jogador tem como objetivo desvendar um mistério, lidando com desafios de raciocínio lógico e obstáculos a partir da interação com personagens, tendo como foco a narrativa não-linear. 
  
***
  
## 2. Descrição Detalhada do Projeto  
### O que é o The Teacher Disappearence?  
The Teacher Disappearence é um jogo de suspense investigativo, criado pelos alunos Lucas Gabriel de Araújo Dias e Emilly Mirely Mariz de Andrade, composto por enigmas e obstáculos a serem superados. O jogador, aluno da escola, tem como objetivo descobrir o que aconteceu com a professora Maíra, que está desaparecida do Instituto Federal do Rio Grande do Norte Campus Caicó há alguns dias. O mistério começa quando o aluno encontra uma matrícula estranha em um livro incomum da biblioteca do Campus, que tem gravado no interior de sua capa o nome da professora sumida, esse livro leva o usuário a um grande quebra-cabeça de pistas a serem desvendadas. Sua trajetória no jogo envolve coletar itens, explorar a escola e conversar com personagens, com o auxílio de um mapa para guiá-lo pelos caminhos incertos, descobrindo lugares nunca antes vistos. 
  
Curiosidade: The Teacher Disappearence envolve o uso de comandos de voz em seu funcionamento geral (pausar, começar, sair, pegar, entre outros) e para entrar em salas restritas ou acessar informações em computadores. O uso dessa funcionalidade melhora a inserção do jogador com o ambiente digital, aumentando o divertimento.
  
### 2.1 Funcionalidades Principais  
* **Motor do Jogo**:  
  
  * Navegação por salas (mapeamento do IFRN).  
  * Sistema de coleta de itens (livros, bilhetes, entre outros).  
  * Detecção de eventos (ao entrar em salas específicas).  
  * Sistema de pistas e progressão narrativa.  
  * Comandos de voz (utilizados em seu funcionamento geral e em partes específicas).
  
* **Interface Gráfica**:  
  
  * Estilo pixel art 2D com estética sombria.  
  * Inventário com itens coletados e mapa do Campus.  
  * Telas de início/pausa/game over.  
  
* **Extras**:  
  
  * Trilhas sonoras e efeitos sonoros personalizados.  
  * Sistema de múltiplos finais.  
  
### 2.2 Arquitetura do Código
  
```
tetris/
├── main.py            # Ponto de entrada (inicialização do jogo)
├── game.py            # Lógica principal (estado do jogo, loop principal)
├── pieces.py          # Definição dos tetrominós e rotações
├── grid.py            # Gerenciamento do grid e checagem de linhas
├── ui/                # Interface do usuário
│   ├── render.py      # Renderização gráfica (Pygame)
│   └── sounds.py      # Gerenciamento de áudio
└── utils/             # Utilitários
    ├── config.py      # Constantes (cores, tamanhos)
    └── scores.py      # Manipulação de high scores
```
  
## 3. Descrição Detalhada do Projeto  
### Etapa 1: Protótipo Básico (Semana 1-2)  
* Configuração do ambiente (Python 3.10+, Pygame 2.5+).  
* Estrutura inicial do projeto (módulos principais).  
* Implementação do grid e renderização básica.  
* Movimentação manual de um bloco (sem colisões).  
  
### Etapa 2: Lógica do Jogo (Semana 3-4)  
* Sistema completo de peças (7 tetrominós com rotações).  
* Detecção de colisões e limites do grid.  
* Lógica de linhas completas e pontuação.  
* Controles do jogador (teclado/configurável).  
  
### Etapa 3: Polimento (Semana 5)
* Menu inicial e telas auxiliares (pausa/game over).  
* Sistema de níveis (velocidade aumenta progressivamente).  
* Efeitos sonoros e high score.  
  
### Etapa 4: Testes e Entrega Final (Semana 6)  
* Testes de usabilidade (feedback de jogadores).  
* Correção de bugs (ex.: ghosting de peças).  
* Documentação final (README.md + comentários no código).  
  
## 4. Requisitos técnicos  
### 4.1 Exemplo de dependências (requirements.txt)  

```
pygame==2.5.2
numpy==1.26.0  # Opcional para cálculos de matrizes
```
