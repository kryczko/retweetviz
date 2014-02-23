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

node_p_chain = int(n_nodes / 5.)
# radius between nodes
r = (ysize - 150)/ node_p_chain

def set_node_positions():
    # the 'king' node
    xorig = int(xsize/2.)
    yorig = 50
    x.append(int(xsize/2.))
    y.append(int(yorig))
    nodecolours.append(darkBlue)
    nodesizes.append(headnodesize)

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
    edgeinfo1 = font.render("Smaller nodes - groups of 50 entities following the node above", 1, black)
    edgeinfo2 = font.render("Larger node - An entity with many followers", 1, black)
    screen.blit(edgeinfo1, (50, 50))
    screen.blit(edgeinfo2, (50, 80))


def has_message_hit_node(node,mx, my):
    for i in range(n_nodes):
        if abs(mx - x[i]) < 20 and abs(my - y[i]) < 20 and i != node:
           retweet_message = font.render("Entities retweeting!",1,black)
           screen.blit(retweet_message,(mx-50,my-50))
           time.sleep(0.1)
           return i
    return -1

end_pos_nodes = []
for i in range(1,n_nodes+1):
    end_pos_nodes.append(50)
def show_rates(node, t, layer):
    n_retweets = 0
    entities_per_node = 100
    rate_text = font.render("Rate of retweeting:",1,black)
    screen.blit(rate_text,(300,ysize - 50))
    if node == 0 and layer == 1:
       start_ypos = ysize - 50
       start_xpos = 500
       end_x_pos = trans_prob * n_chains * entities_per_node * exp(-t/0.05) * 20
       n_retweets = trans_prob * n_chains * entities_per_node * exp(-t/0.05)
       pygame.draw.rect(screen, black, [start_xpos, start_ypos, end_x_pos, 30], 5)
    elif node == 0 and layer != 1:
        entities_per_node = trans_prob**layer * entities_per_node
        start_ypos = ysize - 50
        start_xpos = 500
        end_x_pos = trans_prob * n_chains * entities_per_node * exp(-t/0.05) * 20
        n_retweets = trans_prob * n_chains * entities_per_node * exp(-t/0.05)
        pygame.draw.rect(screen, black, [start_xpos, start_ypos, end_x_pos, 30], 5)
    elif node != 0 and layer == 1:
        start_ypos = ysize - 50
        start_xpos = 500
        end_x_pos = trans_prob * entities_per_node * exp(-t/0.05) * 20
        n_retweets = trans_prob * entities_per_node * exp(-t/0.05)
        pygame.draw.rect(screen, black, [start_xpos, start_ypos, end_x_pos, 30], 5)
    elif node != 0 and layer != 1:
        entities_per_node = trans_prob**layer * entities_per_node
        start_ypos = ysize - 50
        start_xpos = 500
        end_x_pos = trans_prob * entities_per_node * exp(-t/0.05) * 20
        n_retweets = trans_prob * entities_per_node * exp(-t/0.05)
        pygame.draw.rect(screen, black, [start_xpos, start_ypos, end_x_pos, 30], 5)
    return n_retweets  
        
def which_layer(dist):
    layer = dist / float(r)
    return round(layer)        
     
def send_a_message(node):
    entities = []
    total_retweets = 0
    if node == 0:
        mx = []
        my = []
        for i in range(n_chains):
            mx.append(x[0])
            my.append(y[0])
        move = True
        while move:
            node_count = 0
            for i in range(n_chains):
                pygame.draw.rect(screen, green, [mx[i], my[i], 30, 20])
                mx[i] -= 2*sin((i+1)*0.523 + 1.57)
                my[i] -= 2*cos((i+1)*0.523 + 1.57)
                if (my[i] > ysize - 100):
                    move = False
                if has_message_hit_node(node,mx[i], my[i]) != -1:
                    node_count += 1
                    if node_count == n_chains:
                        t1 = time.time()
                        minutes = (t1 - t0) % 60
                        t = minutes / 60.0
                        total_retweets += show_rates(node, t, which_layer(sqrt((mx[i] - x[0])**2+(my[i] - y[0])**2)))
                else:
                    t0 = time.time()
            
            n_retweets = font.render("Total retweets: %i" % total_retweets ,1,black)
            screen.blit(n_retweets,(50,ysize - 50))
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
            if node < rotate[0] - 1:
                xpos -= 2*sin(angle + 1.57)
                ypos -= 2*cos(angle - 1.57)
            else:
                xpos -= sin(angle - 1.57)
                ypos -= cos(angle + 1.57)
            if has_message_hit_node(node,xpos,ypos) != -1:
                t1 = time.time()
                minutes = (t1 - t0) % 60
                t = minutes / 60.0
                total_retweets += show_rates(node, t, which_layer(sqrt((xpos - x[0])**2+(ypos - y[0])**2)))
            else:
                t0 = time.time()  
            if (ypos > abs(ysize - 50 - y[0]) or xpos > abs(xsize - 20)):
                move = False
            n_retweets = font.render("Total retweets: %i" % total_retweets ,1,black)
            screen.blit(n_retweets,(50,ysize - 50))
            pygame.display.flip()
            show_main()     

def clicked_a_node(xypos):
    for i in range(n_nodes):
        if abs(xypos[0] - x[i]) < 20 and abs(xypos[1] - y[i]) < 20:
            text = font.render("I tweeted!",1, green)
            screen.blit(text, (xypos[0], xypos[1]-30))
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
    
    
    