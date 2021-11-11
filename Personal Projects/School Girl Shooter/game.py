# ----------------------------------------------------------------
# School Girl Shooter 
# By Rafael Sanchez
# Description: A simple school shooter arcade.
# ----------------------------------------------------------------
# Code is devided in sections
# ------------------------------------------------- ESSENTIALS ------------------------------------------------------- 
# Imports go here
import pygame
from pygame import mixer
import random

# Here import the buttons that you want from pygame
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_SPACE,
    K_RETURN,
    KEYDOWN,
    QUIT,
)

# Insert Game Title
GAME_TITLE = "School Girl Shooter"

# Here initialize the game. Leave this alone.
pygame.init()
pygame.font.init()
mixer.init()

# Change game Icon for window
programIcon = pygame.image.load('Data\\ikon.png')
pygame.display.set_icon(programIcon)

# Define some playtesting colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Define size of Game Window
WID = 800
HEI = 600

# Width and Height of the screen are initialized
size = (WID, HEI)
screen = pygame.display.set_mode(size)

# Display Game Title
pygame.display.set_caption(GAME_TITLE)

# Define the fonts to be used in-game
MAX_SIZE = 100
SIZES = [int(MAX_SIZE*0.2), int(MAX_SIZE*0.4), int(MAX_SIZE*0.6), int(MAX_SIZE*0.8), MAX_SIZE]

# Used to manage how fast the screen updates
clock = pygame.time.Clock()
# ------------------------------------------------- ESSENTIALS ------------------------------------------------------- 
# ------------------------------------------------- USEFUL -----------------------------------------------------------
# Define variables for game logic here 
PLAYER_W = 40
PLAYER_H = 80
player_x = WID//2
player_y = HEI//2+77
vel = 3
is_menu = True
sprite_str_g = ['Data\\idle_girl_right_1.png', 'Data\\idle_girl_right_2.png', 'Data\\walk_girl_right_1.png', 'Data\\walk_girl_right_2.png', 'Data\\shootr.png']
all_sprites = pygame.sprite.Group()
moving = False
INT_MAX = 2147483647
FPS = 120
stagePosX = 0
startScrollingPosX = WID//2
spritePosX = player_x
stageVelocity = 0
leftWall = 400
rightWall = 3325
bg_img = pygame.image.load('Data\\bg.png').convert()
bg_rect = bg_img.get_rect()
is_shooting = False
lookingLeft = False
canShootAgain = True
shootingDelay = 0
reloading = False
MAX_BULLETS = 10
bullets = MAX_BULLETS
reloadingDelay = 0
MAX_HEALTH = 100
health = MAX_HEALTH
#kills = 0
#packs = 0
start_time = True
ticks_since_init = 0
#off_screen_left = -999999
#off_screen_right = 3*abs(off_screen_left)
init_location_zombie_left = -500 
init_location_zombie_right = 3*abs(init_location_zombie_left)
pack_reached_her = False
dropHealth = False
start_generation = True
player_moving_dir = 0 # -1 for moving left, 0 for not moving, 1 for moving right
game_state = 0 # 0 for Relaxing Phase, 1 for Build Up Phase, 2 for Climax Phase
game_over = False
out = ' '

# The Sound Function, which plays all sounds in game. Call this to play sounds or music.
def sound_master(soundFilePath, isMusic, onLoop):
    if isMusic:
        mixer.music.load(soundFilePath)
        mixer.music.set_volume(0.7)
        if onLoop:
            mixer.music.play(-1)
    else:
        mixer.Sound(soundFilePath).play()

