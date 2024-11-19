from src.Util import SpriteManager, Animation


class Character():
    def __init__(self, Name, STR, INT, CON, DEF, ACC, CHA):
        # Initialize base entity properties
        super().__init__()  # Pass the config to the EntityBase constructor
        self.Name = Name
        self.STR = STR  # Physical damage
        self.INT = INT  # Magical damage
        self.CON = CON  # Health pool
        self.DEF = DEF  # Dodge chance
        self.ACC = ACC  # Hit chance and critical chance
        self.CHA = CHA  # Resistance to debuffs, chance to inflict buffs
        self.HP = self.CON*10
        self.MP = self.INT*10

        self.cal_CON = self.CON
        self.cal_DEF = self.DEF
        self.cal_CHA = self.CHA

        self.Weapons = []
        self.Spells = []
        self.armors = [
            {
                "name": "no armor",
                "rarity": "no",
                "CON": 0,
                "DEF": 0,
                "CHA": 0
            }
        ]

        self.sprite_manager = SpriteManager()
        self.idle_animation = None
        self.position = (100, 100)

    def load_animations(self, Name):
        # Load animations (you can customize this for each character subclass)
        self.idle_animation = self.sprite_manager.spriteCollection.get(Name+"_idle").animation
        # for attack_sprite in attack_sprites:
        # self.attack_animation = self.sprite_manager.spriteCollection.get(attack_sprite).animation
        self.current_animation = self.idle_animation

    def addWeapon(self, weapon):
        self.Weapons.append(weapon)
    
    def addSpell(self, spell):
        self.Spells.append(spell)

    def addArmor(self, armor): 
        self.armors.append(armor)

    def checkarmors(self,armors):
        armor = armors[0]
        if armor["name"] == "no armor":
            pass
        else:
            self.cal_CON = self.CON + armor["CON"] 
            self.cal_DEF = self.DEF + armor["DEF"]
            self.cal_CHA = self.CHA + armor["CHA"]
            self.HP += armor["CON"]*10

    def update(self, dt):
        """Update the character's animation."""
        self.current_animation.update(dt)

    def show_stats(self):
        print(f"{self.Name}'s Stats:")
        print(f"STR: {self.STR}, INT: {self.INT}, CON: {self.CON}")
        print(f"DEF: {self.DEF}, ACC: {self.ACC}, CHA: {self.CHA}")

    def render(self, screen):
        """ Render the current animation. """
        frame_surface = self.current_animation.image
        screen.blit(frame_surface, self.position)
