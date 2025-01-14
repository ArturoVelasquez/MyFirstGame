# import modules
import pygame

# initialize pygame
pygame.init()

# Define the dimensions of screen object
screen = pygame.display.set_mode((1200, 800))

hero=pygame.draw.









# Variable to keep our game loop running
gameRunning = True

# Our game loop
while gameRunning:
	# for loop through the event queue
	for event in pygame.event.get():	
		# Check for QUIT event
		if event.type == pygame.QUIT:
			gameRunning = False

	# Update the display using flip
	pygame.display.flip()
