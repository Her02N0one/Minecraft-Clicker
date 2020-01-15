from block import Block
import os
import random


def get_random_block(biome: dict) -> Block:
    return list(biome.values())[random.randint(0, len(biome.values())) - 1]


def reset_blocks(biome: dict, *args):
    for key in biome:
        for block in args:
            if biome[key] != block:
                biome[key].reset()


debug = dict()
directory = 'assets/sprites/'
for filename in os.listdir(directory):
    if filename.endswith(".png"):
        name = filename[:-4]
        debug[name] = Block(name, 2)

plain = {
    "grass": Block("grass", 5, "dirt"),
    "sand": Block("sand", 5),
    "dirt": Block("dirt", 6),
    "pumpkin": Block("pumpkin", 8),
    "oak_log": Block("log_oak", 9),
    "stone": Block("stone", 10, product="cobblestone")

}

cave_level_1 = {
    "dirt": Block("dirt", 6),
    "stone": Block("stone", 10, product="cobblestone"),
    "coal": Block("coal_ore", 12, product="coal"),
    "iron": Block("iron_ore", 15),
    "obsidian": Block("obsidian", 35)
}
