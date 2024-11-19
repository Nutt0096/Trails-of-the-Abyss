import pygame, math, random, sys, os
from src.constants import *

pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.init()
music_channel = pygame.mixer.Channel(0)
music_channel.set_volume(0.2)

from src.Dependencies import *
from src.resources import *

class GameMain:
    def __init__(self):
        self.max_frame_rate = 60
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        g_state_manager.SetScreen(self.screen)

        states = {
            'start': StartState(),
            'selectCharacter': SelectCharacterState(),
            'stage': StageState(),
            'combat': CombatState(), # add combat stage
            'shop': ShopState(),
            'victory': VictoryState(),
            'defeat': DefeatState()
        }

        g_state_manager.SetStates(states)

    def PlayGame(self):
        clock = pygame.time.Clock()

        g_state_manager.Change("start", None)

        while True:
            pygame.display.set_caption("game running with {:d} FPS".format(int(clock.get_fps())))
            dt = clock.tick(self.max_frame_rate) / 1000.0

            events = pygame.event.get()

            g_state_manager.update(dt, events)

            self.screen.fill((0, 0, 0))
            g_state_manager.render()

            pygame.display.update()


if __name__ == '__main__':
    main = GameMain()
    main.PlayGame()



