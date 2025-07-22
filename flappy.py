import pygame
import sys
import random
import os
from bot import BotPassaro

pygame.init()

LARGURA, ALTURA = 400, 600
TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Flappy Bird Simples")

AZUL_CEU = (135, 206, 250)
VERDE = (0, 200, 0)
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)

passaro_x = 50
passaro_y = ALTURA // 2
passaro_raio = 20
gravidade = 0.5
velocidade = 0

cano_largura = 60
cano_altura = random.randint(150, 400)
cano_espaco = 150
cano_x = LARGURA

clock = pygame.time.Clock()
fonte = pygame.font.SysFont(None, 48)

pontuacao = 0
pontuacao_maxima = 0

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_FILE = os.path.join(SCRIPT_DIR, "save.txt")

passaro_img = pygame.image.load(os.path.join(SCRIPT_DIR, "bird.png"))
passaro_img = pygame.transform.scale(passaro_img, (60, 40))

cano_img = pygame.image.load(os.path.join(SCRIPT_DIR, "cano.png"))
cano_img = pygame.transform.scale(cano_img, (cano_largura, 400))

nuvem_img = pygame.image.load(os.path.join(SCRIPT_DIR, "nuvem.png"))
nuvem_img = pygame.transform.scale(nuvem_img, (80, 50))

def carregar_pontuacao_maxima():
    global pontuacao_maxima
    if not os.path.isfile(SAVE_FILE):
        with open(SAVE_FILE, "w") as f:
            f.write("0")
        pontuacao_maxima = 0
    else:
        with open(SAVE_FILE, "r") as f:
            try:
                pontuacao_maxima = int(f.read())
            except:
                pontuacao_maxima = 0

def salvar_pontuacao_maxima(pontuacao_atual):
    global pontuacao_maxima
    if pontuacao_atual > pontuacao_maxima:
        pontuacao_maxima = pontuacao_atual
        with open(SAVE_FILE, "w") as f:
            f.write(str(pontuacao_maxima))

def desenha_texto(texto, cor, x, y):
    texto_render = fonte.render(texto, True, cor)
    ret = texto_render.get_rect(center=(x, y))
    TELA.blit(texto_render, ret)

def tela_game_over(pontuacao_final):
    salvar_pontuacao_maxima(pontuacao_final)
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = evento.pos
                if 150 <= mouse_x <= 250 and 500 <= mouse_y <= 550:
                    main()
        TELA.fill(AZUL_CEU)
        desenha_texto("Você perdeu!", PRETO, LARGURA // 2, ALTURA // 2 - 80)
        desenha_texto(f"Pontuação: {pontuacao_final}", PRETO, LARGURA // 2, ALTURA // 2 - 20)
        desenha_texto(f"Recorde: {pontuacao_maxima}", PRETO, LARGURA // 2, ALTURA // 2 + 40)
        botao = pygame.Rect(100, 500, 200, 50)
        pygame.draw.rect(TELA, VERDE, botao)
        desenha_texto("Reiniciar", BRANCO, LARGURA // 2, 525)
        pygame.display.update()
        clock.tick(30)

def colisao():
    if passaro_y - passaro_raio <= 0 or passaro_y + passaro_raio >= ALTURA:
        return True
    dentro_x = cano_x < passaro_x + passaro_raio < cano_x + cano_largura
    bateu_cano_superior = passaro_y - passaro_raio < cano_altura
    bateu_cano_inferior = passaro_y + passaro_raio > cano_altura + cano_espaco
    if dentro_x and (bateu_cano_superior or bateu_cano_inferior):
        return True
    return False

def atualizar_e_desenhar_nuvens(nuvens):
    for nuvem in nuvens:
        nuvem[0] -= 1
        if nuvem[0] < -80:
            nuvem[0] = LARGURA
            nuvem[1] = random.randint(20, 150)
        TELA.blit(nuvem_img, (nuvem[0], nuvem[1]))
    return nuvens

def atualizar_e_desenhar_nuvens_rapidas(nuvens_rapidas, pontuacao):
    if pontuacao >= 10 and random.random() < 0.01:
        y = random.randint(0, ALTURA - 60)
        velocidade = random.uniform(8, 12)
        nuvens_rapidas.append({"x": LARGURA, "y": y, "vel": velocidade})
    for nuvem in nuvens_rapidas[:]:
        nuvem["x"] -= nuvem["vel"]
        nuvem_img_red = pygame.transform.scale(nuvem_img, (500, 300))
        TELA.blit(nuvem_img_red, (nuvem["x"], nuvem["y"]))
        if nuvem["x"] < -500:
            nuvens_rapidas.remove(nuvem)
    return nuvens_rapidas

def main():
    global passaro_y, velocidade, cano_x, cano_altura, pontuacao
    carregar_pontuacao_maxima()
    nuvens_rapidas = []
    nuvens = [[random.randint(0, LARGURA), random.randint(20, 150)] for _ in range(5)]
    bot = BotPassaro.criar(passaro_img, LARGURA, ALTURA)
    passaro_y = ALTURA // 2
    velocidade = 0
    cano_x = LARGURA
    cano_altura = random.randint(150, 400)
    pontuacao = 0
    passou_cano = False
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    velocidade = -8
        velocidade += gravidade
        passaro_y += velocidade
        cano_x -= 3
        if cano_x < -cano_largura:
            cano_x = LARGURA
            cano_altura = random.randint(150, 400)
            passou_cano = False
        if not passou_cano and cano_x + cano_largura < passaro_x:
            pontuacao += 1
            passou_cano = True
        if colisao():
            tela_game_over(pontuacao)
        bot.atualizar(cano_altura, cano_espaco, cano_x, LARGURA)
        if bot.fora_da_tela(LARGURA):
            del bot
            bot = BotPassaro.criar(passaro_img, LARGURA, ALTURA)
        TELA.fill(AZUL_CEU)
        nuvens = atualizar_e_desenhar_nuvens(nuvens)
        angulo = max(-30, min(60, -velocidade * 3))
        passaro_rotacionado = pygame.transform.rotate(passaro_img, angulo)
        ret = passaro_rotacionado.get_rect(center=(passaro_x, int(passaro_y)))
        TELA.blit(passaro_rotacionado, ret)
        bot.desenhar(TELA)
        cano_topo = pygame.transform.scale(cano_img, (cano_largura, cano_altura))
        TELA.blit(cano_topo, (cano_x, 0))
        cano_base_altura = ALTURA - (cano_altura + cano_espaco)
        cano_base = pygame.transform.scale(
            pygame.transform.flip(cano_img, False, True),
            (cano_largura, cano_base_altura)
        )
        TELA.blit(cano_base, (cano_x, cano_altura + cano_espaco))
        nuvens_rapidas = atualizar_e_desenhar_nuvens_rapidas(nuvens_rapidas, pontuacao)
        desenha_texto(str(pontuacao), PRETO, LARGURA // 2, 30)
        desenha_texto(f"Recorde: {pontuacao_maxima}", PRETO, LARGURA - 100, 30)
        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
