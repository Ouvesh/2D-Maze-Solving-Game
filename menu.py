import pygame
import sys

from button import Button
from image import Image


def get_font(size):
    font = pygame.font.Font("Buttons/font.ttf", size)
    return font


class Menu:
    controls = "Buttons/Controls.png"
    exit = "Buttons/Exit.png"
    start = "Buttons/Start.png"
    background = "Buttons/Background.png"
    button_spacing = 150
    y_offset = 10

    def __init__(self, game):
        self.end_button = None
        self.control_button = None
        self.start_button = None
        pygame.display.set_caption("2D Maze Solving Game (A level Project)")
        self.clock = pygame.time.Clock()
        self.game = game
        self.start_button = Button(image_path=Menu.start,
                                   centre_y=(self.game.screen_height // 2),
                                   game=self.game, centre_x=(self.game.screen_width // 2),
                                   width=None, height=None)
        self.control_button = Button(image_path=Menu.controls,
                                     centre_y=self.game.screen_height // 2 + Menu.button_spacing,
                                     game=self.game,
                                     centre_x=(self.game.screen_width // 2),
                                     width=None, height=None)
        self.end_button = Button(image_path=Menu.exit, centre_y=self.game.screen_height // 2 + 2 * Menu.button_spacing,
                                 game=self.game, centre_x=(self.game.screen_width // 2),
                                 width=None, height=None)

        self.message = ""

    def draw_buttons(self):
        self.start_button.draw()
        self.control_button.draw()
        self.end_button.draw()

    def check_start_button_pressed(self):
        if self.start_button.check_button_pressed():
            self.game.reset()
            self.game.set_status("game")

    def check_end_button_pressed(self):
        if self.end_button.check_button_pressed():
            pygame.quit()
            sys.exit()

    def check_controls_button_pressed(self):
        if self.control_button.check_button_pressed():
            self.game.set_status("controls")

    def set_message(self, message):
        self.message = message

    def draw_text(self, text, centre, font_size):
        message_text = get_font(font_size).render(text, True, "black")
        message_rect = message_text.get_rect(center=centre)
        self.game.screen.blit(message_text, message_rect)

    def draw(self):
        background = pygame.transform.scale(pygame.image.load(Menu.background),
                                            (self.game.screen_width, self.game.screen_height))
        self.game.screen.blit(background, (0, 0))
        self.draw_text(f"Highscore: {self.game.highscore}",
                       (self.game.screen_width // 2, (self.game.screen_height // 20) + 15), 20)
        self.draw_text("MAIN MENU", (self.game.screen_width // 2, self.game.screen_height // 5), 70)
        self.draw_text(self.message, (self.game.screen_width // 2, (self.game.screen_height // 20) - 10), 20)

    def show_controls(self):
        background = pygame.transform.scale(pygame.image.load(Menu.background),
                                            (self.game.screen_width, self.game.screen_height))
        self.game.screen.blit(background, (0, 0))
        image = Image(image_path="Buttons/control_instructions.png", centre_x=self.game.screen_width // 2,
                      centre_y=self.game.screen_height // 4, game=self.game)
        image.draw()
        back = Button(image_path="Buttons/back.png", x=0, y=0, game=self.game)
        back.draw()

        line_spacing = 20
        lines = [
            "How to play:",
            "Navigate through the maze, avoiding walls and enemies, to reach the exit.",
            "Use arrow keys or WASD to move your character.",
            "Collect coins to increase your score!",
            "Reach the exit as quickly as possible to beat the maze.",
            "If you collide with an enemy you lose one of your three lives.",
            "When you lose all three lives it is game over."
        ]

        y_coordinate = self.game.screen_height // 2 - line_spacing * 3  # Initial y-coordinate

        for line in lines:
            self.draw_text(line, (self.game.screen_width // 2, y_coordinate), 10)
            y_coordinate += line_spacing

        yes_button = Button(image_path="Buttons/Yes.png", x=self.game.screen_width // 2 - 100, y=self.game.screen_height - 140, game=self.game)
        yes_button.draw()
        self.draw_text("Would you like to toggle background?", (self.game.screen_width // 2, self.game.screen_height - 150), 10)
        if yes_button.check_button_pressed():
            self.game.background_status = not self.game.background_status
        if back.check_button_pressed():
            self.game.status = "menu"



    def check_buttons(self):
        self.check_start_button_pressed()
        self.check_end_button_pressed()
        self.check_controls_button_pressed()

    def run(self):
        self.draw()
        self.draw_buttons()
        self.check_buttons()
