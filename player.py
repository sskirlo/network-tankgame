import pygame, sys
from pygame.locals import *
from random import randint
from math import *
from controls import *
from settings import *
from tank import *
from bullit import *
from collisionbox import *

#contains main variables that controls background enviorment including timestep 

class player():

    def __init__(self,dispsurf,pygame,enviorment,settings,keys,bullits,collisionboxes):
        self.settings=settings
        self.keys=keys
        self.controls=controls()
        self.bullits=bullits
        self.collisionboxes=collisionboxes
        self.mytank=tank(dispsurf,pygame,enviorment,settings,bullits,collisionboxes)

    #take event and use to update control object, based on keyset for player
    def updatecontrols(s,event):
        
        if event.type==pygame.KEYDOWN:
            if event.key==s.keys[0]:
                s.controls.startcw()
            if event.key==s.keys[1]:
                s.controls.startccw()
            if event.key==s.keys[2]:
                s.controls.startl()
            if event.key==s.keys[3]:
                s.controls.startr()
            if event.key==s.keys[4]:
                s.controls.startfire() 
        if event.type==pygame.KEYUP:
            if event.key==s.keys[0]:
                s.controls.stopcw()
            if event.key==s.keys[1]:
                s.controls.stopccw()
            if event.key==s.keys[2]:
                s.controls.stopl()
            if event.key==s.keys[3]:
                s.controls.stopr()
            if event.key==s.keys[4]:
                s.controls.stopfire() 

        #s.controls.printstate()

    #do necessary actions to update player information and objects
    def update(self):
        self.mytank.update(self.controls)

        
