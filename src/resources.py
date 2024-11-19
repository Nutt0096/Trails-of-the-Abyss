import pygame
from src.Util import SpriteManager
from src.StateMachine import StateMachine

g_state_manager = StateMachine()

sprite_collection = SpriteManager().spriteCollection

character_image_list = [sprite_collection["knight_idle"].animation,
                        sprite_collection["mage_idle"].animation,
                        sprite_collection["archer_idle"].animation,
                        sprite_collection["sorcerer_idle"].animation,
                        sprite_collection["barbarian_idle"].animation,
                        ]

monster_image_list = [sprite_collection["Crying1"].animation,
                      sprite_collection["Crying2"].animation,
                      sprite_collection["Demon1"].animation,
                      sprite_collection["Demon2"].animation,
                      sprite_collection["Ghost1"].animation,
                      sprite_collection["Ghost2"].animation,
                      sprite_collection["Ghost3"].animation,
                      sprite_collection["Orc1"].animation,  
                      sprite_collection["Orc2"].animation,
                      sprite_collection["Skeleton"].animation,
                      sprite_collection["Slime1"].animation,
                      sprite_collection["Slime2"].animation,
                      ]


gFonts = {
    'M_small': pygame.font.Font('./fonts/MedievalSharp-Regular.ttf', 24),
    'M_medium': pygame.font.Font('./fonts/MedievalSharp-Regular.ttf', 48),
    'M_large': pygame.font.Font('./fonts/MedievalSharp-Regular.ttf', 96)
}

gSounds = {
    'Title_music': pygame.mixer.Sound('sounds/xDeviruchi - Title Theme .wav'),
    'Select_music': pygame.mixer.Sound('sounds/xDeviruchi - And The Journey Begins .wav'),
    'Shop_music': pygame.mixer.Sound('sounds/xDeviruchi - Take some rest and eat some food!.wav'),
    'Stage5_music': pygame.mixer.Sound('sounds/xDeviruchi - Prepare for Battle! .wav'),
    'Stage3_music': pygame.mixer.Sound('sounds/xDeviruchi - Exploring the Unknown.wav'),
    'Stage1_music': pygame.mixer.Sound('sounds/xDeviruchi - Mysterious Dungeon.wav'),
    'select': pygame.mixer.Sound('sounds/select.wav'),
    'no-select': pygame.mixer.Sound('sounds/no-select.wav'),
    'confirm': pygame.mixer.Sound('sounds/confirm.wav'),
    'victory': pygame.mixer.Sound('sounds/Z0mg ⧹⧸Ict0ry!! ^O^.wav'),
    'defeat': pygame.mixer.Sound('sounds/Sad Violin.wav'),
    
}
