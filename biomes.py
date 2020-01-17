from block import Block
import os
import random


class Biome:
    def __init__(self):
        pass
    
    def add_block(self, *args):
        for block in args:
            if "name" not in block:
                raise 
            
            print(block)


def get_random_block(biome: dict) -> Block:
    return list(biome.values())[random.randint(0, len(biome.values())) - 1]


def reset_blocks(biome: dict, *args):
    for key in biome:
        for block in args:
            if biome[key] != block:
                biome[key].reset()


debug = dict()
directory = 'assets/sprites/blocks/'
for filename in os.listdir(directory):
    if filename.endswith(".png"):
        name = filename[:-4]
        debug[name] = Block(name, 2)

plain = Biome().add_block(
    dict(block=Block("grass", 5, "dirt"), rarity=0),
    Block("sand", 5),
    Block("dirt", 6),
    Block("pumpkin", 8),
    Block("log_oak", 9),
    Block("stone", 10, product="cobblestone")

)

cave_level_1 = {
    "dirt": Block("dirt", 6),
    "stone": Block("stone", 10, product="cobblestone"),
    "coal": Block("coal_ore", 12, product="coal", product_image="assets/sprites/items/coal.png"),
    "iron": Block("iron_ore", 15),
    "obsidian": Block("obsidian", 35)
}
