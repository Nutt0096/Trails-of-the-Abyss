from src.states.BaseState import BaseState
import pygame, sys

from src.constants import *
from src.resources import *

class StageState(BaseState):
    def __init__(self):
        super().__init__()
        self.bg_image = pygame.image.load("./graphics/Stages.png")
        self.bg_image = pygame.transform.scale(self.bg_image, (WIDTH, HEIGHT))
        self.stages = [] # False = uncleared, True = cleared
        self.team_characters = []
        self.coins = 0
        self.current_stage = 1
        self.bought_items = []
        self.bought_weapons = []
        self.bought_spells = []
        self.bought_armors = []

    def Enter(self, params):
        print(params)

        gSounds['Shop_music'].stop()
        gSounds['Select_music'].stop()
        gSounds['Stage1_music'].play(-1)

        for i in params:
            if i == "level":
                self.current_stage = params[i]
            elif i == "coins":
                self.coins = params[i]
            elif i == "stages":
                self.stages = params[i]
            elif i == "team":
                self.team_characters = params[i]
            elif i == "item-list":
                self.bought_items = params[i]
            elif i == "weapon-list":
                self.bought_weapons = params[i]
            elif i == "spell-list":
                self.bought_spells = params[i]
            elif i == "armor-list":
                self.bought_armors = params[i]

    def Exit(self):
        pass

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    g_state_manager.Change('start', None)
                elif event.key == pygame.K_RETURN:
                    # play stage
                    g_state_manager.Change('combat', {
                        'level': self.current_stage,
                        'team': self.team_characters,
                        'stages': self.stages,
                        'coins': self.coins,
                        'item-list': self.bought_items,
                        'weapon-list': self.bought_weapons,
                        'spell-list': self.bought_spells,
                        'armor-list': self.bought_armors
                    })
                    pass

    def render(self, screen):
        # Draw the background
        screen.blit(self.bg_image, (0, 0))

        # Draw "STAGE" title
        t_stage = gFonts['M_large'].render("STAGE", False, (255, 255, 255))
        rect = t_stage.get_rect(center=(WIDTH / 2, HEIGHT / 3 - 50))
        screen.blit(t_stage, rect)

        # Draw stage boxes
        stage_box_size = 50
        spacing = 20
        start_x = WIDTH / 2 - (len(self.stages) * (stage_box_size + spacing)) / 2
        y_pos = HEIGHT / 2

        for i, cleared in enumerate(self.stages):
            color = (0, 255, 0) if cleared else (255, 0, 0)  # Green for cleared, Red for uncleared
            rect = pygame.Rect(start_x + i * (stage_box_size + spacing), y_pos, stage_box_size, stage_box_size)
            pygame.draw.rect(screen, color, rect)

            # Draw outline to indicate the selected stage
            if i == self.current_stage - 1:
                pygame.draw.rect(screen, (255, 255, 255), rect, 3)  # White border for current selection

        # Display coin count
        t_coin = gFonts['M_small'].render(f"COIN: {self.coins}", False, (255, 255, 255))
        rect = t_coin.get_rect(bottomright=(WIDTH - 20, HEIGHT - 20))
        screen.blit(t_coin, rect)

