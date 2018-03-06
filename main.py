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
LEFT_WALL = 21
RIGHT_WALL = 402
TOP_BOUND = 48
LOWER_BOUND = 468
PORTAL_LEFT = ((16, 421), (57, 472))    #2 points for a diagonal line
PORTAL_RIGHT = ((402, 421), (362, 471)) #these two are unused

#Switch and Scales
#SWITCH and SCALE are the entire thing, SWITCH_LEFT etc are for drawing the white rectangles
SWITCH = pygame.Rect((121, 239, 180, 64))
SWITCH_LEFT = pygame.Rect((126, 241, 43, 57))
SWITCH_RIGHT = pygame.Rect((253, 241, 43, 57))
SCALE = pygame.Rect((105, 59, 212, 56))
SCALE_LEFT = pygame.Rect((105, 59, 42, 56))
SCALE_RIGHT = pygame.Rect((275, 59, 42, 56))

# Conversion factors
PIXELS_PER_FOOT = 13.75
SECONDS_PER_TICK = .018

# Colors
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (46, 130, 23)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (35, 35, 35)

# Button positions
#defining rectangles for every button on the bottom of the screen
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
SIDE = int(ROBOT_DIMS_FEET[0] * PIXELS_PER_FOOT / 2)
FRONT = int(ROBOT_DIMS_FEET[1] * PIXELS_PER_FOOT / 2)
ROBOT_DIAG_FEET = math.sqrt(ROBOT_DIMS_FEET[0] ** 2 + ROBOT_DIMS_FEET[1] ** 2) / 2
   
