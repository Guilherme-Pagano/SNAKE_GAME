import pygame
import random
import sys
import os
import math

# ============================================================
# Caminhos de recursos
# ============================================================
_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_SCORES_MEDIO   = os.path.join(_DIR, "scores_medio.txt")
ARQUIVO_SCORES_DIFICIL = os.path.join(_DIR, "scores_dificil.txt")
CAMINHO_FONTE      = os.path.join(_DIR, "PressStart2P-Regular.ttf")
CAMINHO_MUSICA_MENU = os.path.join(_DIR, "music_game_8bit-menu.mp3")
CAMINHO_SOM_MORTE     = os.path.join(_DIR, "music_dead.mp3")
CAMINHO_SOM_MASTIGAR  = os.path.join(_DIR, "music_mastigar.mp3")
CAMINHO_SOM_RECORDE   = os.path.join(_DIR, "music_new_record.mp3")
MAX_SCORES = 10
MAX_NICK   = 12

# Acoes de retorno da funcao partida()
ACAO_GAMEOVER  = "gameover"
ACAO_REINICIAR = "reiniciar"
ACAO_MENU      = "menu"


# ============================================================
# Audio
# ============================================================

def tocar_musica_menu():
    """Inicia a musica do menu em loop (nao reinicia se ja estiver tocando)."""
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load(CAMINHO_MUSICA_MENU)
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play(-1)


def parar_musica():
    pygame.mixer.music.stop()


# ============================================================
# Gerenciamento de recordes  (scores = lista de (nick, pts))
# ============================================================

