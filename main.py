import pygame
from pygame.locals import *
import random
import time
import math
import sys
import os


pygame.init()
pygame.mixer.init()
WIDTH, HEIGHT = 598, 598
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill((0, 0, 0))
pygame.display.set_caption("HEROPAZZLES")
font = pygame.font.Font('fonts/Adca.ttf', 35)
clock = pygame.time.Clock()
victory = pygame.mixer.Sound("sounds/TaDa.ogg")
switchScene = None
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
def switch_scene(scene):
    global switchScene
    switchScene = scene

def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image

def terminate():
    pygame.quit()
    sys.exit()

def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Цель игры состоит в том, чтобы расположить ",
                  "все 15 фишек в правильном порядке, а пустую ",
                  "клетку поставить в правый нижний угол."]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    running = True
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('red'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return maingame()
        pygame.display.flip()
        clock.tick(FPS)



def maingame():
    class Tile(object):
        def __init__(self, num, x, y):
            self.number = num
            self.x = x
            self.y = y
            self.width = 99
            self.height = 99

        def draw(self):
            pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height), 0)
            text = font.render(str(self.number), True, WHITE)
            textRect = text.get_rect(center=((2 * self.x + self.width) / 2, (2 * self.y + self.height) / 2))
            screen.blit(text, textRect)

        def moveIt(self, dist):
            final_x = self.x + dist[0]
            final_y = self.y + dist[1]

            while self.x != final_x or self.y != final_y:
                screen.fill(WHITE, [self.x, self.y, 99, 99])
                self.x += int(dist[0] / 50)
                self.y += int(dist[1] / 50)
                self.draw()
                pygame.display.update()

            clock.tick(60)


    def count_inversions(num_order):
        inversions = 0
        for i in range(len(num_order) - 1):
            for k in range(i + 1, len(num_order)):
                if num_order[i] > num_order[k]:
                    inversions += 1
        return inversions


    def moves_display(mytext):
        txt = font.render(mytext, True, WHITE)
        textRect = txt.get_rect(center=(299, 550))
        screen.blit(txt, textRect)


    def show_congrats():
        txt = font.render("Yes! You're win!", True, GREEN)
        textRect = txt.get_rect(center=(299, 49))
        screen.blit(txt, textRect)
        finalTile = Tile(16, empty_x, empty_y)
        finalTile.draw()
        pygame.display.update()


    corret_matches = [[100, 100, 1], [200, 100, 2], [300, 100, 3], [400, 100, 4], [100, 200, 5], [200, 200, 6],
                      [300, 200, 7], [400, 200, 8], [100, 300, 9], [200, 300, 10], [300, 300, 11], [400, 300, 12],
                      [100, 400, 13], [200, 400, 14], [300, 400, 15]]


    def detectWin():
        for tile in listOfTiles:
            curr_arrangement = [tile.x, tile.y, tile.number]
            if curr_arrangement not in corret_matches:
                return False
        return True


    nums = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    random.shuffle(nums)


    while count_inversions(nums) % 2 != 0:
        random.shuffle(nums)

    listOfTiles = []
    move_counter = 0
    index = 0
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, WHITE, (98, 98, 403, 403))
    for y in range(100, 500, 100):
        for x in range(100, 500, 100):
            if index < 15:
                da_num = nums[index]
                newTile = Tile(da_num, x, y)
                listOfTiles.append(newTile)
                newTile.draw()
                index += 1

    empty_x = 400
    empty_y = 400

    pygame.display.update()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                this_pos = pygame.mouse.get_pos()
                x = int(math.floor(this_pos[0] / 100.0)) * 100
                y = int(math.floor(this_pos[1] / 100.0)) * 100
                li = [(empty_x - x), (empty_y - y)]
                if 0 in li and (100 in li or -100 in li):
                    for tile in listOfTiles:
                        if tile.x == x and tile.y == y:
                            move_counter += 1
                            empty_x = tile.x
                            empty_y = tile.y
                            tile.moveIt(li)
            elif event.type == KEYDOWN:
                arrows = [K_LEFT, K_RIGHT, K_UP, K_DOWN]
                if event.key == K_ESCAPE:
                    running = False
                elif event.key in arrows:
                    xy_dist = [None, None]
                    if event.key == K_LEFT:
                        xy_dist = [-100, 0]
                    if event.key == K_RIGHT:
                        xy_dist = [100, 0]
                    if event.key == K_UP:
                        xy_dist = [0, -100]
                    if event.key == K_DOWN:
                        xy_dist = [0, 100]
                    for tile in listOfTiles:
                        if tile.x + xy_dist[0] == empty_x and tile.y + xy_dist[1] == empty_y:
                            move_counter += 1
                            empty_x = tile.x
                            empty_y = tile.y
                            tile.moveIt(xy_dist)
                            break

        screen.fill(BLACK, [200, 515, 200, 85])
        moves_display("Moves: " + str(move_counter))
        pygame.display.update()
        clock.tick(60)

        if detectWin() == True:
            show_congrats()
            victory.play()
            time.sleep(5)
            running = False

start_screen()
pygame.quit()
