import pygame, sys
from pygame.locals import *
from random import randint
from math import *

WHITE= (255,255,255)
BLACK=(0,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)

#contains main variables that controls background enviorment including timestep 

class enviorment():

    def __init__(self,dispsurf,pygame,sizex,sizey,heightground,deltat):
        self.pygame=pygame
        self.dispsurf=dispsurf
        self.maxx=sizex
        self.minx=0
        self.maxy=sizey
        self.miny=0
        self.sizex=sizex
        self.sizey=sizey
        self.heightground=heightground
        self.deltat=deltat

    def update(self):
        #sizex=1
        #print(self.sizex," ",self.sizey)
        pygame.draw.rect(self.dispsurf, BLUE, (self.minx,self.miny,self.sizex,self.sizey) )
        pygame.draw.rect(self.dispsurf, GREEN, (self.minx,self.sizey-self.miny-self.heightground,self.sizex,self.heightground) )
        
        
        
