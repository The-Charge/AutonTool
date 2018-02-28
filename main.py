import pygame
import math
import sys

# Screen positions
SCREEN_X = 421
SCREEN_Y = 559

# Center of robot at start
STARTING_Y = 447

#Initial invalid zones
LEFT_BOUND = 79
RIGHT_BOUND = 342
CONTROL_BORDER = 479
EXCHANGE_LEFT = 117
EXCHANGE_RIGHT = 221

#Other robot instructions
FORWARD = 0
REVERSE = 1
SWITCH_POSITION = 2
SCALE_POSITION = 3
OPEN_CLAW = 4
DRIVE_TO_CURRENT_SWITCH = 5
DRIVE_TO_CURRENT_SCALE = 6
STARTING = 7
#timeouts will be -(value)

#Field barriers
LEFT_WALL = 22
RIGHT_WALL = 401
TOP_BOUND = 48
LOWER_BOUND = 468

#Switch and Scales
SWITCH = pygame.Rect((121, 239, 180, 64))
SWITCH_LEFT = pygame.Rect((126, 241, 43, 57))
SWITCH_RIGHT = pygame.Rect((253, 241, 43, 57))
SCALE = pygame.Rect((105, 59, 212, 56))
SCALE_LEFT = pygame.Rect((105, 59, 42, 56))
SCALE_RIGHT = pygame.Rect((275, 59, 42, 56))

# Conversion factors
PIXELS_PER_FOOT = 13.75

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (46, 130, 23)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Button positions
BTN_LL = pygame.Rect((0, 479, 50, 40))
BTN_LR = pygame.Rect((50, 479, 50, 40))
BTN_RL = pygame.Rect((100, 479, 50, 40))
BTN_RR = pygame.Rect((150, 479, 50, 40))
BTN_CLONE = pygame.Rect((200, 479, 68, 40))
BTN_ALL = pygame.Rect((268, 479, 67, 40))
BTN_EXPORT = pygame.Rect((335, 479, 86, 40))
BTN_DTC = pygame.Rect((0, 519, 57, 40))
BTN_SWITCH = pygame.Rect((57, 519, 77, 40))
BTN_SCALE = pygame.Rect((134, 519, 67, 40))
BTN_WAIT = pygame.Rect((201, 519, 67, 40))
BTN_DROP = pygame.Rect((268, 519, 67, 40))
BTN_REVERSE = pygame.Rect((335, 519, 86, 40))

# Robot dimensions
ROBOT_DIMS_INCHES = [38.5, 33.5]
ROBOT_DIMS_FEET = [dim / 12 for dim in ROBOT_DIMS_INCHES]
ROBOT_PIXELS_HALF = [int(dim * PIXELS_PER_FOOT / 2) for dim in ROBOT_DIMS_FEET]
SIDE = int(ROBOT_DIMS_FEET[0] * PIXELS_PER_FOOT / 2)
FRONT = int(ROBOT_DIMS_FEET[1] * PIXELS_PER_FOOT / 2)
ROBOT_DIAG_FEET = math.sqrt(ROBOT_DIMS_FEET[0] ** 2 + ROBOT_DIMS_FEET[1] ** 2) / 2

