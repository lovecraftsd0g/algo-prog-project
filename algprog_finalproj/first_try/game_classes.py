from typing import Any
import pygame
from pygame.sprite import Group
import random
import copy
import math
import time
import random
global scx
global scy
scx = 1000
scy = 500
listofen = []
class mellee_rectangle(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((45,45))
        self.rect = self.image.get_rect(center = (x,y))
        self.max_attack_state_tick = 20
        self.attack_state_tick = self.max_attack_state_tick
    def update(self) :
        '''after certain ticks it removes itself from all groups'''
        self.image.fill('Red')
        if self.attack_state_tick > 0:
            self.attack_state_tick -= 1
        elif self.attack_state_tick <= 0:
            self.kill()

class player_class(pygame.sprite.Sprite):
    def __init__(self,xpo,ypo,speed):
        pygame.sprite.Sprite.__init__(self)
        self.playerhealth = 0
        self.speed = speed
        self.image = pygame.image.load('first_try\images\player.bmp')
        self.rect = self.image.get_rect(center = (xpo,ypo))
        self.tick = 0
        self.jump_tick_max = 70
        self.jump_amount = 1
        self.jump_tick = self.jump_tick_max 
        self.jump_state = False
        self.lasttpneg = 0
        self.lasttppos = 0

    def move(self,col):
        '''always moving in the direction of speed'''
        lel = pygame.sprite.spritecollide(self,col,dokill=False)
        keys = pygame.key.get_pressed()
        speed = 0
        
        '''tracking if the jump_state is true'''
        if self.jump_state:
            self.jump()
        '''spurce of value for speed change based on input'''
        if keys[pygame.K_d]:
            speed = self.speed[0]
        elif keys[pygame.K_a]:
            speed = -self.speed[1] 

                
        self.rect.x += speed
        self.rect.y += self.speed[2]
                    
        


    def collison(self,col1):
        
        k = pygame.key.get_pressed()
        '''constantly detecting collision and storing the collisded objects in a list and adjust the speed acording to that'''
        

        collision_check = pygame.sprite.spritecollide(self,col1,dokill=False)

        if collision_check:
            for collided in collision_check:
                '''if the objects top and the sprites bottom are at a certain distance it will set the speed[2] variable to 0'''
                if abs(collided.rect.top - self.rect.bottom) <= 3  and self.rect.centerx<collided.rect.right and self.rect.centerx > collided.rect.left:
                    self.speed[2] = 0
                    if k[pygame.K_w] and collided.rect.top > self.rect.bottom -10:
                        self.jump_state = True
                
                '''
                if the object left is at a certain distance with the collided right, and the bottom of the object is below the collided's top than it will set the 
                speed[1] to 0
                if anything else it will be of the normal speed
                '''
                if (abs(collided.rect.right - self.rect.left)  < 5 and collided.rect.top < self.rect.bottom - 5) or self.rect.left <= 0:
                    self.speed[1] = 0
                else:
                    self.speed[1] = 2

                if (abs(collided.rect.left - self.rect.right)  < 5 and collided.rect.top < self.rect.bottom - 5) or self.rect.right >= 1000:
                    self.speed[0] = 0
                else:
                    self.speed[0] = 2
        else:
            '''simply the if functions if it ever reaches a point where it is not colliding with anything'''
            if self.rect.left <= 0:
                self.speed[1] = 0
            else:
                self.speed[1] = 2
            if self.rect.right >= scx:
                self.speed[0] = 0
            else:
                self.speed[0] = 2
            self.speed[2] = 2
    def jump(self):
        '''each time the tick is not empty'''
        if self.jump_tick > 0:
            self.speed[2] = -2
            self.jump_tick -= 1
        elif self.jump_tick <= 0:
            self.jump_state = False
            self.jump_tick = self.jump_tick_max

class bullet(pygame.sprite.Sprite):
    def __init__(self,speed,target,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.image = pygame.Surface((10,10))
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center = (x,y))
        #measuring the angle of the slope
        angle = math.atan2(target[1]-self.rect.centery,target[0]-self.rect.centerx) 
        #the amount of necesarry x and y values are multiplied for greater speed
        self.dx = math.cos(angle)*self.speed
        self.dy = math.sin(angle)*self.speed
    def update(self) :
        self.image.fill('Black')
        self.x += self.dx
        self.y += self.dy
        self.rect.centerx = self.x
        self.rect.centery = self.y

class flying_enemy(pygame.sprite.Sprite):
    def __init__(self,x,y,player,speed):
        pygame.sprite.Sprite.__init__(self)
        self.images = [
        'first_try\images\cetaghoul\cetaghoul0.png',
        'first_try\images\cetaghoul\cetaghoul1.png',
        'first_try\images\cetaghoul\cetaghoul2.png',
        'first_try\images\cetaghoul\cetaghoul3.png',
        'first_try\images\cetaghoul\cetaghoul4.png',
        'first_try\images\cetaghoul\cetaghoul5.png'
        ]

        self.current = 0
        self.image = pygame.Surface((40,40))
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center=(self.x,self.y))
        self.target = player
        self.speed = speed
    def update(self):
        if self.current < len(self.images) - 1:
            self.current += 1
        else:
            self.current = 0
        self.image = pygame.image.load(self.images[self.current])

        if self.target.rect.centerx < self.rect.centerx:
            self.image = pygame.transform.flip(self.image,True,False)



        #constantly finding the neccesary x and y value to make the che correct diagonal movement
        angle = math.atan2(self.target.rect.centery - self.rect.centery,self.target.rect.centerx - self.rect.centerx)
        self.dirx = math.cos(angle) * self.speed
        self.diry = math.sin(angle) * self.speed
        self.x += self.dirx 
        self.y += self.diry
        self.rect.centerx = self.x
        self.rect.centery = self.y

