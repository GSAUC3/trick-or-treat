import pygame as pg
import time,os,sys
import random
from random import randrange
import backend

'''
Author: Rajarshi Banerjee
RULES : 
    1. get hit by ghost or pumpkin:   instant death
    2. double candy: +5
    3. rest candies: +2 
'''

pg.font.init()
pg.init()

pg.display.set_caption('TRICK OR TREAT')

bugs_dies=pg.mixer.Sound(os.path.join('sounds','mariodies.wav'))
game_over_sound=pg.mixer.Sound(os.path.join('sounds','jumpsonenemy.wav'))
pochat=pg.mixer.Sound(os.path.join('sounds','pochat.mp3'))

MUSIC=pg.mixer.music.load(os.path.join('sounds','halloween.mp3'))
pg.mixer.music.play(-1)

WIN=pg.display.set_mode((1280,720))

# Load images 
BACK=pg.image.load('images/back.png')

PUMPKIN=pg.transform.scale(pg.image.load(os.path.join('images','pumpkin.png')),(90,90))
GHOST=pg.transform.scale(pg.image.load(os.path.join('images','ghost.png')),(60,92))
WEB=pg.transform.scale(pg.image.load(os.path.join('images','web.png')),(90,90))

CANDY1=pg.image.load(os.path.join('images','candy1.png'))
CANDY2=pg.image.load(os.path.join('images','candy2.png'))
CANDY3=pg.image.load(os.path.join('images','candy3.png'))
CANDY4=pg.image.load(os.path.join('images','candy4.png'))
BUGS=pg.image.load('images/bugs.png')


def collide(obj1,obj2):
    offset_x=obj2.x-obj1.x
    offset_y=obj2.y-obj1.y
    return obj1.mask.overlap(obj2.mask,(offset_x,offset_y)) !=None

class Player:
    # our player is bugs bunny
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.lives=3
        self.mask=pg.mask.from_surface(BUGS)

    def draw(self):
        WIN.blit(BUGS,(self.x,self.y))
    
    def reset(self):
        self.x=1280>>1
        self.y=720>>1
        
    def get_width(self):
        return BUGS.get_width()
    
    def get_height(self):
        return BUGS.get_height()    
    
    def collision(self,obj):
        return collide(self,obj)
 
class General:
    def __init__(self,x,y,character):
        self.char=character
        self.x=x
        self.y=y
        self.velocity=3
        self.mask=pg.mask.from_surface(character)

    def move_down(self):
        self.y=(self.y+self.velocity)
            
        if self.y>=720 and self.y<=750:
            self.x=randrange(20,1180)
            self.y=random.choice([-200,-150,-100,-300,-500,-400,-1000,-800,-900,-700,-600])
        WIN.blit(self.char,(self.x,self.y))
    
    def move_right(self):
        self.x=(self.x+self.velocity)
        if self.x>=1380:
            self.x=random.choice([-200,-150,-100,-300,-500,-400,-1000,-800,-900,-700,-600])
            self.y=randrange(40,600)

        WIN.blit(self.char,(self.x,self.y))


    def move_up(self):
        self.y=(self.y-self.velocity)
        if self.y<=0:
            self.x=randrange(20,1180)
            self.y=random.choice([720,760,800,840,800,870,1280,1300,1400,1500])
            
        WIN.blit(self.char,(self.x,self.y))


    def move_left(self):
        self.x=(self.x-self.velocity)
        if self.x<=0:
            self.x=random.choice([1280,1300,1400,1500,1600,1700,1800,1900,2000])
            self.y=randrange(40,600)

        WIN.blit(self.char,(self.x,self.y))

    def get_width(self):
        return self.char.get_width()
    
    def get_height(self):
        return self.char.get_height()

    def reset(self,string):
        if string == 'left':
            self.x=random.choice([1280,1300,1400,1500,1600,1700,1800,1900,2000])
        if string == 'right':
            self.x=random.choice([-200,-150,-100,-300,-500,-400,-1000,-800,-900,-700,-600])
        if string == 'up':
            self.y=random.choice([720,760,800,840,800,870,1280,1300,1400,1500])
        if string == 'down':
            self.y=random.choice([-200,-150,-100,-300,-500,-400,-1000,-800,-900,-700,-600])

