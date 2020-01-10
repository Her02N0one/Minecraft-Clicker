import pygame
import random


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

        if color is None:
            self.image = pygame.image.load(image_path).convert()
            self.image = pygame.transform.scale(self.image, (width, height))
        else:
            self.image = pygame.Surface((width, height))
            self.image.fill(color)

        self.sx = startx
        self.sy = starty
        self.life = random.randint(30, 180)

    def move(self):

        self.y += 5

        self.x += random.randint(-4, 4)


class Block:
    def __init__(self, name, strength=10):
        self.name = name
        self.strength = strength

        self.image = pygame.image.load("assets/sprites/" + name +
                                       ".png").convert()
        self.mask = pygame.Surface((self.image.get_width(),
                                    self.image.get_height()))
        self.rect = self.image.get_rect()

        self.set_size(256, 256)

        self.damage = 0
        self.mask_stage = -1

        self.button_down = False
        self.broken = False

        self.particles_created = False
        self.particles = list()

    def set_size(self, width, height):
        self.image = pygame.transform.scale(self.image, (width, height))
        self.mask = pygame.transform.scale(self.mask, (width, height))
        self.rect.width = width
        self.rect.height = height

    def hit(self, hit_strength=1):
        self.damage += 1 * hit_strength
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
                if particle.y <= self.rect.y + self.rect.height:
                    particle.move()
                particle.life -= 1
            else:
                self.particles.remove(particle)

    def render(self, screen):
        if not self.is_broken():
            screen.blit(self.image, self.rect)
            if self.mask_stage >= 0:
                screen.blit(self.mask, self.rect)
        else:
            for particle in self.particles:
                screen.blit(particle.image, (particle.x, particle.y))
                # pygame.draw.rect(screen, particle.col,
                #                  ((particle.x, particle.y), (32, 32)))

    def create_particles(self):
        particle_template = pygame.Rect((0, 0), (16, 16))

        for _ in range(250):
            x = random.randint(self.rect.x,
                               self.rect.width - particle_template.width)
            y = random.randint(self.rect.y,
                               self.rect.height - particle_template.height)

            self.particles.append(
                Particle(
                    x,
                    y,
                    particle_template.width,
                    particle_template.height,
                    image_path="assets/sprites/" + self.name + "_particle.png"))

    def is_broken(self):
        return self.broken

    def copy(self):
        return Block(self.name, self.strength)
