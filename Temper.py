#!/usr/bin/python3

import pygame
import random

BLACK = (  0,  0,  0)
AQUA  = (  0,255,255)
WHITE = (255,255,255)
GREY  = (100,100,100)

ALPHA = 100

ENEMY_COLOR = BLACK
PLAYER_COLOR = AQUA
TEXT_COLOR = WHITE
BACKGROUND_COLOR = GREY

SIZE = 20

pygame.init()

screen_width = 700
screen_height = 400
screen = pygame.display.set_mode([screen_width, screen_height])

enemy_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()

class Block(pygame.sprite.Sprite):
    def __init__(self, color, size):
        super().__init__()
        self.image = pygame.Surface([size, size])
        self.image.fill(color)
        self.image.set_alpha(ALPHA)
        self.rect = self.image.get_rect()
        self.size = size
        self.alive = True

    def isDead(self):
        return not self.alive

    def revive(self, list):
        self.alive = True

    def die(self):
        self.alive = False

    def changeSize(self, amount, color, list):
        if self.size + amount <= 0:
            self.die()
            screen.fill(BACKGROUND_COLOR)
            imploded = font.render("You imploded.", True, (255,255,255))
            implodedRect = imploded.get_rect()
            implodedRect.center = (screen_width // 2, screen_height // 4 + 90)
            screen.blit(imploded, implodedRect)
            pygame.display.flip()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONUP:
                        self = self.changeSize(20, PLAYER_COLOR, list)
                        self.die()
                        return self
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
        if self.size + amount >= min(screen_width,screen_height):
            self.die()
            screen.fill(BACKGROUND_COLOR)
            exploded = font.render("You exploded.", True, (255,255,255))
            explodedRect = exploded.get_rect()
            explodedRect.center = (screen_width // 2, screen_height // 4 + 90)
            screen.blit(exploded, explodedRect)
            
            pygame.display.flip()
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONUP:
                        self = self.changeSize(-(self.size - 20),PLAYER_COLOR, list)
                        self.die()
                        return self
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
        
        list.remove(self)
        temp = Block(color, self.size + amount)
        list.add(temp)
        del(self)
        return temp
    def getPos(self):
        return [self.rect.y, self.rect.x]
    def setPos(self, y, x):
        self.rect.y = y
        self.rect.x = x
    def reset_pos(self):
        self.rect.y = random.randrange(-300, -20)
        self.rect.x = random.randrange(0, screen_width)
    def update(self):
        self.rect.y += (self.size // 10) + 1
        if self.rect.y > 410:
            self.reset_pos()
    

player = Block(PLAYER_COLOR, SIZE)
all_sprites_list.add(player)
done = False
clock = pygame.time.Clock()
font = pygame.font.Font("SourceCodePro-Regular.ttf", 28)

for i in range(50):
    enemy = Block(ENEMY_COLOR, SIZE)
    enemy.rect.x = random.randrange(screen_width)
    enemy.rect.y = random.randrange(screen_height)
    enemy_list.add(enemy)
    all_sprites_list.add(enemy)


while not done:
    if player.isDead():
        player = player.changeSize(SIZE, PLAYER_COLOR, all_sprites_list)
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    screen.fill(BACKGROUND_COLOR)
    pos = pygame.mouse.get_pos()
    enemy_hit_list = pygame.sprite.spritecollide(player, enemy_list, False)
    for enemy in enemy_hit_list:
        enemy.reset_pos()
        player = player.changeSize(enemy.size//3, PLAYER_COLOR, all_sprites_list)
        
        if player.isDead():
            player = player.changeSize(SIZE, PLAYER_COLOR, all_sprites_list)
    #have player shrink over time, even when not shitting
    player = player.changeSize(-.25, PLAYER_COLOR, all_sprites_list)
    if player.isDead():
        player = player.changeSize(SIZE, PLAYER_COLOR, all_sprites_list)
    player.rect.x = pos[0]
    player.rect.y = pos[1]

    all_sprites_list.draw(screen)
    pygame.display.flip()
    clock.tick(60)
    enemy_list.update()
pygame.quit()

