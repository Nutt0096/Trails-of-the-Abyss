from character.CharacterBase import Character

class Barbarian(Character):
    def __init__(self):
        super().__init__(Name="barbarian", STR=9, INT=3, CON=9, DEF=7, ACC=5, CHA=3)
        self.Weapons.append(
            {
                    "name": "Axe",
                    "ACC": 1,
                    "STR": 0,
                    "damage_dice": 10,
                    "dice": 1
            }
        )
        self.load_animations(self.Name)
    

    def update(self, dt):
        self.current_animation = self.idle_animation
        super().update(dt)
