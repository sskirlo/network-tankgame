import pygame, sys
from pygame.locals import *
from random import randint
from math import *
from settings import *
from enviorment import *
from explosion import *
from collisionbox import *

#create new bullit object

VEL=4
GRAVITY=-0.02
LENBULLIT=6
WIDTHBULLIT=3

EXPLOSIONNUM=10
EXPLOSIONRAD=40

YELLOW=(125,125,0)

class bullit():

    def __init__(self,pygame,dispsurf,enviorment,settings,turretpos,turretlen,collisionboxes):
        #set moving states
        self.pygame=pygame
        self.dispsurf=dispsurf
        self.enviorment=enviorment
        self.settings=settings
        self.turretpos=turretpos
        self.collisionboxes=collisionboxes

        #calculate initial position and velocity
        angle=self.settings.angleturret

        #create bullit outside tank so we don't have problem with it blowing itself 
        self.pos0=(self.turretpos[0]+turretlen*cos(angle),self.turretpos[1]-turretlen*sin(angle))
        self.pos=self.pos0
        self.v0=(VEL*cos(angle),-VEL*sin(angle))
        self.v=self.v0
        self.time=0

        #explosion variables
        self.exploded=0
        self.explosionstep=0

        #create explosion class 
        self.explosion=explosion(pygame,dispsurf,EXPLOSIONNUM,EXPLOSIONRAD,collisionboxes)
        
    def update(s):
        collided=s.checkcollision()
        #we update two different directions depending on whether or not collided
        #with something
        
        if collided==0:
            s.time=s.time+s.enviorment.deltat
            #calculate velocity at current position
            s.v=(s.v0[0],s.v0[1]-GRAVITY*s.time)
            s.pos=(s.pos0[0]+s.v0[0]*s.time,s.pos0[1]+s.v0[1]*s.time-1/2*GRAVITY*pow(s.time,2))
            #calculate bullit angle from velocity vector
            ag=atan2(s.v[1],s.v[0])
            #drawline for bullit
            start=(int(s.pos[0]-LENBULLIT*cos(ag)),int(s.pos[1]-LENBULLIT*sin(ag)))
            end=(int(s.pos[0]+LENBULLIT*cos(ag)),int(s.pos[1]+LENBULLIT*sin(ag)))
            pygame.draw.line(s.dispsurf,YELLOW,start,end,WIDTHBULLIT)
        elif collided==1:
            if s.explosionstep<EXPLOSIONNUM:
                s.explosionstep+=1
                s.explosion.update(s.explosionstep,s.pos)
            else:
                s.exploded=1  #set marker to exploded after finished with animation
            
    def checkcollision(s):
        #check if hit enviorment boundary
        if (s.enviorment.sizey-s.enviorment.heightground)<s.pos[1]:
            return 1
        
        #check if hit one of the collision boxes 
        for collisionbob in s.collisionboxes:
            if collisionbob.hitbox(s.pos)==1:
                return 1
        
        return 0

    #tells us if bullit exploded so we can remove from list 
    def isexploded(s):
        return s.exploded
        