def main():
    #start on the "LL" tab
    currentPath = "LL"
    #a list of every button
    buttonSizes = [BTN_LL, BTN_LR, BTN_RL, BTN_RR, BTN_CLONE, BTN_ALL, BTN_EXPORT, BTN_DTC, BTN_SWITCH, BTN_SCALE, BTN_WAIT, BTN_DROP, BTN_REVERSE]
    """
    Each of the dictionaries {} that have "LL": etc will contain separate information for each tab (LL, LR, RL, RR).
    Changing the tab by clicking on the respective button will change 'currentPath', which is used to call the information in the dictionary.
    Each auton setting needs a separate set of instructions and variables
    
    paths holds coordinates: ((x, y, other instruction))
    The 'other instructions' are defined as constants above ('SWITCH_POSITION', etc) and are used in outputPath()
    
    angle stores the angle at any given positions
    variables are for various states of the robot
    """
    paths = {"LL":[], "LR":[], "RL":[], "RR":[]}
    angles = {"LL":[], "LR":[], "RL":[], "RR":[]}
    variables = {"LL":{"reversed":False, "clawOpen":False, "elevatorPosition":0, "moved":False}, \
                 "LR":{"reversed":False, "clawOpen":False, "elevatorPosition":0, "moved":False}, \
                 "RL":{"reversed":False, "clawOpen":False, "elevatorPosition":0, "moved":False}, \
                 "RR":{"reversed":False, "clawOpen":False, "elevatorPosition":0, "moved":False}}
    
    #this is used to keep track of a number for each button. When it's pressed, it adds a number of seconds to it.
    #In drawControls(), the number decrements and a rectangle is drawn around each box until it reaches 0
    #this highlights the button for a certain amount of time when clicked
    timers = {}
    for button in buttonSizes:
        timers[str(button)] = 0
    
    #initialize pygame, self explanatory
    pygame.init()
    
    #the screen is the object that pygame functions draw to
    screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
    
    #words in top left
    pygame.display.set_caption("AutonTool: LL")
    
    #refresh the screen
    pygame.display.update()
    
    #set background image
    background = pygame.image.load("Field.png")
    
    #creates a rectangle object based on the background image
    backgroundRect = background.get_rect()
    
    #a list of characters that is passed to drawControls and printed as a number (when taking keyboard input)
    timeList = []
    
    #cloning is toggled by the CLONE button and is referenced in the LL LR etc buttons (when cloning is true, it will make copy the
    #current path into the one you click
    cloning = False
    
    #waitInput is true when you click WAIT and need to take keyboard input - locks most functions until you finish
    waitInput = False
    
    #loop the program
    finished = False
    
    while not finished:
        #place the field on the background
        screen.blit(background, backgroundRect)
        
        #this is in a separate function to tidy up main()
        #it draws all the buttons and other designs
        drawControls(screen, currentPath, paths, variables, cloning, waitInput, timeList, timers, buttonSizes)
        #draws the robots and lines
        drawPath(screen, paths[currentPath], angles[currentPath])
        #refresh the screen
        pygame.display.flip()
        
        #check if the robot has already been moved forwards
        variables[currentPath]["moved"] = False
        for x in paths[currentPath]:
            if x[2] == FORWARD:
                variables[currentPath]["moved"] = True
        #prevent you from going backwards until you've already gone forwards
        if not variables[currentPath]["moved"]:
            variables[currentPath]["reversed"] = False
        #prevents adding a timeout if the robot's initial position isn't defined
        if len(paths[currentPath]) < 1:
            waitInput = False
        
        #loop through the queued events, which are mouse clicks and key inputs
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                #if you click on the field and you aren't taking keyboard input
                if event.pos[1] < CONTROL_BORDER and not waitInput:
                    #event.pos is a tuple of the mouse's coordinates: (xpos, ypos). use event.pos[0] or [1] to get the components
                    #different code depending on which move you're making (initial position, first move forward, everthing else after)
                    
                    #initial position                    
                    if len(paths[currentPath]) == 0:
                        #take the xpos of the click and correct it if it's not in legal range
                        start_x = event.pos[0]
                        start_x = checkStart(start_x)
                        #the y position is always constant for the first move
                        paths[currentPath].append((start_x, STARTING_Y, STARTING))
                        #first angle is always 0
                        angles[currentPath].append(0)
                        print(paths[currentPath][-1])
                    #"moved" is the variable that tells if the robot has already made its first move (forward)
                    elif not variables[currentPath]["moved"]:
                        #use the first move correction code to prevent it from going past the switch or scale
                        firstMove = checkFirstMove(event.pos, paths[currentPath])
                        #add a coordinate with the corrected y coordinate and the original x coordinate
                        paths[currentPath].append((paths[currentPath][0][0], firstMove, FORWARD))
                        angles[currentPath].append(0)
                        print(paths[currentPath][-1])
                    #if the robot has already been placed down and moved forward
                    else:
                        #create a mutable list that contains the mouse coordinates
                        pos = [event.pos[0], event.pos[1]]
                        #find the previous point's coordinates
                        lastPoint = (paths[currentPath][-1][0], paths[currentPath][-1][1])
                        #find the angle from the last point to the current point
                        angle = calcAngle(paths[currentPath][-1], pos)
                        
                        #if the robot's directions is within 5degrees, allign it to the grid(the x/y pos of the last position)
                        #90% of movements are done at 90deg angles
                        #don't bother with this part if there is no position change (angle == 999)
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
                        
                        #takes the mouseclick, last position, and whether or not it's driving backwards and stops the robot before colliding
                        pos = correctPosition(lastPoint, pos)
                        
                        #if the robot can be moved from its current position, it doesn't return 999
                        if pos != 999:
                            #if reverse drive is enabled, give it the REVERSE instruction, which is used in outputPath()
                            if variables[currentPath]["reversed"] and paths[currentPath][-1][2] != (pos[0], pos[1], REVERSE):
                                paths[currentPath].append((pos[0], pos[1], REVERSE))
                            #otherwise give it the basic FORWARD instruction
                            elif paths[currentPath][-1][2] != (pos[0], pos[1], FORWARD):
                                paths[currentPath].append((pos[0], pos[1], FORWARD))
                            #add the angle to the list of angles
                            if angle != 999:
                                angles[currentPath].append(angle)
                            #if there is no position change, copy the angle from the last position
                            else:
                                angles[currentPath].append(angles[currentPath][-1])
                            print(paths[currentPath][-1])
                #if the click is in the button area
                if event.pos[1] >= CONTROL_BORDER:
                    #loop through a list of Rect objects (the buttons) and find the one that was clicked
                    for x in range(len(buttonSizes)):
                        if buttonSizes[x].collidepoint(event.pos):
                            #save the index of the button clicked
                            indexClicked = x
                    #BTN_LL
                    if indexClicked == 0 and not waitInput:
                        if not cloning:
                            #switch currentPath to the LL key
                            currentPath = "LL"
                        else:
                            #copy the information from the current path onto LL
                            paths["LL"] = clone(paths[currentPath])
                            variables["LL"] = dict(variables[currentPath])
                            angles["LL"] = clone(angles[currentPath])
                            cloning = False
                            currentPath = "LL"
                    #BTN_LR
                    elif indexClicked == 1 and not waitInput:
                        if not cloning:
                            currentPath = "LR"
                        else:
                            paths["LR"] = clone(paths[currentPath])
                            variables["LR"] = dict(variables[currentPath])
                            angles["LR"] = clone(angles[currentPath])
                            cloning = False
                            currentPath = "LR"
                    #BTN_RL
                    elif indexClicked == 2 and not waitInput:
                        if not cloning:
                            currentPath = "RL"
                        else:
                            paths["RL"] = clone(paths[currentPath])
                            variables["RL"] = dict(variables[currentPath])
                            angles["RL"] = clone(angles[currentPath])
                            cloning = False
                            currentPath = "RL"
                    #BTN_RR
                    elif indexClicked == 3 and not waitInput:
                        if not cloning:
                            currentPath = "RR"
                        else:
                            paths["RR"] = clone(paths[currentPath])
                            variables["RR"] = dict(variables[currentPath])
                            angles["RR"] = clone(angles[currentPath])
                            cloning = False
                            currentPath = "RR"
                    #BTN_CLONE - toggles
                    elif indexClicked == 4 and not waitInput:
                        cloning = not cloning
                    #BTN_ALL
                    elif indexClicked == 5 and not waitInput:
                        cloning = False
                        #sets a timer to highlight the button for a short time
                        timers[str(BTN_ALL)] = .1
                        #clone the current path's information onto all other paths
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
                    #BTN_EXPORT
                    elif indexClicked == 6 and not waitInput:
                        timers[str(BTN_EXPORT)] = .1
                        #writing instructions to a file is done in outputPath()
                        #output to the console will be done here
                        print("\n----------------------------------------\n-----LL-----")
                        outputPath(paths["LL"], angles["LL"], "LL")
                        print("\n-----LR-----")
                        outputPath(paths["LR"], angles["LR"], "LR")
                        print("\n-----RL-----")
                        outputPath(paths["RL"], angles["RL"], "RL")
                        print("\n-----RR-----")
                        outputPath(paths["RR"], angles["RR"], "RR")
                    #BTN_DTC
                    elif indexClicked == 7 and not waitInput and not cloning:
                        #take the angle the robot is at and find a position very far away in that directions
                        #correctPosition() will stop it right when it hits an obstacle
                        #only do DTC if the robot has moved and the elevator has been raised
                        if variables[currentPath]["moved"] and variables[currentPath]["elevatorPosition"] != 0:
                            lastPoint = paths[currentPath][-1]
                            #find current angle in radians
                            angle = angles[currentPath][-1]
                            angle-=90
                            angle = math.radians(angle)
                            xComp = math.cos(angle)
                            yComp = math.sin(angle)
                            #create a point very far away in the robot's current direction
                            #then use the regular correctPosition function to stop it before it hits an obstacle
                            newPoint = (lastPoint[0] + xComp*1000, lastPoint[1] + yComp*1000)
                            newPoint = correctPosition(lastPoint, newPoint)
                            if newPoint != 999:
                                timers[str(BTN_DTC)] = .1
                                #the positioning is only for the pygame to use. The robot will only see the DTC command
                                #use the write DTC parameters for the current elevator position
                                if variables[currentPath]["elevatorPosition"] == SWITCH_POSITION:
                                    paths[currentPath].append((int(newPoint[0]), int(newPoint[1]), DRIVE_TO_CURRENT_SWITCH))
                                else:
                                    paths[currentPath].append((int(newPoint[0]), int(newPoint[1]), DRIVE_TO_CURRENT_SCALE))
                                angles[currentPath].append(angles[currentPath][-1])
                                print(paths[currentPath][-1])
                    #BTN_SWITCH
                    elif indexClicked == 8 and not waitInput and not cloning:
                    #SWITCH button pressed, can't be clicked when taking keyboard input or cloning a path
                        #don't add the elevate command if it's already raised to that position
                        if len(paths[currentPath]) > 0 and variables[currentPath]["elevatorPosition"] != SWITCH_POSITION:
                            timers[str(BTN_SWITCH)] = .1
                            paths[currentPath].append((paths[currentPath][-1][0], paths[currentPath][-1][1], SWITCH_POSITION))
                            #store the elevator position for future reference
                            variables[currentPath]["elevatorPosition"] = SWITCH_POSITION
                            angles[currentPath].append(angles[currentPath][-1])
                            print(paths[currentPath][-1])
                    #BTN_SCALE
                    elif indexClicked == 9 and not waitInput and not cloning:
                    #SCALE button pressed, can't be clicked when taking keyboard input or cloning a path
                        #don't add the elevate command if it's already raised to that position
                        if len(paths[currentPath]) > 0 and variables[currentPath]["elevatorPosition"] != SCALE_POSITION:
                            timers[str(BTN_SCALE)] = .1
                            paths[currentPath].append((paths[currentPath][-1][0], paths[currentPath][-1][1], SCALE_POSITION))
                            #store the elevator position for future reference
                            variables[currentPath]["elevatorPosition"] = SCALE_POSITION
                            angles[currentPath].append(angles[currentPath][-1])
                            print(paths[currentPath][-1])
                    #BTN_WAIT
                    elif indexClicked == 10 and not cloning:
                    #enables key input (see below) to pause the robot, can't be clicked when cloning a path
                        if len(paths[currentPath]) > 0:
                            waitInput = not waitInput   #toggles the mode
                            #these variables are used later
                            decimal = False
                            integerList = []
                            decimalList = []
                            timeList = []
                    #BTN_DROP
                    elif indexClicked == 11 and not waitInput and not cloning:
                        #only drop the cube if the elevator is raised
                        if len(paths[currentPath]) > 1 and variables[currentPath]["elevatorPosition"] != 0 and not variables[currentPath]["clawOpen"]:
                            timers[str(BTN_DROP)] = .1
                            paths[currentPath].append((paths[currentPath][-1][0], paths[currentPath][-1][1], OPEN_CLAW))
                            #store claw state for future reference
                            variables[currentPath]["clawOpen"] = True
                            angles[currentPath].append(angles[currentPath][-1])
                            print(paths[currentPath][-1])
                    #BTN_REVERSE
                    elif indexClicked == 12 and not cloning:
                        #toggle reverse drive on or off
                        if len(paths[currentPath]) > 1:
                            variables[currentPath]["reversed"] = not variables[currentPath]["reversed"]
                    #update the window text
                    pygame.display.set_caption("AutonTool: " + currentPath)
            #right click
            #remove the last coordinate/instruction given from paths[] and update the robot's state in variables[]
            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                #do nothing if there's nothing in paths[currentPath] - nothing to delete
                if len(paths[currentPath]) > 0:
                    #remove the last item in paths[currentPath] and angles[currentPath]
                    paths[currentPath].pop()
                    angles[currentPath].pop()
                    
                    #first, set these variables false
                    waitInput = False
                    variables[currentPath]["clawOpen"] = False
                    variables[currentPath]["elevatorPosition"] = 0
                    
                    #then loop through the path and update them if their commands are found - because variables[] isn't stored for each position
                    for point in paths[currentPath]:
                        if point[2] == SWITCH_POSITION:
                            variables[currentPath]["elevatorPosition"] = SWITCH_POSITION
                        elif point[2] == SCALE_POSITION:
                            variables[currentPath]["elevatorPosition"] = SCALE_POSITION
                        elif point[2] == OPEN_CLAW:
                            variables[currentPath]["clawOpen"] = True
                if len(paths[currentPath]) < 2:
                    variables[currentPath]["moved"] = False
            #if WAIT is toggled and a key press is detected
            if event.type == pygame.KEYDOWN and waitInput:
                #takes the correct digit and adds it to the correct list
                #stores a separate list of digits for integers and decimals, then puts them together at the end
                #decimal is a boolean of whether or not the '.' key has been pressed
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
                #set the decimal bool true, a decimal will show up in the string output
                #and any subsequent keys will be added to the decimal list
                elif event.key == pygame.K_PERIOD:
                    decimal = True
                #undo the keypress
                elif event.key == pygame.K_BACKSPACE:
                    if len(decimalList) > 0:
                        decimalList.pop()
                    elif len(decimalList) == 0 and decimal:
                        decimal = False
                    elif len(integerList) > 0 and not decimal:
                        integerList.pop()
                #toggle WAIT off - also you can click BTN_WAIT
                elif event.key == pygame.K_ESCAPE:
                    waitInput = False
                #add the typed number as a paramater in paths[currentPath]
                elif event.key == pygame.K_RETURN:
                    timeout = 0
                    #math for getting number from list of digits
                    for pow in range(len(integerList)-1, -1, -1):
                        timeout += integerList[len(integerList)-(pow+1)] * (10 ** pow)
                    for pow in range(-1, -1*len(decimalList)-1, -1):
                        timeout += decimalList[-pow-1] * (10 ** pow)
                    #cap the wait period at 15 seconds
                    timeout = min(timeout, 15)
                    if timeout != 0:
                        #timeout values are negative to differentiate them from things like FORWARD=0, OPEN_CLAW=4, etc
                        paths[currentPath].append((paths[currentPath][-1][0], paths[currentPath][-1][1], -1*timeout))
                        angles[currentPath].append(angles[currentPath][-1])
                    waitInput = False
                #after evey key, update the string output list that is put on the screen
                timeList = mergeDigits(integerList, decimalList, decimal)
    pygame.quit()
    quit()

