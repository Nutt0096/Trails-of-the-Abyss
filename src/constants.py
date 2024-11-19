import math

WIDTH = 1280 #1280
HEIGHT = 720 #720

PLAYER_WALK_SPEED = 180

NUM_CHARACTER = 3

CURRENT_STAGE = [False, False, False, False, False]


def stage_update(new_stage):
    CURRENT_STAGE = new_stage