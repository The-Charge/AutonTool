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

#Field barriers
LEFT_WALL = 22
RIGHT_WALL = 401
TOP_BOUND = 48
LOWER_BOUND = 468

#Switch and Scales
SWITCH = pygame.Rect((121, 239, 180 , 64))
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
ROBOT_DIAG_FEET = math.sqrt(ROBOT_DIMS_FEET[0] ** 2 + ROBOT_DIMS_FEET[1] ** 2) / 2

#Draws buttons
def drawControls(screen, currentPath, paths, reversed):
	font = pygame.font.SysFont('arial', 22, True)
	
	text0 = font.render(' LL', True, BLACK)
	text1 = font.render(' LR', True, BLACK)
	text2 = font.render(' RL', True, BLACK)
	text3 = font.render(' RR', True, BLACK)
	text4 = font.render('CLONE', True, BLACK)
	text5 = font.render('TO ALL', True, BLACK)
	
	text6 = font.render('EXPORT', True, BLACK)
	text7 = font.render('D.T.C.', True, BLACK)
	text8 = font.render('SWITCH', True, BLACK)
	text9 = font.render('SCALE', True, BLACK)
	text10 = font.render('WAIT', True, BLACK)
	text11 = font.render('DROP', True, BLACK)
	text12 = font.render('REVERSE', True, BLACK)
	
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
	pygame.draw.line(screen, BLACK, BTN_RR.topright, BTN_RR.bottomright, 2)
	
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
	
	if len(paths[currentPath]) > 0:
		if paths[currentPath][-1][2] == 1:
			pygame.draw.rect(screen, BLACK, BTN_DTC, 2)
		elif paths[currentPath][-1][2] == 2:
			pygame.draw.rect(screen, BLACK, BTN_SWITCH, 2)
		elif paths[currentPath][-1][2] == 3:
			pygame.draw.rect(screen, BLACK, BTN_SCALE, 2)
		elif paths[currentPath][-1][2] == 4:
			pygame.draw.rect(screen, BLACK, BTN_DROP, 2)
	
	if reversed[currentPath]:
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
			if next_point[2] == 5:
				if angle < 0:
					angle += 180
				else:
					angle -= 180
			drawRobot(screen, last_point[:2], angle, BLUE)
			drawRobot(screen, next_point[:2], angle, RED)
			pygame.draw.line(screen, YELLOW, last_point[:2], next_point[:2], 1)
	if len(path) > 0:
		drawRobot(screen, path[0][:2], 0, BLUE)

#Takes in a list of coordinates and instructions and returns a string of distances and angles
def outputPath(path):
	output = ""
	previousAngle = 0
	for x in range(len(path)):
		if len(path) > 0:
			if path[x][2] == 1:
				output += "dc,"
			elif path[x][2] == 2:
				output += "2el,"
			elif path[x][2] == 3:
				output += "5el,"
			elif path[x][2] == 4:
				output += "cl,"
		if x != len(path)-1:
			p1 = path[x]
			p2 = path[x + 1]
			angle = calcAngle(p1[:2], p2[:2])
			if p2[2] == 5:
				if angle < 0:
					angle += 180
				else:
					angle -= 180
			if angle != 999 and angle != previousAngle and x != 0:
				output += (str(round(angle, 2)) + "dg,")
			if angle != 999:
				previousAngle = angle
			distance = calcDist(p2[:2], p1[:2]) / PIXELS_PER_FOOT
			if distance != 0:
				if p2[2] == 0:
					output += (str(round(distance, 2)) + "ft,")
				elif p2[2] == 5:
					output += (str(round(distance, 2)) + "rv,")
	return output

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
	if path[-1][0]+ROBOT_PIXELS_HALF[0] > SCALE.left and path[-1][0]-ROBOT_PIXELS_HALF[0] < SCALE.right:
		if path[-1][0]+ROBOT_PIXELS_HALF[0] > SWITCH.left and [-1][0]-ROBOT_PIXELS_HALF[0] < SWITCH.right:
			if point[1]-ROBOT_PIXELS_HALF[1] < SWITCH.bottom:
				ypos = SWITCH.bottom+ROBOT_PIXELS_HALF[1]
			else:
				ypos = point[1]
		else:
			if point[1]-ROBOT_PIXELS_HALF[1] < SCALE.bottom:
				ypos = SCALE.bottom+ROBOT_PIXELS_HALF[1]
			else:
				ypos = point[1]
	else:
		if point[1]-ROBOT_PIXELS_HALF[1] < TOP_BOUND:
			ypos = TOP_BOUND+ROBOT_PIXELS_HALF[1]
		elif point[1]-ROBOT_PIXELS_HALF[1] > LOWER_BOUND:
			ypos = LOWER_BOUND-ROBOT_PIXELS_HALF[1]
		else:
			ypos = point[1]
	return ypos

