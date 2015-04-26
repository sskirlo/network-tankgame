import pygame, pygame.font, pygame.event, pygame.draw, string
from pygame.locals import *
from sys import exit
import re
import socket
import gametank

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

#uses regular expressions to check if valid ip address
#doesn't actually work
def validIP(ip):
    """Validates IPv4 addresses.
    """
    #check type 
    
    pattern = re.compile(r"""
        ^
        (?:
          # Dotted variants:
          (?:
            # Decimal 1-255 (no leading 0's)
            [3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}
          |
            0x0*[0-9a-f]{1,2}  # Hexadecimal 0x0 - 0xFF (possible leading 0's)
          |
            0+[1-3]?[0-7]{0,2} # Octal 0 - 0377 (possible leading 0's)
          )
          (?:                  # Repeat 0-3 times, separated by a dot
            \.
            (?:
              [3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}
            |
              0x0*[0-9a-f]{1,2}
            |
              0+[1-3]?[0-7]{0,2}
            )
          ){0,3}
        |
          0x0*[0-9a-f]{1,8}    # Hexadecimal notation, 0x0 - 0xffffffff
        |
          0+[0-3]?[0-7]{0,10}  # Octal notation, 0 - 037777777777
        |
          # Decimal notation, 1-4294967295:
          429496729[0-5]|42949672[0-8]\d|4294967[01]\d\d|429496[0-6]\d{3}|
          42949[0-5]\d{4}|4294[0-8]\d{5}|429[0-3]\d{6}|42[0-8]\d{7}|
          4[01]\d{8}|[1-3]\d{0,9}|[4-9]\d{0,8}
        )
        $
    """, re.VERBOSE | re.IGNORECASE)

    #need to convert ip to a string, list type when it comes in
    print(pattern.match(''.join(ip)))

    
    return pattern.match(''.join(ip)) is not None
    
def validName(name):
    return not(not(name)) #return boolean form of name, false if empty

def validColor(color):
    color=''.join(color)  #convert to string type so we can compare 
    if color=='r':
        return True
    elif color=='g':
        return True
    elif color=='b':
        return True
    elif color=='or':
        return False
    
def main():

    screen = pygame.display.set_mode((400,240))
    pygame.display.set_caption('Tanks: The classic game of explosions')

    #keep querying until we get a valid ip

    ipserver=''

    while not(validIP(ipserver)):
        request=ask(screen, "Enter Server ip (127.0.0.1 for local): ")
        if request=='q':
            quitgame()
        else:
            ipserver=request
            print(jString(request," was entered"))

    name=''

    while not(validName(name)):
        request=ask(screen, "Enter Name: ")
        if request=='q':
            quitgame()
        else:
            name=request
            print(jString(request," was entered"))

    color=''

    while not(validColor(color)):
        request=ask(screen, "Enter Color (r,g,b,or): ")
        if request=='q':
            quitgame()
        else:
            color=request
            print(jString(request," was entered"))

    #we should put try catch loop in here 

    PORT = 12345    # Arbitrary non-privileged port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((''.join(ipserver),PORT))  #connect to server wait for reply

    display_box(screen,'Connected: waiting for other players to connect')

    message1=s.recv(1024)  #tells us our player number all total players
    message1=message1.decode()
    print(message1) #we need to decode byte object back into string

    #need to extract player number and total players from string

    NUMPLAYER=int(message1.split()[0])
    NUMPLAYERS=int(message1.split()[1])

    print('Player number ',NUMPLAYER)
    print('Number of players ',NUMPLAYERS)

    #send player data to server
    s.sendall(str.encode(''.join(name)+' '+''.join(color))) #encode into byte object

    print('sent data')

    #receive all player data
    message2=s.recv(1024)
    message2=message2.decode()

    #now extract player data from extracted screen and create lists
    playernames=[]
    playercolors=[]

    for n in range(0,NUMPLAYERS):
      playernames.append(message2.split()[0+n*NUMPLAYERS])
      playercolors.append(message2.split()[1+n*NUMPLAYERS])

    print(playernames)
    print(playercolors)

    #now we have enough information to be able to start the game 

    finished=0

    while finished==0:
      finished=gametank.main(s,NUMPLAYERS,NUMPLAYER,playernames,playercolors)

    quitgame()

    
if __name__ == '__main__': main()
