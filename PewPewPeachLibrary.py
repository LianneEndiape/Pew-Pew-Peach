from graphics import *
import pygame
from os import *
import random
#Music ================================================================


def get_music(file_name):
    music = pygame.mixer.music.load(path.join(music_folder, file_name))
    return music


def play_sfx(file_name):
    pygame.mixer.Sound.play(file_name)
  

def play_music(file_name):
    get_music(file_name)
    pygame.mixer.music.play(-1)

def stopMusic():
    pygame.mixer.music.stop()

#Graphics.py ===================================

def get_image(x,y,picture,win):
    get_img = (path.join(img_folder, picture))
    image = Image(Point(x,y),get_img)
    image.draw(win)
    time.sleep(0.5)
    image.undraw()

def image2(x,y,picture,win):
    get_img = (path.join(img_folder, picture))
    pic = Image(Point(x,y),get_img)
    pic.draw(win)
    return pic

def loadingScreen(menu, win):
    while menu:   
        final = image2(275,300, 'Planet1.png', win)
        PressA = image2(275,490, 'PressA.png', win)
        PressB = image2(275,570,'PressB.png', win)

        key = win.checkKey()
        if key == "a" or key == "A" :
            return key
            break 
        if key == "b" or key == "B":
            return key 
            break 

    
#=======================================================

#Setting
pygame.font.init()
pygame.init()
pygame.mixer.init() 

WIDTH, HEIGHT = 1600, 800
SHIP_WIDTH, SHIP_HEIGHT = 115, 115
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Pew Pew Peach!")

clock = pygame.time.Clock()
FPS = 70
meteor_count = 0

font_name = pygame.font.match_font("Retro Gaming.ttf")



#Images ================================================================

def get_img(file_name):
    image = pygame.image.load(path.join(img_folder, file_name))
    return image

# IMAGES =========================================================
game_folder = path.dirname(__file__)
img_folder = path.join(game_folder, "Assets") 
music_folder = path.join(game_folder, "Music")

#Sprites
ship_img = get_img('Ship.png')
ship_rect = ship_img.get_rect()
bullet_img = get_img('Peach.png')

ufo_img = get_img("UFO.png")
ufo_img2 = get_img("UFO2.png")
UFObullet_img = get_img("pancake.png")
boss_img = get_img("boss.png")

# Menu / GUI Images
heart_img = get_img('heart.png')
border_img = get_img('border.png')
notification = get_img("StageCleared.png")
bossWarning = get_img("StageBoss.png")

gameOverMenu1 = get_img('gameOver1.png')
gameOverMenu2 = get_img('gameOver2.png')
gameOverMenu3 = get_img('gameOver3.png')
gameOverMenu4 = get_img('gameOver4.png')

congratulations1 = get_img('clear1.png')
congratulations2 = get_img('clear2.png')
congratulations3 = get_img('clear3.png')
congratulations4 = get_img('clear4.png')

#MUSIC =========================================================
bg_music = pygame.mixer.Sound(path.join(music_folder, "Storm-RG-Cool-Journey.wav"))
load = pygame.mixer.Sound(path.join(music_folder, "LoadSFX.wav"))
start = pygame.mixer.Sound(path.join(music_folder, 'Start.wav'))
loseLife = pygame.mixer.Sound(path.join(music_folder, "LoseLife.wav"))
bossNotif = pygame.mixer.Sound(path.join(music_folder, "IncomingBoss.wav"))
success = pygame.mixer.Sound(path.join(music_folder, "Success.wav"))
gun =  pygame.mixer.Sound(path.join(music_folder, "gun.wav"))
heal =  pygame.mixer.Sound(path.join(music_folder, "Heal.wav"))
enemyExplosion =  pygame.mixer.Sound(path.join(music_folder, 'EnemyExplosion.wav'))
damage = pygame.mixer.Sound(path.join(music_folder, "Hurt.wav"))
lose = pygame.mixer.Sound(path.join(music_folder, "GameOver.wav"))

