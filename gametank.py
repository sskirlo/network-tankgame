import pygame, sys
from pygame.locals import *
from random import randint
from math import *
from settings import *
from enviorment import *
from controls import *
from player import *
from bullit import *
import socket

WHITE= (255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
BLUE=(0,0,255)
GREEN=(0,255,0)
GREY=(125,125,125)
ORANGE=(255,155,0)
FPS=60;

SIZEX=1000
SIZEY=600
HEIGHTGROUND=30

DELTAT=2

STARTRADLEFT=45/180.0*pi
STARTRADRIGHT=(180.0-45)/180.0*pi

BUF=30

START1X=BUF
START2X=SIZEX-BUF

ColorDict={'r':RED,'g':GREEN,'b':BLUE,'or':ORANGE}

def main(socket,NUMPLAYERS,NUMPLAYER,playernames,playercolors):

     pygame.init()
     DISPLAYSURF = pygame.display.set_mode((SIZEX, SIZEY),0,32)
     pygame.display.set_caption('Tanks: The classic game of explosions')

   
     clock=pygame.time.Clock()

     #this controls quitting game
     qt=-1

     #this list will store all bullet objects for the game
     bullits=[]
     collisionboxes=[]
     players=[]

     #initialize enviorment
     envior=enviorment(DISPLAYSURF,pygame,SIZEX,SIZEY,HEIGHTGROUND,DELTAT)

     #initialize players
     
     if NUMPLAYERS==2:
          #create settings object for tank 
          settings1=settings(ColorDict[playercolors[0]],START1X,0,STARTRADLEFT)
          keys1=(K_w,K_s,K_a,K_d,K_x)
          player1=player(DISPLAYSURF,pygame,envior,settings1,keys1,bullits,collisionboxes)
          players.append(player1)

          #create settings object for tank 
          settings2=settings(ColorDict[playercolors[1]],START2X,0,STARTRADRIGHT)
          keys2=(K_UP,K_DOWN,K_LEFT,K_RIGHT,K_RETURN)
          player2=player(DISPLAYSURF,pygame,envior,settings2,keys2,bullits,collisionboxes)
          players.append(player2)


     while True: # main game loop

          #update enviorment
          envior.update()

          #update bullits
          #update bullits for tank
          bullitremove=[]
          for bullitguy in bullits:
               bullitguy.update()
               if bullitguy.isexploded():
                    bullitremove.append(bullitguy)

          #need to remove bullits which are finished executing 
          for bullitguy in bullitremove:
               bullits.remove(bullitguy)
               #print(len(bullits))

          #update players
          for playerbob in players:               
               playerbob.update()


          #respond to use inputs
          for event in pygame.event.get():
               #print(event.type)
               #print(QUIT)
               if event.type == QUIT and qt == -1:
                    pygame.quit()
                    qt=1
               if qt == 1:
                    break

               #update local player based on chosen keymap
               players[NUMPLAYER-1].updatecontrols(event)

               #now get player control state and send to server
               state=(str(players[NUMPLAYER-1].controls.velx)+' '
               +str(players[NUMPLAYER-1].controls.velrad)+' '
               +str(players[NUMPLAYER-1].controls.fire))

               socket.send(state.encode())

               #set control state of all players based on what we receive
               #from server

               data=socket.recv(1024)
               data=data.decode()
               #print(data)
               #extract states from data string

               for n in range(0,NUMPLAYERS):
                    players[n].controls.velx=float(data.split()[0+3*n])
                    players[n].controls.velrad=float(data.split()[1+3*n])
                    players[n].controls.fire=int(data.split()[2+3*n])
               
          if qt == 1:
               break
          pygame.display.update()
          clock.tick(FPS)

     return 0 #quit

    # print('exit')

