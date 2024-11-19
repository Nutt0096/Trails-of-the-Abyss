from character.CharacterBase import Character

class Archer(Character):
    def __init__(self):
        super().__init__(Name="archer", STR=6, INT=4, CON=6, DEF=6, ACC=8, CHA=5)
        self.Weapons.append(
            {
                    "name": "Short Bow",
                    "ACC": 4,
                    "STR": 0,
                    "damage_dice": 6,
                    "dice": 1
            }
        )
        self.load_animations(self.Name)

    def update(self, dt):
        self.current_animation = self.idle_animation
        super().update(dt)
    