#Draws buttons
def drawControls(screen, currentPath, paths, variables, cloning, waitInput, timeList):
    font = pygame.font.SysFont('arial', 22, True)
    numDisplay = ""
    if waitInput:
        numDisplay = "Enter a time: "
        for digit in timeList:
            numDisplay += digit
        
    text0 = font.render(' LL', True, BLACK)
    text1 = font.render(' LR', True, BLACK)
    text2 = font.render(' RL', True, BLACK)
    text3 = font.render(' RR', True, BLACK)
    text4 = font.render('CLONE', True, BLACK)
    text5 = font.render('TO ALL', True, BLACK)
    text6 = font.render(' EXPORT', True, BLACK)
    text7 = font.render('D.T.C.', True, BLACK)
    text8 = font.render('SWITCH', True, BLACK)
    text9 = font.render('SCALE', True, BLACK)
    text10 = font.render('  WAIT', True, BLACK)
    text11 = font.render(' DROP', True, BLACK)
    text12 = font.render('REVERSE', True, BLACK)
    textNumber = font.render(numDisplay, True, BLACK)
    
    pygame.draw.rect(screen, GREEN, BTN_LL, 0)
    pygame.draw.rect(screen, YELLOW, BTN_LR, 0) 
    pygame.draw.rect(screen, GREEN, BTN_RL, 0) 
    pygame.draw.rect(screen, YELLOW, BTN_RR, 0) 
    pygame.draw.rect(screen, YELLOW, BTN_CLONE, 0) 
    pygame.draw.rect(screen, GREEN, BTN_ALL, 0) 
    pygame.draw.rect(screen, YELLOW, BTN_EXPORT, 0)
    pygame.draw.rect(screen, YELLOW, BTN_DTC, 0)
    pygame.draw.rect(screen, GREEN, BTN_SWITCH, 0)
    pygame.draw.rect(screen, YELLOW, BTN_SCALE, 0)
    pygame.draw.rect(screen, GREEN, BTN_WAIT, 0)
    pygame.draw.rect(screen, YELLOW, BTN_DROP, 0)
    pygame.draw.rect(screen, GREEN, BTN_REVERSE, 0)
    pygame.draw.line(screen, GREEN, BTN_RR.topright, BTN_RR.bottomright, 2)
    
    if currentPath == "LL":
        pygame.draw.rect(screen, BLACK, BTN_LL, 2)
        pygame.draw.rect(screen, WHITE, SWITCH_LEFT, 3)
        pygame.draw.rect(screen, WHITE, SCALE_LEFT, 3)
    elif currentPath == "LR":
        pygame.draw.rect(screen, BLACK, BTN_LR, 2)
        pygame.draw.rect(screen, WHITE, SWITCH_LEFT, 3)
        pygame.draw.rect(screen, WHITE, SCALE_RIGHT, 3)
    elif currentPath == "RL":
        pygame.draw.rect(screen, BLACK, BTN_RL, 2)
        pygame.draw.rect(screen, WHITE, SWITCH_RIGHT, 3)
        pygame.draw.rect(screen, WHITE, SCALE_LEFT, 3)
    elif currentPath == "RR":
        pygame.draw.rect(screen, BLACK, BTN_RR, 2)
        pygame.draw.rect(screen, WHITE, SWITCH_RIGHT, 3)
        pygame.draw.rect(screen, WHITE, SCALE_RIGHT, 3)
    
    if cloning:
        pygame.draw.rect(screen, BLACK, BTN_CLONE, 2)
    if waitInput:
        pygame.draw.rect(screen, BLACK, BTN_WAIT, 2)
    if paths["LL"] == paths["LR"] and paths["LL"] == paths["RL"] and paths["LL"] == paths["RR"] and paths["LL"] != []:
        pygame.draw.rect(screen, BLACK, BTN_ALL, 2)
    if variables[currentPath]["driveToCurrent"]:
        pygame.draw.rect(screen, BLACK, BTN_DTC, 2)
    if variables[currentPath]["elevatorPosition"] == SWITCH_POSITION:
        pygame.draw.rect(screen, BLACK, BTN_SWITCH, 2)
    if variables[currentPath]["elevatorPosition"] == SCALE_POSITION:
        pygame.draw.rect(screen, BLACK, BTN_SCALE, 2)
    if variables[currentPath]["driveToCurrent"]:
        pygame.draw.rect(screen, BLACK, BTN_DTC, 2)
    if variables[currentPath]["clawOpen"]:
        pygame.draw.rect(screen, BLACK, BTN_DROP, 2)
    if variables[currentPath]["reversed"]:
        pygame.draw.rect(screen, BLACK, BTN_REVERSE, 2)
    
    screen.blit(text0, BTN_LL.topleft)
    screen.blit(text1, BTN_LR.topleft)
    screen.blit(text2, BTN_RL.topleft)
    screen.blit(text3, BTN_RR.topleft)
    screen.blit(text4, BTN_CLONE.topleft)
    screen.blit(text5, BTN_ALL.topleft)
    screen.blit(text6, BTN_EXPORT.topleft)
    screen.blit(text7, BTN_DTC.topleft)
    screen.blit(text8, BTN_SWITCH.topleft)
    screen.blit(text9, BTN_SCALE.topleft)
    screen.blit(text10, BTN_WAIT.topleft)
    screen.blit(text11, BTN_DROP.topleft)
    screen.blit(text12, BTN_REVERSE.topleft)
    screen.blit(textNumber, (0, CONTROL_BORDER-35))

