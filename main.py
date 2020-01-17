import pygame
from constants import *
import utils
from states import GameState

# TODO: add an animation module for pygame surfaces


running = True if pygame.display.get_surface() is not None else False

# set up clock for limiting framerate and getting dt
clock = pygame.time.Clock()

states = utils.StateStack()  # Stack that holds all the States
state_data = dict(screen=screen, states=states)
states.push(GameState(state_data))

# ====== Main Game Loop ======

while running:
    clock.tick(FPS)
    dt = clock.get_time() / 1000

    # Update
    if states.isEmpty() is not True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            states.top().update_events(dt, event)

        states.top().update(dt)
        if states.top().get_quit():
            states.top().end_state()
            states.pop()
    else:
        running = False

    # Render

    screen.fill((69, 69, 69))

    if not states.isEmpty():
        states.top().render()

    fps = str(round(clock.get_fps(), 2))

    small_font.render_to(screen, (WIDTH - 80, 5), fps, (0, 0, 0))

    pygame.display.flip()

pygame.quit()
