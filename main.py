import pygame
from pygame.locals import *
import random
import time


class Apple:
    def __init__(self, screen):
        self.screen = screen
        self.x_x = random.randrange(0, 400, 20)
        self.y_y = random.randrange(0, 400, 20)
        self.apple = pygame.image.load("apple.png").convert()

    def draw(self):
        self.screen.blit(self.apple, (self.x_x, self.y_y))
        pygame.display.flip()

    def place(self):
        self.x_x = random.randrange(0, 400, 20)
        self.y_y = random.randrange(0, 400, 20)
        self.screen.blit(self.apple, (self.x_x, self.y_y))
        pygame.display.flip()


class Snake:
    def __init__(self, screen):
        self.screen = screen
        self.block = pygame.image.load("block.png").convert()
        self.x = 100
        self.y = 100
        self.direction = "down"

    def draw(self, apple, amount, directions, game_over):
        temp_x = self.x
        temp_y = self.y
        self.screen.fill((125, 125, 125))
        apple.draw()
        self.screen.blit(self.block, (self.x, self.y))
        temp = len(directions) - 1
        for i in range(amount):
            if len(directions) != 0:
                if directions[temp] == "down":
                    temp_y -= 20
                    self.screen.blit(self.block, (temp_x, temp_y))
                    if self.x == temp_x and self.y == temp_y:
                        game_over.game_over()
                        break
                if directions[temp] == "up":
                    temp_y += 20
                    self.screen.blit(self.block, (temp_x, temp_y))
                    if self.x == temp_x and self.y == temp_y:
                        game_over.game_over()
                        break
                if directions[temp] == "right":
                    temp_x -= 20
                    self.screen.blit(self.block, (temp_x, temp_y))
                    if self.x == temp_x and self.y == temp_y:
                        game_over.game_over()
                        break
                if directions[temp] == "left":
                    temp_x += 20
                    self.screen.blit(self.block, (temp_x, temp_y))
                    if self.x == temp_x and self.y == temp_y:
                        game_over.game_over()
                        break
                temp -= 1
        font = pygame.font.SysFont(None, 24)
        image = font.render(f"Score : {amount}", True, (255, 255, 0))
        self.screen.blit(image, (0, 0))
        pygame.display.flip()

    def move_right(self):
        self.direction = "right"

    def move_left(self):
        self.direction = "left"

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"

    def walk(self, apple, score, directions, game_over):
        directions.append(self.direction)
        if self.direction == "left":
            self.x -= 20
            self.draw(apple, score, directions, game_over)
        if self.direction == "right":
            self.x += 20
            self.draw(apple, score, directions, game_over)
        if self.direction == "up":
            self.y -= 20
            self.draw(apple, score, directions, game_over)
        if self.direction == "down":
            self.y += 20
            self.draw(apple, score, directions, game_over)


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((400, 400))
        self.surface.fill((125, 125, 125))
        self.apple = Apple(self.surface)
        self.snake = Snake(self.surface)
        self.snake.draw(self.apple, 0, [], self)
        self.run_time = False
        pygame.display.set_caption("Snake")
        pygame.display.flip()

    def running(self):
        if self.snake.x >= 400 or self.snake.x <= -20 or self.snake.y >= 400 or self.snake.y <= -20:
            return True
        else:
            return False

    def game_win_screen(self):
        self.surface.fill((125, 125, 125))
        font = pygame.font.SysFont(None, 50)
        font1 = pygame.font.SysFont(None, 25)
        image = font.render("YOU WİN", True, (255, 255, 0))
        image2 = font1.render("Do you want play again Y/N", True, (187, 124, 200))
        self.surface.blit(image, (130, 180))
        self.surface.blit(image2, (95, 230))
        pygame.display.flip()

    def game_over(self):
        self.surface.fill((125, 125, 125))
        font = pygame.font.SysFont(None, 50)
        font1 = pygame.font.SysFont(None, 25)
        image = font.render("GAME OVER", True, (255, 255, 0))
        image2 = font1.render("Do you want play again Y/N", True, (187, 124, 200))
        self.surface.blit(image, (100, 180))
        self.surface.blit(image2, (95, 230))
        pygame.display.flip()
        self.run_time = True

    def game_over_screen(self):
        boolean = self.running()
        if boolean:
            self.surface.fill((125, 125, 125))
            font = pygame.font.SysFont(None, 50)
            font1 = pygame.font.SysFont(None, 25)
            image = font.render("GAME OVER", True, (255, 255, 0))
            image2 = font1.render("Do you want play again Y/N", True, (187, 124, 200))
            self.surface.blit(image, (100, 180))
            self.surface.blit(image2, (95, 230))
            pygame.display.flip()
            return False
        else:
            return True

    def run(self):
        score = 0
        timer = 0.3
        directions = []
        while not self.run_time:
            if self.game_over_screen():
                if self.snake.x == self.apple.x_x and self.snake.y == self.apple.y_y:
                    score += 1
                    self.apple.place()
                self.snake.walk(self.apple, score, directions, self)
                time.sleep(timer)
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP and self.snake.direction != "down":
                            self.snake.move_up()
                        if event.key == pygame.K_DOWN and self.snake.direction != "up":
                            self.snake.move_down()
                        if event.key == pygame.K_RIGHT and self.snake.direction != "left":
                            self.snake.move_right()
                        if event.key == pygame.K_LEFT and self.snake.direction != "right":
                            self.snake.move_left()
                        if event.key == pygame.K_ESCAPE:
                            self.run_time = True
                    elif event.type == QUIT:
                        self.run_time = True
                if score == 100:
                    self.game_win_screen()
                    self.run_time = True
            else:
                self.run_time = True
        self.run_time = False
        while not self.run_time:
            pygame.init()
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.run_time = True
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.run_time = True
                    if event.key == K_y:
                        new_game = Game()
                        new_game.run()
                    if event.key == K_n:
                        self.run_time = True


if __name__ == "__main__":
    game = Game()
    game.run()


