from src.states.BaseState import BaseState
from src.combat_utils import *
from src.item_effects import apply_item_effect
from character import *
from monster.Monster import MONSTER_POOLS
from character.Monster import Monster
import pygame, sys, random, json

from src.constants import *
from src.resources import *

# CombatState Class
class CombatState(BaseState):
    def __init__(self):
        super().__init__()
        self.bg_image = pygame.image.load("./graphics/Dungeon.png")
        self.bg_image = pygame.transform.scale(self.bg_image, (WIDTH, HEIGHT))

        # Colors
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.BLACK = (0, 0, 0)
        self.GREEN = (0, 255, 0)
        self.PANEL_COLOR = (64, 32, 64)

        # <--- DUMMY DATA

        # Character and monster setup
        self.team_characters = []
        self.selected_weapon = None 
        self.selected_spell = None
        self.selected_item = None
        self.spell_positions = []
        self.selected_character = 0
        self.selected_monster = 0

        self.monsters = []

        # Item setup
        self.bought_items = []
        self.bought_weapons = []
        self.bought_spells = []
        self.bought_armors = []

        # character animation time
        self.animation_time = 0
        self.animation_speed = 100
        self.animation_frame = 0

        self.right_panel_show = 0 # initial as show item panel

        # Positioning
        self.character_positions = [(WIDTH/4, 150), (WIDTH/4, 250), (WIDTH/4, 350)]
        self.monster_positions = [(3*WIDTH/4, 150), (3*WIDTH/4, 250), (3*WIDTH/4, 350)]

        # Turns
        self.player_turn = True
        self.turn_order = self.team_characters + self.monsters
        self.current_turn_index = 0
        self.waiting_for_player_action = True

        # show dialogue
        self.show_text_char = True  # Flag to track whether the text is visible or not
        self.show_text_mon = False
        self.text_display_time = 1000  # 1000 milliseconds = 1 second
        self.start_time = pygame.time.get_ticks()  # Get the current time in milliseconds
        self.start_time_mon = 0
        self.show_dialogue_char = ""


    def handle_turn(self):
        """Handle the current entity's turn."""
        if self.waiting_for_player_action and self.player_turn:
            return  # Only wait for player input during the player's turn

        current_entity = self.turn_order[self.current_turn_index]
        print(f"Turn Index: {self.current_turn_index}, Entity: {current_entity.Name}")

        if not self.monsters:
            print("No monsters left!")
            return

        if self.player_turn:
            # Handle player's turn
            print(f"select character {current_entity}")
            if current_entity in self.team_characters:
                self.selected_character = self.team_characters.index(current_entity)
                target = self.monsters[self.selected_monster]

                print(f"{current_entity.Name}'s turn!")
                if self.right_panel_show == 1:  # Weapon panel selected
                    if self.selected_weapon is None:
                        print(f"{current_entity.Name} has no weapon selected!")
                        self.waiting_for_player_action = True
                        return

                    weapon = current_entity.Weapons[self.selected_weapon]
                    if self.monsters:  # Check if there are still monsters to target
                        target = self.monsters[self.selected_monster]
                        result = resolve_attack(current_entity, target, weapon)
                        self.show_dialogue_char = result
                        print(result)
                        

                        if target.HP <= 0:
                            print(f"{target.Name} is defeated!")
                            self.monsters.remove(target)
                            if not self.monsters:
                                self.selected_monster = 0  # Reset if no monsters remain
                            else:
                                self.selected_monster = min(self.selected_monster, len(self.monsters) - 1)

                elif self.right_panel_show == 2:  # Spell selected
                    if self.selected_spell is None:
                        print(f"No spell selected!")
                        self.waiting_for_player_action = True
                        return

                    spell = current_entity.Spells[self.selected_spell]
                    if self.monsters:  # Check if there are still monsters to target
                        target = self.monsters[self.selected_monster]
                        result = resolve_spell(current_entity, target, spell, self.monsters, self.selected_monster)
                        self.show_dialogue_char = result
                        print(result)

                        if target.HP <= 0:  # Adjust selection after a monster is defeated
                            print(f"{target.Name} is defeated!")
                            self.monsters.remove(target)
                            if not self.monsters:
                                self.selected_monster = 0  # Reset if no monsters remain
                            else:
                                self.selected_monster = min(self.selected_monster, len(self.monsters) - 1)

                elif self.right_panel_show == 3:  # Item selected
                    if self.selected_item is None:
                        print("No item selected!")
                        self.waiting_for_player_action = True
                        return
                    
                    item = self.bought_items[self.selected_item]
                    current_character = self.team_characters[self.selected_character]
                    target_enemy = self.monsters[self.selected_monster]

                    if "allies" in item["on use"]:
                        result = apply_item_effect(item, target=current_character, team=self.team_characters)
                    elif "enemies" in item["on use"]: 
                        result = apply_item_effect(item, enemies=self.monsters)
                    elif "enemy" in item["on use"] and "coins" in item["on use"]:
                        result = apply_item_effect(item, target=target_enemy, coins=self.coins)
                    elif "enemy" in item["on use"] and "yourself" in item["on use"]:
                        result = apply_item_effect(item, target=current_character, enemies=self.monsters)
                    elif "enemy" in item["on use"]:
                        result = apply_item_effect(item, target=target_enemy)
                    elif "coins" in item["on use"]:
                        result = apply_item_effect(item, target=current_character, coins=self.coins)
                    else:
                        result = apply_item_effect(item, target=current_character)
    
                    print(result)

                    self.bought_items.pop(self.selected_item)
                    self.selected_item = None
            
            if self.current_turn_index < len(self.team_characters):  # Ensure it's a character's turn
                self.selected_character = self.current_turn_index
                print(f"Pointer moved to character: {self.team_characters[self.selected_character].Name}")

        else:
            # Handle enemy's turn automatically
            if current_entity in self.monsters:
                target = random.choice(self.team_characters)
                result = resolve_attack_monster(current_entity, target)
                self.show_text_mon = True
                self.start_time_mon = pygame.time.get_ticks()
                print(result)

                # Remove defeated character if necessary
                if target.HP <= 0:
                    self.team_characters.remove(target)

        self.end_turn()

    def end_turn(self):
        """Advance to the next entity's turn."""
        # Rebuild the turn order dynamically
        self.turn_order = [entity for entity in self.team_characters if entity.HP > 0] + \
                      [entity for entity in self.monsters if entity.HP > 0]

        # Skip defeated entities
        while self.turn_order and (
            (self.current_turn_index < len(self.team_characters) and self.team_characters[self.current_turn_index].HP <= 0) or
            (self.current_turn_index >= len(self.team_characters) and 
            self.monsters and 
            self.current_turn_index - len(self.team_characters) < len(self.monsters) and
            self.monsters[self.current_turn_index - len(self.team_characters)].HP <= 0)
        ):
            self.current_turn_index = (self.current_turn_index + 1) % len(self.turn_order)

        # Increment turn index safely
        if self.turn_order:
            self.current_turn_index = (self.current_turn_index + 1) % len(self.turn_order)

            # Update selected_character for player's turn
            if self.current_turn_index < len(self.team_characters):  # If it's a player's turn
                self.selected_character = self.current_turn_index
                print(f"Pointer updated to character: {self.team_characters[self.selected_character].Name}")
            else:
                self.selected_character = None  # No character selected during monsters' turn
        else:
            self.current_turn_index = 0

        # Check if all enemies have acted
        if not self.player_turn and (not self.monsters or self.current_turn_index < len(self.team_characters)):
            self.player_turn = True  # Switch back to player's turn
            self.current_turn_index = 0  # Restart player turns

        # If all players have acted, switch to enemies' turn
        if self.player_turn and self.current_turn_index >= len(self.team_characters):
            self.player_turn = False
            self.current_turn_index = len(self.team_characters)  # Start enemy turns

        self.waiting_for_player_action = self.player_turn  # Only wait for action during player's turn

        # Check game over conditions
        if not self.monsters:  # If no monsters remain, transition to victory
            print("All monsters defeated! You win!")
            self.stages[self.current_stage - 1] = True
            self.current_stage += 1
            self.coins += 50

            if self.current_stage >= 6:  # set to 6, may change for debugging purpose
                g_state_manager.Change('victory', {'coins': self.coins})
            else:
                g_state_manager.Change('shop', {
                    'level': self.current_stage,
                    'team': self.team_characters,
                    'stages': self.stages,
                    'coins': self.coins,
                    'item-list': self.bought_items,
                    'weapon-list': self.bought_weapons,
                    'spell-list': self.bought_spells,
                    'armor-list': self.bought_armors
                })
        elif not self.team_characters:  # If no characters remain, transition to game over
            print("All characters defeated! Game over.")
            g_state_manager.Change('defeat', None)

    def process_player_action(self, action):
        """Process player inputs."""
        if action == "up":
            self.selected_monster = (self.selected_monster - 1) % len(self.monsters)
        elif action == "down":
            self.selected_monster = (self.selected_monster + 1) % len(self.monsters)
        elif action == "attack":
            self.waiting_for_player_action = False  # Execute the attack on the selected monster
    
    def create_monsters(self,monsters):
        mon_all = []
        for i in range( len(monsters)):
            Each_Monster = Monster(monsters[i])
            print("Monter:", Each_Monster)
            mon_all.append(Each_Monster)

        return mon_all
    
    def load_monsters_for_stage(self, stage):
        """Load monsters for the given stage."""
        if stage in MONSTER_POOLS:
            pool = MONSTER_POOLS[stage]
            num_monsters = min(3, len(pool))
            monster_config_list = random.sample(pool, num_monsters)
            self.monsters = self.create_monsters(monster_config_list)
        else:
            self.monsters = []

    def draw_health_bar(self, screen, x, y, health):
        pygame.draw.rect(screen, self.RED, (x, y, health, 10))

    def draw_mana_bar(self, screen, x, y, mana):
        pygame.draw.rect(screen, self.BLUE, (x, y, mana, 10))

    def display_characters_and_monsters(self, screen, selected_character, selected_monster):
        # Display characters
        for i, character in enumerate(self.team_characters):
            pos = self.character_positions[i]
            character.position = pos
            character.render(screen)
            self.draw_health_bar(screen, pos[0] - 40, pos[1] - 35, character.HP)
            self.draw_mana_bar(screen, pos[0] - 40, pos[1] - 15, character.MP)
            if i == selected_character:
                shift_amount = 20
                pygame.draw.polygon(screen, self.GREEN, [
                    (pos[0] + shift_amount, pos[1] - 50),  # Shift the first point
                    (pos[0] + shift_amount - 10, pos[1] - 60),  # Shift the second point
                    (pos[0] + shift_amount + 10, pos[1] - 60)   # Shift the third point
                ])

        # Display monsters
        for i, monster in enumerate(self.monsters):
            pos = self.monster_positions[i]
            monster.position = pos
            monster.render(screen)
            self.draw_health_bar(screen, pos[0] - 40, pos[1] - 35, monster.HP)
            if i == selected_monster:
                shift_amount = 30
                pygame.draw.polygon(screen, self.GREEN, [
                    (pos[0] + shift_amount, pos[1] - 50),  # Shift the first point
                    (pos[0] + shift_amount - 10, pos[1] - 60),  # Shift the second point
                    (pos[0] + shift_amount + 10, pos[1] - 60)   # Shift the third point
                ])

    def display_action_panel(self, screen, selected_character):
        if selected_character is None:
            return
    
        pygame.draw.rect(screen, self.PANEL_COLOR, (35, HEIGHT/2 + 50, 600, 300)) 
        current_character = self.team_characters[selected_character]
        char_text = gFonts['M_small'].render(f"{current_character.Name} HP: {current_character.HP} MP: {current_character.MP}", True, self.WHITE)
        screen.blit(char_text, (90, 430))

        # Action buttons
        weapon_button = pygame.draw.rect(screen, self.BLACK, (125, 520, 150, 50))
        spell_button = pygame.draw.rect(screen, self.BLACK, (375, 520, 150, 50))
        item_button = pygame.draw.rect(screen, self.BLACK, (125, 600, 150, 50))
        escape_button = pygame.draw.rect(screen, self.BLACK, (375, 600, 150, 50))
        
        screen.blit(gFonts['M_small'].render("WEAPON", True, self.WHITE), (135, 530))
        screen.blit(gFonts['M_small'].render("SPELL", True, self.WHITE), (385, 530))
        screen.blit(gFonts['M_small'].render("ITEM", True, self.WHITE), (135, 610))
        screen.blit(gFonts['M_small'].render("ESCAPE", True, self.WHITE), (385, 610))
        
        return weapon_button, spell_button, item_button, escape_button

    def display_right_panel(self, screen, bought_items):
        if self.right_panel_show == 1:  # Weapon panel
            if 0 <= self.current_turn_index < len(self.team_characters):  # Validate index
                pygame.draw.rect(screen, self.PANEL_COLOR, (645, HEIGHT / 2 + 50, 600, 300))
                char_text = gFonts['M_small'].render("WEAPONS", True, self.WHITE)
                screen.blit(char_text, (700, 430))

                # Show weapons for the current character
                current_character = self.team_characters[self.current_turn_index]
                for i, weapon in enumerate(current_character.Weapons):
                    color = self.GREEN if i == self.selected_weapon else self.WHITE
                    weapon_text = gFonts['M_small'].render(f"{weapon['name']} ACC: {weapon['ACC']} D: d{weapon['damage_dice']}", True, color)
                    screen.blit(weapon_text, (700, 470 + (i * 40)))

        elif self.right_panel_show == 2:  # Spell panel
            if self.player_turn and 0 <= self.current_turn_index < len(self.team_characters):
                pygame.draw.rect(screen, self.PANEL_COLOR, (645, HEIGHT / 2 + 50, 600, 300))
                char_text = gFonts['M_small'].render("SPELLS", True, self.WHITE)
                screen.blit(char_text, (700, 430))

                current_character = self.team_characters[self.current_turn_index]
                for i, spell in enumerate(current_character.Spells):
                    # Highlight selected spell
                    color = self.GREEN if i == self.selected_spell else self.WHITE
                    spell_text = gFonts['M_small'].render(f"{spell['name']} ACC: {spell['ACC']} D: d{spell['damage_dice']} MP: {spell['mana_cost']}", True, color)
                    screen.blit(spell_text, (700, 470 + (i * 40)))

                    if not hasattr(self, "spell_positions"):
                        self.spell_positions = []
                    if i >= len(self.spell_positions):
                        self.spell_positions.append(spell_text)

        elif self.right_panel_show == 3:  # Item panel
            if self.player_turn:
                pygame.draw.rect(screen, self.PANEL_COLOR, (645, HEIGHT / 2 + 50, 600, 300))
                char_text = gFonts['M_small'].render("ITEMS", True, self.WHITE)
                screen.blit(char_text, (700, 430))

                for i, item in enumerate(bought_items):
                    color = self.GREEN if i == self.selected_item else self.WHITE
                    item_text = gFonts['M_small'].render(item['name'], True, color)
                    screen.blit(item_text, (700, 470 + (i * 40)))

        elif self.right_panel_show == 4:  # Escape selected
            pygame.draw.rect(screen, self.PANEL_COLOR, (645, HEIGHT / 2 + 50, 600, 300))
            char_text = gFonts['M_small'].render("Are you sure?", True, self.WHITE)
            screen.blit(char_text, (700, 430))

            # Draw "I will come back" and "Just kidding" buttons
            comeback_button = pygame.draw.rect(screen, self.BLACK, (700, 520, 250, 50))
            just_kidding_button = pygame.draw.rect(screen, self.BLACK, (700, 600, 250, 50))

            screen.blit(gFonts['M_small'].render("I will come back! >:(", True, self.RED), (710, 530))
            screen.blit(gFonts['M_small'].render("Just kidding! >:P", True, self.GREEN), (710, 610))

            return comeback_button, just_kidding_button
        return None, None
    

    def weapon_update(self,team_characters,bought_weapons):
        for character in team_characters:
            for weapon in bought_weapons:
                if weapon['user'] == character.Name:
                    dice_str = weapon["dice"]
                    dice_parts = dice_str.split("d")

                    num_dice = int(dice_parts[0])
                    damage_dice = int(dice_parts[1])

                    character.addWeapon(
                        {
                            "name": weapon["name"],
                            "ACC": weapon["modify stats"]["ACC"],
                            "STR": weapon["modify stats"]["STR"],
                            "damage_dice": damage_dice,
                            "dice":num_dice,
                        })
    
    def spell_update(self,team_characters,bought_spells):
        for character in team_characters:
            for spell in bought_spells:
                if spell['user'] == character.Name:
                    dice_str = spell["dice"]
                    dice_parts = dice_str.split("d")

                    num_dice = int(dice_parts[0])
                    damage_dice = int(dice_parts[1])

                    character.addSpell(
                        {
                            "name": spell["name"],
                            "ACC": spell["modify stats"]["ACC"],
                            "INT": spell["modify stats"]["INT"],
                            "damage_dice": damage_dice,
                            "dice":num_dice,
                            "mana_cost": spell["mana"],
                            "effect": None
                        }
                        )
    
    def armor_update(self,team_characters,bought_armors):
        for character in team_characters:
            for armor in bought_armors:
                if armor['user'] == character.Name:
                    if not character.armors:
                        character.addArmor(
                            {
                            "name": armor["name"],
                            "rarity": armor["rarity"],
                            "CON": armor["modify stats"]["CON"],
                            "DEF": armor["modify stats"]["DEF"],
                            "CHA": armor["modify stats"]["CHA"]
                        }
                        )
                    else:
                        armor_rarity = {"no": 0,"common": 1,"rare": 2,"legendary": 3}
                        new_armor_rare = armor_rarity[armor["rarity"]]
                        old_armor_rare = armor_rarity[character.armors[0]["rarity"]]

                        if old_armor_rare < new_armor_rare:
                            character.armors.pop(0)

                            character.addArmor(
                                {
                                    "name": armor["name"],
                                    "rarity": armor["rarity"],
                                    "CON": armor["modify stats"]["CON"],
                                    "DEF": armor["modify stats"]["DEF"],
                                    "CHA": armor["modify stats"]["CHA"]
                                }
                            )
                        else: # old_armor_rare > new_armor_rare or old_armor_rare == new_armor_rare
                            pass



    def Enter(self, params):
        self.selected_weapon = None 
        self.selected_spell = None
        self.selected_item = None
        self.spell_positions = []
        self.selected_character = 0
        self.selected_monster = 0

        for i in params:
            if i == "level":
                self.current_stage = params[i]
                self.load_monsters_for_stage(self.current_stage)
            elif i == "team":
                self.team_characters = params[i]
            elif i == "stages":
                self.stages = params[i]
            elif i == "coins":
                self.coins = params[i]
            elif i == "item-list":
                self.bought_items = params[i]
            elif i == "weapon-list":
                self.bought_weapons = params[i]
            elif i == "spell-list":
                self.bought_spells = params[i]
            elif i == "armor-list":
                self.bought_armors = params[i]

        self.weapon_update(self.team_characters,self.bought_weapons)
        self.spell_update(self.team_characters,self.bought_spells)
        self.armor_update(self.team_characters,self.bought_armors)

        for character in self.team_characters:
            character.checkarmors(character.armors)
        
        self.bought_weapons = []
        self.bought_spells = []
        self.bought_armors = []

        self.player_turn = True
        self.turn_order = self.team_characters + self.monsters
        self.current_turn_index = 0
        self.waiting_for_player_action = True

        # time dialogue
        self.show_text_char = True
        self.show_text_mon = False
        self.start_time = pygame.time.get_ticks()
        self.show_dialogue_char = ""
   
    def update(self, dt, events):
        current_time = pygame.time.get_ticks()
        self.dialogue_start_time = pygame.time.get_ticks()

        self.animation_time += dt
        if self.animation_time > self.animation_speed:
            self.animation_time = 0
            self.animation_frame = (self.animation_frame + 1) % 4

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    g_state_manager.Change('stage', None)  # Exit to stage
                elif event.key == pygame.K_RETURN:
                    self.process_player_action("attack")
                    self.show_text_char = True  # Make text visible again
                    self.start_time = pygame.time.get_ticks()

                # Navigate monsters
                if event.key == pygame.K_UP:
                    self.process_player_action("up")
                elif event.key == pygame.K_DOWN:
                    self.process_player_action("down")
                
                # Reset right panel display when arrow keys are pressed
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    self.right_panel_show = 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                weapon_button, spell_button, item_button, escape_button = self.display_action_panel(
                    g_state_manager.screen, self.selected_character
                )
                if weapon_button.collidepoint(event.pos):
                    print("Weapon selected")
                    self.right_panel_show = 1
                    self.selected_weapon = None
                elif spell_button.collidepoint(event.pos):
                    print("Spell selected")
                    self.right_panel_show = 2
                    self.selected_spell = None
                elif item_button.collidepoint(event.pos):
                    print("Item selected")
                    self.right_panel_show = 3
                    self.selected_item = None
                elif escape_button.collidepoint(event.pos):
                    print("Escape selected")
                    self.right_panel_show = 4

                if self.right_panel_show == 1:
                    current_character = self.team_characters[self.selected_character]
                    for i, weapon in enumerate(current_character.Weapons):
                        # Check if the click is within this weapon's row
                        weapon_rect = pygame.Rect(700, 470 + (i * 40), 400, 30)  # Adjust as needed
                        if weapon_rect.collidepoint(event.pos):
                            self.selected_weapon = i
                            print(f"Selected weapon: {current_character.Weapons[i]['name']}")

                if self.right_panel_show == 2:  # Spell panel is open
                    current_character = self.team_characters[self.current_turn_index]
                    for i, spell in enumerate(self.spell_positions):
                        spell_rect = pygame.Rect(700, 470 + (i * 40), 400, 30)
                        if spell_rect.collidepoint(event.pos):
                            self.selected_spell = i
                            print(f"Selected spell: {current_character.Spells[i]['name']}")

                if self.right_panel_show == 3:  # Item panel is open
                    for i, item in enumerate(self.bought_items):
                        item_rect = pygame.Rect(700, 470 + (i * 40), 400, 30)
                        if item_rect.collidepoint(event.pos):
                            self.selected_item = i
                            print(f"Selected item: {item['name']} | Description: {item['description']}")

                 # Handle the "I will come back" and "Just kidding" buttons
                comeback_button, just_kidding_button = self.display_right_panel(
                    g_state_manager.screen, self.bought_items
                )
                if comeback_button and comeback_button.collidepoint(event.pos):
                    print("Returning to stage state")
                    g_state_manager.Change('start', None)  # Go back to stage state
                elif just_kidding_button and just_kidding_button.collidepoint(event.pos):
                    print("Returning to item selection")
                    self.right_panel_show = 0  # Go back to item display
        
        self.handle_turn()

        if current_time - self.start_time >= self.text_display_time and self.show_text_char:
            self.show_text_char = False
        
        if current_time - self.start_time_mon >= 1000 and self.show_text_mon:
            self.show_text_mon = False
        
        # self.show_time_mon = pygame.time.get_ticks()

        for character in self.team_characters:
            character.update(dt)

        for monster in self.monsters:
            monster.update(dt)

    def render(self, screen):
        screen.blit(self.bg_image, (0, 0))  # Draw background image
        if self.show_text_char:
            text = gFonts['M_small'].render(self.show_dialogue_char, True, self.RED)
            screen.blit(text, (WIDTH//4 + 50 - text.get_width()//2 , 15)) 

        if self.show_text_mon:
            text = gFonts['M_small'].render("All monsters Attack!", True, self.RED)
            screen.blit(text, (WIDTH - WIDTH//5 - 30 - text.get_width()//2, 15))
        
        self.display_characters_and_monsters(screen, self.selected_character, self.selected_monster)
        self.display_action_panel(screen, self.selected_character)  # Update action panel
        self.display_right_panel(screen, self.bought_items)  # Update right panel

    def Exit(self):
        # Clean up when leaving the combat state
        pass
