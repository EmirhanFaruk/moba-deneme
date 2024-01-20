
# Modification date: Fri Mar  4 14:39:54 2022

# Production date: Sun Sep  3 15:43:48 2023

import pygame
from math import sqrt
from random import randint

pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shooter')


class Enemy:
    def __init__(self, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        #self.image = pygame.transform.scale(pf, (int(pf.get_width() * scale), int(pf.get_height() * scale)))
        #player images
        self.pf = pygame.image.load("man_front.png")
        self.pf1 = pygame.image.load("man_front1.png")
        self.pf2 = pygame.image.load("man_front2.png")
        self.pf = pygame.transform.scale(self.pf, (int(self.pf.get_width() * scale), int(self.pf.get_height() * scale)))
        self.pf1 = pygame.transform.scale(self.pf1, (int(self.pf1.get_width() * scale), int(self.pf1.get_height() * scale)))
        self.pf2 = pygame.transform.scale(self.pf2, (int(self.pf2.get_width() * scale), int(self.pf2.get_height() * scale)))
        self.pwfb = [self.pf, self.pf1, self.pf, self.pf2]
        self.pr = pygame.image.load("man_right.png")
        self.pr1 = pygame.image.load("man_right1.png")
        self.pr = pygame.transform.scale(self.pr, (int(self.pr.get_width() * scale), int(self.pr.get_height() * scale)))
        self.pr1 = pygame.transform.scale(self.pr1, (int(self.pr1.get_width() * scale), int(self.pr1.get_height() * scale)))
        self.pl = pygame.image.load("man_left.png")
        self.pl1 = pygame.image.load("man_left1.png")
        self.pl = pygame.transform.scale(self.pl, (int(self.pl.get_width() * scale), int(self.pl.get_height() * scale)))
        self.pl1 = pygame.transform.scale(self.pl1, (int(self.pl1.get_width() * scale), int(self.pl1.get_height() * scale)))
        self.pwl = [self.pl, self.pl1]
        self.pwr = [self.pr, self.pr1]
        self.rect = self.pf.get_rect()
        self.rect = self.pr.get_rect()
        self.w = self.pl.get_width()
        self.h = self.pl.get_height()
        self.rect.center = (x, y)
        self.front = True
        self.back = False
        self.right = False
        self.left = False
        self.speed = speed
        self.mf = False
        self.mb = False
        self.mr = False
        self.ml = False
        self.ad = ""

        self.mc = 0
    
    def move(self, balls):
        if self.ad in ["ur", "ul", "dr", "dl", "u", "d", "l", "r"]:
            balls.append(Ball(self.rect.x + self.w//2, self.rect.y + self.h//2, 5, (150, 150, 50), self.ad))
            self.ad = ""
            #balls.append(Ball(self.x, self.y, 10, (200, 50, 30), self, self.target_pos))

        if self.mf:
            self.rect.y += self.speed
        if self.mb:
            self.rect.y -= self.speed
        if self.mr:
            self.rect.x += self.speed
        if self.ml:
            self.rect.x -= self.speed

            

        
    def draw(self):
        if self.mf or self.mb:
            screen.blit(self.pwfb[int(self.mc%4)], self.rect)
            self.mc += 0.2
        elif self.mr:
            screen.blit(self.pwr[int(self.mc%2)], self.rect)
            self.mc += 0.2
        elif self.ml:
            screen.blit(self.pwl[int(self.mc%2)], self.rect)
            self.mc += 0.2
        else:
            self.mc = 0
            if self.front or self.back:
                screen.blit(self.pf, self.rect)
            elif self.left:
                screen.blit(self.pwl[0], self.rect)
            elif self.right:
                screen.blit(self.pwr[0], self.rect)
        #screen.blit(self.image, self.rect)

class Ball:
    def __init__(self, x, y, radius, colour, direction):
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.direction = direction
        if self.direction == "ur":
            self.vx = 5
            self.vy = -5
        if self.direction == "ul":
            self.vx = -5
            self.vy = -5
        if self.direction == "dr":
            self.vx = 5
            self.vy = 5
        if self.direction == "dl":
            self.vx = -5
            self.vy = 5
        if self.direction == "d":
            self.vx = 0
            self.vy = 10
        if self.direction == "u":
            self.vx = 0
            self.vy = -10
        if self.direction == "l":
            self.vx = -10
            self.vy = 0
        if self.direction == "r":
            self.vx = 10
            self.vy = 0
    
    def distance(self, enemy):
        return sqrt((enemy.x + enemy.w//2 - self.x)**2 + (enemy.y + enemy.h//2 - self.y)**2)
    def move(self, enemies, balls):
        for i in range(len(enemies)):
            if self.distance(enemies[i]) <= 32:
                enemies.pop(i)
                balls.remove(self)
                return
        self.x = self.x + self.vx
        self.y = self.y + self.vy

    
    def draw(self, win):
        pygame.draw.circle(win, self.colour, [self.x, self.y], self.radius, 0)
        pygame.draw.rect(win, (255, 255, 255), [self.x, self.y, self.radius//2, self.radius//2])
        return



class Man(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        #self.image = pygame.transform.scale(pf, (int(pf.get_width() * scale), int(pf.get_height() * scale)))
        #player images
        self.pf = pygame.image.load("man_front.png")
        self.pf1 = pygame.image.load("man_front1.png")
        self.pf2 = pygame.image.load("man_front2.png")
        self.pf = pygame.transform.scale(self.pf, (int(self.pf.get_width() * scale), int(self.pf.get_height() * scale)))
        self.pf1 = pygame.transform.scale(self.pf1, (int(self.pf1.get_width() * scale), int(self.pf1.get_height() * scale)))
        self.pf2 = pygame.transform.scale(self.pf2, (int(self.pf2.get_width() * scale), int(self.pf2.get_height() * scale)))
        self.pwfb = [self.pf, self.pf1, self.pf, self.pf2]
        self.pr = pygame.image.load("man_right.png")
        self.pr1 = pygame.image.load("man_right1.png")
        self.pr = pygame.transform.scale(self.pr, (int(self.pr.get_width() * scale), int(self.pr.get_height() * scale)))
        self.pr1 = pygame.transform.scale(self.pr1, (int(self.pr1.get_width() * scale), int(self.pr1.get_height() * scale)))
        self.pl = pygame.image.load("man_left.png")
        self.pl1 = pygame.image.load("man_left1.png")
        self.pl = pygame.transform.scale(self.pl, (int(self.pl.get_width() * scale), int(self.pl.get_height() * scale)))
        self.pl1 = pygame.transform.scale(self.pl1, (int(self.pl1.get_width() * scale), int(self.pl1.get_height() * scale)))
        self.pwl = [self.pl, self.pl1]
        self.pwr = [self.pr, self.pr1]
        self.rect = self.pf.get_rect()
        self.rect = self.pr.get_rect()
        self.w = self.pl.get_width()
        self.h = self.pl.get_height()
        self.rect.center = (x, y)
        self.front = True
        self.back = False
        self.right = False
        self.left = False
        self.speed = speed
        self.mf = False
        self.mb = False
        self.mr = False
        self.ml = False
        self.ad = ""

        self.mc = 0
    
    def move(self, balls):
        if self.ad in ["ur", "ul", "dr", "dl", "u", "d", "l", "r"]:
            balls.append(Ball(self.rect.x + self.w//2, self.rect.y + self.h//2, 5, (150, 150, 50), self.ad))
            self.ad = ""
            #balls.append(Ball(self.x, self.y, 10, (200, 50, 30), self, self.target_pos))

        if self.mf:
            self.rect.y += self.speed
        if self.mb:
            self.rect.y -= self.speed
        if self.mr:
            self.rect.x += self.speed
        if self.ml:
            self.rect.x -= self.speed

            

        
    def draw(self):
        if self.mf or self.mb:
            screen.blit(self.pwfb[int(self.mc%4)], self.rect)
            self.mc += 0.2
        elif self.mr:
            screen.blit(self.pwr[int(self.mc%2)], self.rect)
            self.mc += 0.2
        elif self.ml:
            screen.blit(self.pwl[int(self.mc%2)], self.rect)
            self.mc += 0.2
        else:
            self.mc = 0
            if self.front or self.back:
                screen.blit(self.pf, self.rect)
            elif self.left:
                screen.blit(self.pwl[0], self.rect)
            elif self.right:
                screen.blit(self.pwr[0], self.rect)
        #screen.blit(self.image, self.rect)



player = Man(200, 200, 10, 3)
player2 = Man(400, 200, 10, 4)

balls = []
enemies = []
for i in range(20):
    rx = randint(0, SCREEN_WIDTH)
    ry = randint(0, SCREEN_HEIGHT)
    enemies.append(Man(rx, ry, 10, 4))

run = True
thicc = 60
clock = pygame.time.Clock()
while run:
    screen.fill((20, 200, 50))
    clock.tick(thicc)

    

    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False

        #keyboard presses
        if event.type == pygame.KEYDOWN:
            #print(event.key)
            if event.key == pygame.K_a:
                player.left = True
                player.right = False
                player.front = False
                player.back = False
                player.ml = True
            if event.key == pygame.K_d:
                player.right = True
                player.left = False
                player.front = False
                player.back = False
                player.mr = True
            if event.key == pygame.K_w:
                player.back = True
                player.right = False
                player.front = False
                player.left = False
                player.mb = True
            if event.key == pygame.K_s:
                player.front = True
                player.right = False
                player.left = False
                player.back = False
                player.mf = True


            if event.key == pygame.K_9 or str(event.key) == "1073741921":
                player.ad = "ur"
            if event.key == pygame.K_8 or str(event.key) == "1073741920" or event.key == pygame.K_UP:
                player.ad = "u"
            if event.key == pygame.K_7 or str(event.key) == "1073741919":
                player.ad = "ul"
            if event.key == pygame.K_6 or str(event.key) == "1073741918" or event.key == pygame.K_RIGHT:
                player.ad = "r"
            if event.key == pygame.K_4 or str(event.key) == "1073741916" or event.key == pygame.K_LEFT:
                player.ad = "l"
            if event.key == pygame.K_3 or str(event.key) == "1073741915":
                player.ad = "dr"
            if event.key == pygame.K_2 or str(event.key) == "1073741914" or event.key == pygame.K_DOWN:
                player.ad = "d"
            if event.key == pygame.K_1 or str(event.key) == "1073741913":
                player.ad = "dl"
            

            if event.key == pygame.K_ESCAPE:
                run = False

        #keyboard button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.ml = False
            if event.key == pygame.K_d:
                player.mr = False
            if event.key == pygame.K_w:
                player.mb = False
            if event.key == pygame.K_s:
                player.mf = False



    #rx = randint(0, SCREEN_WIDTH)
    #ry = randint(0, SCREEN_HEIGHT)
    #enemies.append(Man(rx, ry, 10, 4))

    player.move(balls)
    player.draw()
    if enemies:
        for i in range(len(enemies)):
            try:
                enemies[i].draw()
            except:
                pass
    if balls:
        for i in range(len(balls)):
            try:
                balls[i].draw(screen)
                balls[i].move(enemies, balls)
            except:
                pass
            
    
    #player2.move()
    #player2.draw()
    
    pygame.display.update()
    #print(player.ml, player.mr, player.mb, player.mf)
    #print(player.rect.x, player.rect.y)

pygame.quit()