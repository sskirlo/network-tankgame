import pygame, sys
from pygame.locals import *
from random import randint
from math import *

#define collision box to be associated with tank,
#we will use it to assess whether bullits collide and determine
#distance from explosion to see what damage it takes 

#allow drawing of collision box for debugging purposes
class collisionbox():

    def __init__(self,caller,dispsurf,sizex,sizey,pos):
        #set moving states
        self.caller=caller #we keep caller object because caller object receives damage
        self.dispsurf=dispsurf
        self.sizex=sizex
        self.sizey=sizey
        self.pos=pos

#update collision box location
    def update(s,pos):
        #draw collision box for debugging
        s.pos=pos
        #pygame.draw.rect(s.dispsurf, (255,255,255), (int(s.pos[0]-s.sizex/2.0),int(s.pos[1]-s.sizey/2.0),s.sizex,s.sizey)) 

    def getCenter(s):
        return s.pos

    #pass damage from explosion object to object which created collision box
    def receiveDamage(s,damage):
        s.caller.receiveDamage(damage)

    def hitbox(s,proj):
        #print('check hit')
        xmin=s.pos[0]-s.sizex/2
        xmax=s.pos[0]+s.sizex/2
        ymin=s.pos[1]-s.sizey/2
        ymax=s.pos[1]+s.sizey/2
        if (proj[0]>xmin) & (proj[0]<xmax) & (proj[1]<ymax) & (proj[1]>ymin):
            #print('hit')
            return 1
        else:
            return 0

    
        
        



        
        
    
        
        
        
