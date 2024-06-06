import pygame
from pygame.locals import *
import sys
import random
import time
 
pygame.init() # initialize pygame
vec = pygame.math.Vector2 #2 for two dimensional

# parametere vi bruger igennem koden.
HEIGHT = 450
WIDTH = 400
ACC = 0.5
FRIC = -0.12
FPS = 60
 
FramePerSec = pygame.time.Clock() # en klokke brugt til FPS
 
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT)) #laver vores screen
pygame.display.set_caption("Game")

background = pygame.image.load("background.png") # baggrunds billede
pygame.mixer.music.load("BackgroundSong.mp3") # baggrunds sang
coin_sound = pygame.mixer.Sound("CoinPickUp.mp3") # lyd på vores coins
coin_sound.set_volume(0.1)
 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        img = pygame.image.load('snowman.png')
        self.surf = img # sætter vores surface til at vores "snowman"
        self.rect = self.surf.get_rect() # sætter størrelsen til at passe billedet
   
        self.pos = vec((10, 360))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.jumping = False
        self.score = 0 
 
    def move(self):
        self.acc = vec(0,0.5)# gravity parameter
    
        pressed_keys = pygame.key.get_pressed()
                
        if pressed_keys[K_LEFT]: #gå mod venstre
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]: #gå mod højre
            self.acc.x = ACC
        
        # sætter friction på players movement. kan ændre hastigheden på spilleren ved at ændre FRIC. lidt compliceret matematik.
        self.acc.x += self.vel.x * FRIC 
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
         
        if self.pos.x > WIDTH: # gå så man kan gå fra den ene side af skærmen til den anden.
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
             
        self.rect.midbottom = self.pos
 
    def jump(self): # hop hvis du ikke allerede hopper
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
           self.jumping = True
           self.vel.y = -15
 
    def cancel_jump(self): # gør at man kan lave et lille hop
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3
 
    def update(self):
        hits = pygame.sprite.spritecollide(self ,platforms, False)
        if self.vel.y > 0: #bugfix if der stopper hop      
            if hits:
                if self.pos.y < hits[0].rect.bottom:
                    if hits[0].point == True:  # giv point hvis platformen ikke har et hit
                        hits[0].point = False    # dette gør at man ikke kan få point for at hoppe-
                        self.score +=1          #- flere gange på den samme platform           
                    self.pos.y = hits[0].rect.top +1 # sæt player til toppen af platformen.
                    self.vel.y = 0
                    self.jumping = False
P1 = Player()

