import random
import pygame
import sys
import json

from src.states.BaseState import BaseState
from src.combat_utils import roll_dice, resolve_attack, resolve_spell
from character import *

from src.constants import *
from src.resources import *

# WIDTH = 1280
# HEIGHT = 720
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

class VictoryState(BaseState):
    def __init__(self):
        super().__init__()

        self.bg_image = pygame.image.load("./graphics/Victory.png")
        self.bg_image = pygame.transform.scale(self.bg_image, (WIDTH + 4, HEIGHT + 4))

        self.gob_img = pygame.image.load("./graphics/Gob Thumb Shine.png")
        self.gob_img = pygame.transform.scale(self.gob_img, (300, 300))

        self.font_4s = pygame.font.Font('./fonts/Metamorphous-Regular.ttf', 12)
        self.font_sss = pygame.font.Font('./fonts/Metamorphous-Regular.ttf', 16)
        self.font_ss = pygame.font.Font('./fonts/Metamorphous-Regular.ttf', 20)
        self.font_s = pygame.font.Font('./fonts/Metamorphous-Regular.ttf', 24)
        self.font_shop = pygame.font.Font('./fonts/Metamorphous-Regular.ttf', 36)
        self.font_m = pygame.font.Font('./fonts/Metamorphous-Regular.ttf', 48)
        self.font_l = pygame.font.Font('./fonts/Metamorphous-Regular.ttf', 96)

        # self.font_ss2 = pygame.font.Font('./fonts/MedievalSharp-Regular.ttf', 20)
        # self.font_s2 = pygame.font.Font('./fonts/MedievalSharp-Regular.ttf', 24)
        # self.font_shop2 = pygame.font.Font('./fonts/MedievalSharp-Regular.ttf', 36)
        # self.font_m2 = pygame.font.Font('./fonts/MedievalSharp-Regular.ttf', 48)
        # self.font_l2 = pygame.font.Font('./fonts/MedievalSharp-Regular.ttf', 96)\

        self.money = 0

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    g_state_manager.Change('start', None)

    def render(self, screen):
        screen.blit(self.bg_image, (-2, -2))

        text = self.font_l.render(f'Victory!!', False, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

        screen.blit(self.gob_img, (WIDTH // 2 + 20, HEIGHT // 2 - 260))

        text = self.font_shop.render(f'Coins: {self.money}', False, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 300))
        screen.blit(text, text_rect)

        text = self.font_m.render(f'Press Enter key to return to main menu.', False, BLACK)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 200))
        screen.blit(text, text_rect)

    def Enter(self, params):
        gSounds['Stage1_music'].stop()
        gSounds['victory'].play(-1)

        for i in params:
            if i == "coins":
                self.money = params[i]

    def Exit(self):
        pass