#Draws the robot at the given angle
def drawRobot(screen, point, angle, color):
    baseAngle = 48.972495940751 + angle
    baseAngle -= 90
    angles = [baseAngle, baseAngle + 82.055008118498, baseAngle + 180, baseAngle + 262.0550081185]
    rads = [math.radians(angle) for angle in angles]
    x_points = [math.cos(rad) * ROBOT_DIAG_FEET * PIXELS_PER_FOOT + point[0] for rad in rads]
    y_points = [math.sin(rad) * ROBOT_DIAG_FEET * PIXELS_PER_FOOT + point[1] for rad in rads]
    points = []
    for i in range(len(x_points)):
        points.append([x_points[i], y_points[i]])
    pygame.draw.polygon(screen, color, points, 1)
    pygame.draw.line(screen, BLACK, points[3], points[0], 2)

#Draws the robot's path and positions
def drawPath(screen, path):
    for point in path:
        pygame.draw.circle(screen, YELLOW, point[:2], 2, 0)
    
    for x in range(len(path) - 1):
        last_point = path[x]
        next_point = path[x + 1]
        if next_point[:2] != last_point[:2]:
            angle = calcAngle(last_point[:2], next_point[:2])
            if next_point[2] == REVERSE:
                if angle < 0:
                    angle += 180
                else:
                    angle -= 180
            drawRobot(screen, last_point[:2], angle, BLUE)
            drawRobot(screen, next_point[:2], angle, RED)
            pygame.draw.line(screen, YELLOW, last_point[:2], next_point[:2], 1)
    if len(path) > 0:
        drawRobot(screen, path[0][:2], 0, BLUE)

#Takes in a list of coordinates and instructions and prints auton commands
def outputPath(path):
    previousAngle = 0
    print("addSequential(new ShiftLow());")
    for x in range(len(path)):
        if len(path) > 0:
            if path[x][2] < 0:
                time = -1 * round(path[x][2], 2)
                print("addTimeOut(%s);" % time)
            if path[x][2] == DRIVE_TO_CURRENT_SWITCH:
                print("addSequential(new DriveToCurrent(.2, 5));")
            if path[x][2] == DRIVE_TO_CURRENT_SCALE:
                print("addSequential(new DriveToCurrent(.07, 1);")
            elif path[x][2] == OPEN_CLAW:
                print("addSequential(new RunCollectorReverse(0.05));")
        if x != len(path)-1:
            p1 = path[x]
            p2 = path[x + 1]
            angle = calcAngle(p1[:2], p2[:2])
            if p2[2] == REVERSE:
                if angle < 0:
                    angle += 180
                else:
                    angle -= 180
            if angle != 999 and angle != previousAngle and x != 0:
                print("addSequential(new TurnNDegreesAbsolutePID(%s));" % round(angle, 2))
            if angle != 999:
                previousAngle = angle
            distance = calcDist(p2[:2], p1[:2]) / PIXELS_PER_FOOT
            if p2[2] == REVERSE:
                distance = -1 * distance
            if path[x][2] == SWITCH_POSITION:
                print("addParallel(new ElevateToXPos(2));")
            elif path[x][2] == SCALE_POSITION:
                print("addParallel(new ElevateToXPos(5));")
            if distance != 0 and p2[2] == FORWARD or p2[2] == REVERSE:
                print("addSequential(new DriveXFeetMotionMagic(%s));" % round(distance, 2))

#Checks boundaries of starting position
def checkStart(xpos):
    if xpos < LEFT_BOUND:
        xpos = LEFT_BOUND
    if xpos > RIGHT_BOUND:
        xpos = RIGHT_BOUND
    if xpos > EXCHANGE_LEFT and xpos < EXCHANGE_LEFT + 52:
        xpos = EXCHANGE_LEFT
    if xpos < EXCHANGE_RIGHT and xpos >= EXCHANGE_RIGHT - 52:
        xpos = EXCHANGE_RIGHT
    return xpos