#Takes in two points and shortens the path between if there is an obstacle between them. Returns 999 if the robot can't be moved
def correctPosition(pos1, pos2):
    #trim the coordinate to only the first two, in case something from paths[] is passed
    pos1 = pos1[:2]
    pos2 = pos2[:2]
    #find the distance of the path that needs to be checked for collisions
    dist = calcDist(pos1, pos2)
    #find direction it will check in
    angle = calcAngle(pos1, pos2)
    #don't change anything if there's no position change
    if angle == 999:
        return [pos1, pos2]
    #convert to radians and find components
    xComp = math.cos(math.radians(angle-90))
    yComp = math.sin(math.radians(angle-90))
    if angle == 0:
        xComp = 0
        yComp = -1
    elif angle == 90:
        xComp = 1
        yComp = 0
    elif angle == -90:
        xComp = -1
        yComp = 0
    elif angle == 180 or angle == -180:
        xComp = 0
        yComp = 1
    
    #find coordinates for corners - list of 4 points
    corners = findCorners(pos1, angle)
    #take 2 coordinates from points to make a line
    line = [corners[0], corners[3]]
    
    distTraveled = 0
    xTraveled = 0
    yTraveled = 0
    """
    The loop will slowly move a line (front of robot) forward in the path the robot moves in.
    When it reaches the end of the line (distTraveled >= dist) or it hits something on the field, it will
    stop the line where it is and add distanceTraveled to the robot's coordinate
    """
    #check to see if the robot can be moved from its current position. Don't add anything to paths[] if so
    moveable = False
    scanning = True
    while scanning:
        if not collideRectLine(line) and not checkWallCollision(line) and distTraveled < dist:
            moveable = True
            for point in line:
                point[0]+=xComp
                point[1]+=yComp
            xTraveled += xComp
            yTraveled += yComp
            distTraveled = calcDist([xTraveled, yTraveled], [0, 0])
        else:
            scanning = False
    #return 999 if the robot can't move
    if moveable:
        return [int(pos1[0]+xTraveled), int(pos1[1]+yTraveled)]
    else:
        return 999
    
