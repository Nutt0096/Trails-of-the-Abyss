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

class DefeatState(BaseState):
    def __init__(self):
        super().__init__()

        self.bg_image = pygame.image.load("./graphics/background.jpg")
        self.bg_image = pygame.transform.scale(self.bg_image, (WIDTH + 4, HEIGHT + 4))

        self.font_4s = pygame.font.Font('./fonts/Metamorphous-Regular.ttf', 12)
        self.font_sss = pygame.font.Font('./fonts/Metamorphous-Regular.ttf', 16)
        self.font_ss = pygame.font.Font('./fonts/Metamorphous-Regular.ttf', 20)
        self.font_s = pygame.font.Font('./fonts/Metamorphous-Regular.ttf', 24)
        self.font_shop = pygame.font.Font('./fonts/Metamorphous-Regular.ttf', 36)
        self.font_m = pygame.font.Font('./fonts/Metamorphous-Regular.ttf', 48)
        self.font_l = pygame.font.Font('./fonts/Metamorphous-Regular.ttf', 96)


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

        text = self.font_l.render(f'Defeat!!', False, RED)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)

        text = self.font_m.render(f'Press Enter key to return to main menu.', False, RED)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 200))
        screen.blit(text, text_rect)

    def Enter(self, params):
        gSounds['Stage1_music'].stop()
        gSounds['defeat'].play(-1)

    def Exit(self):
        pass




