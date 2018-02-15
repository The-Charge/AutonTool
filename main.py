import pygame
import math

# Screen positions
SCREEN_X = 421
SCREEN_Y = 600

# Center of robot at start
STARTING_Y = 435

# Conversion factors
PIXELS_PER_FOOT = 13.75

# Colors 
YELLOW = (255, 255, 0)
GREEN = (0 ,204 ,0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Button positions
BTN_LL = pygame.Rect((0, 479, 105, 50))
BTN_LR = pygame.Rect((105, 479, 105, 50))
BTN_RL = pygame.Rect((210, 479, 105, 50))
BTN_RR = pygame.Rect((315, 479, 105, 50))
BTN_EXPORT = pygame.Rect((0, 529, 105, 50))
BTN_SWITCH = pygame.Rect((105, 529, 105, 50))
BTN_SCALE = pygame.Rect((210, 529, 105, 50))

# Robot dimensions
ROBOT_DIMS_INCHES = [38.5, 33.5]
ROBOT_DIMS_FEET = [dim / 12 for dim in ROBOT_DIMS_INCHES]
ROBOT_DIAG_FEET = math.sqrt(ROBOT_DIMS_FEET[0] ** 2 + ROBOT_DIMS_FEET[1] ** 2) / 2

def drawRobot(screen, point, angle, color):
    baseAngle = 48.972495940751 + angle
    baseAngle -= 90
    angles = [baseAngle, baseAngle + 82.055008118498, baseAngle + 180, baseAngle + 262.0550081185]
    rads = [math.radians(angle) for angle in angles]
    x_points = [math.cos(rad) * ROBOT_DIAG_FEET * PIXELS_PER_FOOT + point[0] for rad in rads]
    y_points = [math.sin(rad) * ROBOT_DIAG_FEET * PIXELS_PER_FOOT + point[1] for rad in rads]
    #print(point)
    points = []
    for i in range(len(x_points)):
        points.append([x_points[i], y_points[i]])
    pygame.draw.polygon(screen, color, points, 1)

def drawPath(screen, path):
    for point in path:
        pygame.draw.circle(screen, YELLOW, point, 2, 0)
    
    for x in range(len(path) - 1):
        last_point = path[x]
        next_point = path[x + 1]
        angle = calcAngle(last_point, next_point)
        drawRobot(screen, last_point, angle, BLUE)
        drawRobot(screen, next_point, angle, RED)
        pygame.draw.line(screen, YELLOW, last_point, next_point, 1)
    if len(path) > 0:
        drawRobot(screen, path[0], 0, BLUE)

#Takes in a list of coordinates and returns a string of distances and angles
def outputPath(paths):
    outputList = []
    for x in range(len(paths) - 1):
        
        p1 = paths[x]
        p2 = paths[x + 1]
        
        angle = calcAngle(p1, p2)
        if angle != 0:
            outputList.append((str(round(angle, 2)), "deg"))
        
        distance = calcDist(p2, p1) / PIXELS_PER_FOOT
        outputList.append((str(round(distance, 2)), "ft"))
        
    return outputList

def main():
    currentPath = "LL"
    buttonSizes = [BTN_LL, BTN_LR, BTN_RL, BTN_RR, BTN_EXPORT, BTN_SWITCH, BTN_SCALE]
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
        pygame.draw.rect(screen, GREEN, BTN_SWITCH, 0)
        pygame.draw.rect(screen, YELLOW, BTN_SCALE, 0)
        
        drawPath(screen, paths[currentPath])
        
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
                if event.pos[1] >= 479:
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
                        outputListLL = outputPath(paths["LL"])
                        outputListLR = outputPath(paths["LR"])
                        outputListRL = outputPath(paths["RL"])
                        outputListRR = outputPath(paths["RR"])
                        outputLL = ""
                        outputLR = ""
                        outputRL = ""
                        outputRR = ""
                        
                        for output in outputListLL:
                            outputLL += output[0] + output[1]
                        for output in outputListLR:
                            outputLR += output[0] + output[1]
                        for output in outputListRL:
                            outputRL += output[0] + output[1]
                        for output in outputListRR:
                            outputRR += output[0] + output[1]
                            
                        print("LL: " + outputLL)
                        print("LR: " + outputLR)
                        print("RL: " + outputRL)
                        print("RR: " + outputRR)
                    elif indexClicked == 5:
                        pass
                    elif indexClicked == 6:
                        pass
                    pygame.display.set_caption("AutonTool: " + currentPath)
            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                if len(paths[currentPath]) > 0:
                    paths[currentPath].pop(-1)
                
                
    
    pygame.quit()
    quit()

#Returns the distance between two pygame positions
def calcDist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

#Returns absolute angle from -180 to 180 between two pygame positions, with zero being straight forward
def calcAngle(p1, p2):
    point1 = (p1[0], SCREEN_Y - p1[1])
    point2 = (p2[0], SCREEN_Y - p2[1])
    delta_x = point2[0] - point1[0]
    delta_y = point2[1] - point1[1]
    
    if delta_x == 0 and delta_y > 0:
        theta = 90
    elif delta_x == 0 and delta_y < 0:
        theta = -90
    else:
        theta = math.degrees(math.atan2(delta_y, delta_x))
        
    theta -= 90
    if theta < -180:
        theta += 360
    
    if theta != 180 and theta != 0:
        theta *= -1
        
    return theta
    
if __name__=="__main__":
    main()
