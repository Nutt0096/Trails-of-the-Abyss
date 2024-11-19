import pygame
from src.resources import *

from src.StateMachine import StateMachine
from src.states.BaseState import BaseState
from src.states.game.StartState import StartState
from src.states.game.SelectCharacterState import SelectCharacterState
from src.states.game.StageState import StageState
from src.states.game.CombatState import CombatState
from src.states.game.ShopState import ShopState
from src.states.game.VictoryState import VictoryState
from src.states.game.DefeatState import DefeatState