# Define useful functions for the game here
def font_master(pathFont, font_size, textDrawn, antiAlias, color, centerItForMe, offset_x, offset_y):
    font = pygame.font.Font(pathFont, font_size)
    text = font.render(textDrawn, antiAlias, color)
    textRect = text.get_rect()
    if centerItForMe:
        textRect.topleft = (WID//2-textRect.width//2+offset_x, HEI//2-textRect.width//2+offset_y)
    else:
        textRect.topleft = (offset_x, offset_y)
    screen.blit(text, textRect)

# Objects, Classes, Players, Enemies, everything of that sort
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Data\\idle_girl_right_1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        screen.blit(self.image, self.rect)
        self.index1 = 0
        self.index2 = 0
        self.count = 0
        
    def update(self, x, y, pathToImg, isMoving, shooting):
        self.rect.center = (x, y)
        self.count = self.count + 1
        if self.count % 20 == 0:
            self.index1 += 1
            self.index2 += 1
        if shooting:
            self.image = pygame.image.load(pathToImg[4]).convert_alpha()
        else:
            if not isMoving:
                self.index2 = 0
                self.image = pygame.image.load(pathToImg[self.index1 % (len(pathToImg)-3)]).convert_alpha()
            else:
                self.index1 = 0
                self.image = pygame.image.load(pathToImg[(self.index2 % (len(pathToImg)-3))+2]).convert_alpha()
        screen.blit(self.image, self.rect)

class RZombie:
    def __init__(self, x, y, enemy_img, flipLeft, vel):
        self.x = x
        self.y = y
        self.vel = vel
        self.flipLeft = flipLeft
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(enemy_img).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        screen.blit(self.image, self.rect)

    def position(self):
        return self.x

    def update(self, shotLeft, shotRight, is_player_moving, min_damage, max_damage, spawn_offset, reachedLeftWall):
        #global kills
        #global off_screen_left
        #global off_screen_right
        global health
        sound_to_play = random.randint(0, 2)
        if not self.flipLeft and (self.x > WID//2 or (shotLeft and (self.x > 0))):
            if self.x > WID//2:
                health -= random.randint(min_damage, max_damage)
                if health < 0:
                    health = 0
                sound_master("Data\hurt.wav", False, False)
            #elif shotLeft:
            #    kills += 1
            self.x = spawn_offset
            if sound_to_play==0:
                sound_master("Data\eww1.wav", False, False)
            elif sound_to_play==1:
                sound_master("Data\eww2.wav", False, False)
            else:
                sound_master("Data\eww3.wav", False, False)
        elif self.flipLeft and (self.x < WID//2 or (shotRight and (self.x < WID-20))):
            if self.x < WID//2:
                health -= random.randint(min_damage, max_damage)
                if health < 0:
                    health = 0
                sound_master("Data\hurt.wav", False, False)
            #elif shotRight:
            #    kills += 1
            self.x = spawn_offset
            if sound_to_play==0:
                sound_master("Data\eww1.wav", False, False)
            elif sound_to_play==1:
                sound_master("Data\eww2.wav", False, False)
            else:
                sound_master("Data\eww3.wav", False, False)
        # is_player_moving = 0 for not moving, -1 for moving left, 1 for moving right
        if not self.flipLeft and is_player_moving==-1: # If we are moving to the right and player moving to the left
            self.x += self.vel+2
        elif not self.flipLeft and is_player_moving==1:
            self.x -= self.vel-2
        elif self.flipLeft and is_player_moving==-1 and not reachedLeftWall:
            self.x += self.vel-2
        elif self.flipLeft and is_player_moving==-1 and reachedLeftWall:
            self.x -= self.vel
        elif self.flipLeft and is_player_moving==1:
            self.x -= self.vel+2
        elif not self.flipLeft and is_player_moving==0:
            self.x += self.vel
        elif self.flipLeft and is_player_moving==0:
            self.x -= self.vel
            
        self.rect.center = (self.x, self.y)
        screen.blit(self.image, self.rect)

class HealthPlus:
    def __init__(self, x, y, min_boost, max_boost):
        self.x = x
        self.y = y
        self.min = min_boost
        self.max = max_boost
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Data\\health.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        screen.blit(self.image, self.rect)

    def update(self):
        #global packs
        global pack_reached_her
        global health
        self.y += 3
        if abs(abs(self.y) - abs(player_y)) < 5:
            #packs += 1
            self.y = -10
            pack_reached_her = True
            health += random.randint(self.min, self.max)
            if health > MAX_HEALTH:
                health = MAX_HEALTH
            sound_master("Data\\boost.wav", False, False)
        self.rect.center = (self.x, self.y)
        screen.blit(self.image, self.rect)

# Initialize instances of classes or code using previous functions (Optional)
P = Player(player_x, player_y)
#Eye1 = RZombie(off_screen_left, player_y, 'Data\\eye.png', False, vel)
Eye0 = RZombie(init_location_zombie_right, player_y, 'Data\\eyeLeft.png', True, vel)
Eye1 = RZombie(init_location_zombie_right, player_y, 'Data\\handLeft.png', True, vel+0.3)
Eye2 = RZombie(init_location_zombie_right, player_y, 'Data\\pinkLeft.png', True, vel+0.6)
Eye3 = RZombie(init_location_zombie_right, player_y, 'Data\\maleLeft.png', True, vel+1)
Eye4 = RZombie(init_location_zombie_right, player_y, 'Data\\eyeLeft.png', True, vel+1.3)
Eye5 = RZombie(init_location_zombie_right, player_y, 'Data\\handLeft.png', True, vel+1.6)
Eye6 = RZombie(init_location_zombie_right, player_y, 'Data\\pinkLeft.png', True, vel+2)
#Eye7 = RZombie(init_location_zombie_left, player_y, 'Data\\eye.png', False, vel) # guy coming from behind
#zombie_array = [Eye0, Eye1, Eye2, Eye3, Eye4, Eye5, Eye6, Eye7]
#Pink1 = RZombie(off_screen, player_y, 'Data\\pink.png', False, 3)
#Pink2 = RZombie(off_screen, player_y, 'Data\\pinkLeft.png', True, 4)
#Hand1 = RZombie(off_screen, player_y, 'Data\\hand.png', False, 5)
#Hand2 = RZombie(off_screen, player_y, 'Data\\handLeft.png', True, 6)
#Male1 = RZombie(off_screen, player_y, 'Data\\male.png', False, 7)
#Male2 = RZombie(off_screen, player_y, 'Data\\maleLeft.png', True, 8)
H = HealthPlus(player_x, -10, 10, 20)
sound_master('Data\\title.wav', True, True)
# ------------------------------------------------- USEFUL -----------------------------------------------------------
# ------------------------------------------------- GAME LOGIC & EVERYTHING ------------------------------------------
counter = 0
done = False
while not done:
    # Main event loop
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
 
    # Player Inputs
    keys = pygame.key.get_pressed()
    if keys[K_LEFT] and not is_menu and player_x > leftWall:
        player_x -= vel
        stageVelocity = vel
        lookingLeft = True
        player_moving_dir = -1
    elif keys[K_RIGHT] and not is_menu and player_x < rightWall:
        player_x += vel
        stageVelocity = -1*vel
        lookingLeft = False
        player_moving_dir = 1
    elif keys[K_SPACE] and not is_menu and canShootAgain and not reloading:
        sound_master('Data\\shoot.wav', False, False)
        is_shooting = True
        bullets -= 1
    elif keys[K_RETURN] and is_menu:
        is_menu = False
        pygame.mixer.music.stop()
        sound_master('Data\\ready.wav', False, False)
        sound_master('Data\\fight_them.wav', True, True)
    elif not keys[K_RIGHT] and not keys[K_LEFT] and not is_menu:
        player_moving_dir = 0
        
    # Screen-clearing code goes here. Don't put other drawing commands above this, or they will be erased with this command.
    screen.fill(BLACK)
 
    # Drawing code should go here
    all_sprites.draw(screen)
    if is_menu:
        font_master('Data\\ARCADECLASSIC.TTF', SIZES[3], 'School Girl Shooter', False, RED, True, 0, 130)
        font_master('Data\\ARCADECLASSIC.TTF', SIZES[2], 'By Noodle', False, RED, True, 0, 370)
        font_master('Data\\ARCADECLASSIC.TTF', SIZES[0], 'SPACE BAR', False, WHITE, False, 55, HEI-75)
        font_master('Data\\ARCADECLASSIC.TTF', SIZES[0], 'TO  SHOOT', False, WHITE, False, 55, HEI-55)
        font_master('Data\\ARCADECLASSIC.TTF', SIZES[0], 'ARROW KEYS', False, WHITE, False, WID-150, HEI-75)
        font_master('Data\\ARCADECLASSIC.TTF', SIZES[0], 'TO  MOVE', False, WHITE, False, WID-150, HEI-55)
        if counter % 5 == 0:
            font_master('Data\\ARCADECLASSIC.TTF', SIZES[1], 'PRESS  ENTER  TO  START', False, WHITE, True, 0, 380)
        bg_rect.topleft = (0, 125)
        screen.blit(bg_img, bg_rect)
        P.update(spritePosX, player_y, sprite_str_g, False, False)
    elif not is_menu and not game_over:
        moving = False
        if keys[K_LEFT]:
            sprite_str_g = ['Data\\idle_girl_left_1.png', 'Data\\idle_girl_left_2.png', 'Data\\walk_girl_left_1.png', 'Data\\walk_girl_left_2.png', 'Data\\shootl.png']
            moving = True
        elif keys[K_RIGHT]:
            sprite_str_g = ['Data\\idle_girl_right_1.png', 'Data\\idle_girl_right_2.png', 'Data\\walk_girl_right_1.png', 'Data\\walk_girl_right_2.png', 'Data\\shootr.png']
            moving = True
            
        spritePosX = startScrollingPosX
        if moving:
            stagePosX += stageVelocity
        if player_x <= leftWall:
            stagePosX = 0
        if player_x >= rightWall:
            stagePosX = (WID//2)-rightWall
        
        bg_rect.topleft = (stagePosX, 125)
        screen.blit(bg_img, bg_rect)
        if canShootAgain:
            shootingDelay = counter + 50
            canShootAgain = False
        if shootingDelay == counter:
            is_shooting = False
            canShootAgain = True
        
        P.update(spritePosX, player_y, sprite_str_g, moving, is_shooting)
        if game_state == 0:
            Eye0.update((is_shooting and lookingLeft), (is_shooting and not lookingLeft), player_moving_dir, random.randint(1, 20), random.randint(21, 40), 1500, player_x==leftWall)
            Eye1.update((is_shooting and lookingLeft), (is_shooting and not lookingLeft), player_moving_dir, random.randint(1, 20), random.randint(21, 40), 1500, player_x==leftWall)
        elif game_state == 1:
            Eye0.update((is_shooting and lookingLeft), (is_shooting and not lookingLeft), player_moving_dir, random.randint(1, 20), random.randint(21, 40), 1500, player_x==leftWall)
            Eye1.update((is_shooting and lookingLeft), (is_shooting and not lookingLeft), player_moving_dir, random.randint(1, 20), random.randint(21, 40), 1500, player_x==leftWall)
            Eye2.update((is_shooting and lookingLeft), (is_shooting and not lookingLeft), player_moving_dir, random.randint(1, 20), random.randint(21, 40), 1500, player_x==leftWall)
            Eye3.update((is_shooting and lookingLeft), (is_shooting and not lookingLeft), player_moving_dir, random.randint(1, 20), random.randint(21, 40), 1500, player_x==leftWall)
        elif game_state == 2:
            Eye0.update((is_shooting and lookingLeft), (is_shooting and not lookingLeft), player_moving_dir, random.randint(1, 20), random.randint(21, 40), 1500, player_x==leftWall)
            Eye1.update((is_shooting and lookingLeft), (is_shooting and not lookingLeft), player_moving_dir, random.randint(1, 20), random.randint(21, 40), 1500, player_x==leftWall)
            Eye2.update((is_shooting and lookingLeft), (is_shooting and not lookingLeft), player_moving_dir, random.randint(1, 20), random.randint(21, 40), 1500, player_x==leftWall)
            Eye3.update((is_shooting and lookingLeft), (is_shooting and not lookingLeft), player_moving_dir, random.randint(1, 20), random.randint(21, 40), 1500, player_x==leftWall)
            Eye4.update((is_shooting and lookingLeft), (is_shooting and not lookingLeft), player_moving_dir, random.randint(1, 20), random.randint(21, 40), 1500, player_x==leftWall)
            Eye5.update((is_shooting and lookingLeft), (is_shooting and not lookingLeft), player_moving_dir, random.randint(1, 20), random.randint(21, 40), 1500, player_x==leftWall)
            Eye6.update((is_shooting and lookingLeft), (is_shooting and not lookingLeft), player_moving_dir, random.randint(1, 20), random.randint(21, 40), 1500, player_x==leftWall)
        # For these creatures, there should only be 1 creature coming from 1 side at a time

        if bullets == 0 and not reloading:
            reloading = True
            reloadingDelay = (counter + 400)
        if reloading and counter % 80 == 0:
            sound_master('Data\\click.wav', False, False)
        if reloadingDelay == counter:
            bullets = MAX_BULLETS
            reloading = False

        if start_time:
            start_time = False
            ticks_since_init = pygame.time.get_ticks()
        ticks=pygame.time.get_ticks() - ticks_since_init
        millis=ticks%1000
        seconds=int(ticks/1000 % 60)
        minutes=int(ticks/60000 % 24)
        out='{minutes:02d}  {seconds:02d}  {millis}'.format(minutes=minutes, millis=millis, seconds=seconds)
        
        if seconds % 60 < 10:
            game_state = 0
        elif seconds % 60 < 50:
            game_state = 1
        elif seconds % 60 < 60:
            game_state = 2

        if game_state==0 and start_generation and random.randint(0, 1600) % 1600 == 0:
            dropHealth = True
            start_generation = False

        if dropHealth:
            H.update()
            if pack_reached_her:
                dropHealth = False
                start_generation = True
                pack_reached_her = False

        font_master('Data\\ARCADECLASSIC.TTF', SIZES[0], "FPS  "+str(int(clock.get_fps())), False, WHITE, False, 0, HEI-20)
        font_master('Data\\ARCADECLASSIC.TTF', SIZES[1], "TIME  "+ out, False, WHITE, False, WID//2-150, 0)
        font_master('Data\\ARCADECLASSIC.TTF', SIZES[1], "BULLETS  "+str(bullets), False, WHITE, False, 0, 0)
        font_master('Data\\ARCADECLASSIC.TTF', SIZES[1], "HEALTH  "+str(health), False, WHITE, False, WID-220, 0)
        
        if health == 0:
            game_over = True

    elif game_over:
        font_master('Data\\ARCADECLASSIC.TTF', SIZES[3], "TIME   " + out, False, RED, True, 0, 170)

    # This counter will help us manipulate the frames better
    counter += 1
    
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # Limit frames per second
    clock.tick(FPS)
# ------------------------------------------------- GAME LOGIC & EVERYTHING ------------------------------------------ 
# Close the window and quit.
pygame.quit()
