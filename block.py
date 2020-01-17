import pygame
import random

BLOCK_WIDTH = BLOCK_HEIGHT = 256
BLOCK_X = 250
BLOCK_Y = 125 - 64


class Particle:
    def __init__(self,
                 startx,
                 starty,
                 width,
                 height,
                 image_path=None,
                 color=None):
        self.x = startx
        self.y = starty
        self.width = width
        self.height = height

        if color is None and image_path is not None:
            self.image = pygame.image.load(image_path).convert()
            self.image = pygame.transform.scale(self.image, (BLOCK_WIDTH, BLOCK_HEIGHT))
        elif image_path is None and color is not None:
            self.image = pygame.Surface((width, height))
            self.image.fill(color)
        else:
            raise TypeError(
                "you must put either an image_path or a color. You can't have both and you can't have neither")

        self.sx = startx
        self.sy = starty
        self.life = random.randint(5, 10)
        self.offset_x = random.randint(0, self.width)
        self.offset_y = random.randint(0, self.height)

    def update(self):
        self.y += 7
        self.x += random.randint(-2, 2)

    def render(self, target):
        target.blit(self.image, (self.x, self.y), (self.offset_x, self.offset_y, self.width, self.height))


class Block:
    def __init__(self, name, strength: int = 1, product=None, product_image=None):
        """
        :param name: the name block, must also be the same as the name of the block in the blocks folder
        :param strength: how many clicks it takes to break the block
        :param product: the name of what the block gives you without silktouch
        :param product_image: if the product isn't a block, specify the file location of the image here
        """
        self.name = name
        self.strength = strength
        self.product = product
        self.product_image = product_image
        self.image_location = "assets/sprites/blocks/" + name + ".png"

        if product is None:
            self.product = self.name
            self.product_image = self.image_location
        else:
            self.product = product

            if product_image is None:
                self.product_image = self.image_location
            else:
                self.product_image = product_image

        self.image = pygame.image.load(self.image_location).convert()
        self.mask = pygame.Surface((self.image.get_width(),
                                    self.image.get_height()))
        self.rect = self.image.get_rect()
        self.rect.x = BLOCK_X
        self.rect.y = BLOCK_Y
        self.set_size(BLOCK_WIDTH, BLOCK_HEIGHT)

        self.damage = 0
        self.mask_stage = -1

        self.hit_strength = 1
        self.button_down = False
        self.broken = False

        self.particles = list()

    def set_size(self, width, height):
        self.image = pygame.transform.scale(self.image, (width, height))
        self.mask = pygame.transform.scale(self.mask, (width, height))
        self.rect.width = width
        self.rect.height = height

    def hit(self):
        self.damage += 1 * self.hit_strength
        if not self.broken:
            self.mask_stage = int((self.damage / self.strength) * 9)
            self.mask = pygame.image.load(f"assets/masks/destroy_stage_{self.mask_stage}.png").convert_alpha()
            self.set_size(BLOCK_WIDTH, BLOCK_HEIGHT)
            if self.damage == self.strength:
                self.create_particles()

    def update_events(self, dt, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(*event.pos):
                self.button_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            # If the rect collides with the mouse pos.
            if self.rect.collidepoint(*event.pos) and self.button_down:
                self.hit()
            self.button_down = False

    def update(self, dt):
        if self.damage >= self.strength:
            self.broken = True

        if len(self.particles) != 0:
            for particle in self.particles:
                if particle.life >= 0:
                    if particle.y <= self.rect.y + self.rect.height - particle.height:
                        particle.update()
                    else:
                        particle.life -= 1
                else:
                    self.particles.remove(particle)

    def render(self, target):
        if not self.is_broken():
            target.blit(self.image, self.rect)
            if self.mask_stage >= 0:
                target.blit(self.mask, self.rect)
        else:
            if len(self.particles) != 0:
                for particle in self.particles:
                    particle.render(target)

    def create_particles(self):

        for _ in range(60):
            width = height = random.randint(25, 35)

            x = random.randint(self.rect.x,
                               self.rect.x + self.rect.width - width)
            y = random.randint(self.rect.y,
                               self.rect.y + self.rect.height - height)

            self.particles.append(
                Particle(
                    x,
                    y,
                    width,
                    height,
                    image_path="assets/sprites/blocks/" + self.name + ".png"))

    def reset(self):
        self.damage = 0
        self.mask_stage = -1
        self.broken = False

    def is_broken(self):
        return self.broken

    def copy(self):
        return Block(self.name, self.strength, self.product)