#Takes in a list of coordinates and instructions and prints auton commands to the console and to a file
def outputPath(path, angles, key):
    """
    Output format - one command per line:
    # # #
    First number: 0 or 1
        0 = addSequential
        1 = addParallel
    Second number: 0-5
        0 = DriveXFeetMotionMagic
        1 = ElevateToXPos
        2 = RunCollectorReverse
        3 = DriveToCurrent
        4 = TurnNDegreesAbsolutePID
        5 = WaitNSeconds
    Third number: additional parameters
        DriveXFeetMotionMagic:
            number of feet, positive or negative
        ElevateToXPos:
            2 for switch, 5 for scale
        RunCollectorReverse:
            0.05, same for every instance
        DriveToCurrent:
            0 for switch, 1 for scale
        TurnNDegreesAbsolutePID:
            degree to turn to, from -180 to 180
        WaitNSeconds:
            # of seconds to wait
    """
    if key == "LL":
        f = open("pygameLL.txt", "w")
    elif key == "LR":
        f = open("pygameLR.txt", "w")
    elif key == "RL":
        f = open("pygameRL.txt", "w")
    elif key == "RR":
        f = open("pygameRR.txt", "w")
    #delete the current contents of the file
    f.seek(0)
    f.truncate()
    #the robot's angle will always start at 0deg
    previousAngle = 0
    #All auton is done in low gear
    print("addSequential(new ShiftLow());")
    #Take each coordinate in the path
    for x in range(len(path)):
        #path[x][2] is the third number after the positional coordinates - it gives additional instructions (see constants above)
        #wait timers are just negative numbers
        if path[x][2] < 0:
            #turn it back into a positive number and round it
            time = -1 * round(path[x][2], 2)
            print("addSequential(new WaitNSeconds(%s);" % time)
            f.write("0 5 %s" % time)
            #if it isn't EOF, make a new line - there shouldn't be an empty line at the end
            if x != len(path)-1:
                f.write("\n")
        elif path[x][2] == OPEN_CLAW:
            print("addSequential(new RunCollectorReverse(0.05));")
            f.write("0 2 0.05")
            if x != len(path)-1:
                f.write("\n")
        #check if it needs to output TurnNDegreesAbsolutePID or MotionMagic (they need to check a bucket ahead in paths[])
        moving = False
        if x != len(path)-1:
            moving = True
        #output TurnNDegreesAbsolutePID
        if moving:
            newPoint = path[x+1]
            #angle = calcAngle(path[x][:2], newPoint[:2])
            #NEW- angle is taken from the more accurate angles[] list rather than calculated from pixels
            angle = angles[x+1]
            #flip the angle if it's driving backwards
            if newPoint[2] == REVERSE and angle != 999:
                if angle < 0:
                    angle += 180
                else:
                    angle -= 180
            #don't output any turns if the robot doesn't move
            if angle != 999:
                #if the turning is insignificant, don't bother outputting it
                if calcAngleDifference(angle, previousAngle) > 2:
                    print("addSequential(new TurnNDegreesAbsolutePID(%s));" % round(angle, 2))
                    f.write("0 4 %s" % round(angle, 2))
                    #TurnNDegreesAbsolutePID will always be followed by something else, so you don't need to check for EOF
                    #when adding the \n
                    f.write("\n")
                previousAngle = angle
        #commands to move the elevator
        if path[x][2] == SWITCH_POSITION:
            print("addParallel(new ElevateToXPos(2));")
            f.write("1 1 2")
            if x != len(path)-1:
                f.write("\n")
        elif path[x][2] == SCALE_POSITION:
            print("addParallel(new ElevateToXPos(5));")
            f.write("1 1 5")
            if x != len(path)-1:
                f.write("\n")
        #DriveXFeetMotionMagic
        if moving:
            distance = calcDist(path[x][:2], newPoint[:2]) / PIXELS_PER_FOOT
            if newPoint[2] == REVERSE:
                distance = -1 * distance
            #motion magic
            if distance != 0 and newPoint[2] == FORWARD or newPoint[2] == REVERSE:
                print("addSequential(new DriveXFeetMotionMagic(%s));" % round(distance, 2))
                f.write("0 0 %s" % round(distance, 2))
                if x+1 != len(path)-1:
                    f.write("\n")
            #main() will tell outputPath() which DTC to use
            elif newPoint[2] == DRIVE_TO_CURRENT_SWITCH:
                print("addSequential(new DriveToCurrent(.2, 5));")
                f.write("0 3 0")
                if x+1 != len(path)-1:
                    f.write("\n")
            elif newPoint[2] == DRIVE_TO_CURRENT_SCALE:
                print("addSequential(new DriveToCurrent(.07, 1);")
                f.write("0 3 1")
                if x+1 != len(path)-1:
                    f.write("\n")
    #close the file when finished
    f.close()