#Classes========================================================

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = ship_img
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width*.90/2) 
        self.rect.centerx = WIDTH/2
        self.rect.y = HEIGHT - 150
        self.speed = 10
        self.score = 0

        self.lastBullet = pygame.time.get_ticks()
        self.ship_hidden = False
        self.ship_hide_timer = pygame.time.get_ticks()
        
        self.health = 8
        self.lives = 3            
    def hide_ship(self):
        self.ship_hide_timer = pygame.time.get_ticks()
        self.ship_hidden = True
        self.rect.centerx = WIDTH/2
        self.rect.y = HEIGHT+300
        self.lastBullet = pygame.time.get_ticks()
    def shoot_bullet(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.lastBullet > 250 and self.ship_hidden == False:
            play_sfx(gun)
            self.lastBullet = current_time
            bullet = Bullet(self.rect.centerx, self.rect.top)
            bullets.add(bullet)
            sprites.add(bullet)
    def boundary(self):
        if (self.rect.right > WIDTH - 50):
            self.rect.x = WIDTH - 170
        if (self.rect.left < 50):
            self.rect.x = 50
    def movement(self):
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or (keys[pygame.K_a])):
            self.rect.x -= self.speed
        if (keys[pygame.K_RIGHT] or (keys[pygame.K_d])):
            self.rect.x += self.speed
        if keys[pygame.K_SPACE]:
            
            self.shoot_bullet()    
    def update(self):
        if self.ship_hidden and pygame.time.get_ticks() - self.ship_hide_timer > 1500:
            play_sfx(heal)
            self.ship_hidden = False
            self.rect.centerx = WIDTH/2
            self.rect.y = HEIGHT - 150
       
        self.boundary()
        self.movement()

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        #Finds the coordinates of spaceship 
        self.rect.x = x-20
        self.rect.y = y
        self.speedY = -10
    def update(self):
        self.rect.y += self.speedY
        if self.rect.bottom < 0:
            self.kill()

