import pygame, sys
from pygame.locals import *
from random import randint
from math import *
from collisionbox import * 

#radius to damage factor
RD=0.1

#contains main variables that controls background enviorment including timestep 

class explosion():

    def __init__(self,pygame,dispsurf,explosionnum,rad,collisionboxes):
        self.pygame=pygame
        self.dispsurf=dispsurf
        self.explosionnum=explosionnum
        self.rad=rad
        self.collisionboxes=collisionboxes

    #we simply scale color and radius linearily based on the number of steps
    def update(s,step,location):
        if step==1:  #apply damage on first step
            s.applyDamage(location)
        raddraw=step/s.explosionnum*s.rad
        color=(255,int(255*step/s.explosionnum),0)
        pygame.draw.circle(s.dispsurf,color,(int(location[0]),int(location[1])),int(raddraw))
                
#determine if an object hit the collision box
#once we start explosion, we determine if any hitbox objects are effected, and
#apply damage to objects based on distance from explosion and explosion properties
    def applyDamage(s,location):
        for collisionbob in s.collisionboxes:
            pos2=collisionbob.getCenter()
            #print(location,pos2) 
            dist=s.distance(location,pos2)
            #if within explosion radius
            if dist < (s.rad*1.5): #a little bit larger than actual radius of explosion
                damage=((s.rad*1.5)-dist)*RD
                #print("apply damage ",damage)
                collisionbob.receiveDamage(damage) #apply damage to collision object

    def distance(s,p1,p2):
        return pow(pow(p1[0]-p2[0],2.0)+pow(p1[1]-p2[1],2.0),0.5)
