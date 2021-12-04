# ----------------------------------------------------------------
# POLYBIUS
# By Rafael Sanchez
# Description: A clone of the classic myth.
# ----------------------------------------------------------------
# Code is devided in sections
# ------------------------------------------------- ESSENTIALS ------------------------------------------------------- 
# Imports go here
import pygame
from pygame import mixer
import random
from pygame.constants import K_0

# Here import the buttons that you want from pygame
from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_0,
    K_SPACE,
    K_RETURN,
    K_ESCAPE,
    QUIT,
)

# Insert Game Title
GAME_TITLE = "POLYBIUS"

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
PLAYER_W = 60
PLAYER_H = 40
player_x = WID//2
player_y = HEI-PLAYER_H
circ_r = random.randint(0, 1000)
circ_t = random.randint(0, 1000)
player_v = 6
is_menu = False
shotUp = False
shootDelay = False
is_warning = True
obey_mode = False

# The Sound Function, which plays all sounds in game. Call this to play sounds or music. Returns 0 on success for playing music, and a Sound if playing sounds.
def sound_master(soundFilePath, isMusic, onLoop):
    sound = 0
    if not isMusic:
        sound = mixer.Sound(soundFilePath)
    if isMusic:
        mixer.music.load(soundFilePath)
        mixer.music.set_volume(0.7)
        if onLoop:
            mixer.music.play(-1)
        else:
            mixer.music.play()
    else:
        if onLoop:
            sound.play(-1)
        else:
            sound.play()
    return sound

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

def set_game_border(color, width, height, thickness):
    for x in range(0, width+thickness, thickness):
        pygame.draw.rect(screen, color, [x, 0, thickness, thickness])
        pygame.draw.rect(screen, color, [x, height-thickness, thickness, thickness])
    for x in range(0, height+thickness, thickness):
        pygame.draw.rect(screen, color, [0, x, thickness, thickness])
        pygame.draw.rect(screen, color, [width-thickness, x, thickness, thickness])

# Objects, Classes, Players, Enemies, everything of that sort
class Player:
    def __init__(self, x, y, w, h):
        self.width = w
        self.height = h
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Data\\player1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        screen.blit(self.image, self.rect)
        
    def update(self, x, y):
        self.rect.center = (x, y)
        screen.blit(self.image, self.rect)

class Bullet:
    def __init__(self, x, y, w, h, vel):
        self.vel = vel
        self.width = w
        self.height = h
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Data\\bullet.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        screen.blit(self.image, self.rect)
    
    def update(self, player_pos_x, player_pos_y, shot, delay, collided):
        global shootDelay
        if collided:
            shootDelay = False
            self.x = -100
            self.y = -10
        elif shot and not delay:
            throwaway = sound_master('Data\\shoot.wav', False, False)
            self.x = player_pos_x
            self.y = player_pos_y
        else:
            self.y -= self.vel
            if self.y < 0:
                shootDelay = False
        self.rect.center = (self.x, self.y)
        screen.blit(self.image, self.rect)