def main():
    FPS=60
    on=True
    lives=3
    candies_collected=0
    font=pg.font.SysFont('comicsans',30)
    SCOREfont=pg.font.SysFont('comicsans',100)
    x,y=3,3
    gameoverfont=pg.font.SysFont('chalkduster.ttf',200)
    clock= pg.time.Clock()

    def draw():
        WIN.blit(BACK,(0,0))


        lives_on_screen=font.render(f'Lives: {lives}',1,(0,255,68))
        score_on_screen=font.render(f'Candies Score: {candies_collected}',1,(255, 255, 255))
        WIN.blit(lives_on_screen,(20,5))
        WIN.blit(score_on_screen,(1000,5))

        

    bugs = Player(630,360)
    # this will go to the left
    p_left=General(1200,30,PUMPKIN)
    g_left=General(1280,330,GHOST)
    webl=General(1200,360,WEB)
    c1l=General(1480,600,CANDY1)
    c2l=General(1380,230,CANDY2)
    c3l=General(1280,130,CANDY3)
    c4l=General(1580,530,CANDY4)

    g_right=General(0,300,GHOST)
    webr=General(-120,460,WEB)
    p_right=General(-10,600,PUMPKIN)
    c1r=General(-20,600,CANDY1)
    c2r=General(-30,230,CANDY2)
    c3r=General(-100,130,CANDY3)
    c4r=General(0,530,CANDY4)

    g_down=General(300,50,GHOST)
    p_down=General(200,30,PUMPKIN)
    webd=General(120,46,WEB)
    c1d=General(800,-50,CANDY1)
    c2d=General(600,-150,CANDY2)
    c3d=General(500,0,CANDY3)
    c4d=General(1000,-25,CANDY4)

    
    webu=General(1120,460,WEB)
    g_up=General(300,750,GHOST)
    p_up=General(200,950,PUMPKIN)
    c1u=General(800,1250,CANDY1)
    c2u=General(600,1050,CANDY2)
    c3u=General(500,1250,CANDY3)
    c4u=General(1000,850,CANDY4)

    

    rightwalla=[webr,g_right,p_right,c1r,c2r,c3r,c4r]
    leftwalla=[webl,p_left,g_left,c1l,c2l,c3l,c4l]
    downwalla=[webd,p_down,g_down,c1d,c2d,c3d,c4d]
    upwalla=[webu,p_up,g_up,c1u,c2u,c3u,c4u]
    ELEMENTS = set(rightwalla + leftwalla + downwalla + upwalla)
    ENEMY=set([g_up,g_down,g_left,g_right,p_down,p_up,p_left,p_right,webu,webl,webr,webd])
    FOOD=ELEMENTS-ENEMY


    while on:
        clock.tick(FPS)
        draw()

        for i in leftwalla:
            i.move_left()

        for i in rightwalla:
            i.move_right()

        for i in downwalla:
            i.move_down()

        for i in upwalla:
            i.move_up()

        bugs.draw()
        
      

        if lives<=0:
            if backend.get_score()>=candies_collected:
                bugs_dies.play()
                lost_label=gameoverfont.render('GAME OVER',1,(255,255,255))
                WIN.blit(lost_label,(250,300))
                on_screen=SCOREfont.render(f'Your score: {candies_collected} Highest Score: {backend.get_score()}',
                1,(191, 255, 0) )
                WIN.blit(on_screen,(100,100))
            else:
                bugs_dies.play()
                lost_label=gameoverfont.render('GAME OVER',1,(255,255,255))
                WIN.blit(lost_label,(250,300))
                highscore=SCOREfont.render(f'NEW HIGH SCORE!!! {candies_collected}',1,(191, 255, 0))
                WIN.blit(highscore,(250,100))
                backend.updatescore(candies_collected)
            
            
            pg.display.update()
            time.sleep(5)
            on=False

        for e in pg.event.get():
            if e.type==pg.QUIT:
                on=False

        for i in FOOD:
            if collide(bugs,i):
                candies_collected+=1
                if i in [c1r,c2r,c3r,c4r]:
                    game_over_sound.play()
                    i.reset('right')
                    
                if i in [c1l,c2l,c3l,c4l]:
                    game_over_sound.play()
                    i.reset('left')
                    
                if i in [c1u,c2u,c3u,c4u]:
                    game_over_sound.play()
                    i.reset('up')
                    
                if i in [c1d,c2d,c3d,c4d]:
                    game_over_sound.play()
                    i.reset('down')
                    
        for i in ENEMY:
            if collide(bugs,i):
                lives-=1
                if i in [p_up,g_up,webu]:
                    pochat.play()
                    i.reset('up')
                    bugs.reset()
                if i in [p_down,g_down,webd]:
                    pochat.play()
                    i.reset('down')
                    bugs.reset()
                if i in [p_left,g_left,webl]:
                    pochat.play()
                    i.reset('left')
                    bugs.reset()
                if i in [p_right,g_right,webr]:
                    pochat.play()
                    i.reset('right')
                    bugs.reset()

        keys=pg.key.get_pressed()
        if keys[pg.K_UP] and bugs.y>40:
            bugs.y-=y
        if keys[pg.K_DOWN] and bugs.y+y < 600:
            bugs.y+=y
        if keys[pg.K_RIGHT] and bugs.x<1175:
            bugs.x+=x
        if keys[pg.K_LEFT] and bugs.x>0:
            bugs.x-=x
        
        pg.display.update()

    

if __name__ == '__main__':
    main()