class ground_enemy(pygame.sprite.Sprite):
    def __init__(self,x,y,player,speed):
        pygame.sprite.Sprite.__init__(self)
        self.images = [
        'first_try\images\slime\slimoo0.png',
        'first_try\images\slime\slimoo1.png',
        'first_try\images\slime\slimoo2.png',
        'first_try\images\slime\slimoo3.png']
        self.current = 0

        self.image = pygame.Surface((20,20))
        
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center=(self.x,self.y))
        self.target = player
        self.speed = [3,3,2]
        self.shooter = speed
        self.colobs = pygame.sprite.Group()
    def collision(self):
        '''constantly detecting collision and storing the collisded objects in a list and adjust the speed acording to that'''
        colliding = pygame.sprite.spritecollide(self,self.colobs,False)
        if colliding:
            for objects in colliding:
                if abs(objects.rect.top - self.rect.bottom) <= 5 and self.rect.centerx > objects.rect.left and self.rect.centerx < objects.rect.right:
                    self.speed[2] =0

                if self.rect.right <= objects.rect.left and self.rect.bottom >= objects.rect.top:
                    self.speed[0] = 0
                else:
                    self.speed[0] = 3
                if objects.rect.right <= self.rect.left and self.rect.bottom >= objects.rect.top:
                    self.speed[1] = 0
                else:
                    self.speed[1] = 3
        elif not colliding:
            self.speed[0] = 3
            self.speed[1] = 3
            self.speed[2] = 2
    def update(self):
        if self.current < len(self.images) - 1:
            self.current += 1
        else:
            self.current = 0
        self.image = pygame.image.load(self.images[self.current])
        self.rect.height = 30
        #whilst detecting the collisiion it detects the y values of the player as well
        self.collision()
        function_speed = int()
        if abs(self.target.rect.bottom - self.rect.bottom) <= 5:
            if self.target.rect.centerx < self.rect.centerx:
                function_speed = -self.speed[0]
            elif self.target.rect.centerx > self.rect.centerx:
                function_speed = self.speed[1]
        self.rect.centerx += function_speed
        self.rect.bottom += self.speed[2]

class rectt(pygame.sprite.Sprite):
    def __init__(self,x,y,xpo,ypo):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((x,y))
        self.rect = self.image.get_rect(center = (xpo,ypo))
        self.image.fill('Blue')

class tiled(pygame.sprite.Sprite):
    def __init__(self,xpo,ypo):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("first_try/images/tiles/another-stone.png")
        self.rect = self.image.get_rect(center = (xpo,ypo))

class spawner(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface((1, 1))
        self.rect = self.image.get_rect(center=(x, y))
        self.spawn_point = 1
        self.group = pygame.sprite.Group()
        self.player = pygame.sprite.Sprite()

    def spawn(self,obstacles):
        '''
        if a spawn_point is available it will spawn a creature based on the enemy number
        and give that enemy the neccesary adjusted stats to operate as intended in game
        and it will also put the enemy in the self.current_entity

        so that it may detect if the entity it spawned is still with in the sprite group if it is not in the sprite group
        then it will onceagain restore its spawnpoints and reset the current entity
        '''
        if self.spawn_point > 0:
            enemy_number = random.randint(1, 2)
            if enemy_number == 1:
                een = flying_enemy(self.rect.centerx, self.rect.centery, self.player, 3)
                self.current_entity = een
                self.group.add(een)
            elif enemy_number == 2:
                een = ground_enemy(self.rect.centerx, self.rect.centery, self.player,[2,2,2])
                een.colobs = obstacles
                self.current_entity = een
                self.group.add(een)
            self.spawn_point -= 1
        elif self.spawn_point <= 0:
            if not self.current_entity in self.group.sprites():
                self.spawn_point = 1
                self.current_entity = pygame.sprite.Sprite()