class Enemy:
    def __init__(self, x, y, vel):
        self.vel = vel
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Data\\alien.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        screen.blit(self.image, self.rect)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.place_to_go_x = random.randint(PLAYER_W, WID-PLAYER_W)
        
    def update(self):
        if not self.x >= self.place_to_go_x:
            self.x += self.vel
        else:
            self.y += self.vel
        if self.y > HEI+10:
            self.x = -50
            self.y = random.randint(0, HEI//2)
            self.place_to_go_x = random.randint(PLAYER_W, WID-PLAYER_W)
        self.rect.center = (self.x, self.y)
        screen.blit(self.image, self.rect)

    def collision(self, bullet):
        if abs(bullet.x - self.x) < (self.width-10) and abs(bullet.y - self.y) < (self.height-10):
            self.x = -50
            self.y = random.randint(0, HEI//2)
            self.place_to_go_x = random.randint(PLAYER_W, WID-PLAYER_W)
            throwaway = sound_master('Data\\dead.wav', False, False)
            return True
        return False

class EnemyTwo:
    def __init__(self, x, y, vel):
        self.vel = vel
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Data\\alien1.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        screen.blit(self.image, self.rect)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
    def update(self):
        self.y += self.vel
        if self.y > HEI+10:
            self.y = -10
            self.x = random.randint(PLAYER_W, WID-PLAYER_W)
        self.rect.center = (self.x, self.y)
        screen.blit(self.image, self.rect)

    def collision(self, bullet):
        if abs(bullet.x - self.x) < (self.width-10) and abs(bullet.y - self.y) < (self.height-10):
            self.y = -10
            self.x = random.randint(PLAYER_W, WID-PLAYER_W)
            throwaway = sound_master('Data\\dead.wav', False, False)
            return True
        return False

class EnemyThree:
    def __init__(self, x, y, vel):
        self.vel = vel
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Data\\bonus.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        screen.blit(self.image, self.rect)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        
    def update(self):
        if self.x < WID+PLAYER_W:
            self.x += self.vel
        else:
            self.y += self.vel*10
            self.x = random.randint(-8000, -10)
        if self.y > HEI-(HEI//2):
            self.y = 50
        self.rect.center = (self.x, self.y)
        screen.blit(self.image, self.rect)

    def collision(self, bullet):
        if abs(bullet.x - self.x) < self.width and abs(bullet.y - self.y) < self.height:
            self.y += self.vel*10
            self.x = random.randint(-8000, -10)
            throwaway = sound_master('Data\\red_kill.wav', False, False)
            return True
        return False

class Circle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self, r, t, rgb):
        pygame.draw.circle(screen, rgb, (self.x, self.y), r, t)

# Initialize other varibles, classes (Optional)
p = Player(player_x, player_y, PLAYER_W, PLAYER_H)
e1 = Enemy(-50, 75, 10)
e2 = EnemyTwo(random.randint(PLAYER_W, WID-PLAYER_W), -10, 10)
e3 = EnemyThree(random.randint(-8000, -10), 50, 10)
e11 = Enemy(-50, 75, 7)
e22 = EnemyTwo(random.randint(PLAYER_W, WID-PLAYER_W), -10, 7)
e33 = EnemyThree(random.randint(-8000, -10), 50, 7)
e111 = Enemy(-50, 75, 5)
e222 = EnemyTwo(random.randint(PLAYER_W, WID-PLAYER_W), -10, 5)
e333 = EnemyThree(random.randint(-8000, -10), 50, 5)
e4 = Enemy(-50, 75, 8)
e44 = EnemyTwo(random.randint(PLAYER_W, WID-PLAYER_W), -10, 8)
e5 = Enemy(-50, 75, 6)
e55 = EnemyTwo(random.randint(PLAYER_W, WID-PLAYER_W), -10, 6)
e6 = Enemy(-50, 75, 9)
e66 = EnemyTwo(random.randint(PLAYER_W, WID-PLAYER_W), -10, 9)
bull = Bullet(-100, player_y, 10, 10, 10)
middleCirc = Circle(WID//2, HEI//2)
# ------------------------------------------------- USEFUL -----------------------------------------------------------
# ------------------------------------------------- GAME LOGIC & EVERYTHING ------------------------------------------
counter = 0
done = False
menu_sound = 0
while not done:
    # Main event loop
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True
 
    # Player Inputs
    keys = pygame.key.get_pressed()
    if keys[K_LEFT] and player_x > PLAYER_W:
        player_x -= player_v
    if keys[K_RIGHT] and player_x < (WID-PLAYER_W):
        player_x += player_v
    if keys[K_SPACE]:
        shotUp = True
    if keys[K_RETURN] and is_menu:
        is_menu = False
        mixer.Sound.stop(menu_sound)
        throwaway = sound_master('Data\\game_ost.wav', True, True)
    if keys[K_ESCAPE]:
        done = True
    if keys[K_0] and is_menu:
        obey_mode = True
        is_menu = False
        mixer.Sound.stop(menu_sound)
        throwaway = sound_master('Data\\game_ost.wav', True, True)
        
    # Screen-clearing code goes here. Don't put other drawing commands above this, or they will be erased with this command.
    screen.fill(BLACK)
 
    # Drawing code should go here
    if is_warning:
        max_time = 999
        if counter < max_time:
            font_master('Data\\ARCADECLASSIC.TTF', SIZES[2], 'Polybius has been ', False, WHITE, False, 20, 0)
            font_master('Data\\ARCADECLASSIC.TTF', SIZES[2], 'linked to impaired memory', False, WHITE, False, 20, 50)
            font_master('Data\\ARCADECLASSIC.TTF', SIZES[2], 'and psychological changes', False, WHITE, False, 20, 100)
            font_master('Data\\ARCADECLASSIC.TTF', SIZES[2], 'Gameplay may cause', False, WHITE, False, 20, 200)
            font_master('Data\\ARCADECLASSIC.TTF', SIZES[2], 'seizures and headaches in', False, WHITE, False, 20, 250)
            font_master('Data\\ARCADECLASSIC.TTF', SIZES[2], 'susceptible individuals', False, WHITE, False, 20, 300)
            font_master('Data\\ARCADECLASSIC.TTF', SIZES[2], 'Play at your own risk', False, RED, False, 20, 400)
            font_master('Data\\ARCADECLASSIC.TTF', SIZES[2], 'Game     starts      in     ' + str((max_time-counter)//100 + 1), False, WHITE, False, 20, 500)
        else:
            menu_sound = sound_master('Data\\menu.wav', False, True)
            is_warning = False
            is_menu = True
    elif is_menu:
        font_master('Data\\ARCADECLASSIC.TTF', SIZES[4]+20, 'P O  LY B I U S', False, (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)), True, 0, 160)
        font_master('Data\\ARCADECLASSIC.TTF', SIZES[1], '1981   Sinnesloschen    Inc', False, BLUE, True, 0, 350)
        font_master('Data\\ARCADECLASSIC.TTF', SIZES[1], 'HIGHSCORE   0', False, RED, True, 0, 300)
        set_game_border((random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)), WID, HEI, random.randint(5, 15))
    elif obey_mode:
        if counter % 10 == 0:
            circ_r = random.randint(0, 1000)
            circ_t = random.randint(0, 1000)
        middleCirc.update(circ_r, circ_t, (random.randint(0, 100),random.randint(0, 100),random.randint(0, 100)))
        e1.update()
        e2.update()
        e3.update()
        e11.update()
        e22.update()
        e33.update()
        e111.update()
        e222.update()
        e333.update()
        e4.update()
        e44.update()
        e5.update()
        e55.update()
        e6.update()
        e66.update()
        set_game_border((random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)), WID, HEI, random.randint(5, 15))
        if counter % 100 == 0:
            rand = random.randint(1, 6)
            match rand:
                case 1:
                    font_master('Data\\ARCADECLASSIC.TTF', SIZES[4], 'OBEY', False, WHITE, True, 0, 0)
                case 2:
                    font_master('Data\\ARCADECLASSIC.TTF', SIZES[4], 'CONFORM', False, WHITE, True, 0, 0)
                case 3:
                    font_master('Data\\ARCADECLASSIC.TTF', SIZES[4], 'CONSUME', False, WHITE, True, 0, 0)
                case 4:
                    font_master('Data\\ARCADECLASSIC.TTF', SIZES[4], 'BUY', False, WHITE, True, 0, 0)
                case 5:
                    font_master('Data\\ARCADECLASSIC.TTF', SIZES[3], 'LOSE YOURSELF', False, WHITE, True, 0, 200)
                case 6:
                    font_master('Data\\ARCADECLASSIC.TTF', SIZES[4], 'SUBMIT', False, WHITE, True, 0, 0)
    
    else:
        if counter % 10 == 0:
            circ_r = random.randint(0, 1000)
            circ_t = random.randint(0, 1000)
        middleCirc.update(circ_r, circ_t, (random.randint(0, 100),random.randint(0, 100),random.randint(0, 100)))
        p.update(player_x, player_y)
        e1.update()
        e2.update()
        e3.update()
        e11.update()
        e22.update()
        e33.update()
        e111.update()
        e222.update()
        e333.update()
        e4.update()
        e44.update()
        e5.update()
        e55.update()
        e6.update()
        e66.update()
        collidedAny = e1.collision(bull) or e11.collision(bull) or e111.collision(bull) or e4.collision(bull) or e5.collision(bull) or e6.collision(bull)
        collidedAny = collidedAny or e2.collision(bull) or e22.collision(bull) or e222.collision(bull) or e44.collision(bull) or e55.collision(bull) or e66.collision(bull)
        collidedAny = collidedAny or e3.collision(bull) or e33.collision(bull) or e333.collision(bull)
        bull.update(player_x, player_y, shotUp, shootDelay, collidedAny)
        if shotUp:
            shotUp = False
            shootDelay = True
        set_game_border((random.randint(0, 255),random.randint(0, 255),random.randint(0, 255)), WID, HEI, random.randint(5, 15))
        if counter % 100 == 0:
            rand = random.randint(1, 6)
            match rand:
                case 1:
                    font_master('Data\\ARCADECLASSIC.TTF', SIZES[4], 'OBEY', False, WHITE, True, 0, 0)
                case 2:
                    font_master('Data\\ARCADECLASSIC.TTF', SIZES[4], 'CONFORM', False, WHITE, True, 0, 0)
                case 3:
                    font_master('Data\\ARCADECLASSIC.TTF', SIZES[4], 'CONSUME', False, WHITE, True, 0, 0)
                case 4:
                    font_master('Data\\ARCADECLASSIC.TTF', SIZES[4], 'BUY', False, WHITE, True, 0, 0)
                case 5:
                    font_master('Data\\ARCADECLASSIC.TTF', SIZES[3], 'LOSE YOURSELF', False, WHITE, True, 0, 200)
                case 6:
                    font_master('Data\\ARCADECLASSIC.TTF', SIZES[4], 'SUBMIT', False, WHITE, True, 0, 0)
    
    # This counter will help us manipulate the frames better
    counter += 1
    
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # Limit to 60 frames per second
    clock.tick(60)
# ------------------------------------------------- GAME LOGIC & EVERYTHING ------------------------------------------ 
# Close the window and quit.
pygame.quit()