#Made by Justin Ritterson and Andrew Summers
import pygame, sys, random, time
from pygame.locals import *

pygame.init()

MAXSIZE = 1500
direction = None
segments=[[500,400]]    #Starting position
fruitgrid=[]
fruitflag=False #Spawns fruits - not on snake
fruitscore=0    #Sets up available fruit score
fruitcolor=0
clockspeed=10   #Sets FPS
scoretextfont=pygame.font.Font(None,36)
losetextfont=pygame.font.Font(None,72)
score=0     #Sets initial score
pygame.mixer.music.load('house.ogg')
pygame.event.set_blocked(VIDEORESIZE)   #Non-resizable window

for x in xrange(20,1000,20):    #X boundaries
    for y in xrange(40,800,20): #Y boundaries
        fruitgrid.append([x,y])    

random.seed()

fpsClock = pygame.time.Clock()

window = pygame.display.set_mode((1000, 800))   #Window size
pygame.display.set_caption('SNAKE')

def lose(score,origmode):    #Defines lose/score and replay/menu buttons
    while True:
        pygame.mouse.set_visible(True)
        window.fill((204,204,204))
        losetext=losetextfont.render('You lose! Your score was: %i'%score,
                                      1,(0,0,0))
        textpos = losetext.get_rect(center=(500,400))
        replay=losetextfont.render('REPLAY',1,(255,255,255),(0,102,153))
        replayrect=replay.get_rect(center=(500,550))
        window.blit(losetext,textpos)
        window.blit(replay,replayrect)
        pygame.draw.rect(window,(0,0,0),replayrect,3)

        menubutton=losetextfont.render('MENU',1,(255,255,255),(0,102,153))
        menubuttonpos=menubutton.get_rect(center=(500,650))
        window.blit(menubutton,menubuttonpos)
        pygame.draw.rect(window,(0,0,0),menubuttonpos,3)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == QUIT:      #Allows quit
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONUP and event.button==1:
                #Replay on MOUSEUP click on button
                if replayrect.collidepoint(event.pos):
                    return origmode
                elif menubuttonpos.collidepoint(event.pos):
                    mode=menu()
                    return mode

def instructions():     #Defines instructions part of menu
    while True:
        window.fill((204,204,204))
        losetextfont.set_underline(True)
        losetextfont.set_bold(True)
        institle=losetextfont.render('H O W  T O  P L A Y',1,(0,0,0))
        losetextfont.set_underline(False)
        losetextfont.set_bold(False)
        institlepos=institle.get_rect(center=(500,200))
        window.blit(institle,institlepos)
        instext=('Use the arrow keys to move',
          'Collect fruit to increase your score',
          'Blue fruits are worth 100 points','Purple fruits are worth 500',
          'Red fruits are worth 3000, but they increase your speed a lot',
          'Every time you collect a fruit, you get bigger',
          'Running into the wall or yourself kills you',
          'Speed mode increases speed per fruit and final score',
          'Wraparound lets you go to the other edge when you hit one')
        
        instextlist=[]
        for x in instext:   #Lines of text into list
            instextlist.append(scoretextfont.render(x,1,(0,0,0)))
            
        instext=[]
        for x,y in enumerate(instextlist):  #Sets lines 50px below previous
            instext.append(y.get_rect(center=(500,250+x*50)))
            
        for x,y in zip(instextlist,instext):    #Blits lists to screen
            window.blit(x,y)

        backbutton=losetextfont.render('BACK',1,(255,255,255),(0,102,153))
        backbuttonpos=backbutton.get_rect(center=(500,700))
        window.blit(backbutton,backbuttonpos)
        pygame.draw.rect(window,(0,0,0),backbuttonpos,3)
            
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1 and backbuttonpos.collidepoint(event.pos):
                    return None
                
        
def menu():     #Defines menu - play/modes/instructions buttons and version
    pygame.mixer.music.play(-1)
    while True:
        pygame.mouse.set_visible(True)
        window.fill((204,204,204))
        losetextfont.set_underline(True)
        losetextfont.set_bold(True)
        
        title=losetextfont.render('S N A K E',1,(0,0,0))
        titlepos = title.get_rect(center=(500,200))
        window.blit(title,titlepos)
        
        losetextfont.set_underline(False)
        losetextfont.set_bold(False)
        
        playbutton=losetextfont.render('PLAY',1,(255,255,255),(0,102,153))
        playbuttonpos=playbutton.get_rect(center=(500,300))
        window.blit(playbutton,playbuttonpos)
        pygame.draw.rect(window,(0,0,0),playbuttonpos,3)
        
        insbutton=losetextfont.render('HOW TO PLAY',1,(255,255,255),(0,102,153))
        inspos=insbutton.get_rect(center=(500,600))
        window.blit(insbutton,inspos)
        pygame.draw.rect(window,(0,0,0),inspos,3)
        
        names=scoretextfont.render('Justin Ritterson & Andrew Summers',
                                   1,(0,0,0))
        namespos=names.get_rect(right=1000,bottom=800)
        window.blit(names,namespos)
        
        version=scoretextfont.render('Version 1.2', 1, (0,0,0))
        versionpos=version.get_rect(left=0, bottom=800)
        window.blit(version,versionpos)
        
        speed=losetextfont.render('SPEED MODE',1,(255,255,255),(0,102,153))
        speedpos=speed.get_rect(center=(500,400))
        window.blit(speed,speedpos)
        pygame.draw.rect(window,(0,0,0),speedpos,3)

        wraparound=losetextfont.render('WRAPAROUND MODE',1,(255,255,255),
                                       (0,102,153))
        wrappos=wraparound.get_rect(center=(500,500))
        window.blit(wraparound,wrappos)
        pygame.draw.rect(window,(0,0,0),wrappos,3)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONUP and event.button == 1:
                if playbuttonpos.collidepoint(event.pos):
                    pygame.mixer.music.fadeout(1000)
                    return None
                elif inspos.collidepoint(event.pos):
                    instructions()
                elif speedpos.collidepoint(event.pos):
                    pygame.mixer.music.fadeout(1000)
                    return 'speedmode'       #Enables speed mode
                elif wrappos.collidepoint(event.pos):
                    pygame.mixer.music.fadeout(1000)
                    return 'wraparound'     #Enables wraparound mode
      
