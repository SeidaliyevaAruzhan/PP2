import pygame
import sys


def main():
    pygame.init()
    
    size=w, h=800, 800
    screen = pygame.display.set_mode(size)
    clock=pygame.time.Clock()
    run=True

    backround=(0,0,0)
    blue=(0,0,255)
    red=(255,0,0)
    green=(0,255,0)
    white=(255,255,255)

    points=[]
    colours=[blue, red, green, white]


    
    pressed=pygame.key.get_pressed()
    radius=15
    screen.fill(backround)
    color=backround
    start_pos=None
    mid_pos=None
    rect=False
    circle=False
    tri=False
    trir=False
    pen=True
   
    


    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT :
                run = False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_ESCAPE:
                    run=False
            pygame.draw.rect(screen, (56,56,56), pygame.Rect(0,0,w,h*0.1))
            pygame.draw.rect(screen, (70,70,70), pygame.Rect(w*0.9,0,w*0.1,h))  

            i=h-0.7*h
            for col in colours:
                pygame.draw.rect(screen, col, pygame.Rect(0.9*w+10,i,40,25))
                i+=30
            
            


            if rect:
                pygame.draw.rect(screen, (80,80,80), pygame.Rect(10,10,50,50))
            if not rect:
                pygame.draw.rect(screen, (118,102,102), pygame.Rect(10,10,50,50))

            if circle:
                pygame.draw.circle(screen, (80,80,80), (100,35), 25)
            if not circle:
                pygame.draw.circle(screen, (118,102,102), (100,35), 25)

            if tri:
                pygame.draw.polygon(screen, (80,80,80), [(140,10),(190,10),(165,60)])
            if not tri:
                pygame.draw.polygon(screen, (118,102,102), [(140,10),(190,10),(165,60)])

            

            coor=pygame.mouse.get_pos()
            if coor[0]>0.9*w+10 and coor[1]>h-0.7*h and coor[0]<=0.9*w+50 and coor[1]<=h-0.7*h+25:
                if pygame.mouse.get_pressed()[0]:
                    color=blue
                    pen=True
                    rect=False
                    circle=False
                    tri=False

            if coor[0]>0.9*w+10 and coor[1]>h-0.7*h+30  and coor[0]<=0.9*w+50 and coor[1]<=h-0.7*h+55:
                if pygame.mouse.get_pressed()[0]:
                    color=red
                    rect=False
                    circle=False
                    pen=True
                    tri=False

            if coor[0]>0.9*w+10 and coor[1]>h-0.7*h+60  and coor[0]<=0.9*w+50 and coor[1]<=h-0.7*h+85:
                if pygame.mouse.get_pressed()[0]:
                    color=green
                    pen=True
                    rect=False
                    circle=False
                    tri=False
                    trir=False

            if coor[0]>0.9*w+10 and coor[1]>h-0.7*h+90 and coor[0]<=0.9*w+50 and coor[1]<=h-0.7*h+115:
                if pygame.mouse.get_pressed()[0]:
                    color=backround
                    pen=True
                    rect=False
                    circle=False
                    tri=False
                    trir=False
            
            
            if coor[0]>10 and coor[1]>10 and coor[0]<=60 and coor[1]<=60:
                if pygame.mouse.get_pressed()[0]:
                    rect=not rect
                    circle=False
                    pen=False
                    tri=False
                    trir=False
            if coor[0]>75 and coor[1]>10 and coor[0]<=125 and coor[1]<=60:
                if pygame.mouse.get_pressed()[0]:
                    circle=not circle
                    rect=False
                    pen=False
                    tri=False
                    trir=False
            if coor[0]>140 and coor[1]>10 and coor[0]<=190 and coor[1]<=60:
                if pygame.mouse.get_pressed()[0]:
                    circle=False
                    rect=False
                    pen=False
                    tri=not tri
                    trir=False
            if coor[0]>200 and coor[1]>10 and coor[0]<=250 and coor[1]<=60:
                if pygame.mouse.get_pressed()[0]:
                    circle=False
                    rect=False
                    pen=False
                    tri=False
                    trir=not trir
            


            if event.type == pygame.MOUSEBUTTONDOWN and rect and coor[1]>h*0.1 and coor[0]<w*0.9-10:
                    if start_pos is None: 
                        start_pos = event.pos 
                    else:
                      
                        end_pos = event.pos
                        width = end_pos[0] - start_pos[0]
                        height = end_pos[1] - start_pos[1]
                        
                        
                        pygame.draw.rect(screen, color, (start_pos, (width,height)))
        
                        
                        start_pos = None
            
            if event.type == pygame.MOUSEBUTTONDOWN and circle and coor[1]>h*0.1 and coor[0]<w*0.9-10:
                    if start_pos is None:  
                        start_pos = event.pos 
                    else:
                       
                        end_pos = event.pos
                        width = end_pos[0] - start_pos[0]
                        height = end_pos[1] - start_pos[1]
                        
                        
                        pygame.draw.circle(screen, color, (start_pos[0]+width/2, start_pos[1]+height/2), min(width,height)/2)
        
                        
                        start_pos = None
            
            if event.type == pygame.MOUSEBUTTONDOWN and tri and coor[1]>h*0.1 and coor[0]<w*0.9-10:
                    if start_pos is None  :  
                        start_pos = event.pos 
                    elif mid_pos is None:
                        mid_pos = event.pos
                    else:
                       
                        
                        end_pos=event.pos
                        

                        pygame.draw.polygon(screen, color, [(start_pos[0],start_pos[1]),( mid_pos[0],mid_pos[1]), (end_pos[0],end_pos[1])])
                        
                        start_pos = None
                        mid_pos=None

            if event.type == pygame.MOUSEBUTTONDOWN and trir and coor[1]>h*0.1 and coor[0]<w*0.9-10:
                    if start_pos is None:  
                        start_pos = event.pos 
                    else:
                       
                        end_pos = event.pos
                        width = end_pos[0] - start_pos[0]
                        height = end_pos[1] - start_pos[1]
                        
                        
                        pygame.draw.circle(screen, color, (start_pos[0]+width/2, start_pos[1]+height/2), min(width,height)/2)
        
                        
                        start_pos = None
            
                
            if event.type == pygame.MOUSEMOTION:
               
                position = event.pos
                points = points + [position]
                points = points[-2:]
                if pygame.mouse.get_pressed()[0] and coor[1]>h*0.1 and coor[0]<w*0.9-10 and pen:       
                    line(screen, 0, points[0], points[1], radius, color)

            if event.type==pygame.KEYDOWN and (event.key==pygame.K_RIGHT or event.key==pygame.K_LEFT):
                pressed=pygame.key.get_pressed()
                if pressed[pygame.K_RIGHT] and radius<=50:
                    radius=min(50,radius+1)
                if pressed[pygame.K_LEFT] and radius>0:
                    radius=max(1,radius-1)
            

            




        
        pygame.display.flip()

        clock.tick(60)


def line(screen, index, start, end, radius, colors ):
    dx=start[0]-end[0]
    dy=start[1]-end[1]
    iteration=max(abs(dx), abs(dy))
    
    for i in range(iteration):
        progress = 1.0 * i / iteration
        aprogress = 1 - progress
        x = int(aprogress * start[0] + progress * end[0])
        y = int(aprogress * start[1] + progress * end[1])
        pygame.draw.circle(screen, colors, (x, y), radius)


    
    
    

    
main()