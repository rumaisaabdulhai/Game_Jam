##########
# IMPORT #
##########
import pygame as pg
import random
import os
from pygame import mixer

#############
# CONSTANTS #
#############
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
DIM = (SCREEN_WIDTH,SCREEN_HEIGHT)
WHITE =      (255, 255, 255, 255.0)
BLACK =      ( 23,  23,  23, 255.0)

#########
# FONTS #
#########
pg.font.init()
myfont = pg.font.SysFont('Comic Sans MS', 120)
myfont2 = pg.font.SysFont('VT323-Regular.ttf', 120)
score_font = pg.font.SysFont('VT323-Regular.ttf', 60)
tiny_score_font = pg.font.SysFont('VT323-Regular.ttf', 40)

#############
# VARIABLES #
#############
Speed = 30
max_speed = Speed
Score = 0
banana = False
end_mode_2 = pg.USEREVENT+1

def scale_image(image, scale):
    scaled_width = int(image.get_width() * scale)
    scaled_height = int(image.get_height() * scale)
    return pg.transform.scale(image,(scaled_width, scaled_height))

###############
# GIF SPRITES #
###############
NYANGIF = [scale_image(pg.image.load("images/nyan_gif/" + str(i+1) + ".png"),1/3) for i in range(len(os.listdir("images/nyan_gif"))-1)]
GHOSTGIF = [scale_image(pg.image.load("images/ghost_gif/" + str(i+1) + ".png"),1/3) for i in range(len(os.listdir("images/ghost_gif"))-1)]
DONYANGIF = [scale_image(pg.image.load("images/donyan_gif/" + str(i+1) + ".png"),1/3) for i in range(len(os.listdir("images/donyan_gif"))-1)]

NYANGIFS = [NYANGIF, GHOSTGIF, DONYANGIF]
nyan_mode = 0
nyangifcounter = 0

