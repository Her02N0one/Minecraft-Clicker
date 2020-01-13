import pygame

import os
import random
from constants import *
import gui
import utils
from block import Block

player = utils.Player()


class GameState(utils.State):

    def __init__(self, state_data):
        super().__init__(state_data)

        self.debug = dict()
        directory = 'assets/sprites/'

        for filename in os.listdir(directory):
            if filename.endswith(".png"):
                name = filename[:-4]
                self.debug[name] = dict(name=name, strength=1)

        self.plain = {
            "grass": dict(name="grass", strength=5, product="dirt", ),
            "dirt": dict(name="dirt", strength=6),
            "pumpkin": dict(name="pumpkin", strength=7),
            "stone": dict(name="stone", strength=10, product="cobblestone")

        }

        self.cave = {
            "dirt": dict(name="dirt", strength=6),
            "stone": dict(name="stone", strength=10, product="cobblestone"),
            "iron": dict(name="iron_ore", strength=15),
            "obsidian": dict(name="obsidian", strength=35)
        }

        self.buttons = dict()

        self.buttons["INVENTORY"] = gui.Button(x=0, y=HEIGHT - 60, text="Inventory",
                                               callback=(lambda: self.states.push(InventoryState(state_data))))

        self.current_biome = self.debug

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
                block = list(self.current_biome.values())[random.randint(0, len(self.current_biome.values()) - 1)]
                if "product" not in block:
                    self.blocks.append(Block(name=block["name"], strength=block["strength"]))
                else:
                    self.blocks.append(Block(name=block["name"], strength=block["strength"], product=block["product"]))

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

        for index, item in enumerate(player.inventory):

            if row >= 8:
                row = 0
                col += 1
            target.blit(self.sprites[item[0]], ((row * self.sprite_size) + (row * self.padding) + self.inventory_x,
                                                self.inventory_y + (col * self.sprite_size) + (col * self.padding)))

            minecraft_font.render_to(target, ((row * self.sprite_size) + (row * self.padding) + self.inventory_x + (
                    self.sprite_size - minecraft_font.get_rect(str(item[1])).width),
                                              self.inventory_y + (col * self.sprite_size) + (col * self.padding) + (
                                                          self.sprite_size - minecraft_font.get_rect(
                                                      str(item[1])).height)), str(item[1]), (255, 255, 255))
            row += 1

            # for x in range(128, WIDTH, tile_size):
            #     pygame.draw.line(target, GREY, (x, 128), (x, tile_size*2+128))
            # for y in range(128, HEIGHT, tile_size):
            #     pygame.draw.line(target, GREY, (128, y), (tile_size*10+128, y))

        for button in self.buttons.values():
            button.render(target)

            # small_font.render_to(target, (50, 100), str(player.inventory))
