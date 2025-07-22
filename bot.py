import pygame
import random
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_NOMES = os.path.join(SCRIPT_DIR, "nomes.txt")

class BotPassaro:
    def __init__(self, x, y, sprite, nome="BOT"):
        self.x = x
        self.y = y
        self.sprite_original = sprite
        self.sprite = self.colorir_sprite(sprite)
        self.velocidade = 0
        self.gravidade = 0.5
        self.pulo_forca = -8
        self.velocidade_horizontal = 3
        self.nome = nome
        self.fonte = pygame.font.SysFont(None, 24)

    def colorir_sprite(self, img):
        img = img.copy()
        r = random.uniform(0.5, 1.5)
        g = random.uniform(0.5, 1.5)
        b = random.uniform(0.5, 1.5)

        arr = pygame.surfarray.pixels3d(img)
        arr[:, :, 0] = (arr[:, :, 0] * r).clip(0, 255)
        arr[:, :, 1] = (arr[:, :, 1] * g).clip(0, 255)
        arr[:, :, 2] = (arr[:, :, 2] * b).clip(0, 255)
        del arr
        return img

    def atualizar(self, cano_altura, cano_espaco, cano_x, largura_tela):
        self.velocidade += self.gravidade
        self.y += self.velocidade

        altura_buraco = cano_altura + cano_espaco / 2
        if self.y > altura_buraco:
            self.velocidade = self.pulo_forca

        self.x += self.velocidade_horizontal

    def desenhar(self, tela):
        angulo = max(-30, min(60, -self.velocidade * 3))
        sprite_rot = pygame.transform.rotate(self.sprite, angulo)
        rect = sprite_rot.get_rect(center=(self.x, self.y))
        tela.blit(sprite_rot, rect)

        # Escreve o nome acima do bot
        texto = self.fonte.render(self.nome, True, (0, 0, 0))
        texto_rect = texto.get_rect(center=(self.x, self.y - 30))
        tela.blit(texto, texto_rect)

    def fora_da_tela(self, largura_tela):
        return self.x > largura_tela + 50

    @staticmethod
    def carregar_nomes():
        if os.path.exists(CAMINHO_NOMES):
            with open(CAMINHO_NOMES, "r", encoding="utf-8") as f:
                nomes = [linha.strip() for linha in f if linha.strip()]
            if nomes:
                return nomes
        return ["BOT"]

    @classmethod
    def criar(cls, sprite, largura_tela, altura_tela):
        nomes = cls.carregar_nomes()
        nome_escolhido = random.choice(nomes)
        return cls(-50, altura_tela // 2, sprite, nome_escolhido)
