# MANUAL DO JOGO — SNAKE

> Guia completo de como jogar, pontuar e sobreviver.

---

## Sumário

- [Objetivo](#objetivo)
- [Controles](#controles)
- [Dificuldades](#dificuldades)
- [Frutas e Pontuação](#frutas-e-pontuação)
- [Bombas](#bombas)
- [Velocidade e Níveis](#velocidade-e-níveis)
- [Fases](#fases)
- [Ranking](#ranking)
- [Pausa e Estatísticas](#pausa-e-estatísticas)
- [Fim de Jogo](#fim-de-jogo)

---

## Objetivo

Controle a cobra pelo mapa, coma frutas para crescer e acumular pontos, e **evite colidir** com as paredes, com o próprio corpo ou com bombas.

---

## Controles

| Tecla | Ação |
|-------|------|
| `↑`  `↓`  `←`  `→` | Mover a cobra (setas do teclado) |
| `W`  `A`  `S`  `D` | Mover a cobra (alternativo) |
| `ENTER` | Confirmar seleção / Iniciar / Reiniciar |
| `P` | Pausar o jogo / Retomar |
| `C` (segurar) | Exibir painel de estatísticas em tempo real |
| `ESC` | Voltar ao menu / Sair do jogo |

> A cobra não pode inverter o sentido diretamente (ex.: indo para a direita, não é possível virar imediatamente para a esquerda).

---

## Dificuldades

Ao iniciar uma partida você escolhe um dos três modos:

| Modo | Ranking | Frutas simultâneas | Velocidade | Extras |
|------|---------|--------------------|------------|--------|
| **Fácil** | Sem ranking | 1 fruta sempre | Fixa (4 FPS) | Ideal para aprender |
| **Médio** | Top 10 | Cresce com a pontuação | Aumenta com a pontuação | — |
| **Difícil** | Top 10 | Cresce com a pontuação | Aumenta com a pontuação | Bombas + frutas com tempo limitado |

---

## Frutas e Pontuação

Existem três tipos de fruta, cada uma com pontuação e raridade diferentes:

| Fruta | Pontos | Raridade |
|-------|:------:|----------|
| 🍎 Maçã   | **+10 pts** | Comum  (~50% de chance) |
| 🍌 Banana | **+20 pts** | Média  (~33% de chance) |
| 🍇 Uva    | **+50 pts** | Rara   (~17% de chance) |

**Quantidade de frutas no mapa**

A quantidade de frutas ativas aumenta automaticamente conforme a pontuação (nos modos Médio e Difícil):

| Pontuação acumulada | Frutas simultâneas no mapa |
|--------------------:|:--------------------------:|
| 0 – 199 pts         | 1 fruta                    |
| 200 – 399 pts       | 2 frutas                   |
| 400 pts ou mais     | 3 frutas (máximo)          |

**Frutas com tempo limitado — somente no modo Difícil**

Cada fruta dura **16 segundos** em tela. Se não for comida nesse tempo, desaparece e reaparece em outro lugar. Frutas piscando estão prestes a sumir.

---

## Bombas

As bombas aparecem **somente no modo Difícil**, após o jogador atingir **200 pontos**.

| Detalhe | Valor |
|---------|-------|
| Pontuação mínima para surgir | 200 pts |
| Duração no mapa | 8 segundos |
| Efeito ao colidir | Game over imediato |
| Som ao colidir | Explosão |

**Como identificar uma bomba**

- Objeto escuro (esfera preta com pavio) que pulsa levemente.
- Um **anel colorido** ao redor indica o tempo restante: verde = tempo sobrando, vermelho = prestes a desaparecer.
- Uma **faísca amarela** pisca na ponta do pavio.
- Quando o tempo se esgota a bomba some sem causar dano — apenas evite tocá-la.

**Quantidade máxima de bombas ativas**

| Pontuação acumulada | Bombas máximas no mapa |
|--------------------:|:----------------------:|
| 200 – 999 pts       | 1 bomba                |
| 1000 – 1999 pts     | 2 bombas               |
| 2000 pts ou mais    | 3 bombas               |

---

## Velocidade e Níveis

**Nível**

O nível sobe a cada **100 pontos** marcados:

| Pontuação     | Nível |
|--------------:|:-----:|
| 0 – 99 pts    | 1     |
| 100 – 199 pts | 2     |
| 200 – 299 pts | 3     |
| 300 – 399 pts | 4     |
| ...           | ...   |

**Velocidade (FPS)**

A velocidade da cobra aumenta 1 passo a cada 3 níveis ganhos. No modo Fácil a velocidade é sempre fixa em **4 FPS**.

| Nível alcançado | Velocidade da cobra |
|:---------------:|:-------------------:|
| 1 – 3           | 4 FPS               |
| 4 – 6           | 5 FPS               |
| 7 – 9           | 6 FPS               |
| 10 – 12         | 7 FPS               |
| 13 ou mais      | 8 FPS (máximo)      |

> Quanto maior o FPS, mais rápida a cobra se move e menos tempo você tem para reagir.

---

## Fases

Nos modos Médio e Difícil, se a cobra **preencher todo o mapa** (ocupar todas as células), o jogo avança para a próxima fase:

- A tela exibe uma mensagem de transição com o número da fase.
- A cobra é reiniciada ao centro do mapa, mas a **pontuação é mantida**.
- A quantidade de frutas simultâneas é recalculada com base na pontuação atual.
- No modo Difícil, as bombas são removidas e um novo ciclo começa.

---

## Ranking

Os modos **Médio** e **Difícil** possuem ranking separado com o **Top 10** de jogadores. O modo Fácil não registra pontuação.

- Ao finalizar com uma pontuação que entre no Top 10, uma tela pedirá seu **nick** (até 12 caracteres).
- Se for o **1° lugar geral**, uma música especial de novo recorde é tocada.
- Os rankings podem ser consultados durante a pausa (opção "VER SCORE") ou na tela de Game Over.

---

## Pausa e Estatísticas

**Pausar o jogo**

Pressione `P` durante a partida para abrir o menu de pausa. Opções disponíveis:

| Opção | Ação |
|-------|------|
| VER SCORE    | Exibe o ranking do modo atual            |
| REINICIAR    | Volta à seleção de dificuldade           |
| MENU INICIAL | Retorna à tela inicial                   |

Pressione `P` novamente na tela de pausa para retomar.

**Painel de estatísticas em tempo real**

Segure `C` durante a partida para ver no canto da tela:

| Campo   | O que mostra                          |
|---------|---------------------------------------|
| VEL     | Velocidade atual em FPS               |
| TAMANHO | Número de segmentos da cobra          |
| FRUTAS  | Quantidade de frutas ativas no mapa   |

---

## Fim de Jogo

A partida termina imediatamente quando a cobra:

1. **Bate na parede** — ultrapassa os limites do mapa.
2. **Bate no próprio corpo** — colide com qualquer segmento da cauda.
3. **Bate em uma bomba** — somente no modo Difícil.

Após o Game Over você pode:

- Pressionar `ENTER` para jogar novamente.
- Pressionar `ESC` para voltar ao menu inicial.

---

*Snake Game — desenvolvido em Python com Pygame.*