#Takes in a coordinate's path and aligns it to the grid if it is within 5 degrees
def snapToGrid(pos, path, angle):
	if (angle < 5 and angle > -5) or (angle > 175 or angle < -175):
		pos[0] = path[-1][0]
	elif (angle > 85 and angle < 95) or (angle < -85 and angle > -95):
		pos[1] = path[-1][1]
	return pos

def main():
	currentPath = "LL"
	buttonSizes = [BTN_LL, BTN_LR, BTN_RL, BTN_RR, BTN_CLONE, BTN_ALL, BTN_EXPORT, BTN_DTC, BTN_SWITCH, BTN_SCALE, BTN_WAIT, BTN_DROP, BTN_REVERSE]
	paths = {"LL":[], "LR":[], "RL":[], "RR":[]}
	previousAngles = {"LL":0, "LR":0, "RL":0, "LL":0}
	reversed = {"LL":False, "LR":False, "RL":False, "RR":False}
	
	pygame.init()
	screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
	pygame.display.set_caption("AutonTool: LL")
	pygame.display.update()
	background = pygame.image.load("Field.png")
	backgroundRect = background.get_rect()
	
	indexClicked = 4
	finished = False
	
	while not finished:
		screen.blit(background, backgroundRect)
		drawControls(screen, currentPath, paths, reversed)
		drawPath(screen, paths[currentPath])
		pygame.display.flip()
		if len(paths[currentPath]) < 2:
			reversed[currentPath] = False
		
		for event in pygame.event.get():
			#print(event)
			if event.type == pygame.QUIT:
				finished = True
			if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				if event.pos[1] < CONTROL_BORDER:
					if len(paths[currentPath]) == 0:
						start_x = event.pos[0]
						start_x = checkStart(start_x)
						paths[currentPath].append((start_x, STARTING_Y, 0))
					elif len(paths[currentPath]) == 1:
						firstMove = checkFirstMove(event.pos, paths[currentPath])
						paths[currentPath].append((start_x, firstMove, 0))
					else:
						pos = [event.pos[0], event.pos[1]]
						angle = calcAngle(paths[currentPath][-1], pos)
						
						if (angle > -135 and angle < -45) or (angle > 45 and angle < 135):
							buffer = ROBOT_PIXELS_HALF[1]
						else:
							buffer = ROBOT_PIXELS_HALF[0]
						
						if angle != 999:
							pos = snapToGrid(pos, paths[currentPath], angle)
							
						if pos[0]-buffer < LEFT_WALL:
							pos[0] = LEFT_WALL+buffer
						elif pos[0]+buffer > RIGHT_WALL:
							pos[0] = RIGHT_WALL-buffer
							
						if pos[1]-buffer < TOP_BOUND:
							pos[1] = TOP_BOUND+buffer
						elif pos[1]+buffer > LOWER_BOUND:
							pos[1] = LOWER_BOUND-buffer
						
						#MORE CORRECTION CODE HERE
						
						if reversed[currentPath]:
							if paths[currentPath][-1][2] != (pos[0], pos[1], 5):
								paths[currentPath].append((pos[0], pos[1], 5))
						else:
							if paths[currentPath][-1][2] != (pos[0], pos[1], 0):
								paths[currentPath].append((pos[0], pos[1], 0))
					print(paths[currentPath][-1])
				if event.pos[1] >= CONTROL_BORDER:
					for x in range(len(buttonSizes)):
						if buttonSizes[x].collidepoint(event.pos):
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
						pass
					elif indexClicked == 5:
						pass
					elif indexClicked == 6:
						outputLL = "LL," + outputPath(paths["LL"])
						outputLR = "LR," + outputPath(paths["LR"])
						outputRL = "RL," + outputPath(paths["RL"])
						outputRR = "RR," + outputPath(paths["RR"])
						print(outputLL)
						print(outputLR)
						print(outputRL)
						print(outputRR)
					elif indexClicked == 7:	
						if len(paths[currentPath]) > 1:
							pass
					elif indexClicked == 8:
						if len(paths[currentPath]) > 1:
							paths[currentPath].append((paths[currentPath][-1][0], paths[currentPath][-1][1], 2))
							print(paths[currentPath][-1])
					elif indexClicked == 9:
						if len(paths[currentPath]) > 1:
							paths[currentPath].append((paths[currentPath][-1][0], paths[currentPath][-1][1], 3))
							print(paths[currentPath][-1])
					elif indexClicked == 10:
						pass
						#BTN_WAIT
					elif indexClicked == 11:
						if len(paths[currentPath]) > 1:
							paths[currentPath].append((paths[currentPath][-1][0], paths[currentPath][-1][1], 4))
							print(paths[currentPath][-1])
					elif indexClicked == 12:
						if len(paths[currentPath]) > 1:
							reversed[currentPath] = not reversed[currentPath]
					pygame.display.set_caption("AutonTool: " + currentPath)
			if event.type == pygame.MOUSEBUTTONUP and event.button == 2:
				pass
			if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
				if len(paths[currentPath]) > 0:
					paths[currentPath].pop(-1)
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
	
if __name__=="__main__":
	main()
