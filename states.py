import pygame

import random
from constants import *
import gui
import utils
from block import Block


class GameState(utils.State):

    def __init__(self, state_data):
        super().__init__(state_data)

        self.plain = {
            "grass": dict(name="grass", product="dirt", strength=5),
            "dirt": dict(name="dirt", strength=6),
            "stone": dict(name="stone", product="cobblestone", strength=10),
        }

        self.cave = {
            "dirt": dict(name="dirt", strength=6),
            "stone": dict(name="stone", product="cobblestone", strength=10),
            "iron": dict(name="iron_ore", strength=15),
            "obsidian": dict(name="obsidian", strength=35)
        }

        self.current_biome = self.plain

        self.player = utils.Player()

        self.blocks = list()
        self.blocks.append(Block("dirt", strength=5))
        self.delay = 20

    def update_events(self, dt, event):
        self.blocks[-1].update_events(dt, event)

    def update(self, dt):
        print(self.player.inventory)
        self.blocks[-1].update(dt)
        if self.blocks[-1].is_broken():
            self.delay -= 55 * dt
            if self.delay <= 0:
                block = list(self.current_biome.values())[random.randint(0, len(self.current_biome.values()) - 1)]
                if "product" not in block:
                    self.blocks.append(Block(name=block["name"], strength=block["strength"]))
                else:
                    self.blocks.append(Block(name=block["name"], product=block["product"], strength=block["strength"]))

                self.delay = 20
                self.player.total_blocks_broken += 1
                self.player.add_item(self.blocks[-2].product)
        if len(self.blocks) != 1:
            self.blocks[-2].update(dt)
        if len(self.blocks) > 2:
            self.blocks.remove(self.blocks[-3])

    def render(self, target=None):
        if target is None:
            target = self.state_data["screen"]

        self.blocks[-1].render(target)

        if len(self.blocks) != 1:
            self.blocks[-2].render(target)
