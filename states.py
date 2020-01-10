import pygame

from constants import *
import gui
import utils
from block import Block


class GameState(utils.State):

    def __init__(self, state_data):
        super().__init__(state_data)
        self.block = Block("grass", 5)

    def update_events(self, dt, event):
        self.block.update_events(dt, event)

    def update(self, dt):
        self.block.update(dt)

    def render(self, target=None):
        if target is None:
            target = self.state_data["screen"]

        self.block.render(target)

