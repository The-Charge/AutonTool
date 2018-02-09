import pygame
import math

SCREEN_X = 421
SCREEN_Y = 600
#Start represents front of robot 
STARTING_Y = 435
PIXELS_PER_FOOT = 13.75
DEGREES_PER_RADIAN = 57.2958
YELLOW = (255, 255, 0)
GREEN =(0 ,204 ,0)
BTN_LL = pygame.Rect((0, 479, 105, 50))
BTN_LR = pygame.Rect((105, 479, 105, 50))
BTN_RL = pygame.Rect((210, 479, 105, 50))
BTN_RR = pygame.Rect((315, 479, 105, 50))
BTN_EXPORT = pygame.Rect((0, 529, 105, 50))

def main():
    currentPath = "LL"
    buttonSizes = [BTN_LL, BTN_LR, BTN_RL, BTN_RR, BTN_EXPORT]
    paths = {"LL":[], "LR":[], "RL":[], "RR":[]}
    
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
    pygame.display.set_caption("AutonTool: LL")
    pygame.display.update()
    background = pygame.image.load("Field.png")
    backgroundRect = background.get_rect()
    
    finished = False
    
    while not finished:
        #screen.fill((255, 255, 255))
        screen.blit(background, backgroundRect)
        
        pygame.draw.rect(screen, GREEN, BTN_LL, 0)
        pygame.draw.rect(screen, YELLOW, BTN_LR, 0) 
        pygame.draw.rect(screen, GREEN, BTN_RL, 0) 
        pygame.draw.rect(screen, YELLOW, BTN_RR, 0) 
        pygame.draw.rect(screen, YELLOW, BTN_EXPORT, 0)
        
        for point in paths[currentPath]:
            pygame.draw.circle(screen, YELLOW, point, 2, 0)
        
        for x in range(len(paths[currentPath]) - 1):
            pygame.draw.line(screen, YELLOW, paths[currentPath][x], paths[currentPath][x + 1], 1)
        
        
        pygame.display.flip()
 
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                finished = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if event.pos[1] < 479:
                    print(event.pos)
                    if len(paths[currentPath]) == 0:
                        start_x = event.pos[0]
                        paths[currentPath].append((start_x, STARTING_Y))
                    elif len(paths[currentPath]) == 1:
                        paths[currentPath].append((start_x, event.pos[1]))
                    else:
                        if abs(calcAngle(paths[currentPath][-1], event.pos)) > 5:
                            paths[currentPath].append(event.pos)
                        else:
                            paths[currentPath].append((paths[currentPath][-1][0], event.pos[1]))
                if event.pos[1] > 479:
                    for x in range(len(buttonSizes)):
                        if buttonSizes[x].collidepoint(event.pos) == 1:
                            indexClicked = x
                    if indexClicked == 0:
                        currentPath = "LL"
                    elif indexClicked == 1:
                        currentPath = "LR"
                    elif indexClicked == 2:
                        currentPath = "RL"
                    elif indexClicked == 3:
                        currentPath = "RR"
                    elif indexClicked == 4:
                        outputLL = ""
                        outputLR = ""
                        outputRL = ""
                        outputRR = ""
                        for x in range(len(paths["LL"]) - 1):
                            p1 = paths["LL"][x]
                            p2 = paths["LL"][x + 1]
                            
                            angle = calcAngle(p1, p2)
                            outputLL += str(round(angle, 2)) + "deg"
                            
                            distance = calcDist(p2, p1) / PIXELS_PER_FOOT
                            outputLL += str(round(distance, 2)) + "ft"
                            
                        for x in range(len(paths["LR"]) - 1):
                            pass
                        for x in range(len(paths["RL"]) - 1):
                            pass
                        for x in range(len(paths["RR"]) - 1):
                            pass
                        print("LL: " + outputLL)
                   
                    pygame.display.set_caption("AutonTool: " + currentPath)
            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                if len(paths[currentPath]) > 0:
                    paths[currentPath].pop(-1)
                
                
    
    pygame.quit()
    quit()

#Returns the distance between two pygame positions
def calcDist(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

#Returns absolute angle from -180 to 180 between two pygame positions, with zero being straight forward
def calcAngle(p1, p2):
    point1 = (p1[0], SCREEN_Y - p1[1])
    point2 = (p2[0], SCREEN_Y - p2[1])
    delta_x = point2[0] - point1[0]
    delta_y = point2[1] - point1[1]
    
    if delta_x == 0 and delta_y > 0:
        theta_degrees = 90
    elif delta_x == 0 and delta_y < 0:
        theta_degrees = -90
    else:
        theta_radians = math.atan2(delta_y, delta_x)
        theta_degrees = theta_radians * DEGREES_PER_RADIAN
        
    theta_degrees -= 90
    if theta_degrees < -180:
        theta_degrees += 360
    
    if theta_degrees != 180 and theta_degrees != 0:
        theta_degrees *= -1
        
    return theta_degrees
    
if __name__=="__main__":
    main()