def carregar_scores(arquivo):
    if not os.path.exists(arquivo):
        return []
    scores = []
    with open(arquivo, "r", encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if not linha:
                continue
            if "|" in linha:
                partes = linha.split("|")
                if partes[1].isdigit():
                    nivel = int(partes[2]) if len(partes) >= 3 and partes[2].isdigit() else 1
                    scores.append((partes[0], int(partes[1]), nivel))
            elif linha.isdigit():
                scores.append(("---", int(linha), 1))
    scores.sort(key=lambda e: e[1], reverse=True)
    return scores[:MAX_SCORES]


def salvar_scores(scores, arquivo):
    with open(arquivo, "w", encoding="utf-8") as f:
        for nick, pts, nivel in scores:
            f.write(f"{nick}|{pts}|{nivel}\n")


def qualifica_top10(pontuacao, scores):
    return len(scores) < MAX_SCORES or (scores and pontuacao > scores[-1][1])


def atualizar_scores(pontuacao, nick, nivel, scores, arquivo):
    eh_novo_recorde = (not scores) or (pontuacao > scores[0][1])
    scores = sorted(scores + [(nick, pontuacao, nivel)], key=lambda e: e[1], reverse=True)[:MAX_SCORES]
    salvar_scores(scores, arquivo)
    return scores, eh_novo_recorde


# ============================================================
# Configuracoes
# ============================================================
LARGURA        = 800
ALTURA         = 640
AREA_JOGO_Y    = 44
BORDA_LATERAL  = 20
FPS_BASE         = 4
BOMBA_DURACAO    = 8000
BOMBA_MIN_SCORE  = 400
FRUTA_DURACAO    = 16000  # ms que cada fruta fica na tela no modo dificil

TAMANHO_POR_DIFIC = {"facil": 50, "medio": 40, "dificil": 30}

# Valores iniciais (atualizados por aplicar_dificuldade antes de cada partida)
TAMANHO_CELULA = 40
COLUNAS        = (LARGURA - 2 * BORDA_LATERAL) // TAMANHO_CELULA
LINHAS         = (ALTURA  - AREA_JOGO_Y)       // TAMANHO_CELULA


def aplicar_dificuldade(dificuldade):
    global TAMANHO_CELULA, COLUNAS, LINHAS
    TAMANHO_CELULA = TAMANHO_POR_DIFIC[dificuldade]
    COLUNAS        = (LARGURA - 2 * BORDA_LATERAL) // TAMANHO_CELULA
    LINHAS         = (ALTURA  - AREA_JOGO_Y)       // TAMANHO_CELULA


# ============================================================
# Paleta de cores
# ============================================================
PRETO       = (0,   0,   0)
BRANCO      = (255, 255, 255)
CINZA       = (140, 140, 140)
VERMELHO    = (220, 60,  60)
AMARELO     = (255, 220, 0)
AZUL        = (60,  130, 220)
LARANJA     = (255, 140, 0)
PRATA       = (192, 192, 192)
BRONZE      = (205, 127, 50)
ROXO        = (130, 30,  180)

BG_CLARO    = (106, 163, 47)
BG_ESC      = (84,  130, 37)
BORDA_BG    = (22,  48,  22)

HUD_BG      = (16,  36,  16)
HUD_BORDA   = (38,  80,  38)
VERDE_HUD   = (100, 220, 60)

COBRA_CAB   = (15,  60,  15)
COBRA_CORPO = (25,  90,  25)

FRUTAS = [
    {"forma": "maca",   "cor": VERMELHO, "brilho": AMARELO, "pontos": 10, "peso": 60},
    {"forma": "banana", "cor": AMARELO,  "brilho": BRANCO,  "pontos": 20, "peso": 40},
    {"forma": "uva",    "cor": ROXO,     "brilho": (200, 140, 255), "pontos": 50, "peso": 20},
]

FRUTA_BOMBA = {"forma": "bomba", "cor": (30, 30, 30), "brilho": (80, 80, 80), "pontos": 0, "peso": 0}



# ============================================================
# Direcoes
# ============================================================
CIMA     = (0, -1)
BAIXO    = (0,  1)
ESQUERDA = (-1, 0)
DIREITA  = (1,  0)

TECLAS = {
    pygame.K_UP:    CIMA,
    pygame.K_DOWN:  BAIXO,
    pygame.K_LEFT:  ESQUERDA,
    pygame.K_RIGHT: DIREITA,
    pygame.K_w:     CIMA,
    pygame.K_s:     BAIXO,
    pygame.K_a:     ESQUERDA,
    pygame.K_d:     DIREITA,
}
OPOSTO = {CIMA: BAIXO, BAIXO: CIMA, ESQUERDA: DIREITA, DIREITA: ESQUERDA}


# ============================================================
# Helpers
# ============================================================

def celula_para_rect(col, lin):
    x = BORDA_LATERAL + col * TAMANHO_CELULA
    y = AREA_JOGO_Y   + lin * TAMANHO_CELULA
    return pygame.Rect(x + 1, y + 1, TAMANHO_CELULA - 2, TAMANHO_CELULA - 2)


def gerar_comida(corpo, extras=None):
    ocupadas = set(corpo)
    if extras:
        ocupadas.update(extras)
    livres = [(c, l) for c in range(COLUNAS) for l in range(LINHAS) if (c, l) not in ocupadas]
    return random.choice(livres) if livres else None


def sortear_fruta():
    return random.choices(FRUTAS, weights=[f["peso"] for f in FRUTAS], k=1)[0]


def fps_atual(pontuacao):
    return min(8, FPS_BASE + (pontuacao // 150))


def nivel_atual(pontuacao):
    return (pontuacao // 50) + 1


def frutas_por_score(pontuacao):
    return 1 + (pontuacao // 200)


def fonte(tamanho):
    return pygame.font.Font(CAMINHO_FONTE, tamanho)


def blit_centro(tela, surf, cy, cx=None):
    if cx is None:
        cx = LARGURA // 2
    tela.blit(surf, (cx - surf.get_width() // 2, cy))


def criar_sprites_cobra(tamanho):
    t = tamanho

    # CORPO
    img_corpo = pygame.Surface((t, t), pygame.SRCALPHA)
    pygame.draw.rect(img_corpo, COBRA_CORPO, (3, 3, t - 6, t - 6), border_radius=8)
    pygame.draw.ellipse(img_corpo, (20, 75, 20), (t // 4, t // 4, t // 2, t // 2))

    # CABEÇA — base voltada para DIREITA
    cab = pygame.Surface((t, t), pygame.SRCALPHA)
    pygame.draw.rect(cab, COBRA_CAB, (2, 2, t - 4, t - 4), border_radius=10)

    ox = t * 3 // 4          # olhos no lado direito
    oy1, oy2 = t // 3, t * 2 // 3
    pygame.draw.circle(cab, BRANCO, (ox, oy1), 5)
    pygame.draw.circle(cab, BRANCO, (ox, oy2), 5)
    pygame.draw.circle(cab, PRETO,  (ox + 1, oy1), 3)
    pygame.draw.circle(cab, PRETO,  (ox + 1, oy2), 3)

    # língua bífida saindo pela direita
    lc = (200, 0, 0)
    m  = t // 2
    pygame.draw.line(cab, lc, (t - 7, m), (t - 1, m - 5), 2)
    pygame.draw.line(cab, lc, (t - 7, m), (t - 1, m + 5), 2)

    # pré-rotacionar as 4 direções (pygame.transform.rotate = sentido anti-horário)
    sprites_cab = {
        DIREITA:  cab,
        CIMA:     pygame.transform.rotate(cab, 90),
        ESQUERDA: pygame.transform.rotate(cab, 180),
        BAIXO:    pygame.transform.rotate(cab, 270),
    }

    return sprites_cab, img_corpo


# ============================================================
# Funcoes de desenho – jogo
# ============================================================

def desenhar_fundo(tela):
    tela.fill(BORDA_BG)
    for col in range(COLUNAS):
        for lin in range(LINHAS):
            cor = BG_CLARO if (col + lin) % 2 == 0 else BG_ESC
            pygame.draw.rect(tela, cor,
                             (BORDA_LATERAL + col * TAMANHO_CELULA,
                              AREA_JOGO_Y   + lin * TAMANHO_CELULA,
                              TAMANHO_CELULA, TAMANHO_CELULA))


def desenhar_cobra(tela, corpo, direcao, sprites_cab, img_corpo):
    t = TAMANHO_CELULA
    for i, (col, lin) in enumerate(corpo):
        x = BORDA_LATERAL + col * t
        y = AREA_JOGO_Y   + lin * t
        if i == 0:
            tela.blit(sprites_cab[direcao], (x, y))
        else:
            tela.blit(img_corpo, (x, y))


def _desenhar_maca(tela, cx, cy):
    t = TAMANHO_CELULA
    r = t // 2 - 4
    pygame.draw.circle(tela, VERMELHO, (cx, cy), r)
    pygame.draw.circle(tela, (255, 130, 130), (cx - r // 3, cy - r // 3), max(2, r // 4))
    lw = max(1, t // 15)
    pygame.draw.line(tela, (101, 67, 33),
                     (cx, cy - r),
                     (cx + max(2, t // 10), cy - r - max(3, t // 7)),
                     lw)
    fw, fh = max(8, t // 2), max(5, t // 4)
    folha = pygame.Surface((fw, fh), pygame.SRCALPHA)
    pygame.draw.ellipse(folha, (60, 180, 60), (0, 0, fw, fh))
    folha_r = pygame.transform.rotate(folha, 40)
    tela.blit(folha_r, (cx + max(1, t // 20), cy - r - max(5, t // 5)))


def _desenhar_banana(tela, cx, cy):
    t      = TAMANHO_CELULA
    sy     = cy - t // 5
    cw     = max(3, t // 10)
    ch     = max(5, t // 4)
    pygame.draw.rect(tela, (60, 35, 10), (cx - cw // 2, sy - ch // 2, cw, ch), border_radius=2)
    bw     = max(5, t * 3 // 10)
    bh     = max(8, t * 2 // 3)
    tip    = max(3, t // 6)
    dx_off = t * 2 // 5
    dedos  = [(-dx_off, t // 3, -25), (0, t * 13 // 30, 0), (dx_off, t // 3, 25)]
    for dx, dy, ang in dedos:
        s = pygame.Surface((bw, bh), pygame.SRCALPHA)
        pygame.draw.ellipse(s, (255, 220, 0),   (0,       0,   bw,  bh))
        pygame.draw.ellipse(s, (255, 240, 120), (1,       2,   bw-2, bh // 3))
        pygame.draw.ellipse(s, (200, 160, 0),   (0, bh-tip,   bw,  tip))
        rot = pygame.transform.rotate(s, ang)
        rw, rh = rot.get_size()
        tela.blit(rot, (cx + dx - rw // 2, sy + dy - rh // 2))


def _desenhar_uva(tela, cx, cy):
    t      = TAMANHO_CELULA
    r      = max(3, t // 5)
    sh     = max(r, t * 3 // 10)
    sv     = max(r, t * 3 // 10)
    cor    = (130, 30, 180)
    brilho = (200, 140, 255)
    uvas = [
        (cx,      cy - sv),
        (cx - sh, cy),
        (cx + sh, cy),
        (cx - sh, cy + sv),
        (cx,      cy + sv),
        (cx + sh, cy + sv),
    ]
    for ux, uy in uvas:
        pygame.draw.circle(tela, cor,    (ux, uy),                   r)
        pygame.draw.circle(tela, brilho, (ux - r // 3, uy - r // 3), max(1, r // 3))
    pygame.draw.line(tela, (80, 50, 20),
                     (cx, cy - sv),
                     (cx + r // 2, cy - sv - r // 2),
                     max(1, t // 15))


def _desenhar_bomba(surf, cx, cy):
    t  = TAMANHO_CELULA
    r  = t // 2 - 5
    pygame.draw.circle(surf, (25, 25, 25), (cx, cy), r)
    pygame.draw.circle(surf, (75, 75, 75), (cx - r // 3, cy - r // 3), max(2, r // 4))
    # pavio
    px, py = cx + r // 2, cy - r
    pygame.draw.line(surf, (120, 90, 30), (px, py), (px + max(3, t // 12), py - max(6, t // 7)), max(1, t // 22))


def desenhar_bomba_mapa(tela, posicao, spawn_time):
    col, lin = posicao
    rect     = celula_para_rect(col, lin)
    cx, cy   = rect.centerx, rect.centery
    agora    = pygame.time.get_ticks()
    restante = max(0, BOMBA_DURACAO - (agora - spawn_time))
    proporcao = restante / BOMBA_DURACAO

    t  = TAMANHO_CELULA
    sc = t // 2
    escala = 1.0 + 0.06 * math.sin(agora * 0.005)

    surf = pygame.Surface((t, t), pygame.SRCALPHA)
    _desenhar_bomba(surf, sc, sc)

    novo_t = max(1, int(t * escala))
    scaled = pygame.transform.scale(surf, (novo_t, novo_t))
    sw, sh = scaled.get_size()
    tela.blit(scaled, (cx - sw // 2, cy - sh // 2))

    # Faísca animada na ponta do pavio
    px = cx + t // 4 + max(3, t // 12)
    py = cy - t // 2 + 2 - max(6, t // 7)
    if (agora // 150) % 2 == 0:
        pygame.draw.circle(tela, AMARELO,  (px, py), max(2, t // 18))
        pygame.draw.circle(tela, (255, 180, 0), (px, py), max(1, t // 28))

    # Anel de contagem regressiva: verde → vermelho
    r_anel = t // 2 + 3
    r_cor  = min(255, int(510 * (1 - proporcao)))
    g_cor  = min(255, int(510 * proporcao))
    cor_anel = (r_cor, g_cor, 0)
    rect_anel = pygame.Rect(cx - r_anel, cy - r_anel, r_anel * 2, r_anel * 2)
    if proporcao > 0:
        fim   = math.pi / 2
        inicio = fim + 2 * math.pi * proporcao
        pygame.draw.arc(tela, cor_anel, rect_anel, fim, inicio, 3)


def desenhar_comida(tela, posicao, fruta):
    col, lin = posicao
    rect = celula_para_rect(col, lin)
    cx, cy = rect.centerx, rect.centery
    forma  = fruta["forma"]

    # pulso de zoom: oscila ±15 % com período ~1.6 s
    escala  = 1.0 + 0.15 * math.sin(pygame.time.get_ticks() * 0.004)
    t       = TAMANHO_CELULA
    sc      = t // 2          # centro da superfície temporária

    surf = pygame.Surface((t, t), pygame.SRCALPHA)
    if forma == "maca":
        _desenhar_maca(surf, sc, sc)
    elif forma == "banana":
        _desenhar_banana(surf, sc, sc)
    elif forma == "uva":
        _desenhar_uva(surf, sc, sc)
    else:
        r = sc - 2
        pygame.draw.circle(surf, fruta["cor"],    (sc, sc),           r)
        pygame.draw.circle(surf, fruta["brilho"], (sc - 2, sc - 3),   3)

    novo_t = max(1, int(t * escala))
    scaled = pygame.transform.scale(surf, (novo_t, novo_t))
    sw, sh = scaled.get_size()
    tela.blit(scaled, (cx - sw // 2, cy - sh // 2))


def desenhar_stats_overlay(tela, fps, tamanho_cobra, num_frutas_tela):
    f = fonte(9)
    linhas = [
        f"VEL   : {fps} FPS",
        f"TAMANHO: {tamanho_cobra}",
        f"FRUTAS : {num_frutas_tela}",
    ]
    pad = 10
    lw  = max(f.size(l)[0] for l in linhas)
    lh  = f.get_height()
    bw  = lw + pad * 2
    bh  = lh * len(linhas) + pad * 2 + (len(linhas) - 1) * 4
    bx  = LARGURA - bw - 12
    by  = AREA_JOGO_Y + 12
    overlay = pygame.Surface((bw, bh), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 190))
    tela.blit(overlay, (bx, by))
    pygame.draw.rect(tela, VERDE_HUD, (bx, by, bw, bh), 1, border_radius=3)
    y = by + pad
    for linha in linhas:
        tela.blit(f.render(linha, True, BRANCO), (bx + pad, y))
        y += lh + 4


def desenhar_hud(tela, f_hud, pontuacao, nivel, recorde, fase=1, dificuldade="medio"):
    pygame.draw.rect(tela, HUD_BG, (0, 0, LARGURA, AREA_JOGO_Y))
    pygame.draw.line(tela, HUD_BORDA, (0, AREA_JOGO_Y - 1), (LARGURA, AREA_JOGO_Y - 1))

    _cores_dif  = {"facil": (80, 220, 80), "medio": AMARELO, "dificil": VERMELHO}
    _labels_dif = {"facil": "FAC", "medio": "MED", "dificil": "DIF"}
    cor_dif   = _cores_dif.get(dificuldade, CINZA)
    label_dif = _labels_dif.get(dificuldade, "???")
    s_dif = f_hud.render(label_dif, True, cor_dif)
    tela.blit(s_dif, (8, 14))
    tela.blit(f_hud.render(f"PT:{pontuacao}", True, VERDE_HUD), (8 + s_dif.get_width() + 6, 14))

    s_rec = f_hud.render(f"REC:{recorde}", True, AMARELO)
    blit_centro(tela, s_rec, 14)
    s_niv = f_hud.render(f"LVL:{nivel}", True, CINZA)
    tela.blit(s_niv, (LARGURA - s_niv.get_width() - 8, 14))
    if fase > 1:
        s_fase = f_hud.render(f"F{fase}", True, LARANJA)
        tela.blit(s_fase, (LARGURA - s_niv.get_width() - s_fase.get_width() - 20, 14))


# ============================================================
# Tela de pause
# ============================================================

_OPCOES_PAUSE = ["VER SCORE", "REINICIAR", "MENU INICIAL"]


def desenhar_pause(tela, opcao_sel, cobinha_menu=None):
    """Overlay de pausa com menu de 3 opcoes navegaveis."""
    overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    overlay.fill((0, 20, 0, 200))
    tela.blit(overlay, (0, 0))

    f_titulo = fonte(18)
    f_item   = fonte(11)
    f_dica   = fonte(8)

    y = 180
    blit_centro(tela, f_titulo.render("- PAUSA -", True, VERDE_HUD), y)
    y += 55

    for i, txt in enumerate(_OPCOES_PAUSE):
        cor = AMARELO if i == opcao_sel else CINZA
        prefixo = "> " if i == opcao_sel else "  "
        blit_centro(tela, f_item.render(prefixo + txt, True, cor), y)
        y += 34

    y += 10
    blit_centro(tela, f_dica.render("P - CONTINUAR", True, (80, 80, 80)), y)

    if cobinha_menu is not None:
        cobinha_menu.update()
        cobinha_menu.draw(tela)

    pygame.display.flip()


def desenhar_scores_pause(tela, scores, dificuldade="medio"):
    """Mostra o top 10 dentro do menu de pausa."""
    overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    overlay.fill((0, 20, 0, 215))
    tela.blit(overlay, (0, 0))

    f_titulo = fonte(14)
    f_rank   = fonte(9)
    f_dica   = fonte(8)

    _titulos_rank = {"medio": "RANKING MODO MEDIO", "dificil": "RANKING MODO DIFICIL"}
    titulo_rank = _titulos_rank.get(dificuldade, "--- TOP 10 ---")

    f_sub = fonte(9)

    y = 60
    blit_centro(tela, f_titulo.render(titulo_rank, True, AMARELO), y)
    y += 28
    blit_centro(tela, f_sub.render("( TOP 10 )", True, CINZA), y)
    y += 22

    X_RANK = 55
    X_NICK = 105
    X_LVL  = 440
    X_PTS  = 590
    cores_pos = [AMARELO, PRATA, BRONZE]

    f_leg = fonte(7)
    COR_LEG = (100, 100, 100)
    tela.blit(f_leg.render("N",     True, COR_LEG), (X_RANK, y))
    tela.blit(f_leg.render("NICK",  True, COR_LEG), (X_NICK, y))
    s_lh = f_leg.render("LEVEL", True, COR_LEG)
    tela.blit(s_lh, (X_LVL - s_lh.get_width(), y))
    s_ph = f_leg.render("PTS",   True, COR_LEG)
    tela.blit(s_ph, (X_PTS - s_ph.get_width(), y))
    y += 14
    pygame.draw.line(tela, COR_LEG, (X_RANK, y), (X_PTS, y), 1)
    y += 6

    for i, (nick, pts, nivel) in enumerate(scores):
        cor = cores_pos[i] if i < 3 else CINZA
        tela.blit(f_rank.render(f"#{i+1}", True, cor), (X_RANK, y))
        tela.blit(f_rank.render(nick[:MAX_NICK], True, cor), (X_NICK, y))
        s_lv = f_rank.render(f"LV:{nivel}", True, cor)
        tela.blit(s_lv, (X_LVL - s_lv.get_width(), y))
        s = f_rank.render(f"{pts}pts", True, cor)
        tela.blit(s, (X_PTS - s.get_width(), y))
        y += 19

    if not scores:
        blit_centro(tela, f_rank.render("SEM RECORDES", True, CINZA), y)

    y = ALTURA - 40
    blit_centro(tela, f_dica.render("ENTER / ESC - VOLTAR", True, (80, 80, 80)), y)

    pygame.display.flip()


# ============================================================
# Cobinha animada do menu
# ============================================================

class CobrinhaMenu:
    _SEG = 8     # espaçamento entre segmentos (px)
    _NUM = 13    # quantidade de segmentos
    _VEL = 2     # pixels por frame
    _Y   = 460   # posição vertical base

    def __init__(self):
        self._hx    = 80
        self._hy    = self._Y
        self._dx    = self._VEL
        self._tick  = 0
        self._ltick = 0
        self._lvis  = False
        cap         = self._NUM * self._SEG + 1
        self._hist  = [(self._hx, self._hy)] * cap

    def update(self):
        self._tick += 1
        self._hx   += self._dx
        self._hy    = self._Y + int(math.sin(self._tick * 0.08) * 10)
        if self._hx > LARGURA - 30:
            self._dx = -self._VEL
        elif self._hx < 30:
            self._dx = self._VEL
        self._hist  = [(self._hx, self._hy)] + self._hist[:-1]
        self._ltick += 1
        if self._ltick >= 20:
            self._lvis  = not self._lvis
            self._ltick = 0

    def draw(self, tela):
        s = self._SEG
        r = s // 2
        for i in range(self._NUM - 1, -1, -1):
            idx = min(i * s, len(self._hist) - 1)
            x, y = self._hist[idx]
            cor  = (15, 110, 15) if i == 0 else (35, 160, 35)
            pygame.draw.circle(tela, cor, (int(x), int(y)), r)
        hx, hy = self._hist[0]
        pygame.draw.circle(tela, (220, 220, 220), (int(hx), int(hy)), 2)
        if self._lvis:
            fx = int(hx) + (9 if self._dx > 0 else -9)
            pygame.draw.line(tela, (220, 0, 0), (int(hx), int(hy)), (fx, int(hy) - 3), 1)
            pygame.draw.line(tela, (220, 0, 0), (int(hx), int(hy)), (fx, int(hy) + 3), 1)


# ============================================================
# Tela inicial
# ============================================================

def desenhar_tela_inicial(tela, scores):
    tela.fill(PRETO)

    blit_centro(tela, fonte(28).render("SNAKE", True, BG_CLARO), 100)

    if scores:
        nick_top, pts_top, *_ = scores[0]
        blit_centro(tela, fonte(14).render(f"REC: {pts_top}", True, AMARELO), 175)
        blit_centro(tela, fonte(10).render(f"by {nick_top}", True, CINZA), 200)
    else:
        blit_centro(tela, fonte(14).render("SEM RECORDE", True, CINZA), 175)

    agora = pygame.time.get_ticks()
    if (agora // 600) % 2 == 0:
        blit_centro(tela, fonte(10).render("ENTER - JOGAR", True, BRANCO), 290)

    blit_centro(tela, fonte(8).render("SETAS / WASD  |  P - PAUSA  |  ESC - SAIR", True, CINZA), 330)
    blit_centro(tela, fonte(8).render("ENTER - ESCOLHER DIFICULDADE", True, LARANJA), 362)


# ============================================================
# Captura de nick
# ============================================================

def capturar_nick(tela, pontuacao, eh_novo_recorde):
    nick = ""
    f_titulo = fonte(14)
    f_pts    = fonte(12)
    f_prompt = fonte(9)
    f_input  = fonte(14)
    f_dica   = fonte(8)

    overlay = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 215))

    titulo_txt = "** NOVO RECORDE! **" if eh_novo_recorde else "PARABENS! VOCE ESTA NO TOP 10!"
    titulo_cor = AMARELO if eh_novo_recorde else AZUL

    relogio = pygame.time.Clock()

    while True:
        relogio.tick(30)
        agora = pygame.time.get_ticks()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    return nick.strip() if nick.strip() else "Anonimo"
                elif evento.key == pygame.K_BACKSPACE:
                    nick = nick[:-1]
                elif evento.key == pygame.K_ESCAPE:
                    return "Anonimo"
                elif evento.unicode and evento.unicode.isprintable() and len(nick) < MAX_NICK:
                    nick += evento.unicode

        tela.blit(overlay, (0, 0))

        y = 130
        blit_centro(tela, f_titulo.render(titulo_txt, True, titulo_cor), y)
        y += 40
        blit_centro(tela, f_pts.render(f"PONTOS: {pontuacao}", True, BRANCO), y)
        y += 50
        blit_centro(tela, f_prompt.render("DIGITE SEU NICK:", True, CINZA), y)
        y += 28

        caixa = pygame.Rect(LARGURA // 2 - 160, y, 320, 36)
        pygame.draw.rect(tela, (40, 40, 40), caixa, border_radius=4)
        pygame.draw.rect(tela, AZUL, caixa, 2, border_radius=4)

        cursor = "|" if (agora // 500) % 2 == 0 else " "
        s_inp = f_input.render(nick + cursor, True, BRANCO)
        tela.blit(s_inp, (caixa.x + 10, caixa.y + 5))

        y += 52
        blit_centro(tela, f_dica.render("ENTER-CONFIRMAR    ESC-PULAR", True, CINZA), y)
        pygame.display.flip()


# ============================================================
# Tela de game over
# ============================================================

def desenhar_game_over(tela, pontuacao, scores, novo_recorde, dificuldade="medio"):
    tela.fill(PRETO)

    f_titulo = fonte(18)
    f_medio  = fonte(12)
    f_small  = fonte(9)
    f_rank   = fonte(9)

    _titulos_rank = {"medio": "RANKING MODO MEDIO", "dificil": "RANKING MODO DIFICIL"}
    titulo_rank = _titulos_rank.get(dificuldade, "--- TOP 10 ---")
    _cores_titulo = {"medio": AMARELO, "dificil": VERMELHO}
    cor_titulo = _cores_titulo.get(dificuldade, AZUL)

    y = 30
    blit_centro(tela, f_titulo.render(titulo_rank, True, cor_titulo), y)
    y += 30
    blit_centro(tela, f_small.render("( TOP 10 )", True, CINZA), y)
    y += 24

    blit_centro(tela, f_medio.render(f"PONTOS: {pontuacao}", True, BRANCO), y)
    y += 30
    if novo_recorde:
        blit_centro(tela, f_medio.render("** NOVO RECORDE! **", True, AMARELO), y)
        y += 30

    X_RANK = 55
    X_NICK = 105
    X_LVL  = 440
    X_PTS  = 590
    cores_pos = [AMARELO, PRATA, BRONZE]

    f_leg = fonte(7)
    COR_LEG = (100, 100, 100)
    tela.blit(f_leg.render("N",     True, COR_LEG), (X_RANK, y))
    tela.blit(f_leg.render("NICK",  True, COR_LEG), (X_NICK, y))
    s_lh = f_leg.render("LEVEL", True, COR_LEG)
    tela.blit(s_lh, (X_LVL - s_lh.get_width(), y))
    s_ph = f_leg.render("PTS",   True, COR_LEG)
    tela.blit(s_ph, (X_PTS - s_ph.get_width(), y))
    y += 14
    pygame.draw.line(tela, COR_LEG, (X_RANK, y), (X_PTS, y), 1)
    y += 6

    for i, (nick, s, nivel) in enumerate(scores):
        cor = cores_pos[i] if i < 3 else CINZA
        if novo_recorde and i == 0 and s == pontuacao:
            cor = AMARELO
        tela.blit(f_rank.render(f"#{i+1}",      True, cor), (X_RANK, y))
        tela.blit(f_rank.render(nick[:MAX_NICK], True, cor), (X_NICK, y))
        s_lv = f_rank.render(f"LV:{nivel}", True, cor)
        tela.blit(s_lv, (X_LVL - s_lv.get_width(), y))
        s_pts = f_rank.render(f"{s}pts", True, cor)
        tela.blit(s_pts, (X_PTS - s_pts.get_width(), y))
        y += 18

    y += 10
    blit_centro(tela, f_small.render("ENTER - JOGAR NOVAMENTE", True, VERDE_HUD), y)
    y += 22
    blit_centro(tela, f_small.render("ESC - MENU INICIAL", True, CINZA), y)

    pygame.display.flip()


# ============================================================
# Tela de selecao de dificuldade
# ============================================================

_DIFICULDADES = [
    ("FACIL",   (80, 220, 80),  "SEM RANKING  |  1 FRUTA  |  VELOCIDADE FIXA"),
    ("MEDIO",   AMARELO,        "RANKING  |  +1 FRUTA/200PTS  |  VEL. CRESCE"),
    ("DIFICIL", VERMELHO,       "RANKING  |  BOMBA APOS 400PTS  |  +1 FRUTA/200PTS"),
]
_DIFIC_IDS = ["facil", "medio", "dificil"]


def selecionar_dificuldade(tela, relogio, cobinha_menu):
    tocar_musica_menu()
    sel      = 1
    f_titulo = fonte(16)
    f_item   = fonte(12)
    f_desc   = fonte(8)
    f_dica   = fonte(8)

    while True:
        relogio.tick(30)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_UP, pygame.K_w):
                    sel = (sel - 1) % len(_DIFICULDADES)
                elif evento.key in (pygame.K_DOWN, pygame.K_s):
                    sel = (sel + 1) % len(_DIFICULDADES)
                elif evento.key == pygame.K_RETURN:
                    parar_musica()
                    return _DIFIC_IDS[sel]
                elif evento.key == pygame.K_ESCAPE:
                    return None

        tela.fill(PRETO)
        y = 80
        blit_centro(tela, f_titulo.render("DIFICULDADE", True, BG_CLARO), y)
        y += 65

        for i, (nome, cor, _) in enumerate(_DIFICULDADES):
            cor_item = cor if i == sel else CINZA
            prefixo  = "> " if i == sel else "  "
            blit_centro(tela, f_item.render(prefixo + nome, True, cor_item), y)
            y += 42

        y += 12
        _, cor_sel, desc_sel = _DIFICULDADES[sel]
        blit_centro(tela, f_desc.render(desc_sel, True, cor_sel), y)

        y = ALTURA - 55
        blit_centro(tela, f_dica.render("SETAS - NAVEGAR  |  ENTER - JOGAR  |  ESC - VOLTAR", True, (80, 80, 80)), y)

        cobinha_menu.update()
        cobinha_menu.draw(tela)
        pygame.display.flip()


# ============================================================
# Helpers de fase
# ============================================================

def _gerar_itens(corpo, n, extras=None):
    """Gera n pares (posicao, fruta) sem colidir com corpo nem entre si."""
    ocupadas = set(corpo)
    if extras:
        ocupadas.update(extras)
    itens = []
    for _ in range(n):
        livres = [(c, l) for c in range(COLUNAS) for l in range(LINHAS) if (c, l) not in ocupadas]
        if not livres:
            break
        pos = random.choice(livres)
        ocupadas.add(pos)
        itens.append((pos, sortear_fruta()))
    return itens


def _flash_fase(tela, relogio, fase, num_frutas):
    """Overlay de transição entre fases (~1,8 s)."""
    overlay  = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    f_titulo = fonte(24)
    f_sub    = fonte(10)
    inicio   = pygame.time.get_ticks()
    while pygame.time.get_ticks() - inicio < 1800:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit(); sys.exit()
        tela.blit(overlay, (0, 0))
        blit_centro(tela, f_titulo.render(f"FASE {fase}!", True, LARANJA), 230)
        blit_centro(tela, f_sub.render("MAPA COMPLETADO!", True, AMARELO), 282)
        blit_centro(tela, f_sub.render(f"{num_frutas} FRUTAS POR VEZ", True, CINZA), 308)
        pygame.display.flip()
        relogio.tick(30)


# ============================================================
# Loop de uma partida  – retorna (ACAO, pontuacao)
# ============================================================

def partida(tela, relogio, f_hud, recorde_atual, scores, som_morte, som_mastigar,
            sprites_cab, img_corpo, dificuldade="medio", cobinha_menu=None):
    corpo        = [(COLUNAS // 2, LINHAS // 2)]
    direcao      = DIREITA
    prox_direcao = DIREITA
    pontuacao    = 0
    fase         = 1

    num_frutas = 1
    itens = _gerar_itens(corpo, num_frutas)

    # Tempo de spawn de cada fruta (pos -> ms), usado no modo dificil
    _t0 = pygame.time.get_ticks()
    fruta_spawn = {pos: _t0 for pos, _ in itens}

    # Bombas (apenas modo dificil) — lista de (pos, spawn_time)
    bombas        = []
    proximo_bomba = _t0 + random.randint(8000, 15000)

    pausado     = False
    opcao_pause = 0
    ver_score   = False

    while True:
        agora = pygame.time.get_ticks()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit(); sys.exit()

            if evento.type == pygame.KEYDOWN:
                if pausado:
                    if ver_score:
                        if evento.key in (pygame.K_RETURN, pygame.K_ESCAPE, pygame.K_p):
                            ver_score = False
                    else:
                        if evento.key == pygame.K_p:
                            pausado = False
                            parar_musica()
                        elif evento.key in (pygame.K_UP, pygame.K_w):
                            opcao_pause = (opcao_pause - 1) % len(_OPCOES_PAUSE)
                        elif evento.key in (pygame.K_DOWN, pygame.K_s):
                            opcao_pause = (opcao_pause + 1) % len(_OPCOES_PAUSE)
                        elif evento.key == pygame.K_RETURN:
                            if opcao_pause == 0:
                                ver_score = True
                            elif opcao_pause == 1:
                                parar_musica()
                                return (ACAO_REINICIAR, 0)
                            elif opcao_pause == 2:
                                parar_musica()
                                return (ACAO_MENU, 0)
                else:
                    if evento.key == pygame.K_p:
                        pausado     = True
                        opcao_pause = 0
                        ver_score   = False
                        tocar_musica_menu()
                    else:
                        nova_dir = TECLAS.get(evento.key)
                        if nova_dir and nova_dir != OPOSTO.get(direcao):
                            prox_direcao = nova_dir

        if pausado:
            if ver_score:
                desenhar_scores_pause(tela, scores, dificuldade)
            else:
                desenhar_pause(tela, opcao_pause, cobinha_menu)
            relogio.tick(30)
            continue

        # ---- Logica das bombas (modo dificil) ----
        if dificuldade == "dificil" and pontuacao >= BOMBA_MIN_SCORE:
            bombas = [(p, t) for p, t in bombas if agora - t < BOMBA_DURACAO]
            max_bombas = min(3, 1 + (pontuacao // 1000))
            if len(bombas) < max_bombas and agora >= proximo_bomba:
                pos_bombas = {p for p, _ in bombas}
                ocupadas   = set(corpo) | {p for p, _ in itens} | pos_bombas
                livres     = [(c, l) for c in range(COLUNAS) for l in range(LINHAS)
                              if (c, l) not in ocupadas]
                if livres:
                    bombas.append((random.choice(livres), agora))
                proximo_bomba = agora + random.randint(5000, 12000)

        # ---- Logica de movimento ----
        direcao = prox_direcao
        col, lin = corpo[0]
        nova_cabeca = (col + direcao[0], lin + direcao[1])

        if not (0 <= nova_cabeca[0] < COLUNAS and 0 <= nova_cabeca[1] < LINHAS):
            som_morte.play()
            return (ACAO_GAMEOVER, pontuacao)
        if nova_cabeca in corpo:
            som_morte.play()
            return (ACAO_GAMEOVER, pontuacao)
        if nova_cabeca in {p for p, _ in bombas}:
            som_morte.play()
            return (ACAO_GAMEOVER, pontuacao)

        corpo.insert(0, nova_cabeca)

        # ---- Mapa completo → proxima fase (nao existe em facil) ----
        if dificuldade != "facil" and len(corpo) == COLUNAS * LINHAS:
            fase += 1
            num_frutas = frutas_por_score(pontuacao)
            corpo      = [(COLUNAS // 2, LINHAS // 2)]
            direcao      = DIREITA
            prox_direcao = DIREITA
            bombas        = []
            proximo_bomba = agora + random.randint(8000, 15000)
            _flash_fase(tela, relogio, fase, num_frutas)
            itens = _gerar_itens(corpo, num_frutas)
            fruta_spawn = {pos: agora for pos, _ in itens}
            continue

        # ---- Verificar se comeu alguma fruta ----
        comeu = False
        for i, (pos, fruta) in enumerate(itens):
            if nova_cabeca == pos:
                som_mastigar.play()
                pontuacao += fruta["pontos"]
                pos_bombas = {p for p, _ in bombas}
                outras = {p for j, (p, _) in enumerate(itens) if j != i} | pos_bombas
                nova_pos = gerar_comida(corpo, outras)
                fruta_spawn.pop(pos, None)
                if nova_pos:
                    itens[i] = (nova_pos, sortear_fruta())
                    fruta_spawn[nova_pos] = agora
                if dificuldade != "facil":
                    nova_num = frutas_por_score(pontuacao)
                    if nova_num > num_frutas:
                        extras = {p for p, _ in itens} | pos_bombas
                        novos = _gerar_itens(corpo, nova_num - num_frutas, extras)
                        itens.extend(novos)
                        for p, _ in novos:
                            fruta_spawn[p] = agora
                        num_frutas = nova_num
                comeu = True
                break

        if not comeu:
            corpo.pop()

        # ---- Expirar frutas por tempo (modo dificil) ----
        if dificuldade == "dificil":
            pos_bombas = {p for p, _ in bombas}
            novos_itens = []
            for pos, fruta in itens:
                if agora - fruta_spawn.get(pos, agora) >= FRUTA_DURACAO:
                    fruta_spawn.pop(pos, None)
                    outras_ocup = {p for p, _ in itens if p != pos} | pos_bombas
                    nova_pos = gerar_comida(corpo, outras_ocup)
                    if nova_pos:
                        novos_itens.append((nova_pos, sortear_fruta()))
                        fruta_spawn[nova_pos] = agora
                else:
                    novos_itens.append((pos, fruta))
            itens = novos_itens
            num_frutas = len(itens)

        fps = FPS_BASE if dificuldade == "facil" else fps_atual(pontuacao)

        desenhar_fundo(tela)
        desenhar_cobra(tela, corpo, direcao, sprites_cab, img_corpo)
        for pos, fruta in itens:
            restante = FRUTA_DURACAO - (agora - fruta_spawn.get(pos, agora))
            if dificuldade != "dificil" or restante > 3000 or (agora // 300) % 2 == 0:
                desenhar_comida(tela, pos, fruta)
        for b_pos, b_spawn in bombas:
            desenhar_bomba_mapa(tela, b_pos, b_spawn)
        desenhar_hud(tela, f_hud, pontuacao, nivel_atual(pontuacao),
                     max(recorde_atual, pontuacao), fase, dificuldade)
        if pygame.key.get_pressed()[pygame.K_c]:
            desenhar_stats_overlay(tela, fps, len(corpo), len(itens))
        pygame.display.flip()
        relogio.tick(fps)


# ============================================================
# Ponto de entrada
# ============================================================

def main():
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    tela    = pygame.display.set_mode((LARGURA, ALTURA))
    relogio = pygame.time.Clock()
    pygame.display.set_caption("SNAKE")

    f_hud          = fonte(10)
    som_morte      = pygame.mixer.Sound(CAMINHO_SOM_MORTE)
    som_morte.set_volume(0.8)
    som_mastigar   = pygame.mixer.Sound(CAMINHO_SOM_MASTIGAR)
    som_mastigar.set_volume(0.7)
    som_recorde    = pygame.mixer.Sound(CAMINHO_SOM_RECORDE)
    som_recorde.set_volume(1.0)
    sprites_cab, img_corpo = criar_sprites_cobra(TAMANHO_CELULA)
    scores_medio   = carregar_scores(ARQUIVO_SCORES_MEDIO)
    scores_dificil = carregar_scores(ARQUIVO_SCORES_DIFICIL)
    cobinha_menu   = CobrinhaMenu()

    estado       = "menu"
    dificuldade  = "medio"
    pontuacao    = 0
    novo_recorde = False

    def scores_ativos():
        if dificuldade == "dificil":
            return scores_dificil
        elif dificuldade == "medio":
            return scores_medio
        return []  # facil nao tem ranking

    def arquivo_ativo():
        return ARQUIVO_SCORES_DIFICIL if dificuldade == "dificil" else ARQUIVO_SCORES_MEDIO

    while True:

        # ======== TELA INICIAL ========
        if estado == "menu":
            tocar_musica_menu()
            scores_menu = sorted(
                scores_medio + scores_dificil, key=lambda e: e[1], reverse=True
            )[:MAX_SCORES]
            while True:
                relogio.tick(30)
                desenhar_tela_inicial(tela, scores_menu)
                cobinha_menu.update()
                cobinha_menu.draw(tela)
                pygame.display.flip()

                saiu = False
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit(); sys.exit()
                    if evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_ESCAPE:
                            pygame.quit(); sys.exit()
                        if evento.key == pygame.K_RETURN:
                            saiu = True
                if saiu:
                    parar_musica()
                    estado = "selecionar"
                    break

        # ======== SELECAO DE DIFICULDADE ========
        if estado == "selecionar":
            resultado = selecionar_dificuldade(tela, relogio, cobinha_menu)
            if resultado is None:
                estado = "menu"
                continue
            dificuldade = resultado
            aplicar_dificuldade(dificuldade)
            sprites_cab, img_corpo = criar_sprites_cobra(TAMANHO_CELULA)
            estado = "jogando"

        # ======== PARTIDA ========
        if estado == "jogando":
            scores = scores_ativos()
            recorde_atual = scores[0][1] if scores else 0
            acao, pontuacao = partida(
                tela, relogio, f_hud, recorde_atual, scores,
                som_morte, som_mastigar, sprites_cab, img_corpo, dificuldade,
                cobinha_menu
            )

            if acao == ACAO_REINICIAR:
                estado = "selecionar"
                continue

            if acao == ACAO_MENU:
                estado = "menu"
                continue

            # ACAO_GAMEOVER — facil nao entra no ranking
            novo_recorde = False
            scores = scores_ativos()
            if dificuldade != "facil" and qualifica_top10(pontuacao, scores):
                eh_rec = (not scores) or (pontuacao > scores[0][1])
                nick   = capturar_nick(tela, pontuacao, eh_rec)
                scores, novo_recorde = atualizar_scores(pontuacao, nick, nivel_atual(pontuacao), scores, arquivo_ativo())
                if dificuldade == "dificil":
                    scores_dificil = scores
                else:
                    scores_medio = scores
                if novo_recorde:
                    som_recorde.play()
            estado = "gameover"

        # ======== GAME OVER ========
        if estado == "gameover":
            desenhar_game_over(tela, pontuacao, scores_ativos(), novo_recorde, dificuldade)
            while True:
                relogio.tick(30)
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit(); sys.exit()
                    if evento.type == pygame.KEYDOWN:
                        if evento.key == pygame.K_RETURN:
                            estado = "jogando"
                        elif evento.key == pygame.K_ESCAPE:
                            estado = "menu"
                if estado != "gameover":
                    break


if __name__ == "__main__":
    main()
