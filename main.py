import pygame
import math
import sys

# Screen positions
SCREEN_X = 421
SCREEN_Y = 600

# Center of robot at start
STARTING_Y = 447

#Initial invalid zones
LEFT_BOUND = 79
RIGHT_BOUND = 342
TOP_BOUND = 50
CONTROL_BORDER = 479
EXCHANGE_LEFT = 117
EXCHANGE_RIGHT = 221

#Switch and Scales
SWITCH = pygame.Rect((121, 239, 178, 64))
SCALE_LEFT = pygame.Rect((0, 0, 0, 0))
SCALE_RIGHT = pygame.Rect((0, 0, 0, 0))

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
BTN_DROP = pygame.Rect((315, 529, 105, 50))

# Robot dimensions
ROBOT_DIMS_INCHES = [38.5, 33.5]
ROBOT_DIMS_FEET = [dim / 12 for dim in ROBOT_DIMS_INCHES]
ROBOT_DIAG_FEET = math.sqrt(ROBOT_DIMS_FEET[0] ** 2 + ROBOT_DIMS_FEET[1] ** 2) / 2

previousAngle = 0

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
	pygame.draw.line(screen, (0, 0, 0), points[3], points[0], 2)

def drawPath(screen, path):
	for point in path:
		pygame.draw.circle(screen, YELLOW, point[:2], 2, 0)
	
	for x in range(len(path) - 1):
		last_point = path[x]
		next_point = path[x + 1]
		if next_point[:2] != last_point[:2]:
			angle = calcAngle(last_point[:2], next_point[:2])
			drawRobot(screen, last_point[:2], angle, BLUE)
			drawRobot(screen, next_point[:2], angle, RED)
			pygame.draw.line(screen, YELLOW, last_point[:2], next_point[:2], 1)
	if len(path) > 0:
		drawRobot(screen, path[0][:2], 0, BLUE)

#Takes in a list of coordinates and instructions and returns a string of distances and angles
def outputPath(path):
	outputList = []
	for x in range(len(path)):
		if path[x][2] == 0 and x != len(path)-1:
			p1 = path[x][:2]
			p2 = path[x + 1][:2]
			angle = calcAngle(p1, p2)
			if angle != 999:
				if not (x == 0 and angle == 0):
					outputList.append([str(round(angle, 2)), "dg,"])
			distance = calcDist(p2, p1) / PIXELS_PER_FOOT
			if distance != 0:
				outputList.append([str(round(distance, 2)), "ft,"])
		if path[x][2] == 1 and path[x-1][2] != 1:
			outputList.append(["", "2el,"])
		if path[x][2] == 2 and path[x-1][2] != 2:
			outputList.append(["", "5el,"])
		if path[x][2] == 3 and path[x-1][2] != 3:
			outputList.append(["", "cl,"])
	return outputList

