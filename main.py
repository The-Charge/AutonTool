import pygame
import math
import sys
import copy

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
SECONDS_PER_TICK = .019

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
def drawControls(screen, currentPath, paths, variables, cloning, waitInput, timeList, timers, buttonSizes):
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
    if variables[currentPath]["reversed"]:
        pygame.draw.rect(screen, BLACK, BTN_REVERSE, 2)
    
    for button in buttonSizes:
        if timers[str(button)] > 0:
            pygame.draw.rect(screen, BLACK, button, 2)
            timers[str(button)] -= SECONDS_PER_TICK
        if timers[str(button)] < 0:
            timers[str(button)] = 0
    
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
                print("addSequential(new TimeOut(%s);" % time)
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
            if angle != 999 and angle != previousAngle and x != 0 and p2[2] != DRIVE_TO_CURRENT_SCALE and p2[2] != DRIVE_TO_CURRENT_SWITCH:
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
    angles = {"LL":[], "LR":[], "RL":[], "RR":[]}
    variables = {"LL":{"reversed":False, "clawOpen":False, "waitInput":False, "elevatorPosition":0, "moved":False}, \
                 "LR":{"reversed":False, "clawOpen":False, "waitInput":False, "elevatorPosition":0, "moved":False}, \
                 "RL":{"reversed":False, "clawOpen":False, "waitInput":False, "elevatorPosition":0, "moved":False}, \
                 "RR":{"reversed":False, "clawOpen":False, "waitInput":False, "elevatorPosition":0, "moved":False}}
    timers = {}
    for button in buttonSizes:
        timers[str(button)] = 0
    
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
    pygame.display.set_caption("AutonTool: LL")
    pygame.display.update()
    background = pygame.image.load("Field.png")
    backgroundRect = background.get_rect()
    timeList = []
    cloning = False
    waitInput = False
    finished = False
    
    while not finished:
        screen.blit(background, backgroundRect)
        drawControls(screen, currentPath, paths, variables, cloning, waitInput, timeList, timers, buttonSizes)
        drawPath(screen, paths[currentPath])
        pygame.display.flip()
        
        if len(paths[currentPath]) < 2:
            variables[currentPath]["reversed"] = False
            waitInput = False
        variables[currentPath]["moved"] = False
        for x in paths[currentPath]:
            if x[2] == FORWARD:
                variables[currentPath]["moved"] = True
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                validClick = True
                if SCALE.collidepoint(event.pos) or SWITCH.collidepoint(event.pos):
                    validClick = False
                if event.pos[1] < CONTROL_BORDER and not waitInput:
                    if len(paths[currentPath]) == 0:
                        start_x = event.pos[0]
                        start_x = checkStart(start_x)
                        paths[currentPath].append((start_x, STARTING_Y, STARTING))
                        angles[currentPath].append(0)
                    elif not variables[currentPath]["moved"]:
                        firstMove = checkFirstMove(event.pos, paths[currentPath])
                        paths[currentPath].append((start_x, firstMove, FORWARD))
                        angles[currentPath].append(0)
                    #elif validClick:
                    else:
                        pos = [event.pos[0], event.pos[1]]
                        lastPoint = (paths[currentPath][-1][0], paths[currentPath][-1][1])
                        angle = calcAngle(paths[currentPath][-1], pos)
                        
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
                        
                        pos = correctPosition(lastPoint, pos, variables[currentPath]["reversed"])
                        
                        
                        if variables[currentPath]["reversed"]:
                            if paths[currentPath][-1][2] != (pos[0], pos[1], REVERSE):
                                paths[currentPath].append((pos[0], pos[1], REVERSE))
                        else:
                            if paths[currentPath][-1][2] != (pos[0], pos[1], FORWARD):
                                paths[currentPath].append((pos[0], pos[1], FORWARD))
                        if angle != 999:
                            angles[currentPath].append(angle)
                        else:
                            angles[currentPath].append(angles[currentPath][-1])
                    #print(angles)
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
                            angles["LL"] = clone(angles[currentPath])
                            cloning = False
                            currentPath = "LL"
                    elif indexClicked == 1 and not waitInput:
                        if not cloning:
                            currentPath = "LR"
                        else:
                            paths["LR"] = clone(paths[currentPath])
                            variables["LR"] = dict(variables[currentPath])
                            angles["LR"] = clone(angles[currentPath])
                            cloning = False
                            currentPath = "LR"
                    elif indexClicked == 2 and not waitInput:
                        if not cloning:
                            currentPath = "RL"
                        else:
                            paths["RL"] = clone(paths[currentPath])
                            variables["RL"] = dict(variables[currentPath])
                            angles["RL"] = clone(angles[currentPath])
                            cloning = False
                            currentPath = "RL"
                    elif indexClicked == 3 and not waitInput:
                        if not cloning:
                            currentPath = "RR"
                        else:
                            paths["RR"] = clone(paths[currentPath])
                            variables["RR"] = dict(variables[currentPath])
                            angles["RR"] = clone(angles[currentPath])
                            cloning = False
                            currentPath = "RR"
                    elif indexClicked == 4 and not waitInput:
                        cloning = not cloning
                    elif indexClicked == 5 and not waitInput:
                        cloning = False
                        timers[str(BTN_ALL)] = .1
                        if currentPath != "LL":
                            paths["LL"] = clone(paths[currentPath])
                            variables["LL"] = dict(variables[currentPath])
                            angles["LL"] = clone(angles[currentPath])
                        if currentPath != "LR":
                            paths["LR"] = clone(paths[currentPath])
                            variables["LR"] = dict(variables[currentPath])
                            angles["LR"] = clone(angles[currentPath])
                        if currentPath != "RL":
                            paths["RL"] = clone(paths[currentPath])
                            variables["RL"] = dict(variables[currentPath])
                            angles["RL"] = clone(angles[currentPath])
                        if currentPath != "RR":
                            paths["RR"] = clone(paths[currentPath])
                            variables["RR"] = dict(variables[currentPath])
                            angles["RR"] = clone(angles[currentPath])
                    elif indexClicked == 6 and not waitInput:
                        timers[str(BTN_EXPORT)] = .1
                        print("\n----------------------------------------\n-----LL-----")
                        outputPath(paths["LL"])
                        print("\n-----LR-----")
                        outputPath(paths["LR"])
                        print("\n-----RL-----")
                        outputPath(paths["RL"])
                        print("\n-----RR-----")
                        outputPath(paths["RR"])
                    elif indexClicked == 7 and not waitInput and not cloning:
                        if variables[currentPath]["moved"] and variables[currentPath]["elevatorPosition"] != 0:
                            timers[str(BTN_DTC)] = .1
                            lastPoint = paths[currentPath][-1]
                            angle = math.radians(angles[currentPath][-1]-90)
                            xComp = math.cos(angle)
                            yComp = math.sin(angle)
                            newPoint = (int(lastPoint[0] + xComp*1000), int(lastPoint[1] + yComp*1000))
                            newPoint = correctPosition(lastPoint, newPoint, False)
                            if variables[currentPath]["elevatorPosition"] == SWITCH_POSITION:
                                paths[currentPath].append((newPoint[0], newPoint[1], DRIVE_TO_CURRENT_SWITCH))
                            else:
                                paths[currentPath].append((newPoint[0], newPoint[1], DRIVE_TO_CURRENT_SCALE))
                            angles[currentPath].append(angles[currentPath][-1])
                    elif indexClicked == 8 and not waitInput and not cloning:
                    #SWITCH button pressed, can't be clicked when taking keyboard input or cloning a path
                        if len(paths[currentPath]) > 0:
                            if variables[currentPath]["elevatorPosition"] != SWITCH_POSITION:
                                timers[str(BTN_SWITCH)] = .1
                                paths[currentPath].append((paths[currentPath][-1][0], paths[currentPath][-1][1], SWITCH_POSITION))
                                variables[currentPath]["elevatorPosition"] = SWITCH_POSITION
                                angles[currentPath].append(angles[currentPath][-1])
                                print(paths[currentPath][-1])
                    elif indexClicked == 9 and not waitInput and not cloning:
                    #SCALE button pressed, can't be clicked when taking keyboard input or cloning a path
                        if len(paths[currentPath]) > 0:
                        #can't be clicked if initial position is not defined in paths[currentPath]
                            if variables[currentPath]["elevatorPosition"] != SCALE_POSITION:
                                timers[str(BTN_SCALE)] = .1
                                paths[currentPath].append((paths[currentPath][-1][0], paths[currentPath][-1][1], SCALE_POSITION))
                                variables[currentPath]["elevatorPosition"] = SCALE_POSITION
                                angles[currentPath].append(angles[currentPath][-1])
                                print(paths[currentPath][-1])
                    elif indexClicked == 10 and not cloning:
                    #WAIT button enables key input (see below) for a timeout and can't be clicked when cloning a papth
                        if len(paths[currentPath]) > 0:
                            waitInput = not waitInput   #toggles the mode
                            #these variables are used later
                            decimal = False
                            integerList = []
                            decimalList = []
                            timeList = []
                    elif indexClicked == 11 and not waitInput and not cloning:
                        if len(paths[currentPath]) > 1:
                            if variables[currentPath]["elevatorPosition"] != 0 and not variables[currentPath]["clawOpen"]:
                                timers[str(BTN_DROP)] = .1
                                paths[currentPath].append((paths[currentPath][-1][0], paths[currentPath][-1][1], OPEN_CLAW))
                                variables[currentPath]["clawOpen"] = True
                                angles[currentPath].append(angles[currentPath][-1])
                                print(paths[currentPath][-1])
                    elif indexClicked == 12 and not cloning:
                        if len(paths[currentPath]) > 1:
                            variables[currentPath]["reversed"] = not variables[currentPath]["reversed"]
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
                    paths[currentPath].pop(-1)
                    angles[currentPath].pop(-1)
                if len(paths[currentPath]) < 2:
                    variables[currentPath]["moved"] = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pass
            if event.type == pygame.KEYDOWN and waitInput:
                if event.key == pygame.K_0:
                    addKey(0, decimal, integerList, decimalList)
                elif event.key == pygame.K_1:
                    addKey(1, decimal, integerList, decimalList)
                elif event.key == pygame.K_2:
                    addKey(2, decimal, integerList, decimalList)
                elif event.key == pygame.K_3:
                    addKey(3, decimal, integerList, decimalList)
                elif event.key == pygame.K_4:
                    addKey(4, decimal, integerList, decimalList)
                elif event.key == pygame.K_5:
                    addKey(5, decimal, integerList, decimalList)
                elif event.key == pygame.K_6:
                    addKey(6, decimal, integerList, decimalList)
                elif event.key == pygame.K_7:
                    addKey(7, decimal, integerList, decimalList)
                elif event.key == pygame.K_8:
                    addKey(8, decimal, integerList, decimalList)
                elif event.key == pygame.K_9:
                    addKey(9, decimal, integerList, decimalList)
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
                        angles[currentPath].append(angles[currentPath][-1])
                    waitInput = False
                timeList = mergeDigits(integerList, decimalList, decimal)
    pygame.quit()
    quit()

