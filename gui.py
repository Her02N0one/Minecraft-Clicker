import pygame

import constants


class Button:
    # TODO: make a way to add different images for each button state

    def __init__(self,
                 x=10,
                 y=10,
                 width=200,
                 height=60,
                 text="",
                 font=constants.small_font,
                 idle_color=(100, 100, 100),
                 hover_color=(150, 150, 150),
                 active_color=(120, 120, 120),
                 hover_sound=pygame.mixer.Sound("assets/sounds/sfx/tap-resonant.aif"),
                 active_sound=pygame.mixer.Sound("assets/sounds/sfx/tap-warm.aif"),
                 callback=(lambda: None)
                 ):

        self.shape = pygame.Rect((x, y, width, height))
        self.colors = {"IDLE": idle_color, "HOVER": hover_color, "ACTIVE": active_color}
        self.sounds = {"BTN_HOVER": hover_sound, "BTN_ACTIVE": active_sound}
        self.text = text
        self.font = font
        self.textPos = ((self.shape.x + (self.shape.width / 2) - font.get_rect(text).width / 2),
                        (self.shape.y + (self.shape.height / 2) - font.get_rect(text).height / 2))

        self.current_color = self.colors["IDLE"]
        self.button_down = False
        self.button_idle = True
        self.hover_sound_ready = True
        self.pressed = False
        self.callback = callback

    def set_callback(self, func):
        self.callback = func

    def is_pressed(self):
        return self.button_down

    def update_events(self, dt, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.shape.collidepoint(*event.pos):
                self.current_color = self.colors["ACTIVE"]
                self.sounds["BTN_ACTIVE"].play()
                self.button_down = True

        elif event.type == pygame.MOUSEBUTTONUP:
            # If the rect collides with the mouse pos.
            if self.shape.collidepoint(*event.pos) and self.button_down:
                self.callback()  # Call the function.
                self.current_color = self.colors["HOVER"]
            self.button_down = False

        elif event.type == pygame.MOUSEMOTION:
            collided = self.shape.collidepoint(*event.pos)
            if collided and self.button_idle:
                self.sounds["BTN_HOVER"].play()
                self.button_idle = False
            elif collided and not self.button_down:
                self.current_color = self.colors["HOVER"]
            elif not collided:
                self.current_color = self.colors["IDLE"]
                self.button_idle = True

    def update(self, dt):
        pass

    def render(self, target):
        pygame.draw.rect(target, self.current_color, self.shape)
        self.font.render_to(target, self.textPos, self.text, (0, 0, 0))


class Slider:
    # TODO: add a way for the slider to go up in increments based on a "ticks" variable
    def __init__(self,
                 x=200,
                 y=200,
                 width=200,
                 initial_value=0.5,
                 idle_slider_color=(120, 120, 120),
                 hover_slider_color=(100, 100, 100),
                 active_slider_color=(110, 110, 110),
                 line_color=(200, 200, 200),
                 active_line_color=(180, 180, 180),
                 progress_color=(180, 180, 255),
                 active_progress_color=(150, 150, 255),
                 ):

        self.radius = 8
        self.height = 5
        self.line = pygame.Rect((x, y), (width, self.height))
        self.slider = pygame.Rect((initial_value * self.line.width - (self.radius / 2) + self.line.x,
                                   y - (self.radius / 2) - self.line.height / 3),
                                  (self.radius * 2, self.radius * 2))

        self.progress = pygame.Rect((x, y), (self.slider.x - self.line.x, self.height))

        self.slider_colors = {"IDLE": idle_slider_color, "HOVER": hover_slider_color, "ACTIVE": active_slider_color}
        self.line_colors = {"IDLE": line_color, "ACTIVE": active_line_color}
        self.progress_colors = {"IDLE": progress_color, "ACTIVE": active_progress_color}

        self.current_slider_color = self.slider_colors["IDLE"]
        self.current_line_color = self.line_colors["IDLE"]
        self.current_progress_color = self.progress_colors["IDLE"]

        self.button_down = False
        self.button_hover = False
        self.collided = False

    def get_percent(self):
        return (self.slider.x + self.radius / 2 - self.line.x) / self.line.width

    def update_events(self, dt, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.slider.collidepoint(*event.pos):
                self.current_slider_color = self.slider_colors["ACTIVE"]
                self.current_line_color = self.line_colors["ACTIVE"]
                self.current_progress_color = self.progress_colors["ACTIVE"]
                self.button_down = True
                self.collided = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.slider.collidepoint(*event.pos) and self.button_down:
                self.current_slider_color = self.slider_colors["HOVER"]
                self.current_line_color = self.line_colors["IDLE"]
                self.current_progress_color = self.progress_colors["IDLE"]
            self.button_down = False
            self.collided = False

        elif event.type == pygame.MOUSEMOTION:
            if self.slider.collidepoint(*event.pos):
                self.current_slider_color = self.slider_colors["HOVER"]
            if self.collided:
                self.slider.centerx = event.pos[0]
            elif not self.slider.collidepoint(*event.pos):
                self.current_slider_color = self.slider_colors["IDLE"]
                self.current_progress_color = self.progress_colors["IDLE"]
                self.current_line_color = self.line_colors["IDLE"]

    def update(self, dt):
        if self.slider.x >= self.line.x + self.line.width - self.radius / 2:
            self.slider.x = self.line.x + self.line.width - self.radius / 2
        if self.slider.x <= self.line.x - self.radius / 2:
            self.slider.x = self.line.x - self.radius / 2
        self.progress.width = self.slider.x - self.line.x

    def render(self, target):

        pygame.draw.rect(target, self.current_line_color, self.line)
        pygame.draw.rect(target, self.current_progress_color, self.progress)
        pygame.draw.circle(target, self.current_slider_color, (self.slider.x + self.radius,
                                                               self.slider.y + self.radius), self.radius)
