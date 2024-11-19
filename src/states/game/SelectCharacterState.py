from src.states.BaseState import BaseState
from src.constants import *
from src.Dependencies import *
from character.Knight import Knight
from character.Mage import Mage
from character.Archer import Archer
from character.Sorcerer import Sorcerer
from character.Barbarian import Barbarian
from src.resources import character_image_list
import pygame, sys

class SelectCharacterState(BaseState):
    def __init__(self):
        super(SelectCharacterState, self).__init__()
        self.bg_image = pygame.image.load("./graphics/Entry.png")
        self.bg_image = pygame.transform.scale(self.bg_image, (WIDTH, HEIGHT))
        
        self.curr_character = 1
        self.team_character = []
        self.team_select_show = []
        self.character_select_num = []
        self.curr_num_char = 0
        self.current_stage = 1
        self.coins = 0
        self.inventory = []

        # Load arrow images for navigation
        self.l_arrow_image = sprite_collection["l_arrow"].image
        self.r_arrow_image = sprite_collection["r_arrow"].image

        # Animation control
        self.animation_time = 0  # Track time for animation updates
        self.animation_speed = 100  # In milliseconds, adjust as needed
        self.animation_frame = 0  # Current frame of animation

        # Load animations for character idle state (e.g., knight, mage, archer)
        self.knight_idle_animation = character_image_list[0]
        self.mage_idle_animation = character_image_list[1]
        self.archer_idle_animation = character_image_list[2]
        self.sorcerer_idle_animation = character_image_list[3]
        self.babarian_idle_animation = character_image_list[4]

        self.character_animations = {
            1: self.knight_idle_animation,
            2: self.mage_idle_animation,
            3: self.archer_idle_animation,
            4: self.sorcerer_idle_animation,
            5: self.babarian_idle_animation
        }

        self.num_character = len(self.character_animations)

    def Exit(self):
        pass

    def Enter(self, params):
        gSounds['Title_music'].stop()
        gSounds['Select_music'].play(-1)
    
        self.curr_character = 1
        self.team_character = []
        self.team_select_show = []
        self.character_select_num = []
        self.curr_num_char = 0
        self.current_stage = 1
        self.coins = 0
        self.inventory = []

         # Create instances of the characters
        self.knight = Knight()
        self.mage = Mage()
        self.archer = Archer()
        self.sorcerer = Sorcerer()
        self.babarian = Barbarian()

        # Map character id to character instance
        self.charter_sheet = {
            1: self.knight,
            2: self.mage,
            3: self.archer,
            4: self.sorcerer,
            5: self.babarian
        }

    def update(self, dt, events):
        # Update animation time (this controls how quickly we change frames)
        self.animation_time += dt
        if self.animation_time > self.animation_speed:
            self.animation_time = 0
            self.animation_frame = (self.animation_frame + 1) % 4  # Assuming the animation has 4 frames

        # Handle events (key presses for navigation and selection)
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if self.curr_character == 1:
                        gSounds['no-select'].play()
                    else:
                        gSounds['select'].play()
                        self.curr_character -= 1
                elif event.key == pygame.K_RIGHT:
                    if self.curr_character == self.num_character:
                        gSounds['no-select'].play()
                    else:
                        self.curr_character += 1
                        gSounds['select'].play()

                if event.key == pygame.K_ESCAPE:
                    gSounds['confirm'].play()
                    g_state_manager.Change('start', None)

                if event.key == pygame.K_RETURN:
                    gSounds['confirm'].play()

                    # Add the selected character to the team
                    if self.curr_character not in self.character_select_num:
                        self.character_select_num.append(self.curr_character)
                        self.team_select_show.append(self.charter_sheet.get(self.curr_character).Name)
                        self.team_character.append(self.charter_sheet.get(self.curr_character))
                        self.curr_num_char += 1

                        # If the team is full, transition to the next state (e.g., stage)
                        if self.curr_num_char == NUM_CHARACTER:
                            self.s_current_stage = self.current_stage
                            self.s_team_character = self.team_character

                            self.curr_num_char = 0
                            self.current_stage = 1
                            self.team_character = []
                            self.coins = 0

                            g_state_manager.Change('stage', {
                                'level': self.s_current_stage,
                                'team': self.s_team_character,
                                'stages': [False, False, False, False, False],
                                'item-list':[],
                                'weapon-list': [],
                                'spell-list': [],
                                'armor-list': [],
                                'coins': self.coins
                            })

                    # If already selected, remove the character from the team
                    elif self.curr_character in self.character_select_num:
                        for i in range(len(self.character_select_num)):
                            if self.character_select_num[i] == self.curr_character:
                                print("Removing character:", self.character_select_num[i])
                                self.character_select_num.pop(i)
                                self.team_select_show.pop(i)
                                self.team_character.pop(i)
                                self.curr_num_char -= 1
                                break

        # Update the current character's animation (pass dt to the update function)
        current_animation = self.character_animations[self.curr_character]
        current_animation.update(dt)

    def render(self, screen):
        screen.blit(self.bg_image, (0, 0))

        # Render instructions and text
        t_instruct = gFonts['M_medium'].render("Select your Character (left right)", False, (255, 255, 255))
        rect = t_instruct.get_rect(center=(WIDTH / 2, HEIGHT / 4))
        screen.blit(t_instruct, rect)

        t_enter = gFonts['M_small'].render("Press Enter to Select", False, (255, 255, 255))
        rect = t_enter.get_rect(center=(WIDTH / 2, HEIGHT / 3))
        screen.blit(t_enter, rect)

        t_number = gFonts['M_small'].render(f"Number of chosen: {self.curr_num_char}", False, (255, 255, 255))
        rect = t_number.get_rect(topright=(WIDTH - 50, 20))
        screen.blit(t_number, rect)

        t_team = gFonts['M_small'].render(f"Character chosen: {', '.join(map(str, self.team_select_show))}", False, (255, 255, 255))
        rect = t_team.get_rect(topright=(WIDTH - 50, 50))
        screen.blit(t_team, rect)

        # Get the current character's animation
        current_char = self.charter_sheet[self.curr_character]
        current_animation = self.character_animations[self.curr_character]

        # Display character's name and stats
        t_Name = gFonts['M_medium'].render(f"{current_char.Name}", False, (255, 255, 255))
        rect = t_Name.get_rect(center=(WIDTH / 2, HEIGHT / 3 + 50))
        screen.blit(t_Name, rect)

        stat_lines = [
            f"STR: {current_char.STR}  INT: {current_char.INT}  CON: {current_char.CON}",
            f"DEF: {current_char.DEF}  ACC: {current_char.ACC}  CHA: {current_char.CHA}"
        ]

        y_position = HEIGHT / 3 + 100
        for line in stat_lines:
            t_stat = gFonts['M_small'].render(line, False, (255, 255, 255))
            rect = t_stat.get_rect(center=(WIDTH / 2, y_position))
            screen.blit(t_stat, rect)
            y_position += 30

        # Render arrows for character navigation
        if self.curr_character == 1:
            self.l_arrow_image.set_alpha(128)

        screen.blit(self.l_arrow_image, (WIDTH / 4 - 72, HEIGHT - HEIGHT / 3))
        self.l_arrow_image.set_alpha(255)

        if self.curr_character == self.num_character:
            self.r_arrow_image.set_alpha(128)

        screen.blit(self.r_arrow_image, (WIDTH - WIDTH / 4, HEIGHT - HEIGHT / 3))
        self.r_arrow_image.set_alpha(255)
    
        # Render the current character's animation (current_frame is the image in the animation)
        rect = current_animation.image.get_rect(midtop=(WIDTH / 2 - 10, HEIGHT - HEIGHT / 3))
        screen.blit(current_animation.image, rect)