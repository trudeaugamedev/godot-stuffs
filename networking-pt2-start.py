import pygame
import socket

# Connect to the server at this IP address and port number
sock = socket.create_connection(("127.0.0.1", 12345))
# Don't wait too long to send or receive data so the game can keep running
sock.settimeout(0.01)

# Set up pygame window
pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Client")
# Use clock to run game loop at a regular speed
clock = pygame.time.Clock()

# Position of our player
x = 0
y = 0

# Game loop
running = True
while running:
	# Check for new events
    for event in pygame.event.get():
		# If the close button was pressed, stop running
        if event.type == pygame.QUIT:
            running = False

	# Clear the window with this RGB background colour
    screen.fill((0, 0, 0))

	# Do player movement
    speed = 5
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        x -= speed
    if keys[pygame.K_RIGHT]:
        x += speed
    if keys[pygame.K_UP]:
        y -= speed
    if keys[pygame.K_DOWN]:
        y += speed

    # Send our new location to the server
    sock.send(f"{x},{y};".encode())

    try:
        # Receive new messages from the server
        data = sock.recv(1024)
    except socket.timeout:
		# No data received in more than 0.01 seconds (setting at top of file), give up
        pass
    else:
		# Data was received, split individual messages by semicolons
        messages = data.decode().split(";")
        for message in messages:
			# Split values by commas
            coords = message.split(",")
            try:
			    # Parse the other player position
                other_x = int(coords[0])
                other_y = int(coords[1])
            except (IndexError, ValueError):
				# Invalid message, ignore
                pass
            else:
				# Draw the other player
                pygame.draw.rect(screen, (255, 0, 0), (other_x, other_y, 50, 50))

	# Draw our player
    pygame.draw.rect(screen, (0, 255, 0), (x, y, 50, 50))

	# Update the display and wait for the next frame
    pygame.display.update()
    clock.tick(60)

# Close the window after we're done running the game
pygame.quit()
