from graphics import *
import pygame
from os import *
from PewPewPeachLibrary import *

pygame.font.init()
pygame.init()
pygame.mixer.init() 

menu = True
#Graphics.py ===================================

win = GraphWin("PEW PEW PEACH!", 550,800)
win.setBackground("black")


play_sfx(load)
poster = image2(275,400, 'group.png', win)
time.sleep(3)
poster.undraw


play_music('Intro.wav')
poster = image2(275,400, 'poster.png', win)
time.sleep(3)
poster.undraw


backgroundGraphics = image2(275,400, 'loadScreen.png', win)
load = image2(275,400, 'load0.png', win)

    
for i in range(12):
    load = get_image(275,300,f'Planet{i+1}.png',win)
    backgroundGraphics.move(0,5)
    mouse = win.checkMouse() 
    if i == 2:
        load = image2(275,400,'load1.png',win)
    if i == 4:
        load = image2(275,400,'load2.png',win)
    if i == 7:
        load = image2(275,400,'load3.png',win)
    if i == 8:
        load = image2(275,400,'load4.png',win)
    if i == 10:
        load = image2(275,400,'load5.png',win)
planet = image2(275,300,'Planet1.png', win)
load = loadingScreen(menu, win)


#===============================================
#Pygame ========================================
def main():
    player.hide_ship
    player.hide_ship
    
    clock = pygame.time.Clock()
    FPS = 60
    spawnCount = 0
    ufoShootCount = 0
    stageTimer = 0
    distance = 0
    
    play_music("Storm-RG-Cool-Journey.wav")

    def minus_lives():
        if player.lives == 2:
            heart3.kill()
        if player.lives == 2 and player.health == 8:
            play_sfx(loseLife)
        
        if player.lives == 1:
            heart2.kill()
        if player.lives == 1 and player.health == 8:
            play_sfx(loseLife)
            
        if player.lives < 1:
            play_sfx(lose)
            heart1.kill()
            meteor_collisions(meteor_collision)
            gameOver()

    heart1 = LivesDisplay(250,8)
    heart2 = LivesDisplay(280,8)
    heart3 = LivesDisplay(310,8)
    heart_group.add(heart1, heart2, heart3)

    runStage1 = True
    runStage2 = False
    runStage3 = False
    runStage4 = False

    if runStage1:  
        ship_health_display()
        for i in range(10): 
            spawn_meteor() 
        background = get_img('bg1.png')
        background_rect = background.get_rect()

    while runStage1:
        distance += 1
        stageTimer+=1
        spawnCount += 1
        clock.tick(FPS)
        
        WIN.blit(background, background_rect)
        sprites.update() 
        sprites.draw(WIN)
        WIN.blit(border_img, (0, 0))
        messages('1', 60, (250,250,250), 800, 85)
        messages(f'{player.score}', 45, (164,185,202), 550, 24)
    
        heart_group.update()
        playersprite.update()
        playersprite.draw(WIN)
        heart_group.draw(WIN)

        pygame.display.update()

        if  distance == 6 : 
            player.score += 1
            distance = 0

        if spawnCount == 150: 
            for i in range (15):
                spawn_meteor()
            spawnCount = 0

        if stageTimer > 1805:
            player.health = 8 
            stageTimer = 0
            ship_health_display()
            stage_clear()
            pygame.display.update()
            spawnCount = 0
            distance = 0
            runStage1 = False
            runStage2 = True



        #Collisions
        meteor_collision = pygame.sprite.spritecollide(player, meteors, True, pygame.sprite.collide_circle)
        for collide in meteor_collision:
            meteor_collisions(meteor_collision)
            minus_lives()
            ship_health_display()
            player.score -= 20
                
        #Shooting 
        bullet_collision = pygame.sprite.groupcollide(bullets, meteors, True, True)
        for collision in bullet_collision:
            shipBullet_collide_object(bullet_collision)
            player.score += 10
        
        # EVENT STAGE
        keys = pygame.key.get_pressed() 
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:
                    pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
    #=========================================================
    #STAGE 2 =========================================================
    #=========================================================
    pygame.font.init()
    if runStage2:
        for i in range(10): 
            spawn_ufo() 
        background = get_img('bg2.png')
        background_rect = background.get_rect()

    while runStage2:
        distance +=1
        stageTimer +=1
        spawnCount += 1
        clock.tick(FPS)
        WIN.blit(background, background_rect)
        sprites.update()
        sprites.draw(WIN)
        WIN.blit(border_img, (0, 0))

        messages('2', 60, (250,250,250), 800, 85)
        messages(f'{player.score}', 45, (164,185,202), 550, 24)
        heart_group.update()
        playersprite.update()
        playersprite.draw(WIN)
        heart_group.draw(WIN)

        pygame.display.update()

        if distance > 3.5: 
            player.score += 1
            distance = 0 
        if spawnCount == 150: 
            for i in range (10):
                spawn_ufo()
            spawnCount = 0
        if stageTimer> 1805:
            player.health = 8 
            stageTimer = 0
            distance = 0 
            spawnCount = 0
            ship_health_display()
            stage_clear()

            runStage2 = False
            runStage3 = True


        #Ship Crash
        ufo_collision = pygame.sprite.spritecollide(player, ufo_group, True)
        for collide in ufo_collision:
            bullet_ufo_collision (ufo_collision)
            minus_lives()
            ship_health_display()
            player.score -= 20
        meteor_collision = pygame.sprite.spritecollide(player, meteors, True, pygame.sprite.collide_circle)
        for collide in meteor_collision:
            meteor_collisions(meteor_collision)
            minus_lives()
            ship_health_display()
            player.score -= 20


        #Shooting 
        bullet_collision = pygame.sprite.groupcollide(bullets, meteors, True, True)
        for collision in bullet_collision:
            shipBullet_collide_object(bullet_collision)
            player.score += 10
        bullet_collision2 = pygame.sprite.groupcollide(bullets, ufo_group, True, True)
        for collision in bullet_collision2:
            shipBullet_collide_object(bullet_collision2)
            player.score += 15

        #EVENT STAGE
        keys = pygame.key.get_pressed() 
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:
                    pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()   
    #=========================================================
    #STAGE 3 =========================================================
    #=========================================================
    if runStage3:
        for i in range(20): 
            spawn_ufo2() 
        background = get_img('bg3.png')
        background_rect = background.get_rect()

    while runStage3:
        distance += 1
        stageTimer +=1
        spawnCount += 1
        ufoShootCount +=1
        clock.tick(FPS)
        WIN.blit(background, background_rect)
        sprites.update()
        sprites.draw(WIN)
        WIN.blit(border_img, (0, 0))

        messages('3', 60, (250,250,250), 800, 85)
        messages(f'{player.score}', 45, (164,185,202), 550, 24)
        heart_group.update()
        playersprite.update()
        playersprite.draw(WIN)
        heart_group.draw(WIN)

        pygame.display.update()

        if distance > 3.5: 
            player.score += 1
            distance = 0 
        if spawnCount == 75: 
            for i in range (5):
                spawn_ufo2()
            spawnCount = 0
        if stageTimer > 3605:
            player.health = 8 
            stageTimer = 0
            distance = 0 
            spawnCount = 0
            ship_health_display()
            stage_boss()
            runStage3 = False
            runStage4 = True


        #Ship Crash
        ufo_collision = pygame.sprite.spritecollide(player, ufo_group, True)
        for collide in ufo_collision:
            bullet_ufo_collision (ufo_collision)
            minus_lives()
            ship_health_display()
            player.score -= 20

        ufo_bullet_collision = pygame.sprite.spritecollide(player, UFObullets, True)
        for collide2 in ufo_bullet_collision:
            bullet_ufo_collision (ufo_bullet_collision)
            minus_lives()
            ship_health_display()
            player.score -= 20
    
            
        #Shooting 
        bullet_collision2 = pygame.sprite.groupcollide(bullets, ufo_group, True, True)
        for collision in bullet_collision2:
            shipBullet_collide_object(bullet_collision2)
            player.score += 15
        bullet_collision3 = pygame.sprite.groupcollide(bullets, ShootingUfo_group, True, True)
        for collision in bullet_collision3:
            shipBullet_collide_object(bullet_collision3)
            player.score += 30

        # EVENT STAGE
        keys = pygame.key.get_pressed() 
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:
                    pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()      
    #=========================================================
    #STAGE 4 =========================================================
    #=========================================================
    if runStage4:  
        boss_health_display()
        play_sfx(bossNotif)                 
        bossSprite.add(bossShip)
        background = get_img('bg4.png')
        background_rect = background.get_rect()

    while runStage4:
        spawnCount += 1
        ufoShootCount +=1
        clock.tick(FPS)
        WIN.blit(background, background_rect)
        sprites.update()
        sprites.draw(WIN)
        WIN.blit(border_img, (0, 0))

        messages('4', 60, (250,250,250), 800, 85) 
        messages(f'{player.score}', 45, (164,185,202), 550, 24)
        heart_group.update()
        playersprite.update()
        bossSprite.update()
        heart_group.draw(WIN)
        playersprite.draw(WIN)
        bossSprite.draw(WIN)
        pygame.display.update()

        if spawnCount == 200: 
            for i in range (3):
                spawn_ufo3()
                spawn_ufo4()
                spawn_meteor()
            spawnCount = 0
        
        #Ship Crash
        ufo_bullet_collision = pygame.sprite.spritecollide(player, UFObullets, True)
        for collide in ufo_bullet_collision:
            bullet_ufo_collision (ufo_bullet_collision)
            minus_lives()
            ship_health_display()
            player.score -= 20

        meteor_collision = pygame.sprite.spritecollide(player, meteors, True, pygame.sprite.collide_circle)
        for collide in meteor_collision:
            meteor_collisions(meteor_collision)
            minus_lives()
            ship_health_display()
            player.score -= 20

        boss_bullet_collision = pygame.sprite.spritecollide(player, bossbullets, True, pygame.sprite.collide_circle)
        for collide in boss_bullet_collision :
            bullet_boss_collision(boss_bullet_collision)
            minus_lives()
            ship_health_display()
            player.score -= 20


        #Shooting 
        bullet_collision1 = pygame.sprite.groupcollide(bullets, meteors, True, True)
        for collision in bullet_collision1:
            shipBullet_collide_object(bullet_collision1)
            player.score += 15
        bullet_collision3 = pygame.sprite.groupcollide(bullets, ShootingUfo_group, True, True)
        for collision in bullet_collision3:
            shipBullet_collide_object(bullet_collision3) 
            player.score += 30
        bullet_collision4 = pygame.sprite.spritecollide(bossShip, bullets,  True, pygame.sprite.collide_circle)
        for collision in bullet_collision4:
            shipBullet_collide_boss(bullet_collision4)
            boss_health_display()
        
            if bossShip.life == 0:
                play_sfx(success)
                stageCleared()

        # EVENT STAGE
        keys = pygame.key.get_pressed() 
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:
                    pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()     

