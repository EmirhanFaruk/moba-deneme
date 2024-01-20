
# Modification date: Mon Mar 14 23:12:12 2022

# Production date: Sun Sep  3 15:43:48 2023

import pygame
from math import sqrt, atan

pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Shooter')


class Ball():
    def __init__(self, x, y, radius, color, man, target):
        pygame.sprite.Sprite.__init__(self)
        self.x = man.rect.x
        self.y = man.rect.y
        self.radius = radius
        self.color = color
        self.dx = target[0] - man.rect.x
        self.dy = target[1] - man.rect.y


        #https://www.omnicalculator.com/math/right-triangle-side-angle#how-to-find-the-angle-of-a-right-triangle
        if self.dx == 0 or self.dy == 0:
            if self.dx == 0:
                self.vx = 0
                if self.dy > 0:
                    self.vy = 10
                else:
                    self.vy = -10
            elif self.dy == 0:
                if self.dx > 0:
                    self.vx = 10
                else:
                    self.vx = -10
                self.vy = 0
        else:
            if self.dx > 0 and self.dy > 0:
                alpha = atan(self.dy / self.dx)







        if self.dx > self.dy:
            self.perc = self.dy / self.dx
            if man.x > target[0]:
                self.vx = -abs((1 - self.perc) * 5)
            elif man.x < target[0]:
                self.vx = abs((1 - self.perc) * 5)
            if man.y > target[1]:
                self.vy = -abs(self.perc * 5)
            elif man.y < target[1]:
                self.vy = abs(self.perc * 5)

        else:
            self.perc = self.dx / self.dy
            if man.x > target[0]:
                self.vx = -abs(self.perc * 5)
            elif man.x < target[0]:
                self.vx = abs(self.perc * 5)
            if man.y > target[1]:
                self.vy = -abs((1 - self.perc) * 5)
            elif man.y < target[1]:
                self.vy = abs((1 - self.perc) * 5)
            #self.perc = self.dx / self.dy
            #self.vy = (1 - self.perc) * 5
            #self.vx = self.perc * 5

    
    def distance(self, enemy):
        return sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
    def move(self, enemies):
        for i in range(len(enemies)):
            if self.distance(enemies[i]) <= self.radius:
                enemies.pop(i)
                del self
                return
        self.x = self.x + self.vx
        self.y = self.y + self.vy
    
    def draw(self, win):
        #pygame.draw.circle(surface, color, center, radius, width)
        pygame.draw.circle(win, self.color, [self.x, self.y], self.radius, 0)

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
        self.target = None
        self.target_pos = None

        self.mc = 0
    
    def move(self, balls):
        """
        if self.target_pos:
            print(int(sqrt((self.target_pos[0] - self.rect.x) ** 2 + (self.target_pos[1] - self.rect.y) ** 2)))
            if int(sqrt((self.target_pos[0] - self.rect.x) ** 2 + (self.target_pos[1] - self.rect.y) ** 2)) > 0:
                if not(self.target_pos[0] > self.rect.x + self.pl.get_width()//4 and self.target_pos[0] < self.rect.x + (self.pl.get_width()//4) * 3):
                    if self.target_pos[0] < self.rect.x:
                        self.ml = True
                        self.mr = False
                    elif self.target_pos[0] > self.rect.x + self.pl.get_width():
                        self.mr = True
                        self.ml = False
                else:
                    self.mr = False
                    self.ml = False
                if not(self.target_pos[1] > self.rect.y + self.pl.get_height()//4 and self.target_pos[1] < self.rect.y + (self.pl.get_height()//4) * 3):
                    if self.target_pos[1] < self.rect.y:
                        self.mb = True
                        self.mf = False
                    elif self.target_pos[1] > self.rect.y + self.pl.get_height():
                        self.mb = False
                        self.mf = True
                else:
                    self.mb = False
                    self.mf = False
            else:
                self.target = None
                self.target_pos = None
                self.mb = False
                self.mf = False
                self.ml = False
                self.mr = False
        """
        if self.target_pos:
            balls.append(Ball(self.x, self.y, 10, (200, 50, 30), self, self.target_pos))
            self.target_pos = None

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
enemies.append(Man(400, 200, 10, 4))

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
            if event.key == pygame.K_a:
                player.left = True
                player.right = False
                player.front = False
                player.back = False
                player.ml = True
                player.target = None
                player.target_pos = None
            if event.key == pygame.K_d:
                player.right = True
                player.left = False
                player.front = False
                player.back = False
                player.mr = True
                player.target = None
                player.target_pos = None
            if event.key == pygame.K_w:
                player.back = True
                player.right = False
                player.front = False
                player.left = False
                player.mb = True
                player.target = None
                player.target_pos = None
            if event.key == pygame.K_s:
                player.front = True
                player.right = False
                player.left = False
                player.back = False
                player.mf = True
                player.target = None
                player.target_pos = None

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

        if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                player.target_pos = pos


    player.move(balls)
    player.draw()
    for i in range(len(balls)):
        balls[i].move(enemies)
        balls[i].draw(screen)
    for i in range(len(enemies)):
        enemies[i].draw()
    #player2.move()
    #player2.draw()
    
    pygame.display.update()
    print(player.ml, player.mr, player.mb, player.mf)
    print(player.rect.x, player.rect.y, player.target_pos)

pygame.quit()