#Draws buttons - separated from main for organization
def drawControls(screen, currentPath, paths, variables, cloning, waitInput, timeList, timers, buttonSizes):
    font = pygame.font.SysFont('arial', 22, True)
    smallFont = pygame.font.SysFont('arial', 12, True)
    numDisplay = ""
    if waitInput:
        numDisplay = "Enter a time: "
        for digit in timeList:
            numDisplay += digit
        
    textLL = font.render(' LL', True, BLACK)
    textLR = font.render(' LR', True, BLACK)
    textRL = font.render(' RL', True, BLACK)
    textRR = font.render(' RR', True, BLACK)
    textCLONE = font.render('CLONE', True, BLACK)
    textTO_ALL = font.render('TO ALL', True, BLACK)
    textEXPORT = font.render(' EXPORT', True, BLACK)
    textDTC = font.render('D.T.C.', True, BLACK)
    textSWITCH = font.render('SWITCH', True, BLACK)
    textSCALE = font.render('SCALE', True, BLACK)
    textWAIT = font.render('  WAIT', True, BLACK)
    textDROP = font.render(' DROP', True, BLACK)
    textREVERSE = font.render('REVERSE', True, BLACK)
    textNumber = font.render(numDisplay, True, BLACK)
    textELEVATOR = smallFont.render("Elevator Position:", True, BLACK)
    
    #draw green and red rectangles over the Rect objects
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
    
    #highlight the corresponding field elements for the current path
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
    
    #highlight buttons when they are toggled ON
    if cloning:
        pygame.draw.rect(screen, BLACK, BTN_CLONE, 2)
    if waitInput:
        pygame.draw.rect(screen, BLACK, BTN_WAIT, 2)
    if variables[currentPath]["reversed"]:
        pygame.draw.rect(screen, BLACK, BTN_REVERSE, 2)
    
    #highlight buttons for a set time when they are clicked
    for button in buttonSizes:
        if timers[str(button)] > 0:
            pygame.draw.rect(screen, BLACK, button, 2)
            timers[str(button)] -= SECONDS_PER_TICK
        if timers[str(button)] < 0:
            timers[str(button)] = 0
    
    #display text on the screen in various locations
    screen.blit(textLL, BTN_LL.topleft)
    screen.blit(textLR, BTN_LR.topleft)
    screen.blit(textRL, BTN_RL.topleft)
    screen.blit(textRR, BTN_RR.topleft)
    screen.blit(textCLONE, BTN_CLONE.topleft)
    screen.blit(textTO_ALL, BTN_ALL.topleft)
    screen.blit(textEXPORT, BTN_EXPORT.topleft)
    screen.blit(textDTC, BTN_DTC.topleft)
    screen.blit(textSWITCH, BTN_SWITCH.topleft)
    screen.blit(textSCALE, BTN_SCALE.topleft)
    screen.blit(textWAIT, BTN_WAIT.topleft)
    screen.blit(textDROP, BTN_DROP.topleft)
    screen.blit(textREVERSE, BTN_REVERSE.topleft)
    screen.blit(textNumber, (0, CONTROL_BORDER-35))
    
    if len(paths[currentPath]) > 0:
        cube = pygame.image.load("cube.png")
        screen.blit(textELEVATOR, (152, 110))
        pygame.draw.rect(screen, DARK_GRAY, (240, 100, 20, 40), 0)
        if variables[currentPath]["elevatorPosition"] == 0:
            pygame.draw.rect(screen, GRAY, (238, 134, 24, 5), 0)
            if not variables[currentPath]["clawOpen"]:
                screen.blit(cube, (242, 124))
        elif variables[currentPath]["elevatorPosition"] == SWITCH_POSITION:
            pygame.draw.rect(screen, GRAY, (238, 125, 24, 5), 0)
            if not variables[currentPath]["clawOpen"]:
                screen.blit(cube, (242, 115))
        elif variables[currentPath]["elevatorPosition"] == SCALE_POSITION:
            pygame.draw.rect(screen, GRAY, (238, 100, 24, 5), 0)
            if not variables[currentPath]["clawOpen"]:
                screen.blit(cube, (242, 90))