#=========================================================
# GAME OVER =========================================================
#=========================================================

def gameOver():
    gameEnd = True
    if gameEnd:
        messages(f'Final Score: {player.score}', 50, (250,250,250), 1080, 250)
        if player.score > 15000:
            WIN.blit(gameOverMenu1, (0,0))
        elif player.score > 5999 and player.score < 15000:
            WIN.blit(gameOverMenu2, (0,0))
        elif player.score > 1499 and player.score < 6000:
             WIN.blit(gameOverMenu3, (0,0))
        elif player.score < 1299:
             WIN.blit(gameOverMenu4, (0,0))
        pygame.display.update()

    while gameEnd:
        keys = pygame.key.get_pressed() 
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:
                    pygame.quit() 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    play_sfx(start)
                    gameEnd = False
                    player.health = 8
                    player.lives = 3
                    player.score = 0

                    bullets.empty()
                    ufo_group.empty() 
                    ShootingUfo_group.empty() 
                    bossbullets.empty()  
                    UFObullets.empty
                    meteors.empty()
                    sprites.empty()
                    main()
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    play_sfx(start)
                    stopMusic()
                    #win.close()
                    pygame.quit()
                    quit()
#=========================================================
# STAGE CLEARED =========================================================
#=========================================================
  
def stageCleared():
    cleared = True
    if cleared:
        messages(f'Final Score: {player.score}', 50, (250,250,250), 1080, 250)
        if player.score > 15000:
            WIN.blit(congratulations1, (0,0))
        elif player.score > 5999 and player.score < 15000:
            WIN.blit(congratulations2, (0,0))
        elif player.score > 1499 and player.score < 6000:
             WIN.blit(congratulations3, (0,0))
        elif player.score < 1299:
             WIN.blit(congratulations4, (0,0))
        pygame.display.update()

    while cleared:
        keys = pygame.key.get_pressed() 
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:
                    pygame.quit() 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    play_sfx(start)
                    cleared = False
                    player.health = 8
                    player.lives = 3
                    player.score = 0

                    bullets.empty()
                    ufo_group.empty() 
                    ShootingUfo_group.empty() 
                    bossbullets.empty()  
                    UFObullets.empty
                    meteors.empty()
                    sprites.empty()
                    main()
        
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    play_sfx(start)
                    stopMusic()
                    win.close()
                    pygame.quit()
                    quit()               
if load == 'a': 
    play_sfx(start)
    rules = image2(275,400, 'Rules.png', win)
    time.sleep(5)

    controls = image2(275,400, 'Controls.png', win)
    time.sleep(3)

    stopMusic()
    win.close()
    menu = False
    win.close()
    main()

if load == 'b':
    play_sfx(start)
    menu = False
    stopMusic()
    win.close()
    pygame.quit()
    quit()
          
pygame.quit()
quit()

            

