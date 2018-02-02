import pygame
 
def main():
    
    pygame.init()
    pygame.display.set_mode((800,600))
    pygame.display.set_caption("AutonTool")
    pygame.display.update()
    
    finished = False
    
    while not finished:
        for event in pygame.event.get():
            print(event)
            if event.type == pygame.QUIT:
                finished = True
    
    pygame.quit()
    quit()
    
if __name__=="__main__":
    main()