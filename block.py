import pygame
import random

CUBE_WIDTH = CUBE_HEIGHT = 256
CUBE_X = 250
CUBE_Y = 125 - 64


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

        if color is None:
            self.image = pygame.image.load(image_path).convert()
            self.image = pygame.transform.scale(self.image, (CUBE_WIDTH, CUBE_HEIGHT))
        else:
            self.image = pygame.Surface((width, height))
            self.image.fill(color)

        self.sx = startx
        self.sy = starty
        self.life = random.randint(5, 10)
        self.offset_x = random.randint(0, self.width)
        self.offset_y = random.randint(0, self.height)

    def move(self):
        self.y += 7
        self.x += random.randint(-2, 2)

    def render(self, target):
        target.blit(self.image, (self.x, self.y), (self.offset_x, self.offset_y, self.width, self.height))


class Block:
    def __init__(self, name, strength=1, product=None):
        self.name = name
        if product is None:
            self.product = self.name
        else:
            self.product = product

        self.strength = strength

        self.image = pygame.image.load("assets/sprites/" + name +
                                       ".png").convert()
        self.mask = pygame.Surface((self.image.get_width(),
                                    self.image.get_height()))
        self.rect = self.image.get_rect()
        self.rect.x = CUBE_X
        self.rect.y = CUBE_Y
        self.set_size(CUBE_WIDTH, CUBE_HEIGHT)

        self.damage = 0
        self.mask_stage = -1

        self.hit_strength = 1
        self.button_down = False
        self.broken = False

        self.particles_created = False
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
            self.mask = pygame.image.load(
                f"assets/masks/destroy_stage_{self.mask_stage}.png"
            ).convert_alpha()
            self.set_size(256, 256)
            if self.damage == self.strength:
                self.create_particles()

    def update_events(self, dt, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
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

        for particle in self.particles:
            if particle.life >= 0:
                if particle.y <= self.rect.y + self.rect.height - particle.height:
                    particle.move()
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
            for particle in self.particles:
                particle.render(target)
                # pygame.draw.rect(screen, particle.col,
                #                  ((particle.x, particle.y), (32, 32)))

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
                    image_path="assets/sprites/" + self.name + ".png"))

    def is_broken(self):
        return self.broken

    def copy(self):
        return Block(self.name, self.strength)
