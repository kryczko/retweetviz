#!/opt/local/bin/python2.7

import pygame, sys, numpy, time, math
from numpy import *
from pygame.locals import *

### get the number of nodes and transmission probability
n_nodes = int(sys.argv[1])
trans_prob = float(sys.argv[2])

# some colours
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
darkBlue = (0,0,128)
white = (255,255,255)
black = (0,0,0)
pink = (255,200,200)

# screen size
xsize = 1400
ysize = 900

# initialize pygame
pygame.init()
# set the screen size, create the screen and add a caption
size = [xsize,ysize]
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Retweet algorithm")
# controls the exit of the program
done = False
# set the clock
clock = pygame.time.Clock()

# colour of circle
ballcolour = red

# draw text on the screen using this font
font = pygame.font.Font(None, 30)

# lists to hold node positions
x = []
y = []
nodecolours = []
nodesizes = []
headnodesize = 35
othernodesize = 20
n_chains = 5 # constant
rotate = []
def set_node_positions():
    # the 'king' node
    xorig = int(xsize/2.)
    yorig = 50
    x.append(int(xsize/2.))
    y.append(int(yorig))
    nodecolours.append(darkBlue)
    nodesizes.append(headnodesize)

    # the others attached by a 'chain'

    # radius between nodes
    node_p_chain = int(n_nodes / 5.)
    # radius between nodes
    r = (ysize - 150)/ node_p_chain

    for i in range(1,n_chains + 1):
        for j in range(1,node_p_chain + 1):
            x.append(int(x[0] - j*r*sin(i*0.523 + 1.571)))
            y.append(int(y[0] - j*r*cos(i*0.523 + 1.571)))
            nodecolours.append(red)
            nodesizes.append(othernodesize)
            if i == n_chains - 1 and j == 1:
                rotate.append(len(x))
                
                

def draw_arrow(xpos, ypos):
    xorig = int(xsize/2.)
    yorig = 50
    pygame.draw.line(screen, red, [xorig, yorig], [xpos,ypos], 5)
    
    
def print_info_text():
    edgeinfo1 = font.render("Smaller nodes - 100 entities following the node above", 1, black)
    edgeinfo2 = font.render("Larger node - An entity with many followers", 1, black)
    screen.blit(edgeinfo1, (50, 50))
    screen.blit(edgeinfo2, (50, 80))

            
def send_a_message(node):
    if node == 0:
        mx = []
        my = []
        for i in range(n_chains):
            mx.append(x[0])
            my.append(y[0])
        move = True
        while move:
            for i in range(n_chains):
                pygame.draw.rect(screen, green, [mx[i], my[i], 30, 20])
                mx[i] -= 10*sin((i+1)*0.523 + 1.57)
                my[i] -= 10*cos((i+1)*0.523 + 1.57)
                if (my[i] > ysize - 100):
                    move = False
            pygame.display.flip()
            show_main()
    else:
        xdist = x[node] - x[0]
        ydist = y[node] - y[0]
        angle = math.atan(float(ydist)/float(xdist))
        move = True
        xpos = x[node]
        ypos = y[node]
        while move:
            pygame.draw.rect(screen, green, [xpos, ypos, 30, 20])
            pygame.display.flip()
            show_main()
            if node < rotate[0] - 1:
                xpos -= 10*sin(angle + 1.57)
                ypos -= 10*cos(angle - 1.57)
            else:
                xpos -= 10*sin(angle - 1.57)
                ypos -= 10*cos(angle + 1.57)
                
            if (ypos > ysize - 100 - y[0]):
                move = False

def clicked_a_node(xypos):
    for i in range(n_nodes):
        if abs(xypos[0] - x[i]) < 20 and abs(xypos[1] - y[i]) < 20:
            text = font.render("I tweeted!",1, green)
            screen.blit(text, xypos)
            pygame.display.flip()
            time.sleep(0.5)
            send_a_message(i)
            
def promote_node(xypos):    
    for i in range(n_nodes):
        if abs(xypos[0] - x[i]) < 20 and abs(xypos[1] - y[i]) < 20:
            return i       
    return -1

def text_promote(i, pos):
    text = font.render("Click me!", 1, black)
    screen.blit(text,pos)  
    pygame.display.flip()  
    
def on_node(xypos):
    for i in range(n_nodes):
        if abs(xypos[0] - x[i]) < 20 and abs(xypos[1] - y[i]) < 20:
            return True;
    return False;
    
def show_main():
    screen.fill(white)
    for i in range(n_nodes):
        draw_arrow(x[n_nodes - (i+1)], y[n_nodes - (i+1)])
        pygame.draw.circle(screen, nodecolours[n_nodes - (i+1)], [x[n_nodes - (i+1)], y[n_nodes - (i+1)]], nodesizes[n_nodes - (i+1)])
    # draw the head node
    pygame.draw.circle(screen, darkBlue, [x[0], y[0]], 35)
    # call main functions during loop
    print_info_text()

def main_loop():
    done = False
    while done == False:
        for event in pygame.event.get():
            # if user clicks the exit icon, exit!
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                while on_node(mouse_pos):
                    ni = promote_node(mouse_pos)
                    text_promote(ni, mouse_pos)
                    time.sleep(0.5)
                    break
            elif event.type == pygame.MOUSEBUTTONUP:
               clicked_a_node(mouse_pos)
            
        show_main()
        clock.tick(20)
        pygame.display.flip()
    
    pygame.quit()
    
def main():

    set_node_positions()
    main_loop()
    
if __name__ == "__main__":
    main()
    
    
    