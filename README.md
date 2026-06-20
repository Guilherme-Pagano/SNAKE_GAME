# 🐍👨🏻‍💻 SNAKE GAME

Releitura do clássico jogo da cobrinha desenvolvida em **Python** com a biblioteca **Pygame**, como projeto da disciplina de **Algoritmos e Programação**.

Além da mecânica tradicional, o jogo conta com três níveis de dificuldade, frutas com pontuações diferentes, bombas, sistema de fases, ranking de recordes, música e efeitos sonoros — tudo com visual retrô em estilo 8-bit.

---

## 📑 Sumário

- [Demonstração](#-demonstração)
- [Funcionalidades](#-funcionalidades)
- [Como executar](#-como-executar)
- [Controles](#-controles)
- [Níveis de dificuldade](#-níveis-de-dificuldade)
- [Mecânicas do jogo](#-mecânicas-do-jogo)
- [Estrutura do projeto](#-estrutura-do-projeto)
- [Tecnologias](#-tecnologias)
- [Autores](#-autores)

---

## 🎬 Demonstração

> 🎥 **Vídeo demonstrativo:

https://github.com/user-attachments/assets/33d45468-b1e4-40d1-9d47-26aed71850c1


--> TELA DE INICIO
<img width="1165" height="934" alt="{6A22C989-9783-4ECD-B9F9-F05151C5B24D}" src="https://github.com/user-attachments/assets/4d62574b-0b22-4b92-9c76-bb4354e323d6" />

<!-- Dica: você também pode colocar um GIF ou um print do jogo aqui, por exemplo: -->

---

## ✨ Funcionalidades

- **Três níveis de dificuldade**: Fácil, Médio e Difícil.
- **Frutas variadas**: maçã, banana e uva, cada uma com pontuação e raridade diferentes.
- **Bombas** (no modo Difícil): aparecem após certa pontuação e encerram o jogo se a cobra encostar.
- **Sistema de fases**: ao preencher todo o mapa, o jogador avança de fase e o desafio aumenta.
- **Ranking Top 10** com captura de nick, salvo separadamente por dificuldade.
- **Detecção de novo recorde**, com tela especial para registrar o nome.
- **HUD completo**: pontuação, recorde, nível, fase e dificuldade na tela.
- **Painel de estatísticas** (segurando a tecla `C`): FPS, tamanho da cobra e frutas em tela.
- **Menu de pausa navegável**: ver pontuação, reiniciar ou voltar ao menu inicial.
- **Trilha sonora e efeitos** em 8-bit (menu, mastigar, morte e novo recorde).
- **Visual retrô** com fonte *PressStart2P* e sprites desenhados em código.
- **Cobrinha animada** na tela de menu.

---

## ▶️ Como executar

### Pré-requisitos

- [Python 3](https://www.python.org/downloads/) instalado
- Biblioteca **Pygame**

### Passo a passo

1. Clone o repositório:
   ```bash
   git clone https://github.com/Guilherme-Pagano/SNAKE_GAME.git
   cd SNAKE_GAME
   ```

2. Instale a dependência:
   ```bash
   pip install pygame
   ```

3. Execute o jogo:
   ```bash
   python snake_main.py
   ```

> 💡 Se você usa `python3` no terminal, rode `python3 snake_main.py`.

---

## 🎮 Controles

| Tecla | Ação |
|-------|------|
| `↑` `↓` `←` `→` ou `W` `A` `S` `D` | Mover a cobra |
| `ENTER` | Confirmar / Jogar / Reiniciar |
| `P` | Pausar / Continuar |
| `C` (segurar) | Mostrar painel de estatísticas |
| `ESC` | Voltar ao menu / Sair |

---

## 🔥 Níveis de dificuldade

| Modo | Ranking | Frutas | Velocidade | Extras |
|------|:-------:|--------|------------|--------|
| **Fácil** | ❌ | 1 fruta por vez | Fixa | Ideal para aprender |
| **Médio** | ✅ | +1 fruta a cada 200 pts | Aumenta com a pontuação | — |
| **Difícil** | ✅ | +1 fruta a cada 200 pts | Aumenta com a pontuação | Bombas após 400 pts e frutas que expiram por tempo |

---

## 🧩 Mecânicas do jogo

**Frutas e pontuação**

| Fruta | Pontos | Frequência |
|-------|:------:|-----------|
| 🍎 Maçã | 10 | Comum |
| 🍌 Banana | 20 | Média |
| 🍇 Uva | 50 | Rara |

- A **velocidade** aumenta conforme a pontuação sobe (nos modos Médio e Difícil).
- O **nível** sobe a cada 50 pontos.
- No modo Difícil, cada fruta tem tempo limitado em tela e some se não for comida a tempo.
- As **bombas** exibem um anel de contagem regressiva e devem ser evitadas.
- Ao **completar o mapa inteiro**, o jogador avança de **fase**, com mais frutas simultâneas.

**Fim de jogo**

O jogo termina quando a cobra colide com a parede, com o próprio corpo ou com uma bomba. Se a pontuação entrar no Top 10, o jogador pode registrar seu nick.

---

## 📁 Estrutura do projeto

```
SNAKE_GAME/
├── snake_main.py              # Código principal do jogo
├── PressStart2P-Regular.ttf   # Fonte retrô
├── music_game_8bit-menu.mp3   # Música do menu
├── music_mastigar.mp3         # Efeito ao comer
├── music_dead.mp3             # Efeito de game over
├── music_new_record.mp3       # Efeito de novo recorde
├── scores_medio.txt           # Ranking do modo Médio
├── scores_dificil.txt         # Ranking do modo Difícil
└── README.md
```

---

## 🛠️ Tecnologias

- **Python 3**
- **Pygame** — renderização gráfica, áudio e captura de eventos

---

## 👥 Autor

Projeto desenvolvido para a disciplina de **Algoritmos e Programação**.

- [Guilherme Pagano](https://github.com/Guilherme-Pagano)
  
---

## 👨🏻‍💻 Créditos 

Esse projeto tive boa parte dele sendo feita em dupla com o colega Josué, por parte de edição de imagem de fundo e do formato da cobra. 

-[Josué WOLFGRAMM](https://github.com/JoKaWo)

---
Agradeço pelas orientação do projeto e ajuda com as duvidas que tive duranta o projeto Sor Filipo.

-[FILIPO NOVO MÓR](https://github.com/ProfessorFilipo)

---