#Draws the robot at the given angle
def drawRobot(screen, point, angle, color):
    #finds 4 points around the robot's center at the correct angle for the corners and draws a polygon around them
    points = findCorners(point, angle)
    pygame.draw.polygon(screen, color, points, 1)
    pygame.draw.line(screen, BLACK, points[3], points[0], 2)

#Draws the robot's path and positions
def drawPath(screen, path, angles):
    #draws a yellow dot at the center of each position
    for point in path:
        pygame.draw.circle(screen, YELLOW, point[:2], 2, 0)
    #set a default angle
    angle = 0
    #go through every point in the path (except the last, because it looks ahead
    for x in range(len(path) - 1):
        #set two points to draw a path between
        last_point = path[x]
        next_point = path[x + 1]
        #don't draw anything if the positional coordinates (first two numbers) are identical to the last (doesn't move)
        if next_point[:2] != last_point[:2]:
            #find the angle for drawRobot() to use
            angle = calcAngle(last_point[:2], next_point[:2])
            angle = angles[x+1]
            #flip it if you're moving backwards
            if next_point[2] == REVERSE:
                if angle < 0:
                    angle += 180
                else:
                    angle -= 180
            #draw a blue and red robot at the start and finish of the path
            drawRobot(screen, last_point[:2], angle, BLUE)
            drawRobot(screen, next_point[:2], angle, RED)
            #connect the points with a line
            pygame.draw.line(screen, YELLOW, last_point[:2], next_point[:2], 1)
        #draw a clock if the robot waits (if the third number is negative)
        elif next_point[2] < 0:
            #load an image
            timer = pygame.image.load("timer.png")
            #display the image on the screen near the robot
            screen.blit(timer, (next_point[0]-13, next_point[1]-20))
        #draw a cube if the robot drops the cube
        elif next_point[2] == OPEN_CLAW:
            #find coordinate 40 pixels in front of robot
            xComp = math.cos(math.radians(angle-90))
            yComp = math.sin(math.radians(angle-90))
            cubepos = [last_point[0]+xComp*40-8, last_point[1]+yComp*40-8]
            #load cube image
            cube = pygame.image.load("cube.png")
            #display image on screen in front of the robot
            screen.blit(cube, cubepos)
    #since it looks at two positions at a time, it needs different code if there's only one coordinate to look at
    if len(path) > 0:
        drawRobot(screen, path[0][:2], 0, BLUE)

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
    #prevents the first move (forward) from going past the switch/scale
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
 
