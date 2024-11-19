from character.CharacterBase import Character

class Sorcerer(Character):
    def __init__(self):
        super().__init__(Name="sorcerer", STR=3, INT=9, CON=4, DEF=4, ACC=6, CHA=8)
        self.Weapons.append(
            {
                "name": "Dagger",
                "ACC": 4,
                "STR": 0,
                "damage_dice": 4,
                "dice": 1
            }
        )

        self.Spells = [
            {
                "name": "Magic Missile",
                "ACC": 4,
                "INT": 0,
                "damage_dice": 6,
                "dice": 1,
                "mana_cost": 5,
                "effect": "force_damage"
            },
            {
                "name": "Shield",
                "ACC": 0,
                "INT": 0,
                "damage_dice": 6,
                "dice": 1,
                "mana_cost": 7,
                "effect": None
            }
        ]

        self.load_animations(self.Name)

    def update(self, dt):
        # Example: Switch to casting spell animation when the mage is casting a spell
        self.current_animation = self.idle_animation
        super().update(dt)

