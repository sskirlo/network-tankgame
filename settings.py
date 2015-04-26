import pygame, sys
from pygame.locals import *
from random import randint
from math import *

#settings class for settings of tank position etc

class settings():

    def __init__(self,color,x,y,angleturret):
        self.color=color
        self.posx=x
        self.posy=y
        self.angleturret=angleturret
        self.fire=0


    
        
        
        