class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = random.choice(meteor_group)
        self.image = self.original_image 
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width/2)
        self.rect.x = random.randrange(0,  WIDTH)
        self.rect.y = random.randrange(-150,-100)
        self.speedY = random.randrange(3,8)
        self.speedX = random.randrange(-3,3)
    #=========================================================            
        self.last_rotation = pygame.time.get_ticks()
    
        self.angle = 0
        self.rotationSpeed = 5
    def rotation(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_rotation > 50:
            self.last_rotation = current_time
            self.angle += self.rotationSpeed
            origCenter = self.rect.center 
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            self.rect = self.image.get_rect()
            self.rect.center = origCenter
    def boundary(self):
        if (self.rect.right > WIDTH - 50) or (self.rect.left <  50):
            spawn_meteor()
            self.kill()
        if self.rect.bottom > HEIGHT:
            self.kill()
        if self.rect.bottom > HEIGHT:
            player.score += 10
            self.kill()
    def update(self):
        self.rect.y += self.speedY
        self.rect.x += self.speedX
        self.boundary()
        self.rotation()

class UFO(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = ufo_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0,  WIDTH)
        self.rect.y = random.randrange(-150,-50)
        self.speedY = random.randrange(5,8)
        self.speedX = random.randrange(0,3)
    def boundary(self):
        if (self.rect.right > WIDTH - 50) or (self.rect.left <  50):
            spawn_ufo()
            self.kill()
        if self.rect.bottom > HEIGHT:
            player.score += 10
            self.kill()
    def update(self):
        self.rect.y += self.speedY
        self.rect.x += self.speedX
        self.boundary()

class shootingUFO(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = ufo_img2
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(-50,-10)
        self.rect.y = random.randrange(100, 400)
        self.speedX = random.randrange(3,8)
        self.ufoShootCount = 0
    def shoot_bullet(self):
        bullet = UFOBullet(self.rect.centerx, self.rect.top)
        UFObullets.add(bullet)
        sprites.add(bullet)
    def update(self):
        self.ufoShootCount += 1
        if self.ufoShootCount == 135: 
            self.shoot_bullet()
            self.ufoShootCount = 0
        self.rect.x += self.speedX

class shootingUFO2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = ufo_img2
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(20,550)

        self.rect.y = 0
        self.speedY = 5
        self.speedY2 = 10
        self.ufoShootCount = 0
    def shoot_bullet(self):
        bullet = UFOBullet(self.rect.centerx, self.rect.top)
        UFObullets.add(bullet)
        sprites.add(bullet)
    def update(self):
        if self.rect.y < 200:
            self.rect.y += self.speedY
        
        self.ufoShootCount += 1
        if self.ufoShootCount == 135: 
            self.shoot_bullet()
        if self.ufoShootCount > 155: 
            self.shoot_bullet()
            self.ufoShootCount = 0  
            if self.rect.y > 0:
                self.rect.y-= self.speedY2
                self.kill()   
              
class shootingUFO3(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = ufo_img2
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(1000,1580)
        self.rect.y = 0
        self.speedY = 5
        self.speedY2 = 10
        self.ufoShootCount = 0
    def shoot_bullet(self):
        bullet = UFOBullet(self.rect.centerx, self.rect.top)
        UFObullets.add(bullet)
        sprites.add(bullet)
    def update(self):
        if self.rect.y < 200:
            self.rect.y += self.speedY
        
        self.ufoShootCount += 1
        if self.ufoShootCount == 135: 
            self.shoot_bullet()
        if self.ufoShootCount > 155: 
            self.shoot_bullet()
            self.ufoShootCount = 0  
            if self.rect.y > 0:
                self.rect.y -= self.speedY2
                self.kill()             

class UFOBullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = UFObullet_img
        self.rect = self.image.get_rect()
        #Finds the coordinates of spaceship 
        self.rect.x = x
        self.rect.y = y
        self.speedY = random.randrange(5,8)

    def update(self):
        self.rect.y += self.speedY
        if self.rect.bottom > HEIGHT:
            self.kill()

class boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = boss_img
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width*.90/2)
        self.rect.x = 600
        self.rect.y = -100
        self.speedY = 5
        self.bossShootCount = 0
        self.life = 240 

    def shoot_bullet(self):
        bossbullet1 = bossBullet(self.rect.centerx-15, self.rect.bottom)
        bossbullet2 = bossBullet(self.rect.centerx-130, self.rect.bottom)
        bossbullet3 = bossBullet(self.rect.centerx+100, self.rect.bottom)
        bossbullets.add(bossbullet1, bossbullet2, bossbullet3)
        sprites.add(bossbullet1, bossbullet2, bossbullet3)

    def update(self):
        self.bossShootCount += 1
        if self.bossShootCount == 100: 
            self.shoot_bullet()
        if self.bossShootCount == 110: 
            self.shoot_bullet()
        if self.bossShootCount == 120: 
            self.shoot_bullet()
            self.bossShootCount = 0
        if self.rect.y < 30:
            self.rect.y += self.speedY

class bossBullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = UFObullet_img
        self.rect = self.image.get_rect()
        
        self.rect.x = x
        self.rect.y = y
        self.speedY = 10
    def update(self):
        self.rect.y += self.speedY
        if self.rect.bottom > HEIGHT:
            self.kill()

class CookieExplosion(pygame.sprite.Sprite):
    def __init__(self, explosionSize, center):
        pygame.sprite.Sprite.__init__(self)
        self.explosionSize = explosionSize
        self.image = self.explosionSize[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.lastFrame = pygame.time.get_ticks()
        self.currentFrame = 0
    
    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.lastFrame > 20:
            self.lastFrame = current_time
            self.currentFrame +=1

            if self.currentFrame == len(self.explosionSize):
                self.kill()

            else:
                oldcenter = self.rect.center
                self.image = self.explosionSize[self.currentFrame]
                self.rect = self.image.get_rect()
                self.rect.center = oldcenter

class LivesDisplay (pygame.sprite.Sprite):
    def __init__(self,x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = heart_img
        self.rect = self.image.get_rect()
        self.center = 5
        self.rect.x = x 
        self.rect.y = y
    def update(self):
        return self.image

class BarDisplay (pygame.sprite.Sprite):
    def __init__(self, bar_image):
        pygame.sprite.Sprite.__init__(self)
        self.image = bar_image
        self.rect = self.image.get_rect()
        self.center = 5
        self.rect.x = 670 
        self.rect.y = 730 
    def update(self):
        return self.image

class BossBarDisplay (pygame.sprite.Sprite):
    def __init__(self, bar_image):
        pygame.sprite.Sprite.__init__(self)
        self.image = bar_image
        self.rect = self.image.get_rect()
        self.center = 5
        self.rect.x = 670 
        self.rect.y = 350
    def update(self):
        return self.image

class notificationStageCleared (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = notification
        self.rect = self.image.get_rect()
        self.speedY = 5
        self.center = 5
        self.rect.x = 0 
        self.rect.y = -50
        self.counter = 0
    def movement(self):
        self.counter += 1
        if self.rect.y < 0:
            self.rect.y += self.speedY
        if self.counter == 35:
            self.kill()
            self.counter = 0
    def update(self):
        self.movement()
        return self.image
    
class notificationBoss (pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = bossWarning
        self.rect = self.image.get_rect()
        self.speedY = 5
        self.center = 5
        self.rect.x = 0 
        self.rect.y = -50
        self.counter = 0
    def movement(self):
        self.counter += 1
        if self.rect.y < 0:
            self.rect.y += self.speedY
        self.rect.y = -10
        if self.counter == 35:
            self.kill()
            self.counter = 0
    def update(self):
        self.movement()
        return self.image


def ship_health_display():
    bar_image1 = get_img('bar1.png')
    bar_image2 = get_img('bar2.png')
    bar_image3 = get_img('bar3.png')
    bar_image4 = get_img('bar4.png')
    bar_image5 = get_img('bar5.png')
    bar_image6 = get_img('bar6.png')
    bar_image7 = get_img('bar7.png')
    bar_image8 = get_img('bar8.png')    
    
        
    if player.health == 8:
        bar = BarDisplay(bar_image8)        
    if player.health == 7:
        bar = BarDisplay(bar_image7) 
    if player.health == 6:
        bar = BarDisplay(bar_image6) 
    if player.health == 5:
        bar = BarDisplay(bar_image5) 
    if player.health == 4:
        bar = BarDisplay(bar_image4) 
    if player.health == 3:
        bar = BarDisplay(bar_image3) 
    if player.health == 2:
        bar = BarDisplay(bar_image2) 
    if player.health == 1:
        bar = BarDisplay(bar_image1) 

    healthbars.add(bar)
    sprites.add(bar)

def boss_health_display():
    bossbar_image0 = get_img('Bossbar0.png')
    bossbar_image1 = get_img('Bossbar1.png')
    bossbar_image2 = get_img('Bossbar2.png')
    bossbar_image3 = get_img('Bossbar3.png')
    bossbar_image4 = get_img('Bossbar4.png')
    bossbar_image5 = get_img('Bossbar5.png')
    bossbar_image6 = get_img('Bossbar6.png')
    bossbar_image7 = get_img('Bossbar7.png')
    bossbar_image8 = get_img('Bossbar8.png')    
    
        
    if bossShip.life <= 240 and bossShip.life > 200: 
        bossbar = BossBarDisplay(bossbar_image8)        
    if bossShip.life <= 210 and bossShip.life > 180: 
        bossbar = BossBarDisplay(bossbar_image7) 
    if bossShip.life <= 180 and bossShip.life > 150: 
        bossbar = BossBarDisplay(bossbar_image6) 
    if bossShip.life <= 150 and bossShip.life > 120: 
        bossbar = BossBarDisplay(bossbar_image5) 
    if bossShip.life <= 120 and bossShip.life > 90:
        bossbar = BossBarDisplay(bossbar_image4) 
    if bossShip.life <= 90 and bossShip.life > 60: 
        bossbar = BossBarDisplay(bossbar_image3) 
    if bossShip.life <= 60 and bossShip.life > 30:
        bossbar = BossBarDisplay(bossbar_image2) 
    if bossShip.life <= 30 and bossShip.life > 20: 
        bossbar = BossBarDisplay(bossbar_image1) 
    if bossShip.life <= 20:
        bossbar = BossBarDisplay(bossbar_image0) 

    healthbars.add(bossbar)
    sprites.add(bossbar)

#Sprites========================================================

bossShip = boss()
player = Player()

sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
meteors = pygame.sprite.Group()
lives_display = pygame.sprite.Group()
ufo_group = pygame.sprite.Group()
ShootingUfo_group = pygame.sprite.Group()
UFObullets = pygame.sprite.Group()
bossbullets = pygame.sprite.Group()
healthbars = pygame.sprite.Group()
heart_group = pygame.sprite.Group()
playersprite = pygame.sprite.Group()
bossSprite = pygame.sprite.Group()

playersprite.add(player)
#Functions======================================================

# Display Functions

def messages (msg, font_size, color, x, y):
    font = pygame.font.SysFont(font_name, font_size)
    text = font.render(msg, True, color)
    text_rect = text.get_rect()
    text_rect.center = (x,y)
    WIN.blit(text, text_rect)

# Spawning Objects

def spawn_meteor():
    meteor = Meteor()
    meteors.add(meteor)
    sprites.add(meteor)

def spawn_ufo():
    ufo = UFO()
    ufo_group.add(ufo)
    sprites.add(ufo)

def spawn_ufo2():
    ufo2 = shootingUFO()
    ShootingUfo_group.add(ufo2)
    sprites.add(ufo2)

def spawn_ufo3():
    ufo3 = shootingUFO2()
    ShootingUfo_group.add(ufo3)
    sprites.add(ufo3)

def spawn_ufo4():
    ufo4 = shootingUFO3()
    ShootingUfo_group.add(ufo4)
    sprites.add(ufo4)  

def stage_clear():
    play_sfx(start)
    notification = notificationStageCleared()
    sprites.add(notification)  

def stage_boss():
    boss_notif = notificationBoss()
    sprites.add(boss_notif) 

# Ship Bullets Collision To Enemies

def shipBullet_collide_object(bullet_collision):
    for collision in bullet_collision:
        play_sfx(enemyExplosion)
        explosion = CookieExplosion(cookie_explosionBig, collision.rect.center)
        sprites.add(explosion)

def shipBullet_collide_boss(bullet_collision):
    for collide in bullet_collision:
        play_sfx(enemyExplosion)
        explosion = CookieExplosion(ship_explosionSmall, bossShip.rect.center)
        sprites.add(explosion)
        bossShip.life -= 1
        if bossShip.life < 1:
            player.score += 5000
            Finalexplosion = CookieExplosion(ship_explosion, player.rect.center)
            sprites.add(Finalexplosion)
            bossShip.kill()
            

# Enemy Bullets Collision to Ship  

def meteor_collisions(meteor_collision):
    ship_health_display()
    for collide in meteor_collision:
        play_sfx(damage)
        explosion = CookieExplosion(ship_explosionSmall, player.rect.center)
        sprites.add(explosion)
        player.health -= 1
        if player.health < 1:
            Finalexplosion = CookieExplosion(ship_explosion, player.rect.center)
            sprites.add(Finalexplosion)
            player.hide_ship()
            player.lives -=1
            player.health = 8   

def bullet_ufo_collision (ufo_collision):
    ship_health_display()
    for collide in ufo_collision:
        play_sfx(damage)
        explosion = CookieExplosion(ship_explosionSmall, player.rect.center)
        sprites.add(explosion)
        player.health -= 1
        if player.health < 1:
            Finalexplosion = CookieExplosion(ship_explosion, player.rect.center)
            sprites.add(Finalexplosion)
            player.hide_ship()
            player.lives -=1
            player.health = 8  

def bullet_boss_collision (ufo_collision):
    ship_health_display()
    for collide in ufo_collision:
        play_sfx(damage)
        explosion = CookieExplosion(ship_explosionSmall, player.rect.center)
        sprites.add(explosion)
        player.health -= 1
        if player.health < 1:
            Finalexplosion = CookieExplosion(ship_explosion, player.rect.center)
            sprites.add(Finalexplosion)
            player.hide_ship()
            player.lives -=1
            player.health = 8  


#ANIMATION of EXPLOSIONS=================================================

cookie_explosionBig = []
ship_explosion = []
ship_explosionSmall = []
meteor_group = []

for i in range(3):
    small_ship_explosion = get_img(f"explosionShip{i+1}.png") 
    ship_explosionSmall.append(pygame.transform.scale(small_ship_explosion, (100,100)))

for i in range(8):
    ship_explosion_img = get_img(f"explosionShip{i+1}.png") 
    ship_explosion.append(ship_explosion_img)

for i in range(5):
    explosion_img = get_img(f"explosionCookie{i+1}.png") 
    cookie_explosionBig.append(pygame.transform.scale(explosion_img, (200,200)))
  
for i in range(3): 
    meteor_img = get_img("cookie{}.png".format(i+1))
    meteor_group.append(meteor_img)
