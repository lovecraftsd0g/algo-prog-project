from game_classes import bullet
from game_classes import player_class
from game_classes import mellee_rectangle
from game_classes import flying_enemy
from game_classes import ground_enemy as gm
from game_classes import tiled
from game_classes import spawner
from pygame.sprite import Group
from pygame import mixer
import pygame
import math
pygame.init()
mixer.init()
global scx
global scy
scx = 1000
scy = 500
mixer.music.load('first_try\sound\music-tired-of-rock.mp3')#credit to nueki
mixer.music.play(-1 )

gunshot = mixer.Sound('first_try\sound\gun_shot.mp3')
swing = mixer.Sound('first_try\sound\swing.mp3')
wound = mixer.Sound('first_try\sound\slash.mp3')
'''basically just a sprite sheet'''
world_data = [
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  3,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [  0,  0,  0,  0,  0,  0,  2,  2,  2,  2,  2,  2,  2,  0,  0,  0,  0,  0,  0,  0],
    [  3,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  3],
    [  2,  2,  2,  2,  2,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  2,  2,  2,  2,  2],
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0],
    [  3,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  3],
    [  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2],
    [  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2,  2]
]

'''groups, screen surface, and sprites etc'''
dis = pygame.display.set_mode((scx,scy))
ti = pygame.time.Clock()
speed = [2,2,5]
theguy1 = player_class(scx//2,scy//2 - 100,speed)
theboys = Group()
projectiles = Group()
theboys.add(theguy1)
enemies = Group()
swords = mellee_rectangle(theguy1.rect.centerx,theguy1.rect.centery)
obs = Group()
melee_thingz = Group(swords)
spawners = Group()



'''the tilesize, and most importantly the target lock mechanics'''
target_lock = 0
lock_potential = []
tilesize = 50



'''for loop nested in the for loop one representing the rows the other the collumn based on the world data above,
it will either put a spawner or a platform'''
for y in range(len(world_data)):
    for x in range(len(world_data[y])):
        if world_data[y][x] == 2:
            onetile = tiled(x*tilesize + 23,y*tilesize)
            obs.add(onetile)
        if world_data[y][x] == 3:
            spawn = spawner(x*tilesize +23,y*tilesize)
            spawn.player = theguy1
            spawn.group = enemies
            spawners.add(spawn)

'''background values i should have put in a game settings'''
points = 0
therun = True
highscore = 0

thefont=  pygame.font.SysFont("Arial",30)
last = 0
now = 0
'''the entire whiloop to run the game'''
bb = False
while therun:
    
    dis.fill('White')
    
    
    scoretext = thefont.render('Score: '+ str(points),True,'Black' )
    highscoretext = thefont.render('highScore: '+ str(highscore) ,True,'Black')
    dis.blit(scoretext,(0,50))
    dis.blit(highscoretext,(0,0))
    
    '''just deletes all the enemies in lock potential which is no longer in the sprite group enemies'''
    lock_potential = [ene for ene in lock_potential if ene in enemies.sprites()]
    '''at a certain distance it will either add or remove an element from the lock potential list, which is used to handle target locking'''
    for enema in enemies.sprites():
        dist = abs(math.sqrt((theguy1.rect.centerx - enema.rect.centerx)**2+(theguy1.rect.centery - enema.rect.centery)**2))
        if dist <= 300:
            if not enema in lock_potential:
                lock_potential.append(enema)
        else:
            if enema in lock_potential:
                lock_potential.remove(enema)

    '''WHILE LOOP EVENT TRACKING'''
    for each in pygame.event.get():
        if each.type == pygame.QUIT:
            quit()
            exit()
        if each.type == pygame.KEYDOWN:
            '''as you can see here it is simply adjusting the values of the targetlock varible based on its value if it gets to the maximum value which would be
            in this case len(lock_potential), target lock will be set to 0, however if targetlock would be less than the maximum it would simply add itself
            by one'''
            if each.key == pygame.K_i:
                if target_lock < len(lock_potential)-1:
                    target_lock += 1
                elif not lock_potential:
                    pass
                else:
                    target_lock = 0

            '''if lock potential is not empty it will shoot a bullet'''
            if each.key == pygame.K_k and lock_potential:
                    nebull = bullet(5,[lock_potential[target_lock].rect.centerx,lock_potential[target_lock].rect.centery],theguy1.rect.centerx,theguy1.rect.centery)
                    gunshot.play()
                    projectiles.add(nebull)

            '''made new sprite added it to the group'''
            if each.key == pygame.K_j:
                swords = mellee_rectangle(theguy1.rect.centerx,theguy1.rect.centery)
                swing.play()
                melee_thingz.add(swords)
    '''just adjust the position for each apeneded sprite which is an element in mellee_thingz'''
    for melee in melee_thingz:
        melee.rect.centerx = theguy1.rect.centerx
        melee.rect.bottom = theguy1.rect.bottom + 3
    '''if the target lock ever gets too large this is used to maintain target lock number with in the index length of the
    lock potential list'''
    if target_lock >= len(lock_potential):
        target_lock = len(lock_potential) -1
        

    '''sword placement'''
    swords.rect.centerx = theguy1.rect.centerx
    swords.rect.bottom = theguy1.rect.bottom + 4
    '''just drawing and updating'''
    melee_thingz.update()
    melee_thingz.draw(dis)
    obs.update()
    '''kill bullet when hit enemy and obstacles, but also kill enemy if bullet hits'''
    pygame.sprite.groupcollide(projectiles,obs,True,False)
    enemyslashed=pygame.sprite.groupcollide(melee_thingz,enemies,False,True)
    enemyattacked=pygame.sprite.groupcollide(projectiles,enemies,True,True)
    playerhit=pygame.sprite.spritecollide(theguy1,enemies,False)
    '''if player gets hit bny the enemy if statement, basically just a death'''
    if playerhit  or theguy1.rect.top >= 500:
        enemies.empty()
        rounds = 0
        points = 0
        theguy1.rect.centerx = scx//2 + 50
        theguy1.rect.centery = scy//2 - 100
        for sp in spawners.sprites():
            sp.spawn(obs)
    '''if there are no enemies in the enemies sprite group the spawners will spawn maore enemies also drawing and updating'''
    spawners.draw(dis)
    if not enemies.sprites():
        for sp in spawners.sprites():
            sp.spawn(obs)
        

    '''point goes up for every enemy killed/hit and highscore change values if the score is higer than the highscore'''
    if enemyattacked:
        for enemie in enemyattacked:
            wound.play()
            points += 1
    elif enemyslashed:
        for enemie in enemyslashed:
            wound.play()
            points += 1
    if points > highscore:
        highscore = points
    '''just draw and update groups here'''
    obs.draw(dis)
    theboys.draw(dis)
    theguy1.collison(obs)
    projectiles.update()
    projectiles.draw(dis)
    theguy1.move(obs)
    enemies.update()
    enemies.draw(dis)
    for sprite in enemies.sprites():
        if sprite.rect.top >= 500:
            sprite.kill()
    '''its just drawing a circle on the selected enemies to target lovck'''
    if lock_potential:
            pygame.draw.circle(dis,'Red',(lock_potential[target_lock].rect.centerx,lock_potential[target_lock].rect.centery),10)
    else:
        target_lock = 0

    ti.tick(120)
    pygame.display.update()




