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

class ShopState(BaseState):
    def __init__(self):
        super().__init__()
        # pygame.init()
        # self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.bg_image = pygame.image.load("./graphics/ShopBG.jpg")
        self.bg_image = pygame.transform.scale(self.bg_image, (WIDTH + 4, HEIGHT + 4))

        self.gob_img = pygame.image.load("./graphics/Gob the Seller.png")
        self.gob_img = pygame.transform.scale(self.gob_img, (300, 300))

        self.gob_img_macho = pygame.image.load("./graphics/Gob the Seller Macho2.png")
        self.gob_img_macho = pygame.transform.scale(self.gob_img_macho, (300, 300))

        self.font_4s = pygame.font.Font('./fonts/Metamorphous-Regular.ttf', 12)
        self.font_sss = pygame.font.Font('./fonts/Metamorphous-Regular.ttf', 16)
        self.font_ss = pygame.font.Font('./fonts/Metamorphous-Regular.ttf', 20)
        self.font_s = pygame.font.Font('./fonts/Metamorphous-Regular.ttf', 24)
        self.font_shop = pygame.font.Font('./fonts/Metamorphous-Regular.ttf', 36)
        self.font_m = pygame.font.Font('./fonts/Metamorphous-Regular.ttf', 48)
        self.font_l = pygame.font.Font('./fonts/Metamorphous-Regular.ttf', 96)

        self.font_ss2 = pygame.font.Font('./fonts/MedievalSharp-Regular.ttf', 20)
        self.font_s2 = pygame.font.Font('./fonts/MedievalSharp-Regular.ttf', 24)
        self.font_shop2 = pygame.font.Font('./fonts/MedievalSharp-Regular.ttf', 36)
        self.font_m2 = pygame.font.Font('./fonts/MedievalSharp-Regular.ttf', 48)
        self.font_l2 = pygame.font.Font('./fonts/MedievalSharp-Regular.ttf', 96)

        self.money = 0  # get value instead when combined
        self.bought_items = []
        self.bought_weapons = []
        self.bought_spells = []
        self.bought_armors = []

        self.select_x = 0
        self.select_y = 0

        self.confirm_window = False
        self.confirm_window_type = -1

        self.gob_dialogue = False
        self.gob_dialogue_timer = 0
        self.gob_dialogue_type = -1

        with open('./items.json', 'r') as f:
            self.template = json.load(f)

        self.shop_list = [[{}, {}, {}, {}],
                          [{}, {}, {}, {}],
                          [{}, {}, {}, {}],
                          [{}, {}, {}, {}]]

    def update(self, dt, events):
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if self.confirm_window:
                    if event.key == pygame.K_z:
                        if self.confirm_window_type == 0:
                            # change to next stage when combined with other state
                            # pygame.quit()
                            # sys.exit()
                            self.confirm_window = False
                            self.confirm_window_type = -1
                            g_state_manager.Change('stage', {
                                'level': self.current_stage,
                                'team': self.team_characters,
                                'stages': self.stages,
                                'coins': self.money,
                                'item-list': self.bought_items,
                                'weapon-list': self.bought_weapons,
                                'spell-list': self.bought_spells,
                                'armor-list': self.bought_armors
                            })
                        elif self.confirm_window_type == 1:
                            if self.money >= self.get_selected()["cost"]:
                                self.money -= self.get_selected()["cost"]
                                if self.select_y == 0:
                                    self.bought_items.append(self.get_selected())
                                elif self.select_y == 1:
                                    self.bought_weapons.append(self.get_selected())
                                    self.shop_list[self.select_y][self.select_x] = None
                                elif self.select_y == 2:
                                    self.bought_spells.append(self.get_selected())
                                    self.shop_list[self.select_y][self.select_x] = None
                                elif self.select_y == 3:
                                    self.bought_armors.append(self.get_selected())
                                    self.shop_list[self.select_y][self.select_x] = None
                                # print(len(self.bought_items))
                                # print(len(self.bought_weapons))
                                # print(len(self.bought_spells))
                                # print(len(self.bought_armors))
                                self.gob_dialogue = True
                                self.gob_dialogue_type = 0
                            else:
                                self.gob_dialogue = True
                                self.gob_dialogue_type = 1
                            self.confirm_window = False
                            self.confirm_window_type = -1
                    if event.key == pygame.K_x:
                        self.confirm_window = False
                        self.confirm_window_type = -1
                else:
                    if event.key == pygame.K_UP:
                        self.select_y -= 1
                    if event.key == pygame.K_DOWN:
                        self.select_y += 1
                    if event.key == pygame.K_LEFT:
                        self.select_x -= 1
                    if event.key == pygame.K_RIGHT:
                        self.select_x += 1
                    if event.key == pygame.K_z:
                        if self.get_selected() is not None:
                            self.confirm_window = True
                            self.confirm_window_type = 1
                            self.gob_dialogue_timer = 0
                            self.gob_dialogue = False
                    if event.key == pygame.K_x:
                        self.confirm_window = True
                        self.confirm_window_type = 0
                        self.gob_dialogue_timer = 0
                        self.gob_dialogue = False

                if self.select_x < 0:
                    self.select_x = 3
                if self.select_y < 0:
                    self.select_y = 3
                if self.select_x == 4:
                    self.select_x = 0
                if self.select_y == 4:
                    self.select_y = 0

        if self.gob_dialogue:
            self.gob_dialogue_timer += dt
            if self.gob_dialogue_timer >= 1:
                self.gob_dialogue_timer = 0
                self.gob_dialogue = False
                self.gob_dialogue_type = -1

    def render(self, screen):
        screen.blit(self.bg_image, (-2, -2))

        # Shop Panel
        s = pygame.Surface((600, 600), pygame.SRCALPHA)
        s.fill((255, 255, 255, 200))
        screen.blit(s, (60, 60))
        pygame.draw.rect(screen, BLACK, pygame.Rect(60, 60, 600, 600), 2)

        # Item Panel
        s = pygame.Surface((600, 50), pygame.SRCALPHA)
        s.fill((255, 255, 0, 80))
        screen.blit(s, (60, 60))
        pygame.draw.rect(screen, BLACK, pygame.Rect(60, 60, 600, 50), 2)
        shop_text = self.font_s.render(f'Item', False, BLACK)
        text_rect = shop_text.get_rect(topleft=(70, 70))
        screen.blit(shop_text, text_rect)

        # weapon Panel
        s = pygame.Surface((600, 50), pygame.SRCALPHA)
        s.fill((255, 0, 0, 80))
        screen.blit(s, (60, 60+150))
        pygame.draw.rect(screen, BLACK, pygame.Rect(60, 60+150, 600, 50), 2)
        shop_text = self.font_s.render(f'Weapon', False, BLACK)
        text_rect = shop_text.get_rect(topleft=(70, 70+150))
        screen.blit(shop_text, text_rect)

        # Spell Panal
        s = pygame.Surface((600, 50), pygame.SRCALPHA)
        s.fill((0, 0, 255, 80))
        screen.blit(s, (60, 60 + 300))
        pygame.draw.rect(screen, BLACK, pygame.Rect(60, 60+300, 600, 50), 2)
        shop_text = self.font_s.render(f'Spell', False, BLACK)
        text_rect = shop_text.get_rect(topleft=(70, 70+300))
        screen.blit(shop_text, text_rect)

        # Armor Panel
        s = pygame.Surface((600, 50), pygame.SRCALPHA)
        s.fill((0, 0, 0, 80))
        screen.blit(s, (60, 60 + 450))
        pygame.draw.rect(screen, BLACK, pygame.Rect(60, 60+450, 600, 50), 2)
        shop_text = self.font_s.render(f'Armor', False, BLACK)
        text_rect = shop_text.get_rect(topleft=(70, 70+450))
        screen.blit(shop_text, text_rect)

        # Loop Items
        for y in range(0, 4):
            for x in range(0, 4):
                pygame.draw.rect(screen, BLACK, pygame.Rect(125 + 130*x, 120 + 150*y, 80, 80), 2)
                if self.shop_list[y][x] is None:
                    # Cross
                    pygame.draw.line(screen, RED, (125 + 130*x, 120 + 150*y), (125 + 130*x + 80, 120 + 150*y + 80), 4)
                    pygame.draw.line(screen, RED, (125 + 130*x, 120 + 150*y + 80), (125 + 130*x + 80, 120 + 150*y), 4)
                else:
                    text = self.font_m.render(f'{self.shop_list[y][x]["name"][0]}', False, BLACK)
                    text_rect = text.get_rect(center=(125 + 130 * x + 40, 120 + 150 * y + 40))
                    screen.blit(text, text_rect)
                if x == self.select_x and y == self.select_y:
                    pygame.draw.rect(screen, (200, 200, 0), pygame.Rect(125 + 130 * x, 120 + 150 * y, 80, 80), 4)

        # Gob Image
        if self.gob_dialogue and self.gob_dialogue_type == 1:
            screen.blit(self.gob_img_macho, (820, 60))
        else:
            screen.blit(self.gob_img, (820, 60))

        # Info Panel
        s = pygame.Surface((500, 260), pygame.SRCALPHA)
        s.fill((255, 255, 255, 200))
        screen.blit(s, (720, 400))
        pygame.draw.rect(screen, BLACK, pygame.Rect(720, 400, 500, 260), 2)

        # Item Info
        if self.get_selected() is not None:
            text = self.font_s.render(f'{self.get_selected()["name"]}', False, BLACK)
            text_rect = text.get_rect(topleft=(740, 415))
            screen.blit(text, text_rect)

            if len(self.get_selected()["description"]) >= 42:
                x = self.get_selected()["description"].find(' ', 60)
                if x == -1:
                    text = self.font_4s.render(f'{self.get_selected()["description"]}',
                                                False, BLACK)
                    text_rect = text.get_rect(topleft=(740, 465))
                    screen.blit(text, text_rect)
                else:
                    text = self.font_4s.render(f'{self.get_selected()["description"][:x+1]}',
                                                False, BLACK)
                    text_rect = text.get_rect(topleft=(740, 455))
                    screen.blit(text, text_rect)
                    text = self.font_4s.render(f'{self.get_selected()["description"][x+1:]}',
                                                False, BLACK)
                    text_rect = text.get_rect(topleft=(740, 475))
                    screen.blit(text, text_rect)
            else:
                text = self.font_ss.render(f'{self.get_selected()["description"]}',
                                           False, BLACK)
                text_rect = text.get_rect(topleft=(740, 460))
                screen.blit(text, text_rect)

            text = self.font_ss.render(f'Cost: ${self.get_selected()["cost"]}', False, BLACK)
            text_rect = text.get_rect(topleft=(740, 500))
            screen.blit(text, text_rect)

            # Rarity may not be used now :(
            text = self.font_ss.render(f'Rarity: {self.get_selected()["rarity"]}', False, BLACK)
            text_rect = text.get_rect(topleft=(740, 530))
            screen.blit(text, text_rect)

            # text = self.font_ss.render(f'User: {self.get_selected()["user"]}', False, BLACK)
            # text_rect = text.get_rect(topleft=(740, 540))
            # screen.blit(text, text_rect)

            if self.get_selected() in self.template['weapons']:
                # User
                text = self.font_ss.render(f'User: {self.get_selected()["user"]}', False, BLACK)
                text_rect = text.get_rect(topleft=(740, 560))
                screen.blit(text, text_rect)

                # Dice and other stats
                text = self.font_ss.render(
                    f'Dice: {self.get_selected()["dice"]}', False, BLACK)
                text_rect = text.get_rect(topleft=(980, 500))
                screen.blit(text, text_rect)
                text = self.font_ss.render(
                    f'STR: {self.get_selected()["modify stats"]["STR"]}', False, BLACK)
                text_rect = text.get_rect(topleft=(980, 530))
                screen.blit(text, text_rect)
                text = self.font_ss.render(
                    f'ACC: {self.get_selected()["modify stats"]["ACC"]}', False, BLACK)
                text_rect = text.get_rect(topleft=(980, 560))
                screen.blit(text, text_rect)

            elif self.get_selected() in self.template['spells']:
                # User
                text = self.font_ss.render(f'User: {self.get_selected()["user"]}', False, BLACK)
                text_rect = text.get_rect(topleft=(740, 560))
                screen.blit(text, text_rect)

                # Dice and other stats
                text = self.font_ss.render(
                    f'Dice: {self.get_selected()["dice"]}', False, BLACK)
                text_rect = text.get_rect(topleft=(980, 500))
                screen.blit(text, text_rect)
                text = self.font_ss.render(
                    f'INT: {self.get_selected()["modify stats"]["INT"]}', False, BLACK)
                text_rect = text.get_rect(topleft=(980, 530))
                screen.blit(text, text_rect)
                text = self.font_ss.render(
                    f'ACC: {self.get_selected()["modify stats"]["ACC"]}', False, BLACK)
                text_rect = text.get_rect(topleft=(980, 560))
                screen.blit(text, text_rect)
                text = self.font_ss.render(
                    f'Mana: {self.get_selected()["mana"]}', False, BLACK)
                text_rect = text.get_rect(topleft=(980, 590))
                screen.blit(text, text_rect)
            elif self.get_selected() in self.template['armors']:
                # User
                text = self.font_ss.render(f'User: {self.get_selected()["user"]}', False, BLACK)
                text_rect = text.get_rect(topleft=(740, 560))
                screen.blit(text, text_rect)

                # Other stats
                text = self.font_ss.render(
                    f'CON: {self.get_selected()["modify stats"]["CON"]}', False, BLACK)
                text_rect = text.get_rect(topleft=(980, 500))
                screen.blit(text, text_rect)
                text = self.font_ss.render(
                    f'DEF: {self.get_selected()["modify stats"]["DEF"]}', False, BLACK)
                text_rect = text.get_rect(topleft=(980, 530))
                screen.blit(text, text_rect)
                text = self.font_ss.render(
                    f'CHA: {self.get_selected()["modify stats"]["CHA"]}', False, BLACK)
                text_rect = text.get_rect(topleft=(980, 560))
                screen.blit(text, text_rect)

        # Display Money
        money_text = self.font_m2.render(f'${self.money}', False, BLACK)
        text_rect = money_text.get_rect(bottomleft=(740, 650))
        screen.blit(money_text, text_rect)

        # key_text = self.font_s.render(f'Z: Buy Item    X: Next Stage', False, WHITE)
        # text_rect = key_text.get_rect(topleft=(80, 680))
        # screen.blit(key_text, text_rect)

        key_text = self.font_s.render(f'Z: Buy Item  X: Next Stage', False, BLACK)
        text_rect = key_text.get_rect(bottomright=(1200, 650))
        screen.blit(key_text, text_rect)

        if self.confirm_window:
            pygame.draw.rect(screen, WHITE, pygame.Rect(WIDTH // 2 - 310, HEIGHT // 2 - 120, 620, 240))
            pygame.draw.rect(screen, BLACK, pygame.Rect(WIDTH // 2 - 310, HEIGHT // 2 - 120, 620, 240), 4)

            pygame.draw.rect(screen, BLACK, pygame.Rect(WIDTH // 2 - 300 + 40, HEIGHT // 2 - 120 + 160, 240, 60), 4)
            text = self.font_shop.render(f'Z : Confirm', False, BLACK)
            text_rect = text.get_rect(center=(WIDTH // 2 - 300 + 40 + 120, HEIGHT // 2 - 120 + 160 + 30))
            screen.blit(text, text_rect)

            pygame.draw.rect(screen, BLACK, pygame.Rect(WIDTH // 2 - 300 + 320, HEIGHT // 2 - 120 + 160, 240, 60),4)
            text = self.font_shop.render(f'X : Cancel', False, BLACK)
            text_rect = text.get_rect(center=(WIDTH // 2 - 300 + 320 + 120, HEIGHT // 2 - 120 + 160 + 30))
            screen.blit(text, text_rect)

            if self.confirm_window_type == 0:
                text = self.font_shop.render(f'Are you sure to continue?', False, BLACK)
                text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))
                screen.blit(text, text_rect)
            elif self.confirm_window_type == 1:
                text = self.font_shop.render(f'Are you sure to buy', False, BLACK)
                text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))
                screen.blit(text, text_rect)
                text = self.font_shop.render(f'{self.get_selected()["name"]}?', False, BLACK)
                text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 20))
                screen.blit(text, text_rect)


        if self.gob_dialogue:
            # pygame.draw.rect(screen, WHITE, pygame.Rect(WIDTH // 2 - 300, HEIGHT // 2 - 50, 600, 100))
            s = pygame.Surface((500, 60), pygame.SRCALPHA)
            s.fill((255, 255, 255, 200))
            screen.blit(s, (720, 300))
            pygame.draw.rect(screen, BLACK, pygame.Rect(720, 300, 500, 60), 2)
            if self.gob_dialogue_type == 0:
                text = self.font_s.render(f'Thanks for buying!', False, BLACK)
                text_rect = text.get_rect(center=(720 + 500 // 2, 300 + 60 // 2))
                screen.blit(text, text_rect)
            elif self.gob_dialogue_type == 1:
                text = self.font_s.render(f'You don\'t have enough money!', False, BLACK)
                text_rect = text.get_rect(center=(720 + 500 // 2, 300 + 60 // 2))
                screen.blit(text, text_rect)

    def Enter(self, params):
        gSounds['Stage1_music'].stop()
        gSounds['Shop_music'].play(-1)

        self.shop_list = self.random_shop()

        for i in params:
            if i == "level":
                self.current_stage = params[i]
            elif i == "team":
                self.team_characters = params[i]
            elif i == "stages":
                self.stages = params[i]
            elif i == "coins":
                self.money = params[i]

        self.bought_items = []
        self.bought_weapons = []
        self.bought_spells = []
        self.bought_armors = []

    def Exit(self):
        pass

    def random_shop(self):
        return_shop = [[{}, {}, {}, {}],
                       [{}, {}, {}, {}],
                       [{}, {}, {}, {}],
                       [{}, {}, {}, {}]]
        return_shop[0] = random.sample(self.template['items'][1:], k=4)
        return_shop[1] = random.sample(self.template['weapons'][1:], k=4)
        return_shop[2] = random.sample(self.template['spells'][1:], k=4)
        return_shop[3] = random.sample(self.template['armors'][1:], k=4)

        return return_shop

    def get_selected(self):
        return self.shop_list[self.select_y][self.select_x]


# if __name__ == '__main__':
#     main = ShopState()
#
#     clock = pygame.time.Clock()
#
#     while True:
#         pygame.display.set_caption("Shop State : {:d} FPS".format(int(clock.get_fps())))
#
#         dt = clock.tick(60)/1000.0
#
#         events = pygame.event.get()
#         main.update(dt, events)
#         main.render()
#
#         pygame.display.update()
