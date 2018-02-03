import pygame
import math

def main():
    PIXELS_PER_FOOT = 13.75
    DEGREES_PER_RADIAN = 57.2958
    YELLOW = (255, 255, 0)
    GREEN =(0 ,204 ,0)
    BTN_LL = pygame.Rect((0, 479, 105, 50))
    BTN_LR = pygame.Rect((105, 479, 105, 50))
    BTN_RL = pygame.Rect((210, 479, 105, 50))
    BTN_RR = pygame.Rect((315, 479, 105, 50))
    BTN_EXPORT = pygame.Rect((0, 529, 105, 50))
    
    currentPath = "LL"
    buttonSizes = [BTN_LL, BTN_LR, BTN_RL, BTN_RR, BTN_EXPORT]
    paths = {"LL":[], "LR":[], "RL":[], "RR":[]}
    
    pygame.init()
    screen = pygame.display.set_mode((421, 600))
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
            print(event)
            if event.type == pygame.QUIT:
                finished = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if event.pos[1] < 479:
                    paths[currentPath].append(event.pos)
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
                            angle = math.atan((p2[1] - p1[1]) / (p2[0] - p1[0])) * DEGREES_PER_RADIAN
                            outputLL += str(round(angle, 2)) + "deg"
                            distance = calcDist(p2, p1) / PIXELS_PER_FOOT
                            outputLL += str(round(distance, 2)) + "ft"
                        for x in range(len(paths["LR"]) - 1):
                            pass
                        for x in range(len(paths["RL"]) - 1):
                            pass
                        for x in range(len(paths["RR"]) - 1):
                            pass
                    print(outputLL)
                    pygame.display.set_caption("AutonTool: " + currentPath)
            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                if len(paths[currentPath]) > 0:
                    paths[currentPath].pop(-1)
                
                
    
    pygame.quit()
    quit()

def calcDist(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)
    
if __name__=="__main__":
    main()