#Checks boundaries of first move
def checkFirstMove(point, path):
    if path[-1][0]+SIDE > SCALE.left and path[-1][0]-SIDE < SCALE.right:
        if path[-1][0]+SIDE > SWITCH.left and path[-1][0]-SIDE < SWITCH.right:
            if point[1]-FRONT < SWITCH.bottom:
                ypos = SWITCH.bottom+FRONT
            else:
                ypos = point[1]
        else:
            if point[1]-FRONT < SCALE.bottom:
                ypos = SCALE.bottom+FRONT
            else:
                ypos = point[1]
    else:
        if point[1]-FRONT < TOP_BOUND:
            ypos = TOP_BOUND+FRONT
        elif point[1]-FRONT > LOWER_BOUND:
            ypos = LOWER_BOUND-FRONT
        else:
            ypos = point[1]
    return ypos

#Not sure how aliasing works in python, so it uses a completely different list
def clone(path):
    newPath = []
    for point in path:
        newPath.append(point)
    return newPath
    
def main():
    currentPath = "LL"
    buttonSizes = [BTN_LL, BTN_LR, BTN_RL, BTN_RR, BTN_CLONE, BTN_ALL, BTN_EXPORT, BTN_DTC, BTN_SWITCH, BTN_SCALE, BTN_WAIT, BTN_DROP, BTN_REVERSE]
    paths = {"LL":[], "LR":[], "RL":[], "RR":[]}
    variables = {"LL":{"reversed":False, "driveToCurrent":False, "clawOpen":False, "waitInput":False, "elevatorPosition":0}, \
                 "LR":{"reversed":False, "driveToCurrent":False, "clawOpen":False, "waitInput":False, "elevatorPosition":0}, \
                 "RL":{"reversed":False, "driveToCurrent":False, "clawOpen":False, "waitInput":False, "elevatorPosition":0}, \
                 "RR":{"reversed":False, "driveToCurrent":False, "clawOpen":False, "waitInput":False, "elevatorPosition":0}}
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
    pygame.display.set_caption("AutonTool: LL")
    pygame.display.update()
    background = pygame.image.load("Field.png")
    backgroundRect = background.get_rect()
    timeList = []
    cloning = False
    waitInput = False
    moved = False
    finished = False
    
    while not finished:
        screen.blit(background, backgroundRect)
        drawControls(screen, currentPath, paths, variables, cloning, waitInput, timeList)
        drawPath(screen, paths[currentPath])
        pygame.display.flip()
        
        if len(paths[currentPath]) < 2:
            variables[currentPath]["reversed"] = False
        if len(paths[currentPath]) < 1:
            variables[currentPath]["driveToCurrent"] = False
            waitInput = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if event.pos[1] < CONTROL_BORDER and not waitInput:
                    for x in paths[currentPath]:
                        if x[2] == FORWARD:
                            moved = True
                    if len(paths[currentPath]) == 0:
                        start_x = event.pos[0]
                        start_x = checkStart(start_x)
                        paths[currentPath].append((start_x, STARTING_Y, STARTING))
                    elif not moved:
                        firstMove = checkFirstMove(event.pos, paths[currentPath])
                        paths[currentPath].append((start_x, firstMove, FORWARD))
                    else:
                        pos = [event.pos[0], event.pos[1]]
                        lastPoint = (paths[currentPath][-1][0], paths[currentPath][-1][1])
                        angle = calcAngle(paths[currentPath][-1], pos)
                        
                        if (angle > -135 and angle < -45) or (angle > 45 and angle < 135):
                            buffer = FRONT
                        else:
                            buffer = SIDE
                        
                        if angle != 999:
                            if angle < 5 and angle > -5:
                                pos[0] = lastPoint[0]
                                angle = 0
                            elif angle > 175 or angle < -175:
                                pos[0] = lastPoint[0]
                                angle = 180
                            elif angle > 85 and angle < 95:
                                pos[1] = lastPoint[1]
                                angle = 90
                            elif angle < -85 and angle > -95:
                                pos[1] = lastPoint[1]
                                angle = -90
                            
                        if pos[0]-buffer < LEFT_WALL:
                            pos[0] = LEFT_WALL+buffer
                        elif pos[0]+buffer > RIGHT_WALL:
                            pos[0] = RIGHT_WALL-buffer
                            
                        if pos[1]-buffer < TOP_BOUND:
                            pos[1] = TOP_BOUND+buffer
                        elif pos[1]+buffer > LOWER_BOUND:
                            pos[1] = LOWER_BOUND-buffer
                        
                        #MORE CORRECTION CODE HERE (if time)
                        
                        if variables[currentPath]["driveToCurrent"]:
                            if angle == 0:
                                if lastPoint[1]-FRONT > SWITCH.bottom:
                                    if lastPoint[0]+SIDE > SWITCH.left and lastPoint[0]-SIDE < SWITCH.right:
                                        pos[1] = SWITCH.bottom+FRONT
                                elif lastPoint[1]-FRONT > SCALE.bottom:
                                    if lastPoint[0]+SIDE > SCALE.left and lastPoint[0]-SIDE < SCALE.right:
                                        pos[1] = SCALE.bottom+FRONT
                                else:
                                    pos[1]= 0
                            elif angle == 90:
                                if lastPoint[1]+SIDE > SCALE.top and lastPoint[1]-SIDE < SCALE.bottom:
                                    if lastPoint[0]+FRONT < SCALE.left:
                                        pos[0] = SCALE.left-FRONT
                                if lastPoint[1]+SIDE > SWITCH.top and lastPoint[1]-SIDE < SWITCH.bottom:
                                    if lastPoint[0]+FRONT < SWITCH.left:
                                        pos[0] = SWITCH.left-FRONT
                            elif angle == 180 or angle == -180:
                                if lastPoint[1]+FRONT < SWITCH.top:
                                    if lastPoint[0]+SIDE > SWITCH.left and lastPoint[0]-SIDE < SWITCH.right:
                                        pos[1] = SWITCH.top-FRONT
                            elif angle == -90:
                                if lastPoint[1]+SIDE > SCALE.top and lastPoint[1]-SIDE < SCALE.bottom:
                                    if lastPoint[0]-FRONT > SCALE.right:
                                        pos[0] = SCALE.right+FRONT
                                if lastPoint[1]+SIDE > SWITCH.top and lastPoint[1]-SIDE < SWITCH.bottom:
                                    if lastPoint[0]-FRONT > SWITCH.bottom:
                                        pos[0] = SWITCH.right+FRONT
                            else:   #DTC for any angle
                                pass
                            if variables[currentPath]["elevatorPosition"] == SWITCH_POSITION:
                                paths[currentPath].append((pos[0], pos[1], DRIVE_TO_CURRENT_SWITCH))
                            else:
                                paths[currentPath].append((pos[0], pos[1], DRIVE_TO_CURRENT_SCALE))
                        elif variables[currentPath]["reversed"]:
                            if paths[currentPath][-1][2] != (pos[0], pos[1], REVERSE):
                                paths[currentPath].append((pos[0], pos[1], REVERSE))
                        else:
                            if paths[currentPath][-1][2] != (pos[0], pos[1], FORWARD):
                                paths[currentPath].append((pos[0], pos[1], FORWARD))
                        variables[currentPath]["driveToCurrent"] = False
                    print(paths[currentPath][-1])
                if event.pos[1] >= CONTROL_BORDER:
                    for x in range(len(buttonSizes)):
                        if buttonSizes[x].collidepoint(event.pos):
                            indexClicked = x
                    if indexClicked == 0 and not waitInput:
                        if not cloning:
                            currentPath = "LL"
                        else:
                            paths["LL"] = clone(paths[currentPath])
                            variables["LL"] = dict(variables[currentPath])
                            cloning = False
                            currentPath = "LL"
                    elif indexClicked == 1 and not waitInput:
                        if not cloning:
                            currentPath = "LR"
                        else:
                            paths["LR"] = clone(paths[currentPath])
                            variables["LR"] = dict(variables[currentPath])
                            cloning = False
                            currentPath = "LR"
                    elif indexClicked == 2 and not waitInput:
                        if not cloning:
                            currentPath = "RL"
                        else:
                            paths["RL"] = clone(paths[currentPath])
                            variables["RL"] = dict(variables[currentPath])
                            cloning = False
                            currentPath = "RL"
                    elif indexClicked == 3 and not waitInput:
                        if not cloning:
                            currentPath = "RR"
                        else:
                            paths["RR"] = clone(paths[currentPath])
                            variables["RR"] = dict(variables[currentPath])
                            cloning = False
                            currentPath = "RR"
                    elif indexClicked == 4 and not waitInput:
                        cloning = not cloning
                    elif indexClicked == 5 and not waitInput:
                        cloning = False
                        if currentPath != "LL":
                            paths["LL"] = clone(paths[currentPath])
                            variables["LL"] = dict(variables[currentPath])
                        if currentPath != "LR":
                            paths["LR"] = clone(paths[currentPath])
                            variables["LR"] = dict(variables[currentPath])
                        if currentPath != "RL":
                            paths["RL"] = clone(paths[currentPath])
                            variables["RL"] = dict(variables[currentPath])
                        if currentPath != "RR":
                            paths["RR"] = clone(paths[currentPath])
                            variables["RR"] = dict(variables[currentPath])
                    elif indexClicked == 6 and not waitInput:
                        print("\n----------------------------------------\n-----LL-----")
                        outputPath(paths["LL"])
                        print("\n-----LR-----")
                        outputPath(paths["LR"])
                        print("\n-----RL-----")
                        outputPath(paths["RL"])
                        print("\n-----RR-----")
                        outputPath(paths["RR"])
                    elif indexClicked == 7 and not waitInput and not cloning:
                        for x in paths[currentPath]:
                            if x[2] == FORWARD:
                                moved = True
                        if moved and variables[currentPath]["elevatorPosition"] != 0:
                            variables[currentPath]["driveToCurrent"] = not variables[currentPath]["driveToCurrent"]
                            variables[currentPath]["reversed"] = False
                    elif indexClicked == 8 and not waitInput and not cloning:
                        if len(paths[currentPath]) > 0:
                            if variables[currentPath]["elevatorPosition"] != SWITCH_POSITION:
                                paths[currentPath].append((paths[currentPath][-1][0], paths[currentPath][-1][1], SWITCH_POSITION))
                                variables[currentPath]["elevatorPosition"] = SWITCH_POSITION
                                print(paths[currentPath][-1])
                    elif indexClicked == 9 and not waitInput and not cloning:
                        if len(paths[currentPath]) > 0:
                            if variables[currentPath]["elevatorPosition"] != SCALE_POSITION:
                                paths[currentPath].append((paths[currentPath][-1][0], paths[currentPath][-1][1], SCALE_POSITION))
                                variables[currentPath]["elevatorPosition"] = SCALE_POSITION
                                print(paths[currentPath][-1])
                    elif indexClicked == 10 and not cloning:
                        if len(paths[currentPath]) > 0:
                            waitInput = not waitInput
                            decimal = False
                            integerList = []
                            decimalList = []
                            timeList = []
                    elif indexClicked == 11 and not waitInput and not cloning:
                        if len(paths[currentPath]) > 1:
                            if variables[currentPath]["elevatorPosition"] != 0 and not variables[currentPath]["clawOpen"]:
                                paths[currentPath].append((paths[currentPath][-1][0], paths[currentPath][-1][1], OPEN_CLAW))
                                variables[currentPath]["clawOpen"] = True
                                print(paths[currentPath][-1])
                    elif indexClicked == 12 and not cloning:
                        if len(paths[currentPath]) > 1:
                            variables[currentPath]["reversed"] = not variables[currentPath]["reversed"]
                            variables[currentPath]["driveToCurrent"] = False
                    pygame.display.set_caption("AutonTool: " + currentPath)
            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                if len(paths[currentPath]) > 0:
                    if paths[currentPath][-1][2] == SWITCH_POSITION or paths[currentPath][-1][2] == SCALE_POSITION:
                        if paths[currentPath][-2][2] == SWITCH_POSITION:
                            variables[currentPath]["elevatorPosition"] = SWITCH_POSITION
                        elif paths[currentPath][-2][2] == SCALE_POSITION:
                            variables[currentPath]["elevatorPosition"] = SCALE_POSITION
                        else:
                            variables[currentPath]["elevatorPosition"] = 0
                    if paths[currentPath][-1][2] == OPEN_CLAW:
                        variables[currentPath]["clawOpen"] = False
                    if paths[currentPath][-1][2] == REVERSE:
                        if paths[currentPath][-1][2] != REVERSE:
                            variables[currentPath]["reversed"] = False
                    variables[currentPath]["driveToCurrent"] = False
                    paths[currentPath].pop(-1)
            if event.type == pygame.KEYDOWN and waitInput:
                if event.key == pygame.K_0:
                    if not decimal:
                        integerList.append(0)  
                    else:
                        decimalList.append(0)
                elif event.key == pygame.K_1:
                    if not decimal:
                        integerList.append(1)
                    else:
                        decimalList.append(1)
                elif event.key == pygame.K_2:
                    if not decimal:
                        integerList.append(2)
                    else:
                        decimalList.append(2)
                elif event.key == pygame.K_3:
                    if not decimal:
                        integerList.append(3)
                    else:
                        decimalList.append(3)
                elif event.key == pygame.K_4:
                    if not decimal:
                        integerList.append(4)
                    else:
                        decimalList.append(4)
                elif event.key == pygame.K_5:
                    if not decimal:
                        integerList.append(5)
                    else:
                        decimalList.append(5)
                elif event.key == pygame.K_6:
                    if not decimal:
                        integerList.append(6)
                    else:
                        decimalList.append(6)
                elif event.key == pygame.K_7:
                    if not decimal:
                        integerList.append(7)
                    else:
                        decimalList.append(7)
                elif event.key == pygame.K_8:
                    if not decimal:
                        integerList.append(8)
                    else:
                        decimalList.append(8)
                elif event.key == pygame.K_9:
                    if not decimal:
                        integerList.append(9)
                    else:
                        decimalList.append(9)
                elif event.key == pygame.K_PERIOD:
                    if decimal == False:
                        decimal = True
                elif event.key == pygame.K_BACKSPACE:
                    if len(decimalList) > 0:
                        decimalList.pop()
                    elif len(decimalList) == 0 and decimal:
                        decimal = False
                    elif len(integerList) > 0 and not decimal:
                        integerList.pop()
                elif event.key == pygame.K_ESCAPE:
                    waitInput = False
                elif event.key == pygame.K_RETURN:
                    timeout = 0
                    for pow in range(len(integerList)-1, -1, -1):
                        timeout += integerList[len(integerList)-(pow+1)] * (10 ** pow)
                    for pow in range(-1, -1*len(decimalList)-1, -1):
                        timeout += decimalList[-pow-1] * (10 ** pow)
                    timeout = min(timeout, 15)
                    if timeout != 0:
                        paths[currentPath].append((paths[currentPath][-1][0], paths[currentPath][-1][1], -1*timeout))
                    waitInput = False
                timeList = mergeDigits(integerList, decimalList, decimal)
    pygame.quit()
    quit()

#Returns the distance between two pygame positions
def calcDist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

#Returns absolute angle from -180 to 180 between two pygame positions, with zero being straight forward, and 999 if there is no position change
def calcAngle(p1, p2):
    global previousAngle
    
    point1 = (p1[0], SCREEN_Y - p1[1])
    point2 = (p2[0], SCREEN_Y - p2[1])
    delta_x = point2[0] - point1[0]
    delta_y = point2[1] - point1[1]
    
    if delta_x == 0 and delta_y > 0:
        theta = 90
    elif delta_x == 0 and delta_y < 0:
        theta = -90
    elif delta_x == 0 and delta_y == 0:
        return 999
    else:
        theta = math.degrees(math.atan2(delta_y, delta_x))
    
    theta -= 90
    while theta < -180:
        theta += 360
    
    if theta != 180 and theta != 0:
        theta *= -1
    return theta

#Takes in 2 lists of digits and merges them into a list of characters to display
def mergeDigits(list1, list2, decimal = False):
    finalList = []
    for digit in list1:
        finalList.append(str(digit))
    if decimal:
        finalList.append(".")
        for digit in list2:
            finalList.append(str(digit))
    return finalList

if __name__=="__main__":
    main()