def main():
	currentPath = "LL"
	buttonSizes = [BTN_LL, BTN_LR, BTN_RL, BTN_RR, BTN_EXPORT, BTN_SWITCH, BTN_SCALE, BTN_DROP]
	paths = {"LL":[], "LR":[], "RL":[], "RR":[]}
	
	pygame.init()
	font = pygame.font.SysFont('arial', 31, True)
	screen = pygame.display.set_mode((SCREEN_X, SCREEN_Y))
	pygame.display.set_caption("AutonTool: LL")
	pygame.display.update()
	background = pygame.image.load("Field.png")
	backgroundRect = background.get_rect()
	
	indexClicked = 4
	
	finished = False
	
	while not finished:
		screen.blit(background, backgroundRect)
		
		pygame.draw.rect(screen, GREEN, BTN_LL, 0)
		pygame.draw.rect(screen, YELLOW, BTN_LR, 0) 
		pygame.draw.rect(screen, GREEN, BTN_RL, 0) 
		pygame.draw.rect(screen, YELLOW, BTN_RR, 0) 
		pygame.draw.rect(screen, YELLOW, BTN_EXPORT, 0)
		pygame.draw.rect(screen, GREEN, BTN_SWITCH, 0)
		pygame.draw.rect(screen, YELLOW, BTN_SCALE, 0)
		pygame.draw.rect(screen, GREEN, BTN_DROP, 0)
		
		if (currentPath == "LL"):
			pygame.draw.rect(screen, (0, 0, 0), BTN_LL, 2)
		elif (currentPath == "LR"):
			pygame.draw.rect(screen, (0, 0, 0), BTN_LR, 2)
		elif (currentPath == "RL"):
			pygame.draw.rect(screen, (0, 0, 0), BTN_RL, 2)
		elif (currentPath == "RR"):
			pygame.draw.rect(screen, (0, 0, 0), BTN_RR, 2)
		
		text0 = font.render(' LL', True, (0, 0, 0))
		text1 = font.render(' LR', True, (0, 0, 0))
		text2 = font.render(' RL', True, (0, 0, 0))
		text3 = font.render(' RR', True, (0, 0, 0))
		text4 = font.render('EXPORT', True, (0, 0, 0))
		text5 = font.render('SWITCH', True, (0, 0, 0))
		text6 = font.render('SCALE', True, (0, 0, 0))
		text7 = font.render('DROP', True, (0, 0, 0))
		
		screen.blit(text0, BTN_LL.topleft)
		screen.blit(text1, BTN_LR.topleft)
		screen.blit(text2, BTN_RL.topleft)
		screen.blit(text3, BTN_RR.topleft)
		screen.blit(text4, BTN_EXPORT.topleft)
		screen.blit(text5, BTN_SWITCH.topleft)
		screen.blit(text6, BTN_SCALE.topleft)
		screen.blit(text7, BTN_DROP.topleft)
		
		drawPath(screen, paths[currentPath])
		
		pygame.display.flip()
 
		for event in pygame.event.get():
			#print(event)
			if event.type == pygame.QUIT:
				finished = True
			if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
				if SWITCH.collidepoint(event.pos) == True:
					print("switch hit")
				if event.pos[1] < CONTROL_BORDER and event.pos[1]  > TOP_BOUND:
					if len(paths[currentPath]) == 0:
						start_x = event.pos[0]
						if start_x < LEFT_BOUND:
							start_x = LEFT_BOUND
						if start_x > RIGHT_BOUND:
							start_x = RIGHT_BOUND
						if start_x > EXCHANGE_LEFT and start_x < EXCHANGE_LEFT + 52:
							start_x = EXCHANGE_LEFT
						if start_x < EXCHANGE_RIGHT and start_x >= EXCHANGE_RIGHT - 52:
							start_x = EXCHANGE_RIGHT
						paths[currentPath].append((start_x, STARTING_Y, 0))
					elif len(paths[currentPath]) == 1:
						if SWITCH.collidepoint(event.pos) == False:
							paths[currentPath].append((start_x, event.pos[1], 0))
					else:
						if SWITCH.collidepoint(event.pos) == False:
							angle = abs(calcAngle(paths[currentPath][-1], event.pos))
							if angle != 999:
								if angle < 5 or (angle > 175 or angle < -175):
									paths[currentPath].append((paths[currentPath][-1][0], event.pos[1], 0))
								elif angle > 85 and angle < 95:
									paths[currentPath].append((event.pos[0], paths[currentPath][-1][1], 0))
								else:
									paths[currentPath].append((event.pos[0], event.pos[1], 0))
					print(paths[currentPath][-1])
				if event.pos[1] >= CONTROL_BORDER:
					for x in range(len(buttonSizes)):
						if buttonSizes[x].collidepoint(event.pos) == True:
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
						for x in range(1000):
							pygame.draw.rect(screen, (0, 0, 0), BTN_EXPORT, 2)
						outputListLL = outputPath(paths["LL"])
						outputListLR = outputPath(paths["LR"])
						outputListRL = outputPath(paths["RL"])
						outputListRR = outputPath(paths["RR"])
						outputLL = "LL,"
						outputLR = "LR,"
						outputRL = "RL,"
						outputRR = "RR,"
						
						for output in outputListLL:
							outputLL += output[0] + output[1]
						for output in outputListLR:
							outputLR += output[0] + output[1]
						for output in outputListRL:
							outputRL += output[0] + output[1]
						for output in outputListRR:
							outputRR += output[0] + output[1]
							
						print(outputLL)
						print(outputLR)
						print(outputRL)
						print(outputRR)
					elif indexClicked == 5:
						if len(paths[currentPath]) > 0:
							paths[currentPath].append((paths[currentPath][-1][0], paths[currentPath][-1][1], 1))
							print(paths[currentPath][-1])
					elif indexClicked == 6:
						if len(paths[currentPath]) > 0:
							paths[currentPath].append((paths[currentPath][-1][0], paths[currentPath][-1][1], 2))
							print(paths[currentPath][-1])
					elif indexClicked == 7:
						if len(paths[currentPath]) > 0:
							paths[currentPath].append((paths[currentPath][-1][0], paths[currentPath][-1][1], 3))
							print(paths[currentPath][-1])
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

#Returns absolute angle from -180 to 180 between two pygame positions, with zero being straight forward
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