########
# NYAN #
########
class Nyan(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 100
        self.y = 200
        self.image = NYANGIFS[0][0]
        self.rect = self.image.get_rect(x=self.x, y=self.y)
    def update(self):
        global nyangifcounter, nyan_mode
        nyangifcounter = nyangifcounter % len(NYANGIFS[nyan_mode])
        if not banana:
            self.image = NYANGIFS[nyan_mode][nyangifcounter]
        else:
            self.image = pg.transform.flip(NYANGIFS[nyan_mode][nyangifcounter],False,True)
        nyangifcounter += 1
        nyangifcounter = nyangifcounter % len(NYANGIFS[nyan_mode])
        keys = pg.key.get_pressed()
        if not banana:
            if keys[pg.K_UP]:
                self.rect.y -= 10
            if keys[pg.K_DOWN]:
                self.rect.y += 10
        else:
            if keys[pg.K_UP]:
                self.rect.y += 10
            if keys[pg.K_DOWN]:
                self.rect.y -= 10
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if  self.rect.left < 0:
                self.rect.left = 0
        if  self.rect.bottom > SCREEN_HEIGHT:
                self.rect.bottom = SCREEN_HEIGHT
        if  self.rect.top < 0:
                self.rect.top = 0

# Cake Sprite - speeds up nyan cake
class Cake(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = scale_image(pg.image.load('images/cake.png'),1/5)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, int(random.random() * (SCREEN_HEIGHT - self.image.get_height())))
    def update(self):
        global Speed
        self.rect.x += 1
        if self.rect.x > SCREEN_WIDTH - self.image.get_width():
            self.kill()
        if collides(self):
            Speed += 10
            self.kill()

# Cake Sprite - speeds up nyan cake
class Donut(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = scale_image(pg.image.load('images/donut.png'),1/20)
        self.rect = self.image.get_rect()
        self.rect.topleft = (0, int(random.random() * (SCREEN_HEIGHT - self.image.get_height())))
    def update(self):
        global nyan_mode
        self.rect.x += 1
        if self.rect.x > SCREEN_WIDTH - self.image.get_width():
            self.kill()
        if collides(self):
            nyan_mode = 2
            banana = False
            pg.time.set_timer(end_mode_2,6800)
            self.kill()

# Peel Sprite
class Peel(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = scale_image(pg.image.load('images/banana_peel.png'),1/7)
        self.rect = self.image.get_rect()
        self.rect.topright = (SCREEN_WIDTH,int(random.random()*(SCREEN_HEIGHT-self.image.get_height())))
        self.speed = int(random.random()*10+5)
    def update(self):
        global Speed, banana
        self.rect.x -= self.speed
        if self.rect.x < 0:
            self.kill()
        if collides(self):
            banana = not banana
            self.kill()

# Bomb Sprite
class Bomb(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = scale_image(pg.image.load('images/bomb.png'),1/6)
        self.rect = self.image.get_rect()
        self.rect.topright = (SCREEN_WIDTH,int(random.random()*(SCREEN_HEIGHT-self.image.get_height())))
        self.speed = int(random.random()*10+5)
    def update(self):
        global Speed
        self.rect.x -= self.speed
        if self.rect.x < 0:
            self.kill()
        if collides(self):
            Speed -= self.speed
            self.kill()

# Asteroid Sprite
class Asteroid(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = scale_image(pg.image.load('images/asteroid.png'),1/4)
        self.rect = self.image.get_rect()
        self.rect.topright = (SCREEN_WIDTH,int(random.random()*(SCREEN_HEIGHT-self.image.get_height())))
        self.speed = int(random.random()*9+1)
    def update(self):
        global Speed
        self.rect.x -= self.speed
        if self.rect.x < 0:
            self.kill()
        if collides(self):
            Speed -= self.speed
            self.kill()

# # Pause button
# class Pause(pg.sprite.Sprite):
#     currently_clicked = False
#     def __init__(self):
#         pg.sprite.Sprite.__init__(self)
#         self.image = scale_image(pg.image.load('images/pause.png'),1/6)
#         self.rect = self.image.get_rect()
#         self.rect.topright = (SCREEN_WIDTH,self.image.get_height())
#     def update(self):
#         if clicked(self):
#             currently_clicked = True

# # Play button
# class Play(pg.sprite.Sprite):
#     currently_clicked = True
#     def __init__(self):
#         pg.sprite.Sprite.__init__(self)
#         self.image = scale_image(pg.image.load('images/play.png'),1/6)
#         self.rect = self.image.get_rect()
#         self.rect.topright = (SCREEN_WIDTH,self.image.get_height())
#     def update(self):
#         if clicked(self):
#             currently_clicked = True
      
def redrawWindow(Screen, bg, bgX, bgX2):
    Screen.blit(bg, (bgX, 0))
    Screen.blit(bg, (bgX2, 0))

nyan = Nyan()

# check if object collides with nyancat
def collides(a):
    global nyan_mode
    if nyan_mode == 2:
        # pg.mixer.pause()
        pg.mixer.music.load('audio/hype_mode.ogg')
        pg.mixer.music.play(0)
        pg.mixer.music.queue('audio/nyan_audio.ogg')
        return False
    return nyan.rect.colliderect(a.rect)

def game_loop(Screen):
    global Score, max_speed, nyan_mode, nyangifcounter, Speed
    Speed = 30
    Score = 0
    max_speed = Speed
    nyan_mode = 0
    nyangifcounter = 0

    bg = pg.image.load('images/background.png').convert()
    bgX = 0
    bgX2 = bg.get_width()
    
    all_sprites = pg.sprite.Group()
    all_sprites.add(nyan)

    playing = True

    while playing:

        Score += Speed/100
        
        if (Speed > max_speed):
            max_speed = Speed

        number = random.random()
        redrawWindow(Screen, bg, bgX, bgX2)

        bgX -= 2.8 * Speed
        bgX2 -= 2.8 * Speed

        # If bg is at the -width then reset position
        if bgX < bg.get_width() * -1:
            bgX = bg.get_width()
        
        if bgX2 < bg.get_width() * -1:
            bgX2 = bg.get_width()

        time = pg.time.get_ticks()/1000

        if number < 1/500 and time > 0.5:
            peel = Peel()
            all_sprites.add(peel)	
        if number < 1/2 and time > 1000:
            donut = Donut()
            all_sprites.add(donut)	
        if number < 1/250 and time > 0.5 and not nyan_mode == 2:
            cake = Cake()
            all_sprites.add(cake)	
        if number < 1/25 and time > 2:
            asteroid = Asteroid()
            all_sprites.add(asteroid)

        for event in pg.event.get():
            if event.type == end_mode_2:
                nyan_mode = 0

            if event.type == pg.QUIT:
                playing = False
                quit = True
           
        all_sprites.update()
        all_sprites.draw(Screen)

        # display the score and the speed
        score_text = score_font.render('Score: ' + str(int(Score)), False, WHITE)
        Screen.blit(score_text,(0,0))
        
        speed_text = score_font.render('Speed: ' + str(Speed), False, WHITE)
        Screen.blit(speed_text,(0,int(speed_text.get_height())))

        pg.display.update()

        # game over screen, max speed + score
        if Speed <= 0:
            playing = False

def end_card(Screen):
    global myfont, nyan_mode, nyangifcounter, max_speed, Score, banana
    ending = True
    bg = pg.image.load('images/background.png').convert()
    nyan_mode = 1
    nyangifcounter = 1
    banana = False
    
    all_sprites = pg.sprite.Group()
    all_sprites.add(nyan)

    quit = False

    while ending:
        Screen.blit(bg, (0, 0))
        all_sprites.update()
        
        rectangle_width = 650
        rectangle_height = 400
        pg.draw.rect(Screen,BLACK,(int((SCREEN_WIDTH-rectangle_width)/2),int((SCREEN_HEIGHT-rectangle_height)/2),rectangle_width,rectangle_height))
        
        game_over_text = myfont2.render('Game Over', False, WHITE)
        Screen.blit(game_over_text,(int(SCREEN_WIDTH/2-game_over_text.get_width()/2),int(SCREEN_HEIGHT/2 - 3*game_over_text.get_height()/2)))

        your_score_text = tiny_score_font.render('Final Score: ' + str(int(Score)) + '           Max Speed: ' + str(max_speed), False, WHITE)
        Screen.blit(your_score_text,(int(SCREEN_WIDTH/2-your_score_text.get_width()/2),int(SCREEN_HEIGHT/2 + your_score_text.get_height())))

        try_again_text = score_font.render('Play Again? Type Y/N', False, WHITE)
        Screen.blit(try_again_text,(int((SCREEN_WIDTH-try_again_text.get_width())/2),int((SCREEN_HEIGHT + 3*game_over_text.get_height())/2)))

        all_sprites.draw(Screen)

        pg.display.update()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                ending = False
                quit = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_y:
                    quit = False
                    ending = False
                if event.key == pg.K_n:
                    quit = True
                    ending = False
        
    return quit
    
def main():
    Screen = pg.display.set_mode(DIM)
    pg.display.set_caption("Nyan Universe")
    clock = pg.time.Clock()
    playing = True
    quit = False

    pg.init()
    pg.mixer.init()
    pg.mixer.music.load('audio/nyan_audio.ogg')
    pg.mixer.music.play(-1)

    while not quit:
        game_loop(Screen)
        quit = end_card(Screen)
    pg.quit()

if __name__ == "__main__":
    main()