#Checks if the front of the robot is hitting the switch or scale
def collideRectLine(line):
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
    
    #distance of line required to test
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
    #like checkFieldCollision, but only checks the two endpoints of the line rather than each point along it,
    #because it's unnecessary for checking if you hit a wall
    for point in line:
        xpos = point[0]
        ypos = point[1]
        if ypos < TOP_BOUND or ypos > LOWER_BOUND or xpos < LEFT_WALL or xpos > RIGHT_WALL:
            return True
    return False

#Return True if two lines intersect
#CRASHES PROGRAM DO NOT USE
def linesIntersect(line1, line2):
    line1 = [[line1[0][0], line1[0][1]], [line1[1][0], line1[1][1]]]
    line2 = [[line2[0][0], line2[0][1]], [line2[1][0], line2[1][1]]]
    
    angle1 = calcAngle(line1[0], line1[1])
    angle2 = calcAngle(line2[0], line2[1])
    
    dist1 = calcDist(line1[0], line1[1])
    dist2 = calcDist(line2[0], line2[1])
    
    xComp1 = math.cos(math.radians(angle1-90))
    yComp1 = math.sin(math.radians(angle1-90))
    xComp2 = math.cos(math.radians(angle2-90))
    yComp2 = math.sin(math.radians(angle2-90))
    
    testPoint1 = line1[0]
    testPoint2 = line2[0]
    
    xTraveled1 = 0
    yTraveled1 = 0
    xTraveled2 = 0
    yTraveled2 = 0
    
    distTraveled1 = 0
    distTraveled2 = 0
    scanning = True
    incrementLine = True
    
    while distTraveled1 < dist1:
        testPoint2 = line2[0]
        distTraveled2 = 0
        xTraveled2 = 0
        yTraveled2 = 0
        while distTraveled2 < dist2:
            if [int(testPoint1[0]), int(testPoint1[1])] == [int(testPoint2[0]), int(testPoint2[1])]:
                return True
            testPoint2[0] += xComp2
            testPoint2[1] += yComp2
            xTraveled2 += xComp2
            yTraveled2 += yComp2
            distTraveled2 = calcDist([int(xTraveled2), int(yTraveled2)], [0, 0])
        testPoint1[0] += xComp1
        testPoint1[1] += yComp1
        xTraveled1 += xComp1
        yTraveled1 += yComp1
        distTraveled1 = calcDist([int(xTraveled1), int(yTraveled1)], [0, 0])
    return False

#Takes in two angles from -180 to 180 and calculates the angle between them
def calcAngleDifference(angle1, angle2):
    lower = min(angle1, angle2)
    greater = max(angle1, angle2)
    difference = greater - lower
    if difference > 180:
        difference = 360 - difference
    return difference

#Returns the distance between two pygame positions
def calcDist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

#Take the robot's position and angle and calculate where the corners of the robot are
def findCorners(point, angle):
    baseAngle = 48.972495940751 + angle
    baseAngle -= 90
    angles = [baseAngle, baseAngle + 82.055008118498, baseAngle + 180, baseAngle + 262.0550081185]
    rads = [math.radians(angle) for angle in angles]
    x_points = [math.cos(rad) * ROBOT_DIAG_FEET * PIXELS_PER_FOOT + point[0] for rad in rads]
    y_points = [math.sin(rad) * ROBOT_DIAG_FEET * PIXELS_PER_FOOT + point[1] for rad in rads]
    points = []
    for i in range(len(x_points)):
        points.append([x_points[i], y_points[i]])
    return points

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
def mergeDigits(list1, list2, decimal):
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