mode=menu()     #Sets the mode - normal/speed/wraparound

while True:     #Start of main loop
    scoretext=scoretextfont.render(str(score),1,(0,0,0))
    pygame.mouse.set_visible(False)
    window.fill((204,204,204))      #Ground color
    window.blit(scoretext,(0,0))
    pygame.draw.rect(window, (0,0,0),(10,30,980,760),2) #Border

    while not fruitflag:    #Makes sure fruits dont spawn on segments
        fruitpos=random.choice(fruitgrid)
        if fruitpos not in segments:
            fruitflag = True
            randnum=random.random()
            if randnum < .05:
                fruitscore=3000
                fruitcolor=(200,0,0)    #Unlucky fruit color (5%)
            elif randnum < .3:
                fruitscore=500
                fruitcolor=(153,102,153)  #Special fruit color (25%)
            else:
                fruitscore=100
                fruitcolor=(0,102,153)    #Fruit color (70%)
            if mode=='speedmode':fruitscore*=2  #Double score on speedmode
            elif mode=='wraparound':fruitscore/=2   #Half score on wraparound

    pygame.draw.circle(window, fruitcolor, fruitpos, 8) #Spawns fruit

    for x in segments:  #Draws all segments
        pygame.draw.circle(window, (0,0,0), x, 10)


    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
        elif event.type == KEYDOWN:     #Defines keys to movement
            if (event.key==K_DOWN or event.key==K_s) and direction != 'up':
                direction = 'down'
                break
            elif (event.key==K_UP or event.key==K_w) and direction != 'down':
                direction = 'up'
                break
            elif (event.key==K_LEFT or event.key==K_a) and direction != 'right':
                direction = 'left'
                break
            elif (event.key==K_RIGHT or event.key==K_d) and direction != 'left':
                direction = 'right'
                break
                
    lastposx=segments[-1][0]    #Allows you to keep moving after fruit pickup
    lastposy=segments[-1][1]

    if segments[0] == fruitpos: #Pick up fruit
        fruitflag = False
        if len(segments) < MAXSIZE:
            segments.append([lastposx,lastposy])    #Adds segment/fruit eaten
            if fruitcolor == (200,0,0):
                if mode=='speedmode':   #Increases FPS with unlucky fruit -
                    clockspeed+=20      #on speedmode
                else:
                    clockspeed+=10  #Increases FPS with unlucky fruit -
            else:                   #all other modes
                if mode=='speedmode':   #Increases FPS with regular fruit -
                    clockspeed+=5       #on speedmode
                else:
                    clockspeed+=1       #Increases FPS on regular mode
        score+=fruitscore       #Adds to score with fruit pickup

    for x in xrange(len(segments)-1):
        segments[len(segments)-x-1][0] = segments[len(segments)-x-2][0]
        segments[len(segments)-x-1][1] = segments[len(segments)-x-2][1]
        #len-1 is the last in list, -x moves it further to left every loop
        #len-x-2 is the index before
    
    if direction == 'down':     #Moves head 20px in direction pressed
        segments[0][1] += 20

    elif direction == 'up':
        segments[0][1] -= 20
        
    elif direction == 'left':
        segments[0][0] -= 20
        
    elif direction == 'right':
        segments[0][0] += 20

    
    if segments[0][0] in (1000,0) or segments[0][1] in (800,20):
        if mode=='wraparound':  #Flips head to opposite side on wraparound mode
            if direction=='down': segments[0][1]=40
            elif direction=='up': segments[0][1]=780
            elif direction=='left': segments[0][0]=980
            else: segments[0][0]=20
        else:   #Pauses on death/calls lose function/resets all variables
            time.sleep(.5)
            mode=lose(score,mode)
            direction = None
            segments=[[500,400]]
            fruitflag=False
            clockspeed=10
            score=0 
        
    if segments[0] in segments[1:]: #Same as above - if you hit yourself
        time.sleep(.5)
        mode=lose(score,mode)
        direction = None
        segments=[[500,400]]
        fruitflag=False
        clockspeed=10
        score=0 
        
    fpsClock.tick(clockspeed)   #Sets FPS
