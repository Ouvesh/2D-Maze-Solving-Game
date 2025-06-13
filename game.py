# game.py
import time
import datetime
import pygame

from button import Button
from coin import Coin, choose_random_nodes
from image import Image
from menu import Menu
from walls import Wall
from enemy import Enemy
from maze_generator import *
import sys

from player import Player


class Game:
    # All of these are a power of 2
    PLAYER_SIZE = ENEMY_SIZE = 32  # This should be a factor of the SQUARE_SIZE
    MOVE_AMOUNT = 4
    MAZE_WALL_SIZE = 8
    SMALL_COIN_SIZE = 16
    top = 0
    left = 1
    bottom = 2
    right = 3

    def __init__(self, n, screen, width, height):
        """

        :param n:
        :param screen:
        :param width:
        :param height:
        :param clock:
        """
        self.SQUARE_SIZE = 128
        self.mst = None
        self.status = "menu"
        self.enemy_nodes = None
        self.exit_rect = None
        self.highscore = 0
        self.score = 0
        self.n = n
        self.screen = screen
        self.screen_width = width
        self.screen_height = height
        self.clock = pygame.time.Clock()
        self.number_of_coins = int(n ** 2 * 0.1)
        self.x_maze = 0
        self.y_maze = 0
        self.maze_width = self.n * self.SQUARE_SIZE
        self.maze_height = self.maze_width
        self.player = None
        self.number_of_enemies = 10
        self.exit_wall = Wall(x=0, y=0, width=self.SQUARE_SIZE, height=Game.MAZE_WALL_SIZE + 4, game=self,
                              colour=(0, 255, 0))
        self.menu = Menu(self)
        self.maze_object = MazeGenerator(self.n)
        self.reset()
        self.background_status = False
        self.paused = False
        self.paused_at = None
        self.total_time = 0
    def draw_walls(self):
        """

        :return:
        """
        for wall in self.walls:
            wall.draw()
        self.exit_wall.draw()

    def create_maze(self):
        mst = self.maze_object.create_mst()
        self.walls = []
        x, y = self.x_maze, self.y_maze

        for row in range(self.n):
            for column in range(self.n):
                node = row * self.n + column

                if mst[node][Game.top] == 0:
                    self.walls.append(Wall(x=x, y=y,
                                           width=self.SQUARE_SIZE,
                                           height=Game.MAZE_WALL_SIZE, game=self))

                if mst[node][Game.right] == 0 \
                        or node == self.n ** 2 - 1:
                    self.walls.append(Wall(
                        x=x + self.SQUARE_SIZE, y=y, game=self,
                        width=Game.MAZE_WALL_SIZE, height=self.SQUARE_SIZE))

                if mst[node][Game.bottom] == 0:
                    self.walls.append(Wall(x=x, y=y + self.SQUARE_SIZE, game=self,
                                           width=self.SQUARE_SIZE + Game.MAZE_WALL_SIZE,
                                           height=Game.MAZE_WALL_SIZE))

                if mst[node][Game.left] == 0 or node == 0:
                    self.walls.append(Wall(x=x, y=y, game=self,
                                           width=Game.MAZE_WALL_SIZE,
                                           height=self.SQUARE_SIZE))
                if node == self.n ** 2 or self.n ** 2 - 1:
                    self.player = Player(x=x + (self.SQUARE_SIZE // 2), y=y + (self.SQUARE_SIZE // 2), game=self,
                                         height=self.PLAYER_SIZE, width=self.PLAYER_SIZE)
                x += self.SQUARE_SIZE

            y += self.SQUARE_SIZE
            x = self.x_maze

        pass

    def reset_maze_offset(self):
        self.offset_x = -(self.maze_width - self.screen_width)
        self.offset_y = -(self.maze_height - self.screen_height)

    def reset_player(self):
        self.player.reset_to_start()
        self.reset_maze_offset()
        self.player.lose_life()

    def create_coins(self):
        self.coin_nodes = choose_random_nodes(self.number_of_coins, self.n ** 2)
        self.coins = []
        x, y = 0, 0

        for row in range(self.n):
            for column in range(self.n):
                node = row * self.n + column
                if node in self.coin_nodes:
                    coin = Coin(x=x + (self.SQUARE_SIZE // 2),
                                y=y + (self.SQUARE_SIZE // 2), game=self, width=self.SMALL_COIN_SIZE,
                                height=self.SMALL_COIN_SIZE)
                    self.coins.append(coin)

                x += self.SQUARE_SIZE

            y += self.SQUARE_SIZE
            x = 0

        # print(self.coins)

    def check_coin_collisions(self):
        remaining_coins = []
        for coin in self.coins:
            if self.player.is_collided(coin):
                self.score += 1
            else:
                remaining_coins.append(coin)

        self.coins = remaining_coins

    def check_wall_collisions(self, game_object):
        for wall in self.walls:
            if game_object.going_to_collide(wall):
                return True

        return False

    def check_enemy_collisions(self):
        for enemy in self.enemies:
            if self.player.is_collided(enemy):
                return True

        return False

    def draw_coins(self):
        for coin in self.coins:
            # print(f'x: {coin.x}, y:{coin.y}')
            coin.draw()

    def check_win(self):
        if self.player.is_collided(self.exit_wall):
            self.status = "win"

    def check_lives(self):
        if not self.player.is_alive():
            self.status = "lose"

    def toggle_pause(self):
        self.paused = not self.paused

    def draw_background(self):
        background = pygame.image.load("Buttons/grass_background.jpg")
        background = pygame.transform.scale(background, (self.screen_width, self.screen_height))
        self.screen.blit(background, (0, 0))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYUP and event.key == pygame.K_p:
                self.toggle_pause()
                if self.paused:
                    current_time = time.time()
                    self.total_time += current_time - self.start_time
                elif not self.paused:
                    current_time = time.time()
                    self.start_time = current_time
            if event.type == pygame.KEYUP and event.key == pygame.K_q and self.paused:
                self.status = "menu"
                self.menu.set_message("You have successfully quit the game!")
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def movement_events(self):
        keys = pygame.key.get_pressed()
        moved = False

        dx, dy = 0, 0
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            dy = -Game.MOVE_AMOUNT
            moved = True
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            dy = Game.MOVE_AMOUNT
            moved = True
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            dx = -Game.MOVE_AMOUNT
            moved = True
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            dx = Game.MOVE_AMOUNT
            moved = True


        self.player.dy = dy
        self.player.dx = dx

        playerx = self.player.x + self.offset_x
        playery = self.player.y + self.offset_y
        RIGHT_THRESHOLD_X = 0.6 * self.screen_width
        LEFT_THRESHOLD_X = 0.4 * self.screen_width
        RIGHT_THRESHOLD_Y = 0.6 * self.screen_height
        LEFT_THRESHOLD_Y = 0.4 * self.screen_height

        if not self.check_wall_collisions(self.player):
            if (playerx < LEFT_THRESHOLD_X) and (self.player.dx <= 0) \
                    or (playerx > RIGHT_THRESHOLD_X) and (self.player.dx >= 0):
                self.offset_x -= dx
            if (playery < LEFT_THRESHOLD_Y) and (self.player.dy <= 0) \
                    or (playery > RIGHT_THRESHOLD_Y) and (self.player.dy >= 0):
                self.offset_y -= dy
            self.player.move()

        if not moved:
            return

    def draw_enemies(self):
        for enemy in self.enemies:
            enemy.draw()

    def set_status(self, status):
        self.status = status

    def create_enemies(self):
        self.enemies = []
        x, y = 0, 0
        self.enemy_nodes = choose_random_nodes(self.number_of_enemies, self.n ** 2)
        for row in range(self.n):
            for column in range(self.n):
                node = row * self.n + column
                if node in self.enemy_nodes:
                    enemy = Enemy(x=x + (self.SQUARE_SIZE // 2),
                                  y=y + (self.SQUARE_SIZE // 2), game=self, width=self.ENEMY_SIZE,
                                  height=self.ENEMY_SIZE)
                    self.enemies.append(enemy)

                x += self.SQUARE_SIZE

            y += self.SQUARE_SIZE
            x = 0

    def draw_lives(self):
        lives_font = pygame.font.Font(None, 30)
        text = lives_font.render(f"Lives: {self.player.lives}", True, (255, 0, 0))
        self.screen.blit(text, (0, 40))

    def draw_score(self):
        score_font = pygame.font.Font(None, 30)
        text = score_font.render(f"Score: {self.score}", True, (255, 0, 0))
        self.screen.blit(text, (0, 0))

    def show_timer(self):
        current_time = time.time()
        time_difference = self.total_time + current_time - self.start_time
        time_text = str(datetime.timedelta(seconds=time_difference)).split(".")[0]
        timer_font = pygame.font.Font(None, 30)
        timer_text = timer_font.render(time_text,
                                       True,
                                       (255, 0, 0))
        self.screen.blit(timer_text, (0, 20))

    def set_menu_status(self):
        self.status = "menu"

    def reset(self):
        self.paused = False
        self.highscore = max(self.score, self.highscore)
        self.start_time = time.time()
        self.coins = []
        self.walls = []
        self.enemies = []
        self.reset_maze_offset()
        self.create_coins()
        self.create_enemies()
        self.create_maze()
        self.score = 0
        self.total_time = 0


    def run_maze(self):
        self.handle_events()
        if self.paused:
            return
        self.movement_events()
        self.screen.fill((255, 255, 255))
        if self.background_status:
            self.draw_background()
        self.draw_walls()
        self.player.draw()

        if self.check_enemy_collisions():
            self.reset_player()
        for enemy in self.enemies:
            if not self.check_wall_collisions(enemy):
                enemy.move()
            else:
                enemy.change_direction()

        self.draw_enemies()
        self.draw_score()
        self.show_timer()
        self.draw_lives()
        self.check_coin_collisions()
        self.draw_coins()
        self.check_lives()
        self.check_win()

    def run(self):
        while True:
            self.handle_events()
            if self.status == "menu":
                self.menu.run()
            if self.status == "game":
                self.run_maze()
            if self.status == "controls":
                self.menu.show_controls()

            if self.status == "win":
                self.menu.set_message("You have won the game!")
                self.set_menu_status()
            if self.status == "lose":
                self.menu.set_message("You have lost the game!")
                self.reset()
                self.set_menu_status()
            pygame.display.flip()
            self.clock.tick(60)
