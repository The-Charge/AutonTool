import pygame
 
def main():
    PIXELS_PER_FOOT = 27.5
    YELLOW = (255, 255, 0)
    
    points = []
    
    pygame.init()
    screen = pygame.display.set_mode((871,957))
    pygame.display.set_caption("AutonTool")
    pygame.display.update()
    background = pygame.image.load("field.png")
    backgroundRect = background.get_rect()
    
    finished = False
    
    while not finished:
        #screen.fill((255, 255, 255))
        screen.blit(background, backgroundRect)
        for point in points:
            pygame.draw.circle(screen, YELLOW, point, 2, 0)
            
        pygame.display.flip()
 
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                finished = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                points.append(event.pos)
                
                
    
    pygame.quit()
    quit()
    
if __name__=="__main__":
    main()