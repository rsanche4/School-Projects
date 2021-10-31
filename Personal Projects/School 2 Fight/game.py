# ----------------------------------------------------------------
# School 2 Fight 
# By Rafael Sanchez
# Description: A simple school zombie arcade.
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
GAME_TITLE = "School 2 Fight"

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
canShootAgain = True
shootingDelay = 0
reloading = False
MAX_BULLETS = 10
bullets = MAX_BULLETS
reloadingDelay = 0
MAX_HEALTH = 100
health = MAX_HEALTH
start_time = True
ticks_since_init = 0

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
        self.image = pygame.image.load('Data\\idle_girl_right_1.png')
        self.image.set_colorkey(BLACK)
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
        

# Initialize instances of classes or code using previous functions (Optional)
P = Player(player_x, player_y)
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
    elif keys[K_RIGHT] and not is_menu and player_x < rightWall:
        player_x += vel
        stageVelocity = -1*vel
    elif keys[K_SPACE] and not is_menu and canShootAgain and not reloading:
        sound_master('Data\\shoot.wav', False, False)
        is_shooting = True
        bullets -= 1
    elif keys[K_RETURN] and is_menu:
        is_menu = False
        pygame.mixer.music.stop()
        sound_master('Data\\ready.wav', False, False)
        
    # Screen-clearing code goes here. Don't put other drawing commands above this, or they will be erased with this command.
    screen.fill(BLACK)
 
    # Drawing code should go here
    all_sprites.draw(screen)
    if is_menu:
        font_master('Data\\ARCADECLASSIC.TTF', SIZES[4], 'School 2 Fight', False, RED, True, 0, 80)
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
    else:
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
        font_master('Data\\ARCADECLASSIC.TTF', SIZES[1], "TIME  "+ out, False, WHITE, False, WID//2-150, 0)
        
        #font_master('Data\\ARCADECLASSIC.TTF', SIZES[1], "FPS  "+str(int(clock.get_fps())), False, WHITE, False, 0, HEI-40)
        font_master('Data\\ARCADECLASSIC.TTF', SIZES[1], "BULLETS  "+str(bullets), False, WHITE, False, 0, 0)
        font_master('Data\\ARCADECLASSIC.TTF', SIZES[1], "HEALTH  "+str(health), False, WHITE, False, WID-220, 0)
    # This counter will help us manipulate the frames better
    counter = counter + 1
    
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # Limit frames per second
    clock.tick(FPS)
# ------------------------------------------------- GAME LOGIC & EVERYTHING ------------------------------------------ 
# Close the window and quit.
pygame.quit()
