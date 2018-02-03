import pygame
 
def main():
    PIXELS_PER_FOOT = 13.75
    YELLOW = (255, 255, 0)
    GREEN =(0 ,204 ,0)
    BTN_LL = pygame.Rect((0, 479, 105, 50))
    BTN_LR = pygame.Rect((105, 479, 105, 50))
    BTN_RL = pygame.Rect((210, 479, 105, 50))
    BTN_RR = pygame.Rect((315, 479, 105, 50))
    
    
    points = []
    buttonSizes = [BTN_LL, BTN_LR, BTN_RL, BTN_RR]
    paths = {"LL":[], "LR":[], "RL":[], "RR":[]}
    
    pygame.init()
    screen = pygame.display.set_mode((421, 600))
    pygame.display.set_caption("AutonTool")
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
        
        for point in points:
            pygame.draw.circle(screen, YELLOW, point, 2, 0)
        
        for x in range(len(points) - 1):
            pygame.draw.line(screen, YELLOW, points[x], points[x + 1], 1)
        
        
        pygame.display.flip()
 
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                finished = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if event.pos[1] < 479:
                    points.append(event.pos)
                if event.pos[1] > 479:
                    for x in range(len(buttonSizes)):
                        if buttonSizes[x].collidepoint(event.pos) == 1:
                            indexClicked = x
                    if indexClicked == 0:
                        
                    elif indexClicked == 1:
                    elif indexClicked == 2:
                    elif indexClicked == 3:
            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                points.pop(-1)
                
                
    
    pygame.quit()
    quit()
    
if __name__=="__main__":
    main()