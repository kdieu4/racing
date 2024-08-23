import sys
import pygame
import random

pygame.init()

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 620
BG_SPEED = 1.5
BG_IMG = pygame.image.load("img/background.png")

X_MARGIN = 80
CAR_WIDTH = 40
CAR_HEIGHT = 60
CAR_SPEED = 3
CAR_IMG = pygame.image.load("img/car.png")

LANE_WIDTH = 60  # độ rộng 1 làn xe (đường có 4 làn)

DISTANCE = 200  # khoảng cách giữa các xe thep chiều dọc
OBSTACLES_SPEED = 2  # tốc độ ban đầu của những chiếc xe
CHANGE_SPEED = 0.001  # tăng tốc độ xe theo thời gian
OBSTACLES_IMG = pygame.image.load("img/obstacles.png")

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("RACING")

FPS = 60
fpsClock = pygame.time.Clock()


class Background:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.speed = BG_SPEED
        self.img = BG_IMG
        self.width = self.img.get_width()
        self.height = self.img.get_height()

    def draw(self):
        window.blit(self.img, (int(self.x), int(self.y)))
        window.blit(self.img, (int(self.x), int(self.y - self.height)))

    def update(self):
        self.y += self.speed
        if self.y > self.height:
            self.y -= self.height


class Car:
    def __init__(self):
        self.width = CAR_WIDTH
        self.height = CAR_HEIGHT
        self.x = (WINDOW_WIDTH - self.width) / 2
        self.y = (WINDOW_HEIGHT - self.height) / 2
        self.speed = CAR_SPEED
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill((255, 255, 255))

    def draw(self):
        window.blit(CAR_IMG, (int(self.x), int(self.y)))

    def update(self, move_left, move_right, move_up, move_down):
        if move_left:
            self.x -= self.speed
        if move_right:
            self.x += self.speed
        if move_up:
            self.y -= self.speed
        if move_down:
            self.y += self.speed

        if self.x < X_MARGIN:
            self.x = X_MARGIN
        if self.x + self.width > WINDOW_WIDTH - X_MARGIN:
            self.x = WINDOW_WIDTH - X_MARGIN - self.width
        if self.y < 0:
            self.y = 0
        if self.y + self.height > WINDOW_HEIGHT:
            self.y = WINDOW_HEIGHT - self.height


class Obstacle:
    def __init__(self):
        self.width = CAR_WIDTH
        self.height = CAR_HEIGHT
        self.distance = DISTANCE
        self.speed = OBSTACLES_SPEED
        self.change_speed = CHANGE_SPEED
        self.ls = []
        for i in range(5):
            y = -CAR_HEIGHT - i * self.distance
            lane = random.randint(0, 3)
            self.ls.append([lane, y])

    def draw(self):
        for i in range(5):
            x = int(X_MARGIN + self.ls[i][0] * LANE_WIDTH + (LANE_WIDTH - self.width) / 2)
            y = int(self.ls[i][1])
            window.blit(OBSTACLES_IMG, (x, y))

    def update(self):
        for i in range(5):
            self.ls[i][1] += self.speed
        self.speed += self.change_speed
        if self.ls[0][1] > WINDOW_HEIGHT:
            self.ls.pop(0)
            y = self.ls[3][1] - self.distance
            lane = random.randint(0, 3)
            self.ls.append([lane, y])


class Score:
    def __init__(self):
        self.score = 0

    def draw(self):
        font = pygame.font.SysFont('consolas', 30)
        score_surface = font.render('Score: ' + str(int(self.score)), True, (0, 0, 0))
        window.blit(score_surface, (10, 10))

    def update(self):
        self.score += 0.02


def rect_collision(rect1, rect2):
    if rect1[0] <= rect2[0] + rect2[2] and rect2[0] <= rect1[0] + rect1[2] and rect1[1] <= rect2[1] + rect2[3] and \
            rect2[1] <= rect1[1] + rect1[3]:
        return True
    return False


def is_game_over(car, obstacle):
    car_rect = [car.x, car.y, car.width, car.height]
    for i in range(5):
        x = int(X_MARGIN + obstacle.ls[i][0] * LANE_WIDTH + (LANE_WIDTH - obstacle.width) / 2)
        y = int(obstacle.ls[i][1])
        obstacle_rect = [x, y, obstacle.width, obstacle.height]
        if rect_collision(car_rect, obstacle_rect):
            return True
    return False


def game_start(bg):
    bg.__init__()
    font = pygame.font.SysFont('consolas', 60)
    heading_surface = font.render('RACING', True, (255, 0, 0))
    heading_size = heading_surface.get_size()

    font = pygame.font.SysFont('consolas', 20)
    comment_surface = font.render('Press "space" to play', True, (0, 0, 0))
    comment_size = comment_surface.get_size()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
        bg.draw()
        window.blit(heading_surface, (int((WINDOW_WIDTH - heading_size[0]) / 2), 100))
        window.blit(comment_surface, (int((WINDOW_WIDTH - heading_size[0]) / 2), 400))
        pygame.display.flip()
        fpsClock.tick(FPS)


def game_play(bg, car, obstacle, score):
    bg.__init__()
    car.__init__()
    obstacle.__init__()
    score.__init__()
    move_left = False
    move_right = False
    move_up = False
    move_down = False
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_left = True
                if event.key == pygame.K_RIGHT:
                    move_right = True
                if event.key == pygame.K_UP:
                    move_up = True
                if event.key == pygame.K_DOWN:
                    move_down = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    move_left = False
                if event.key == pygame.K_RIGHT:
                    move_right = False
                if event.key == pygame.K_UP:
                    move_up = False
                if event.key == pygame.K_DOWN:
                    move_down = False
        if is_game_over(car, obstacle):
            return
        bg.draw()
        bg.update()
        car.draw()
        car.update(move_left, move_right, move_up, move_down)
        obstacle.draw()
        obstacle.update()
        score.draw()
        score.update()
        pygame.display.flip()
        fpsClock.tick(FPS)


def game_over(bg, car, obstacle, score):
    font = pygame.font.SysFont('consolas', 60)
    heading_surface = font.render('GAME OVER', True, (255, 0, 0))
    heading_size = heading_surface.get_size()

    font = pygame.font.SysFont('consolas', 20)
    comment_surface = font.render('Press "space" to replay', True, (0, 0, 0))
    comment_size = comment_surface.get_size()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
        bg.draw()
        car.draw()
        obstacle.draw()
        score.draw()
        window.blit(heading_surface, (int((WINDOW_WIDTH - heading_size[0]) / 2), 100))
        window.blit(comment_surface, (int((WINDOW_WIDTH - heading_size[0]) / 2), 400))
        pygame.display.flip()
        fpsClock.tick(FPS)


def main():
    bg = Background()
    car = Car()
    obstacle = Obstacle()
    score = Score()
    game_start(bg)
    while True:
        game_play(bg, car, obstacle, score)
        game_over(bg, car, obstacle, score)


if __name__ == "__main__":
    main()
pygame.quit()
