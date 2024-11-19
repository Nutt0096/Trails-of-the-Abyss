from src.Util import SpriteManager, Animation
import pygame

class Monster():
    def __init__(self, monster_config):
        # Initialize base entity properties
        super().__init__()  # Pass the config to the EntityBase constructor
        self.Name = monster_config["name"]
        self.STR = monster_config["STR"]
        self.INT = monster_config["INT"]
        self.DEF = monster_config["DEF"]
        self.ACC = monster_config["ACC"]
        self.CHA = monster_config["CHA"]
        self.HP = monster_config["hp"]
        self.MP = self.INT*10

        self.Weapons = []
        self.Spells = []

        self.sprite_manager = SpriteManager()
        self.idle_animation = None
        self.position = (100, 100)

        self.load_animations(self.Name)

    def load_animations(self, Name):
        # Load animations (you can customize this for each character subclass)
        self.idle_animation = self.sprite_manager.spriteCollection.get(Name).animation
        # for attack_sprite in attack_sprites:
        # self.attack_animation = self.sprite_manager.spriteCollection.get(attack_sprite).animation
        self.current_animation = self.idle_animation

    
    def update(self, dt):
        """Update the character's animation."""
        self.current_animation = self.idle_animation
        self.current_animation.update(dt)

    def show_stats(self):
        print(f"{self.Name}'s Stats:")
        print(f"STR: {self.STR}, INT: {self.INT}, CON: {self.CON}")
        print(f"DEF: {self.DEF}, ACC: {self.ACC}, CHA: {self.CHA}")

    def render(self, screen):
        """ Render the current animation. """

        if self.current_animation:
            frame_surface = self.current_animation.image
            frame_surface = pygame.transform.flip(frame_surface, True, False)
            screen.blit(frame_surface, self.position)
        else:
            print("Error: current_animation is None!")

