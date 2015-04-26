import pygame, sys
from pygame.locals import *
from random import randint
from math import *

#space Tanks, tanks in space, now with 100% more space 

#we intrepret left right signals,and turret signals

RADVEL=0.02
VELX=2
VELY=0

class controls():

    def __init__(self):
        #set moving states
        self.velx=0
        self.vely=0
        self.velrad=0
        self.fire=0

    def startl(self):
        self.velx=-VELX

    def stopl(self):
        self.velx=0

    def startr(self):
        self.velx=VELX

    def stopr(self):
        self.velx=0

    def startccw(self):
        self.velrad=-RADVEL

    def stopccw(self):
        self.velrad=0

    def startcw(self):
        self.velrad=RADVEL

    def stopcw(self):
        self.velrad=0

    def startfire(self):
        self.fire=1

    def stopfire(self):
        self.fire=0

    def printstate(self):
        print("Velx ",self.velx," Velrad ",self.velrad," fire ",self.fire)
        
        



        
        
    
        
        
        