#takes in two points and shortens the path if there is an obstacle between them
def correctPosition(pos1, pos2, reversed):
    print(reversed)
    pos1 = pos1[:2]
    pos2 = pos2[:2]
    dist = calcDist(pos1, pos2)
    angle = calcAngle(pos1, pos2)
    if angle == 999:
        return
    
    xComp = math.cos(math.radians(angle-90))
    yComp = math.sin(math.radians(angle-90))
    
    baseAngle = 48.972495940751 + angle
    baseAngle -= 90
    angles = [baseAngle, baseAngle + 82.055008118498, baseAngle + 180, baseAngle + 262.0550081185]
    rads = [math.radians(angle) for angle in angles]
    x_points = [math.cos(rad) * ROBOT_DIAG_FEET * PIXELS_PER_FOOT + pos1[0] for rad in rads]
    y_points = [math.sin(rad) * ROBOT_DIAG_FEET * PIXELS_PER_FOOT + pos1[1] for rad in rads]
    points = []
    for i in range(len(x_points)):
        points.append([x_points[i], y_points[i]])
    line = [points[0], points[3]]
    
    distTraveled = 0
    xTraveled = 0
    yTraveled = 0
        
    scanning = True
    while scanning:
        templine = []
        for point in line:
            templine.append([point[0]+xComp, point[1]+yComp])
        if not checkFieldCollision(templine) and distTraveled < dist:# and not checkWallCollision:
            line = copy.deepcopy(templine)
            xTraveled += xComp
            yTraveled += yComp
            distTraveled = calcDist([xTraveled, yTraveled], [0, 0])
        else:
            scanning = False
    return [int(pos1[0]+xTraveled), int(pos1[1]+yTraveled)]

