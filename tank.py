
import pygame, sys
from pygame.locals import *
from random import randint
from math import *
from enviorment import *
from settings import *
from controls import *
from bullit import *
from collisionbox import *
from explosion import *
from cloud import * 

WHITE= (255,255,255)
BLACK=(0,0,0)
GRAY=(50,50,50)
#RED=(255,0,0)

SYTANK=6
RADWHEEL=2
TURRETRAD=8
TURRETLEN1=17
TURRETWIDTH1=6
TURRETLEN2=35
TURRETWIDTH2=3
FIRING1=12
FIRING2=17
WHEELNUM=10
SXTANK=WHEELNUM*2*RADWHEEL
HEALTHBARY=10
HEALTHBARHEIGHT=5
HEALTH=100

SYTANKTOT=2*RADWHEEL+SYTANK+TURRETRAD

LOWANGLE=-(45-30)/180.0*pi
HIGHANGLE=(225-30)/180.0*pi

EXPLOSIONNUM=15
EXPLOSIONRAD=150

FINISHEDBURNING=6000

GRAVITY=-0.02

class tank():

    def __init__(self,dispsurf,pygame,enviorment,settings,bullits,collisionboxes):
        self.dispsurf=dispsurf
        self.pygame=pygame
        self.enviorment=enviorment
        self.settings=settings
        self.anum=0
        self.bullits=bullits #global bullits list, we add all bullits to this
        self.health=HEALTH
        self.killed=0
        self.killsteps=0
        self.collisionboxes=collisionboxes
        #add self to collisionbox array, box includes turret and bottom part of tank
        #need to pass self as argument to collisionbox method
        self.mycollisionbox=collisionbox(self,dispsurf,SXTANK,SYTANKTOT,(self.settings.posx,enviorment.sizey-(enviorment.heightground+self.settings.posy+SYTANKTOT/2.0)))
        self.collisionboxes.append(self.mycollisionbox)

        #variables connected to killing tank
        self.myclouds=[]
        self.explosion=explosion(pygame,dispsurf,EXPLOSIONNUM,EXPLOSIONRAD,collisionboxes)
        self.turrettraj=(0,0)
        self.spinrate=randint(-100,100)/300.0
        self.v0=(randint(-40,40)/100.0,randint(-400,-200)/50.0)  #initial velocity of turret if we kill tank 

    #drawsbody
    def drawbody(s,color):
        posx=s.settings.posx
        posy=s.settings.posy

        sizey=s.enviorment.sizey-s.enviorment.heightground
        angle=s.settings.angleturret 
        
        pygame.draw.rect(s.dispsurf, BLACK, (posx-SXTANK/2.0,sizey-(posy+RADWHEEL*2),SXTANK,RADWHEEL*2) )
        pygame.draw.rect(s.dispsurf, color, (posx-SXTANK/2.0,sizey-(posy+RADWHEEL*2+SYTANK),SXTANK,SYTANK) )

        #draw wheels
        for n in range(0,WHEELNUM,1):
            pygame.draw.circle(s.dispsurf, WHITE, (int(RADWHEEL+n*2*RADWHEEL+posx-SXTANK/2),int(sizey-RADWHEEL)),RADWHEEL )

    #draws turret 
    def drawturret(s,firescale,posturret):
        
        angle=s.settings.angleturret 
        
        pygame.draw.circle(s.dispsurf, s.settings.color,posturret,TURRETRAD )
        
        #draw gun
        #polygon(Surface, color, pointlist, width=0)
        points1=s.translatePoints(s.calculateRotatedRectangle(TURRETLEN1-FIRING1*firescale,TURRETWIDTH1,angle),posturret)
        points2=s.translatePoints(s.calculateRotatedRectangle(TURRETLEN2-FIRING2*firescale,TURRETWIDTH2,angle),posturret)

        #draw main shaft of gun
        pygame.draw.polygon(s.dispsurf,BLACK,points2)
        pygame.draw.polygon(s.dispsurf,s.settings.color,points1)

    def killtank(s):

        deltat=s.enviorment.deltat
        posx=s.settings.posx
        posy=s.settings.posy

        sizey=s.enviorment.sizey-s.enviorment.heightground 

        ps=(int(posx),int(sizey-(RADWHEEL*2+SYTANK)))

        #initialize turrettraj first killstep
        if s.killsteps==0:
            s.turrettraj=ps
        
        time=deltat*s.killsteps

        if s.turrettraj[1]<sizey:  #stop moving once hits ground
            #print(s.turrettraj,s.v0[0],s.v0[1])
            s.turrettraj=(int(ps[0]+s.v0[0]*time),int(ps[1]+s.v0[1]*time-1/2*GRAVITY*pow(time,2))) #update trajectory
            s.settings.angleturret=s.settings.angleturret+s.spinrate  #keep turret spinning 

        #turret animation
        s.drawturret(0,s.turrettraj)

        #keep updating explosion centered at middle of tank
        if s.killsteps<EXPLOSIONNUM:
            s.explosion.update(s.killsteps,s.mycollisionbox.getCenter())  
            
        sizey=s.enviorment.sizey-s.enviorment.heightground
        
        s.drawbody(GRAY)

        #if finished with explosion, randomly create new clouds
        if (s.killsteps>EXPLOSIONNUM) & (s.killsteps<FINISHEDBURNING):
            makecloud=randint(0,15)
            if makecloud==0:
                s.myclouds.append(cloud(s.dispsurf,s.enviorment,s.mycollisionbox.getCenter())) #include randomness inside 

        #update clouds, get rid of clouds that have left the system 
        killclouds=[]
        for clouds in s.myclouds:
            clouds.update()
            if clouds.gone()==1:
                killclouds.append(clouds)
        
        for clouds in killclouds:
            s.myclouds.remove(clouds)
            #print(len(s.myclouds))
        
        s.killsteps+=1

    def drawtank(s):

        firescale=0
    
        posx=s.settings.posx
        posy=s.settings.posy
        fire=s.settings.fire
            
        sizey=s.enviorment.sizey-s.enviorment.heightground
        angle=s.settings.angleturret          

        posturret=(int(posx),int(sizey-(RADWHEEL*2+SYTANK)))

        #if fire==1:
        #    print("fire")
        #    print(s.anum)
        #    print((s.anum==0) & (fire==1) )

        #animation for firing, we don't respond to next fire command until finished with animation 
        if (s.anum==0) & (fire==1):
            #print("fire!")
            s.bullits.append(bullit(s.pygame,s.dispsurf,s.enviorment,s.settings,posturret,TURRETLEN2,s.collisionboxes)) #add new bullit to bullit list 
            firescale=0.3
            s.anum+=1
        elif s.anum==1:
            firescale=0.6
            s.anum+=1
        elif s.anum==2:
            firescale=1.0
            s.anum+=1
        elif s.anum==3:
            firescale=0.75
            s.anum+=1
        elif s.anum==4:
            firescale=0.5
            s.anum+=1
        elif s.anum==5:
            firescale=0.25
            s.anum+=1
        elif s.anum==6:
            firescale=0
            s.anum=0
        
        s.drawturret(firescale,posturret)
        s.drawbody(s.settings.color) 

    #this is called by collision box which gets called by explosion object 
    def receiveDamage(s,damage):
        s.health=s.health-damage
        if s.health<0.0:  #tank killed if health bellow
            s.health=0
            s.killed=1
            #print("player killed")

    def drawHealthBar(s):
        posx=s.settings.posx
        posy=s.settings.posy
        sizey=s.enviorment.sizey-s.enviorment.heightground
        pygame.draw.rect(s.dispsurf, (255,0,0), (posx-SXTANK/2.0,sizey-(posy+RADWHEEL*2+SYTANK+TURRETRAD+HEALTHBARY),SXTANK,HEALTHBARHEIGHT) )
        pygame.draw.rect(s.dispsurf, (0,255,0), (posx-SXTANK/2.0,sizey-(posy+RADWHEEL*2+SYTANK+TURRETRAD+HEALTHBARY),int(SXTANK*s.health/HEALTH),HEALTHBARHEIGHT) )
        
    def calculateRotatedRectangle(s,length,width,angle):

        #create list of points for rectangle
        listpoints=[(0,0),(0,width),(length,width),(length,0)]
        trans=(0,-width/2.0)
        translated=s.translatePoints(listpoints,trans)
        #rotate points by appropriate angle
        return s.rotatePoints(translated,angle)

    def translatePoints(s,listpoints,trans):
        translated=[]
        for point in listpoints:
            translated.append((point[0]+trans[0],point[1]+trans[1]))
        return translated
        
    def rotatePoints(s,listpoints,angle):
        rotated=[]
        for point in listpoints:
            rotated.append( ( int(point[0]*cos(angle)+point[1]*sin(angle)), int(-point[0]*sin(angle)+point[1]*cos(angle)) ) )
        return rotated

    def update(s,controls):

        #things to take care of if not dead
        if s.killed==0:
        
            deltat=s.enviorment.deltat
            
            s.settings.posx=controls.velx*deltat+s.settings.posx
            #prevent from leaving boundary 
            if s.settings.posx>s.enviorment.maxx:
                s.settings.posx=s.enviorment.maxx
            if s.settings.posx<s.enviorment.minx:
                s.settings.posx=s.enviorment.minx

            angle=s.settings.angleturret    

            angle=controls.velrad*deltat+angle
            s.settings.angleturret=angle
            #prevent from leaving boundary 
            if angle>HIGHANGLE:
                angle=HIGHANGLE
            if angle<LOWANGLE:
                angle=LOWANGLE

            s.settings.angleturret=angle

            #simple for mapping fire control to settings 
            s.settings.fire=controls.fire

            s.drawHealthBar()
        
            s.drawtank()
            #update collision box location
            s.mycollisionbox.update((s.settings.posx,s.enviorment.sizey-(s.enviorment.heightground+s.settings.posy+SYTANKTOT/2.0)))
        else:
            s.killtank()  #handles smoke and death animation

        
        

        
        
            



