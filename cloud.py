import pygame, sys
from pygame.locals import *
from random import randint
from math import *

BLACK=(0,0,0)

#contains main variables that controls background enviorment including timestep 
VX=0.0002
VY=0.001

LEN=30
HEIGHT=10

class cloud():

    def __init__(self,dispsurf,enviorment,pos):
        self.dispsurf=dispsurf
        self.enviorment=enviorment
        self.isgone=0

        #randomly vary initial conditions of cloud 
        dx=randint(-20,20)
        dy=randint(-40,0)

        dvx=randint(-100,100)/200.0*VX
        dvy=randint(-100,100)/200.0*VY

        self.pos=(pos[0]+dx,pos[1]+dy)
        self.vel=(VX+dvx,VY+dvy)

        self.steps=0

    def update(s):
        
        deltat=s.enviorment.deltat

        color=int(s.steps/4.0)
        if color>255:
            color=255
            
        pygame.draw.ellipse(s.dispsurf, (0,0,color), (int(s.pos[0]-LEN/2.0),int(s.pos[1]-HEIGHT/2.0),LEN,HEIGHT) )

        s.pos=(s.pos[0]+s.vel[0]*deltat*s.steps,s.pos[1]-s.vel[1]*deltat*s.steps)

        s.steps+=1

        #clouds have drifted beyond boundary 
        if s.pos[1]<0:
            s.isgone=1

    #tells if clouds have drifted beyond boundary 
    def gone(self):
        return self.isgone
        
        
        
