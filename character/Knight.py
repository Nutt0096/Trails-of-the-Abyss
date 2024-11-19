from character.CharacterBase import Character

class Knight(Character):
    def __init__(self):
        super().__init__(Name="knight", STR=7, INT=3, CON=10, DEF=8, ACC=6, CHA=4)
        self.Weapons.append(
            {
                    "name": "Sword",
                    "ACC": 2,
                    "STR": 0,
                    "damage_dice": 8,
                    "dice": 1
            }
        )
        self.load_animations(self.Name)
    def update(self, dt):
        self.current_animation = self.idle_animation
        # Update the current animation frame
        super().update(dt)  # Call the base class update to handle the animation