class Coin(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.image = pygame.image.load("Coin.png")
        self.rect = self.image.get_rect()

        self.rect.topleft = pos

    def update(self):
        if self.rect.colliderect(P1.rect):
            P1.score += 5
            pygame.mixer.Sound.play(coin_sound)
            self.kill()
 
 
class platform(pygame.sprite.Sprite):
    def __init__(self, width = 0, height = 18):
        super().__init__()

        if width == 0:
            width = random.randint(50, 120)

        self.image = pygame.image.load("platform.png")
        self.surf = pygame.transform.scale(self.image, (width, height))
        self.rect = self.surf.get_rect(center = (random.randint(0,WIDTH-10),
                                               random.randint(0, HEIGHT-30))) #spawn position

        self.point = True   
        self.moving = True
        self.speed = random.randint(-1, 1)

        if (self.speed == 0):
            self.moving == False
        
        if P1.score > 50: # gør spillet sværere når score rammer 50
            if self.speed < 0:
                self.speed = self.speed - 1
            if self.speed > 0:
                self.speed = self.speed + 1
        
        if P1.score > 100: # gør spillet sværere når score rammer 100
            if self.speed < 0:
                self.speed = self.speed - 1
            if self.speed > 0:
                self.speed = self.speed + 1

        if P1.score > 150: # gør spillet sværere når score rammer 100
            if self.speed < 0:
                self.speed = self.speed - 1
            if self.speed > 0:
                self.speed = self.speed + 1

    def move(self): 
        hits = self.rect.colliderect(P1.rect)
        if self.moving == True:  
            self.rect.move_ip(self.speed,0) #move_ip bevæger self.rect imens move() laver en ny self.rect
            if hits:
                P1.pos += (self.speed, 0) # bevæger spilleren med platformen
            if self.speed > 0 and self.rect.left > WIDTH: # går over på den modsatte side af skærmen
                self.rect.right = 0
            if self.speed < 0 and self.rect.right < 0:
                self.rect.left = WIDTH

    def generateCoin(self):
        if (self.speed == 0):
            coins.add(Coin((self.rect.centerx, self.rect.centery - 50)))
 
 
def check(platform, groupies): # return true if collision or a platform is close, else return false.
    if pygame.sprite.spritecollideany(platform,groupies):
        return True
    else:
        for entity in groupies:
            if entity == platform:
                continue
            if (abs(platform.rect.top - entity.rect.bottom) < 40) and (abs(platform.rect.bottom - entity.rect.top) < 40):
                return True
        C = False
 
def plat_gen():
    while len(platforms) < 7:
        width = random.randrange(50,100)
        p  = None      
        C = True
         
        while C:
             p = platform()
             p.rect.center = (random.randrange(0, WIDTH - width),
                              random.randrange(-50, 0))
             C = check(p, platforms)

        p.generateCoin()
        platforms.add(p)
        all_sprites.add(p)
 

all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
coins = pygame.sprite.Group()
        
PT1 = platform(450, 80) 
#PT1.surf = pygame.Surface((WIDTH, 20))
#PT1.surf.fill((255,0,0))
PT1.rect = PT1.surf.get_rect(center = (WIDTH/2, HEIGHT - 10))
PT1.point = False #fjerner point fra base platform
PT1.moving = False #fjerner move fra base platform

all_sprites.add(PT1)
all_sprites.add(P1)
platforms.add(PT1)

pygame.mixer.music.play(-1) # spil musik på repeat

 
for x in range(random.randint(5,6)): #spawner de første platforme
    C = True
    pl = platform()
    while C:
        pl = platform()
        C = check(pl, platforms)
    pl.generateCoin()
    platforms.add(pl)
    all_sprites.add(pl)
 
 
while True: # start på loop
    P1.update()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:    
            if event.key == pygame.K_SPACE: # tryk space for at jump
                P1.jump()
        if event.type == pygame.KEYUP: # slip space for at cancel jump
            if event.key == pygame.K_SPACE:
                P1.cancel_jump()

    if P1.rect.top > HEIGHT: # game over screen
        for entity in all_sprites:
            entity.kill()
            time.sleep(1)
            game_over_font = pygame.font.SysFont('Verdana', 60)
            game_over = game_over_font.render("Game Over", True, (255,0,0))
            displaysurface.blit(game_over, (WIDTH/8, HEIGHT/2.5))
            pygame.display.update()
            time.sleep(2)
            pygame.quit()
            sys.exit()
 
    if P1.rect.top <= HEIGHT / 3: # vores player og platforme følger skræmen når den går op
        P1.pos.y += abs(P1.vel.y)
        for plat in platforms:
            plat.rect.y += abs(P1.vel.y)
            if plat.rect.top >= HEIGHT: # fjern platformen der ryger under skærmen
                plat.kill()

        for coin in coins: # gør det med coins
            coin.rect.y += abs(P1.vel.y)
            if coin.rect.top >= HEIGHT:
                coin.kill()

    keys = pygame.key.get_pressed() #flip the snowman
    if keys[pygame.K_RIGHT]:
        P1.surf = pygame.transform.flip(pygame.image.load('snowman.png'), True, False) 
    if keys[pygame.K_LEFT]:
        P1.surf = pygame.image.load('snowman.png')
    
    plat_gen()
    displaysurface.blit(background, (0, 0)) # display backgound
    f = pygame.font.SysFont("Verdana", 20) # laver font for score    
    g  = f.render(str(P1.score), True, (123,255,0)) # render vores score
    displaysurface.blit(g, (WIDTH/2, 10)) # displayer vores score
     
    for entity in all_sprites: # render og update sprites
        displaysurface.blit(entity.surf, entity.rect)
        entity.move()

    for coin in coins: # render and update coins
        displaysurface.blit(coin.image, coin.rect)
        coin.update()
 
    pygame.display.update()
    FramePerSec.tick(FPS)