#Checks if the front of the robot is hitting the switch or scale
def checkFieldCollision(line):
    #the line is the side of the robot that will be moving forward and hitting something
    #move from one end of the line to the other and test if any point on it intersects the switch or scale
    #deepcopy returns the value - prevents aliasing
    templine = copy.deepcopy(line)
    #tempoint is one line on the path
    temppoint = copy.deepcopy(templine[0])
    angle = calcAngle(templine[0], templine[1])
    angle = math.radians(angle-90)
    
    xComp = math.cos(angle)
    yComp = math.sin(angle)
    
    #distance required to test
    dist = calcDist(templine[0], templine[1])
    #values to track how far forward the coordinates have been tested - compare to distance to test for, and end if it collides or finishes
    xTraveled = 0
    yTraveled = 0
    
    scanning = True
    while scanning:
        #add the components to the respective dimensions
        temppoint[0] += xComp
        temppoint[1] += yComp
        #keep track of how far the testing point has moved
        xTraveled += xComp
        yTraveled += yComp
        distTraveled = calcDist([xTraveled, yTraveled], [0, 0])
        #make sure to int() each value - they are decimals right now
        if SWITCH.collidepoint((int(temppoint[0]), int(temppoint[1]))) or SCALE.collidepoint((int(temppoint[0]), int(temppoint[1]))):
            return True
        #if it reached the end without hitting anything, return collision = false
        if distTraveled >= dist:
            return False

