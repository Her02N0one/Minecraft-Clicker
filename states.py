import pygame

import os
import random
from constants import *
import gui
import utils
import biomes
from block import Block

player = utils.Player()


class GameState(utils.State):

    def __init__(self, state_data):
        super().__init__(state_data)

        self.buttons = dict()

        self.buttons["INVENTORY"] = gui.Button(x=0, y=HEIGHT - 60, text="Inventory",
                                               callback=(lambda: self.states.push(InventoryState(state_data))))

        self.current_biome = biomes.debug

        self.blocks = list()
        self.blocks.append(Block("dirt", 1))
        self.delay = 20

    def update_events(self, dt, event):
        self.blocks[-1].update_events(dt, event)

        for button in self.buttons.values():
            button.update_events(dt, event)

    def update(self, dt):
        self.blocks[-1].update(dt)
        if self.blocks[-1].is_broken():
            self.delay -= 55 * dt
            if self.delay <= 0:
                biomes.reset_blocks(self.current_biome, self.blocks[-1])
                self.blocks.append(biomes.get_random_block(self.current_biome))

                self.delay = 20
                player.total_blocks_broken += 1
                player.add_item(self.blocks[-2].product)
        if len(self.blocks) != 1:
            self.blocks[-2].update(dt)
        if len(self.blocks) > 2:
            self.blocks.remove(self.blocks[-3])

        for button in self.buttons.values():
            button.update(dt)

    def render(self, target=None):
        if target is None:
            target = self.screen

        for button in self.buttons.values():
            button.render(target)

        self.blocks[-1].render(target)

        if len(self.blocks) != 1:
            self.blocks[-2].render(target)


class InventoryState(utils.State):

    def __init__(self, state_data):
        super().__init__(state_data)
        self.buttons = dict()
        self.buttons["BACK"] = gui.Button(x=0, y=HEIGHT - 60, text="Back", callback=(lambda: self.end_state()))
        self.sprite_size = 64
        self.inventory_x = 20
        self.inventory_y = 20
        self.padding = 16
        self.sprites = dict()

    def on_enter(self):
        for item in player.inventory:
            sprite = pygame.image.load("assets/sprites/" + item[0] + ".png").convert()
            sprite = pygame.transform.scale(sprite, (self.sprite_size, self.sprite_size))
            self.sprites[item[0]] = sprite

    def update_events(self, dt, event):
        for button in self.buttons.values():
            button.update_events(dt, event)

    def update(self, dt):
        for button in self.buttons.values():
            button.update(dt)

    def render(self, target=None):
        if target is None:
            target = self.screen

        row = 0
        col = 0

        for item in player.inventory:

            if row >= 8:
                row = 0
                col += 1
            target.blit(self.sprites[item[0]], ((row * self.sprite_size) + (row * self.padding) + self.inventory_x,
                                                self.inventory_y + (col * self.sprite_size) + (col * self.padding)))

            minecraft_font.render_to(target,
                                     (
                                         row * self.padding + row * self.sprite_size + self.sprite_size - minecraft_font.get_rect(
                                             str(item[1])).width + self.inventory_x,
                                         col * self.padding + col * self.sprite_size - minecraft_font.get_rect(((
                                             str(item[1])))).height + self.sprite_size + self.inventory_y),
                                     str(item[1]), (255, 255, 255))
            row += 1

            for button in self.buttons.values():
                button.render(target)
