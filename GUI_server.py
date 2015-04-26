import pygame, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *
from sys import exit
import re
import socket

#while checking get_key also check if want to quit
def get_key():
  while 1:
    event = pygame.event.poll()
    if event.type == KEYDOWN:
        return event.key
    elif event.type == QUIT:
        return 'q'        
    else:
      pass

def display_box(screen, message):
  "Print a message in a box in the middle of the screen"
  fontobject = pygame.font.Font(None,18)

  #refresh screen
  pygame.draw.rect(screen, (0,125,0),
                   (0,0,
                    screen.get_width(),screen.get_height()), 0)
  #pygame.draw.rect(screen, (255,255,255),
  #                 ((screen.get_width() / 2) - 102,
  #                  (screen.get_height() / 2) - 12,
  #                  204,24), 1)
  if len(message) != 0:
    screen.blit(fontobject.render(message, 1, (255,255,255)),
                ((screen.get_width() / 2) - 100, (screen.get_height() / 2) - 10))
  pygame.display.flip()


def ask(screen, question):
  "ask(screen, question) -> answer"
  pygame.font.init()
  current_string = []
  print( jString(question,current_string))
  display_box(screen, jString(question,current_string))
  while 1:
    inkey = get_key()
    if inkey == 'q':  #quitting game
        return 'q'
    elif inkey == K_BACKSPACE:
      current_string = current_string[0:-1]
    elif inkey == K_RETURN:
      break
    elif inkey <= 127:  #other characters
      current_string.append(chr(inkey))
    display_box(screen, jString(question,current_string))
  return current_string

def jString(str1,str2):
    return ''.join(str1)+''.join(str2)

#close up connection and send server appropriate message
def quitgame():
    pygame.quit() #quit pygame and quit application
    quit(0) #quit game no error
    
#main will get inputs necessary for running tank game
#including ip, name and color, and will start tankgame with this information

def validNumber(Number):
    #have to remmeber to convert number to string 
    Number=''.join(Number)
    
    try:
        int(Number) #check if can be converted to integer
        #print('worked')
        if( (int(Number)<5) and (int(Number)>1)): #check if out of range
            return True
        return False
    except:  #catch error and keep going
        #print(int(Number))
        return False
    
def main():

    screen = pygame.display.set_mode((400,240))
    pygame.display.set_caption('Tanks: The classic game of explosions')

    Number=''

    while not(validNumber(Number)):
        request=ask(screen, "(Server) Enter number of players (2-4): ")
        if request=='q':
            quitgame()
        else:
            Number=request
            print(jString(request," was entered"))

    NUMCL=int(''.join(Number))  #if person running server enters valid number

    HOST = '127.0.0.1'   # Symbolic name meaning the local host
    PORT = 12345    # Arbitrary non-privileged port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('Socket created')
    try:
        s.bind((HOST, PORT))
    except socket.error as msg:
        print('Bind failed. Error code: ' + str(msg.errno) + 'Error message: ' + msg.stderror)
        quitgame()
    print('Socket bind complete')
    s.listen(1)
    print('Socket now listening')


    connlist=[]  #connection object list

    for bob in range(0,NUMCL,1):
        (conn, addr) = s.accept()
        print('Connected with ' + addr[0] + ':' + str(addr[1]))
        connlist.append(conn)  #add new connection to connlist

    #tell each player the number of players, and its player num
    num=1
    for bob in connlist:
        bob.sendall(str.encode(str(num)+' '+str(NUMCL)))
        num+=1

    #receive player data (name and color)
    data=''
    for bob in connlist:
        joe=bob.recv(1024)
        joe=joe.decode()
        data=data+' '+joe #need to decode byte object into string 
        print(joe+' received')

    #send all data to all players
    for bob in connlist:  
        bob.sendall(str.encode(data)) #can also do data.encode()

    #run game loop
    while True:
        #receive states from all players
        data=''
        for bob in connlist:
            joe=bob.recv(1024)
            joe=joe.decode()
            data=data+' '+joe 
            #print(joe+' received')
            
        #broadcast states to all players
        #send all data to all players
        for bob in connlist:  
            bob.send(str.encode(data)) #can also do data.encode()


    #ask for player colors and store

    for bob in connlist:   #close all connections to clients 
        bob.close()

    quitgame()

    
if __name__ == '__main__': main()