#Checks if the front of the robot is hitting a wall
def checkWallCollision(line):
    templine = copy.deepcopy(line)
    return

#Takes in two angles from -180 to 180 and calculates their difference
def calcAngleDifference(angle1, angle2):
    pass

#Returns the distance between two pygame positions
def calcDist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

#Appends a digit to either a whole number or decimal list
#Used with WAIT
def addKey(digit, decimal, integerList, decimalList):
    #decimal is whether or not the decimal has been added to the string
    if not decimal:
        integerList.append(digit)   #add the digit to the list that will be put before the decimal
    else:
        decimalList.append(digit)   #"  "   "   ...                             after   "   "

#Returns absolute angle from -180 to 180 between two pygame positions, with zero being straight forward, and 999 if there is no position change
def calcAngle(p1, p2):
    #Conversions to work with trig functions
    point1 = (p1[0], SCREEN_Y - p1[1])
    point2 = (p2[0], SCREEN_Y - p2[1])
    
    delta_x = point2[0] - point1[0]
    delta_y = point2[1] - point1[1]
    
    #Corrections for angles that tan() can't return
    if delta_x == 0 and delta_y > 0:
        theta = 90
    elif delta_x == 0 and delta_y < 0:
        theta = -90
    #999 means there is no position change
    elif delta_x == 0 and delta_y == 0:
        return 999
    #otherwise use trig to get the angle
    else:
        theta = math.degrees(math.atan2(delta_y, delta_x))
    
    #convert from (0-360 going CCW)to (-180 to 180 going CW)
    theta -= 90
    while theta < -180:
        theta += 360
    #don't really know what this is for
    if theta != 180 and theta != 0:
        theta *= -1
    return theta

#Takes in 2 lists of digits and merges them into a list of characters to display
#Used with WAIT
def mergeDigits(list1, list2, decimal = False):
    #adds integers, the decimal, and decimals in that order to a list of strings for output
    finalList = []
    for digit in list1:
        finalList.append(str(digit))
    if decimal:
        finalList.append(".")
        for digit in list2:
            finalList.append(str(digit))
    return finalList

#Main - standard python format
if __name__=="__main__":
    main()
